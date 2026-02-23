---
layout: post
title: Yet Another Blog Migration!
date: 2026-02-22
ai_disclosure: I wrote this as a stream of consciousness post but it was comically bad, so I used Claude Sonnet 4.6 to help edit. And then I edited again for more authenticity.
---

I'm migrating all my blog content from Medium and WordPress to a self-hosted Jekyll site. What better way to kick things off than describing how it went?

About ten years ago, frustrated with WordPress's steady decline, I migrated to Medium. It was the clean, modern blogging platform of the moment. The catch: I couldn't easily bring my old posts along because Medium's format support was too limited, so those got left behind.

Since then Medium has been getting progressively slower and more ad-heavy. I considered Substack, but I don't love the email popup. Also, having watched both WordPress and Medium enshittify, I'm _very_ wary about the future of yet another blogging platform.

To make things worse, Google Sites decoupled DNS registration this past year in a way that quietly prioritized the sites.google.com URL over my domain name. I tried many things but couldn't fix it.

All of that pushed me toward a static site generator. Jekyll fits the bill, and I can host it on GitHub Pages, Vercel, or elsewhere.

I was inspired by a post from Simon Willison, who went through a similar migration and found LLMs effective at converting blog content between formats. That's where I started.

# Converting from Medium

Medium has an account-level export tool, which helped a lot. The only snag was that it wasn't working in Chrome on Linux anymore, so I had to use Firefox. That produced a dump of HTML files, which I converted with pandoc and some sed commands. The output needed cleanup, but Claude Sonnet 4.6 in VS Code handled most of it.

Images were also frustrating because they weren't included in the bulk export. The LLM could run `curl` to download them, but didn't initially verify they were actually image files, so some downloads were silently replaced by HTML error pages. After some trial and error, we added rate limiting and validated content with `file`. Even then, I had to download 2–3 images manually.

# Converting from WordPress

WordPress _had_ an export feature last summer, which I used for another project. Unfortunately that feature has since been removed — if I hadn't already grabbed a copy, I'd have had to crawl my own blog to migrate it.

The export is a single XML file containing everything. I used a Python library to extract the posts and another to convert HTML to Markdown. In hindsight, I should have spent more time on the conversion code upfront; there ended up being a lot of cleanup afterward:
- Restoring paragraph breaks (which led to broken tables that we fixed)
- Removing WordPress-specific markup like `[caption]`
- Removing links to WordPress tags/categories from the old blog
- Checking metadata to identify posts that were actually unpublished drafts

The LLM handled image downloads much better this time, with some upfront guidance on rate limiting and validation. One surprise: many image links were `http` rather than `https`. That makes sense in retrospect: those posts predate the era of HTTPS everywhere, when there was still active debate about the performance overhead.

Deciding which posts to keep was a separate challenge. I gave the LLM a handful of examples to calibrate on and it did a solid job from there.

# Observations

I found a surprising amount of domain hijacking: old blogs or product sites that are now pure ad farms for unrelated topics. That gives me some pause as I consider what to link in the future. I also noticed that many sites that were previously ad-supported are now paywalled or otherwise gated behind logins. And I came across several companies that were acquired and then had their products shut down, or pivoted in a major way.

It's also interesting to see how my writing has changed over the past 16 years. I used to write more short-form posts, and I've always struggled with titles and introductions — 16 years of evidence makes that pretty clear.


# Nostalgia

Going through 16 years of old posts turned up a few pleasant surprises:
- [BBspot](https://en.wikipedia.org/wiki/BBspot), an old tech satire site, is still up. Though BB hasn't posted recently.
- A Newegg link to the specific CPU I bought long ago still resolves, image and all!

And one that stings: [AnandTech](https://en.wikipedia.org/wiki/AnandTech) is gone.

# Lessons Learned

- Start with a link scanner like [Lychee](https://lychee.cli.rs/) _before_ manually fixing anything. A lot of link updates can be automated, and I wasted time doing it by hand first.
- ChatGPT pulled outdated documentation for the GitHub/Squarespace configuration, which made that step harder than it needed to be. I got there eventually.
- When Google Sites transferred DNS to Squarespace, it began promoting the Sites URL in search over the canonical domain. I still need to set up a redirect, but Squarespace doesn't seem to offer that option.

# Looking Forward

I'm looking forward to a cleaner, faster site:
- No external fonts or third-party analytics (both common ad-targeting vectors)
- No external JavaScript
- No social media integrations

The goal is something close to the speed and simplicity of the early web, with the layout quality of modern CSS.
