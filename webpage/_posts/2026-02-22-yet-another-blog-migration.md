---
layout: post
title: Yet Another Blog Migration!
date: 2026-02-22
---

I'm moving all my blog content from Medium and WordPress. What better way to start than by describing the process?

About 10 years ago, I was frustrated with Wordpress getting worse over time and Medium was the new clean blogging platform. So I moved to Medium. But sadly I couldn't easily convert my old posts because Medium didn't support as much of the Wordpress layout at the time.

Now Medium has been getting slower and more ad-heavy over the years so I've been meaning to migrate off of Medium. I considered Substack but I don't like the email popup, and having seen both WordPress and Medium enshittify... I'm _very_ wary of another platform that looks great right now. But who knows, maybe their business model is better designed which would prevent the worst of enshittification.

Also this past year, Google sites got worse by decoupling DNS registration in such a way that www.keith-trnka.com still works but it doesn't show up on Google like it used to. The Google Site URL is now the canonical one, and nothing I've tried has fixed it.

So all of those factors have led me to a site builder like Jekyll. I can host that on github pages, vercel, or elsewhere.

I was inspired by a post from Simon W who went through a similar process, and he found that LLMs were great at converting old blog content from one format to another. So that's how I started!

# Converting from Medium

Medium has an export tool in your account and that helps a lot. The only problem I had is that it wasn't working in Chrome on Linux (but it did work in Firefox!). That got me a dump of HTML files, which we converted with pandoc and some sed commands I think. That needed some cleanup but largely Claude Sonnet 4.6 in vscode could handle it.

The main nuisance was the images. The LLM was able to run curl commands to download, but didn't initially check that they were image files! So some would download and others would be an HTML error page. After some trial and error we were more cautious about rate limits and checked the contents with `file`. Even despite all that, I had to download 2-3 of them manually.

# Converting from WordPress

WordPress _had_ an export feature last summer and I used it for another project. Unfortunately they removed that feature since then so if I hadn't already downloaded a copy, I'd need to crawl my own blog to convert it.

The export file is a single XML file with everything, and I used a Python library to extract the posts, then another to convert HTML to markdown. If I could do that again, I would've spent a little more time on the code to convert files because we ended up doing several cleanup tasks after:
- Restoring paragraph breaks (which led to broken tables that we fixed)
- Removing WordPress specific things like `[caption]`
- Removing links to WordPress tags/categories from the old blog
- Checking the metadata to figure out which posts were actually unpublished drafts

That said, the LLM handled the image downloads much better with some guidance on the Python downloader to write, rate limiting, and so on. We had some surprises because some of the image links were http not https. If I remember right, this was back before https everywhere was common and there was still a debate about the performance hit.

# Some posts aren't worth keeping

The LLM did a great job after we reviewed some examples of what to keep and what not to. I approached it like active learning and that worked well.

# Strange things

There was one post (machine translation part 3) that would cause copilot chat to hang indefinitely. I tried with a fresh context multiple times and it kept having that problem. In the end I did the initial conversion manually.

# Some of my hopes for the future of blogging

I'm looking forward to improving load times by:
- Removing external fonts, which may be used for ad targeting
- Removing third party analytics, which may be used for ad targeting
- Removing external Javascript, which slows down page load
- Zero social media integration

It'd be nice to get back to the speed and simplicity of the web 1.0 with some of the nice formatting of modern sites.

# Some old timer observations as I update things

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
    - BBspot
    - Newegg links to CPUs from 13 years ago
- Renewed sadness
    - AnandTech