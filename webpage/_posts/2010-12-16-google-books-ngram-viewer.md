---
layout: post
title: google books ngram viewer
date: 2010-12-16
---

Today, Google [released](http://googleresearch.blogspot.com/2010/12/find-out-whats-in-word-or-five-with.html) the [Google Books NGram Viewer](https://books.google.com/ngrams), which is a beautiful frontend to a historical ngram model.  They have a separate ngram model for each year and for each language type (English, American English, British English, Simplified Chinese, etc).

To some extent, this already existed in the [Corpus of Historical American English](http://corpus.byu.edu/coha/) (COHA), but that's only American English and it doesn't seem to produce pretty graphs.  However, COHA allows for richer queries.

As a tool, you input a list of terms (phrases work too) and pick a corpus.  It checks the language models and produces a graph like so:

![cheap/stiingy terms over time]({{ "/assets/img/posts/wp/cheap-chart.png" | relative_url }})

How does it work and how can you use it?  The data source is the result of Google's work in scanning books and applying character recognition.  It seems that all of the books in Google Books are included, but it's somewhat unclear.

They record 5-gram models for each corpus and year.  Amazingly, the raw ngram models are [available online](https://books.google.com/ngrams/datasets) for free (though not all of it is online yet).

One funny note is that the term *smoothing* in the context of *ngram* really makes me think of ngram model smoothing, but in this case it's smoothing the graph --- each point is the average of adjacent points to smooth out noise in the graph.

In terms of how you can use it, it's an interesting way to choose between near-synonyms.  In that sense, it's a little like the popular [Google Battle](http://www.googlebattle.com/).  For example, consider the choice of a contrast discourse marker:

![contrast discourse markers]({{ "/assets/img/posts/wp/however-chart.png" | relative_url }})

I didn't expect to see *However* increase in popularity at the expense of *But*.  I wonder if this reflects changes in language or changes in the distribution of book types?

Or thus/therefore/etc:

![thus/therefore etc]({{ "/assets/img/posts/wp/thus-chart.png" | relative_url }})

Note that it's case-sensitive, so you find different things depending on case.  Also, if you intend to use it for anything serious, I suggest taking a look at their pages to understand the tokenization methods.

More than anything this seems to be an incredible resource for corpus linguistics.
