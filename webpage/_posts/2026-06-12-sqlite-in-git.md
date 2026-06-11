---
layout: post
title: SQLite in Git: Fully Reversible Storage for Small Data Projects
date: 2026-06-12
ai_disclosure: I started this with Claude Opus as a dump of a working session, then reviewed and had Opus refine several times. The final revision pass was my own. -Keith
---

## A pattern I've adopted over the past year

For a certain kind of small project, I've taken to committing the application's SQLite database directly to git — versioned right alongside the code, with no cloud database or separate service. It's a niche pattern: a great fit for a narrow set of projects and a bad fit for most.

Before this, I'd usually just keep the data as JSON in the repo. That works, but it has friction: large JSON files clog up GitHub diffs and show up as noise in repo searches. A binary SQLite file sidesteps both, and gives me real queries and structure on top.

The pattern itself isn't unusual — people do track SQLite databases in git, and there are nice write-ups of the mechanics ([this one](https://garrit.xyz/posts/2023-11-01-tracking-sqlite-database-changes-in-git), for example). What I haven't seen covered is the *why* and *when*: when this is a good idea versus standing up a real database, and where the boundaries are. That, plus one compression gotcha I hit, is what I want to cover here.

I run this on [seattle-outdoor-volunteering](https://github.com/ktrnka/seattle-outdoor-volunteering), a small ETL pipeline that scrapes Seattle-area outdoor volunteer events nightly and publishes a static site. GitHub Actions runs the pipeline each night, commits the updated `data/events.sqlite` along with the regenerated `docs/index.html`, and pushes to `main`, which triggers a GitHub Pages rebuild. The whole thing runs for free on GitHub's infrastructure, and the SQLite file is currently around 7 MB.

## Where this started

I originally stored the database compressed, as `events.sqlite.gz`. I have a machine-learning background and a reflexive dislike of committing large binaries to git, so gzipping it felt obviously right. It wasn't, but not for the reason I expected.

The compression meant the file had to be decompressed before Python could load it, and I wrote some sloppy code around that: a simple bug where my local copy kept reading a stale uncompressed file after a `git pull` brought in a newer `.gz`. Nothing clever, just a mistake. But chasing it made me question whether the gzip step was worth its complexity at all, and when I removed it I found something more interesting underneath.

## Why commit SQLite to git instead of standing up a database?

For a nightly ETL job that needs to keep structured results somewhere, the "real" answer is a database server like Postgres. For the right project, that's correct. But for a small project, a hosted database brings a tax that's easy to underestimate:

- **You have to secure it.** A network-reachable database is an attack surface and a set of credentials to manage.
- **Free isn't really free.** Free Postgres tiers tend to be slow, sleep when idle, or come with limits you'll hit.
- **Reversibility is shallow.** Migrations version your *schema*, not your *data*. Drop a column by mistake and the data is gone unless you've already built a backup system.

Committing SQLite to git inverts all of that:

- **Zero infrastructure.** Nothing to provision, secure, or pay for. The database is a file.
- **Real reversibility, for free.** Every commit is a full snapshot. Ship a bad migration or mangle the data? `git revert` and you have the complete prior database back. Your history is the backup and the audit trail.
- **Schema, data, and code stay in lockstep.** Check out a commit from last year and you get that era's database *and* the code that read it, together. They can never disagree, because they're the same commit.

This only works in a specific corner, though. It fits when the dataset is **small** (I'd say under ~20 MB), has enough **structure** to be worth a database rather than a JSON or CSV file, and is **written incrementally** by a single source (or a few infrequent ones) rather than many frequent writers. A nightly job that mostly appends, with the occasional manual run, is the sweet spot. It's the wrong choice the moment the data gets large, frequently written, concurrent, or sensitive. (If the writes were one-shot rather than incremental, the storage math below changes, and gzipping might even make sense again.)

## The gotcha: compressing it defeats git's delta compression

Removing the gzip simplified the code, as expected. The surprise was what it did to git's storage.

Git's delta compression works at the binary level, and it turns out to be well-suited to SQLite's page-based format: a small data change only rewrites a handful of 4 KB pages, so the delta between two revisions is tiny. Simon Willison made exactly this point in a [Hacker News thread](https://news.ycombinator.com/item?id=38110286), where someone measured two revisions of an 864 KB database packing down to 329 KB, about the same as gzipping the file once (328 KB), except git's pack covers *both* revisions.

Gzip output is the opposite. A small data change reshuffles the whole compressed stream, so git sees a brand-new incompressible blob and stores a near-full copy every single night. That's exactly what had been quietly happening in my repo.

### Measuring the switch

On **May 21, 2026** ([commit `84f4578`](https://github.com/ktrnka/seattle-outdoor-volunteering/commit/84f4578167a1019b852ba4bcbad67b9923a66f2d)) I removed the compression. On disk the file grew from 1.4 MB to 7 MB, which felt like a step backward, but the bet was that git would handle the raw file far more efficiently as it changed nightly.

I added a small script ([commit `bacaa89`](https://github.com/ktrnka/seattle-outdoor-volunteering/commit/bacaa89)) to measure pack size after an aggressive GC:

```bash
# scripts/git_pack_size.sh
git gc --aggressive --quiet
git count-objects -vH | grep -E "^(count|size-pack):"
```

After **13 nightly runs** (checked June 3, 2026), I dug into the pack with `git verify-pack`:

```
# Base object (current SQLite, stored in full):
2e545124  blob  7,241,728  1,449,323  <offset>

# Each subsequent nightly commit stored as a delta:
28c43011  blob  28,813  22,519  <offset>  depth=1
b4e0ec84  blob   7,740   6,506  <offset>  depth=2
7716bb33  blob   8,842   7,357  <offset>  depth=3
80a9bd0d  blob  12,063   9,898  <offset>  depth=4
cf6730da  blob  28,749  22,327  <offset>  depth=5
...
```

Git stores the most recent database in full and each older version as a compact delta. The average packed delta was **22 KB**, versus the ~1.4 MB each gzipped version had cost.

| Metric | Old (gzip) | New (uncompressed) |
|--------|-----------|--------------------|
| File size on disk | 1.4 MB | 7 MB |
| Packed size per nightly commit | ~1,366 KB | ~22 KB |
| 14 versions total in git pack | ~18.7 MB | ~1.7 MB |
| Delta compression working? | No — gzip blocks it | Yes — depth 1–13 chain |
| Storage cost per commit | 61× worse | baseline |

**A ~91% reduction in git storage cost** for the database history, just by storing it raw. The on-disk file is 5× larger, but the history for those 14 versions uses about 17 MB less.

My ~22 KB deltas against a 7 MB file are a more extreme version of the same effect than the HN example, and the reason hints at when this technique pays off: the bigger the database is relative to each change, the more stable pages git can reuse, and the bigger the win. The flip side is that if a commit rewrites most of the file, the advantage shrinks toward nothing, which is exactly why the incremental-write criterion above matters.

This is the one gotcha I happened to hit, and probably not the only one the pattern has, but it's the most counterintuitive: the "optimized" format is the wrong choice, because it optimizes disk size while the real cost lives in git's history.

## Summary

If you have a small, structured, incrementally-updated dataset with no secrets in it, committing a raw SQLite file to git is a genuinely nice setup: zero infrastructure, full reversibility, and schema-data-code that can't drift apart. It is not a general-purpose database strategy, and it falls apart the moment your data gets large, concurrent, frequently written, or sensitive.

And if you do commit SQLite to git: store it raw. Don't gzip it. Git's delta compression handles the uncompressed format far better, and you'll get a leaner history despite the larger file on disk.

---

*The seattle-outdoor-volunteering repo is at [github.com/ktrnka/seattle-outdoor-volunteering](https://github.com/ktrnka/seattle-outdoor-volunteering). The switch commit is [`84f4578`](https://github.com/ktrnka/seattle-outdoor-volunteering/commit/84f4578167a1019b852ba4bcbad67b9923a66f2d) and the measurement script is in `scripts/git_pack_size.sh`.*
