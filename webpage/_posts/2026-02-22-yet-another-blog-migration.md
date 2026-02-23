---
layout: post
title: Yet Another Blog Migration!
date: 2026-02-22
---

I'm migrating all my blog content from Medium and WordPress to a self-hosted Jekyll site. What better way to kick things off than describing how it went?

About ten years ago, frustrated with WordPress's steady decline, I jumped to Medium — it was the clean, modern blogging platform of the moment. The catch: I couldn't easily bring my old posts along because Medium's format support was too limited, so those got left behind.

Since then Medium has been getting progressively slower and more ad-heavy. I considered Substack, but I don't love the email popup — and having watched both WordPress and Medium enshittify, I'm _very_ wary of any platform that looks clean and promising right now. Maybe Substack's business model prevents the worst of that; I genuinely don't know.

To make things worse, Google Sites decoupled DNS registration this past year in a way that quietly broke my search visibility: www.keith-trnka.com still loads, but it no longer surfaces in Google the way it used to. The Google Sites URL became the canonical one, and nothing I've tried has fixed it.

All of that pushed me toward a static site generator. Jekyll fits the bill, and I can host it on GitHub Pages, Vercel, or elsewhere.

I was inspired by a post from Simon W, who went through a similar migration and found LLMs surprisingly effective at converting blog content between formats. That's where I started.

# Converting from Medium

Medium has an account-level export tool, which helped a lot. The only snag was that it wasn't working in Chrome on Linux — Firefox did the trick. That produced a dump of HTML files, which I converted with pandoc and some sed commands. The output needed cleanup, but Claude Sonnet 4.6 in VS Code handled most of it.

The main nuisance was images. The LLM could run `curl` to download them, but didn't initially verify they were actually image files — so some downloads were silently replaced by HTML error pages. After some trial and error, we added rate limiting and validated content with `file`. Even then, I had to grab 2–3 images manually.

# Converting from WordPress

WordPress _had_ an export feature last summer, which I used for another project. Unfortunately that feature has since been removed — if I hadn't already grabbed a copy, I'd have had to crawl my own blog to migrate it.

The export is a single XML file containing everything. I used a Python library to extract the posts and another to convert HTML to Markdown. In hindsight, I should have spent more time on the conversion code upfront — there ended up being a lot of cleanup afterward:
- Restoring paragraph breaks (which led to broken tables that we fixed)
- Removing WordPress-specific markup like `[caption]`
- Removing links to WordPress tags/categories from the old blog
- Checking metadata to identify posts that were actually unpublished drafts

The LLM handled image downloads much better this time, with some upfront guidance on rate limiting and validation. One surprise: many image links were `http` rather than `https`. That makes sense in retrospect — those posts predate the era of HTTPS everywhere, when there was still active debate about the performance overhead.

Deciding which posts to keep was a separate challenge. I gave the LLM a handful of examples to calibrate on — essentially active learning — and it did a solid job from there.

One odd footnote: one post (machine translation part 3) consistently caused Copilot Chat to hang indefinitely. Fresh context, multiple attempts — same result. I ended up converting that one by hand.

# Observations

- Interesting broken links
    - The old host for Subversion
    - The old host for Mercurial
    - A lot of software tools that just don't exist anymore
    - Some dead Google products like Google Scribe
    - The original IBM Watson page
- Questionable links
    - Some of the articles I used to comment about are now paywalled. I'm not sure how to feel about that
    - Some have sold their domains (like Google Battle) which have been taken over by just ads. I wonder what percent of page views are just bots
- Surprisingly not broken
    - Google Books ngram viewer
- Academic links tend to be more reliable than industry links, probably because professors stay with institutions MUCH longer
- More domain hijacking than I expected, which encouraged me to edit all links and it's making me reconsider how I want to do links in the future
- Companies that made a major pivot, like Plotly
- Linking to books: Back when I was writing, I felt great about Amazon so I tended to link to books there. Now I don't feel as great about Amazon so I swapped those to Goodreads (still Amazon but a little removed from their store)

Observations on my writing:
- I used to write more short-form posts and I've shifted over the years to more long-form content
- I definitely got more engagement on posts over the years as I started to market them a little more via my social networks
- I've always struggled with titles and introductions... that's abundantly clear when looking over 16 years of posts

# Nostalgia

Going through 16 years of old posts turned up a few pleasant surprises:
- [BBspot](https://en.wikipedia.org/wiki/BBspot) is still up
- A Newegg link to the specific CPU I bought long ago still resolves — image and all

And one that stings: [AnandTech](https://en.wikipedia.org/wiki/AnandTech) is gone.



# Lessons Learned

- Start with a link scanner like [Lychee](https://lychee.cli.rs/) _before_ manually fixing anything. A lot of link updates can be automated, and I wasted time doing it by hand first.
- ChatGPT pulled outdated documentation for the GitHub/Squarespace configuration, which made that step harder than it needed to be. We got there eventually.
- When Google Sites transferred DNS to Squarespace, it began promoting the Sites URL in search over the canonical domain. I still need to set up a redirect, but Squarespace doesn't seem to offer that option.

# Looking Forward

I'm looking forward to a cleaner, faster site:
- No external fonts or third-party analytics (both common ad-targeting vectors)
- No external JavaScript
- No social media integrations

The goal is something close to the speed and simplicity of the early web, with the layout quality of modern CSS.
