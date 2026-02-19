---
layout: post
title: google experiments
date: 2010-10-26
---
Sometimes you need relative frequencies of words/terms and you don't already have a Perl script for your data.  Google experiments are a quick approximation - just search for the sequence of words in quotes and use the number of page results (at the top) as an approximate frequency.
I used this in my PhD proposal - I wanted IDF values for some words, so I used Google page frequency for a few common words like *and* and took the maximum to be an approximation of the total number of documents.  Then I did the same for the words I needed IDF for and came up with reasonable values in my figures in 5 minutes or less.
I also used this years ago to help a friend with learning English but forgot until I saw a number of [xkcd comics](http://xkcd.com/369/) that use the method (and some [BBSpot showdowns](http://www.bbspot.com/News/2005/01/firefox_vs_internet_explorer.html)).  It can also be used for things like estimating conditional probabilities.
If you need to do anything more serious, [Language Log](http://languagelog.ldc.upenn.edu/nll/) advocates using [COCA](http://corpus.byu.edu/coca/).
