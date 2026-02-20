---
layout: post
title: Projecting the number of downloads for torrents
date: 2015-02-13
---

One of my current projects is [Over 9000](http://over9000.bitballoon.com/), a visualization that shows which anime series are currently popular. I get the data by scraping a popular anime torrent site every day and come up with a single number that represents the popularity of a show.

The problem with average number of downloads
============================================

I started off by taking the most recent download count per episode and averaging. That works well but leads to unstable rankings when new episodes are released. Let's take Tokyo Ghoul Root A, Episode 3 for example.

Scrape 1: 0.12 days after release, 20,000 downloads

Scrape 2: 1.12 days after release, 60,400 downloads

Scrape 3: 2.13 days after release, 70,100 downloads

...

Scrape 14: 13.14 days after release, 97,900 downloads

Compared to episodes of other shows this is very popular. But on the first day of a new episode we've only seen 20,000 so it drags down the average. That affects the overall rankings by demoting any series with a new episode. It also means that shows with older episodes will get a slight boost.

![Tokyo Ghoul Root A Episode 3 downloads]({{ "/assets/img/posts/wp/image-1.png" | relative_url }})

Solution: Extrapolate number of downloads at 7 days
===================================================

The download graphs look predictable. So we can probably train a computer to predict. My first thought was to fit a curve. It looks like a log graph: fewer and fewer new downloads per day and it doesn't look like it has an asymptote.

First attempt (Predicted\_1 below): *b* \* log(time\_since\_release + *a*)

The *a* is there because we want the curve to fit (0, 0): zero downloads at release. But log(0) is undefined. The *b* is there because some series/episodes get more downloads per day than others.

And I used [scipy.optimize.curve\_fit](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) to fit this function to each episode individually. It worked alright but would always overestimate after a while. Compared to the projections it seemed that actual downloads were slowing down.

![Anime download prediction]({{ "/assets/img/posts/wp/image-2.png" | relative_url }})

Second attempt (Predicted\_2): *b* \* log(time\_since\_release + *a*) ^ *c*

This fit the data much better. But of course it should! The effect of *c* can't be done by *a*or *b* and I'm basically seeing how well it fits my training data.

I also evaluated by extrapolating from the first few days and measuring accuracy at day 7 which is a better test.

Now what?
---------

Now I can fit a curve to the first few days and plug in f(7) to estimate the number of downloads at day 7. Then I can use the estimated downloads in averaging.

But... you can't fit that function to only 1 day of data plus (0, 0). You need at least one more datapoint. Compared to the old values these are much more accurate but won't be available for one more day.

Also, when we only have 2 points I'd expect the estimate to be poor. It's important to understand that better. So I processed episodes where I had 7+ days of data and computed the accuracy of f(7) when I learned f from 2 days of data, 3 days, 4 days, etc. I found this:

Estimate from 2 days: 84.6% accurate

Estimate from 3 days: 86.7% accurate

Estimate from 4 days: 91.6% accurate

Estimate from 5 days: 92.1% accurate

and so on....

That provides me a little robustness: Instead of a plain average I can use a weighted average where the accuracy of extrapolation is used as the weight.

Wow so this is working?
-----------------------

Uhhh... on my local machine. The daily job runs on Heroku which I learned can't install scipy! Luckily I found [a guide to using Anaconda on Heroku to get around this](http://wallfloweropen.com/?project=heroku-app-for-convex-optimization) so I'll try that out.

Why not linear regression?
==========================

Afterwards I was thinking that even linear regression might solve this problem reasonably. There are two issues though:

* I'd need to train the model explicitly to predict downloads at 7 days. If I ever change my mind I'd need to retrain the whole model. I was also feeling lazy and didn't want to do much feature engineering.
* Fitting a log curve is adding bias or prior knowledge: I'm telling it to learn within a very constrained hypothesis space. That makes it more robust with very little data. I could achieve the same with linear regression but I'd need to only supply 3 features which makes feature engineering harder.

Assorted notes
==============

* The data is incomplete: I don't know how many downloads the episodes were getting before I started crawling. So I have to be careful to exclude old releases.
* Similarly, old releases eventually fall of the lists I can scrape (but not all releases of an episode at a time!). To get around that I filter any data that says the number of downloads decreases from one day to another.
* Sometimes I get numerical errors in fitting the curve so I need a plan b.
* When I say I compare against the prediction at day 7, I really mean the scraped value that's closest to day 7.
