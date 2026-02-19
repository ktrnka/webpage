---
layout: post
title: "Predicting League match outcomes: Gathering data"
date: 2015-08-24
---
The goal
========

I'd like to take the results of pick/ban phase of professional League of Legends matches and compute the probability of the winner. In part I find it interesting to watch analysis of pick/ban phase by regular casters or Saint's VOD reviews. How much of the game is *really* determined at pick/ban phase? Was a match unwinnable after a bad pick/ban or is it just slightly harder? How much does it depend on the specific players? How much depends on the history of those two teams? Is there a measurable probability effect from jet lag? And so on.
Unfortunately there isn't that much data for professional matches. The game is constantly changing and the teams/players are also changing quickly. With so many things changing at once, 1-2 games per week per team is probably not enough to easily develop a machine learning system. So I'll work on a simpler problem and try to apply the insights I learn to professional matches.

Trying a simpler problem
========================

**Can I predict the outcome of a non-professional match based on pick/ban and the player histories?** This is an easier problem in a few ways:

1. Data is easier to get - it's available via Riot API.
2. There's *a lot* more data.
3. Even team queue has a lot more data than pro.

So the problem is much simpler now: I need to crawl match info and build up a database of match and player info. Once I have that I can start working on machine learning.

Crawling the data
=================

There's no list of all active matches or all matches per day in the Riot API. The *only* available list has the current featured matches. You can get 5 matches and it updates maybe every 5-10 minutes. At best we can get 1,440 matches per day this way. In practice, there will be duplicates and some matches aren't ranked 5x5. The other difficulty is that I'm using Heroku for scheduling so at best I can run something every 10 minutes, or max 720 matches per day.
To be able to build up data faster I wrote software that acts like a web crawler: You have some starting points or seeds and crawl outwards from there.
In my case there are three seeds from the API:

1. Featured matches
2. List of challenger players
3. List of masters players

The process is constantly adding more player and match ids to lookup. It works like so:

1. Look up all challenger and master players. Add any new ones to the player database
2. Update all players, up to N lookups and prioritize those that have no data or are scheduled for update
   1. Look up their ranked stats and save them
   2. Look up their match history and queue all new matches for lookup
   3. From match history, compute what time and day we expect them to have played 15 new matches and save that as the date to update this player's info
3. Update all ranked 5x5 matches without detailed info, up to M
   1. Usually we have a match id and player ids already but don't know the outcome of the match or various stats.
4. Look up the featured matches and queue all new players and queue the matches

The reason I look up featured matches at the end is because they fail the match lookup before they're completed. So I want there to be enough of a delay for the matches to complete before the match lookups start. In retrospect it would've been better to set a "don't crawl before date" in the database but this mostly accomplishes the same goal except for very long games.

Issues
======

It took some trial and error to get this working. Some of the mistakes I've made at a design level:

* I didn't know about the challenger and masters APIs at first so it all just started from featured. That meant I wasn't getting quite as many high-level games as I wanted.
* I set the player recrawl date incorrectly: At first I took the difference between the first and last match, computed the number of games played per day, then set it to the last match plus 15 games times the rate. But when a player stops plays 15 games in a row then stops for weeks this will put them at the top of the queue for recrawling. Instead you need to set the end date to the current time. (Fixing this dramatically increased what was crawled)
* At first I didn't limit the number crawled per type at all. What would happen is that my script would never finish the per-player lookups before Heroku killed it to start the next run. So I'd never process any queued matches.

Rate limiting
=============

The developer key allows something like 60 requests per minute and 500 per 10 minutes. In theory if you limit to 1.2s or a little higher between requests you should be fine. But there are other internal rate limits that aren't exposed, leading to 429 rate limit exceeded.
Instead of trying to figure it out I just used exponential backoff: Try waiting 1.3 seconds between requests. If you get 429 error, wait 13 seconds. If you get it again, wait 130 seconds. You can continue this but I've never hit a limit after waiting 130 seconds.
This solves the 429 problem 100%. Even if I'm running two copies of the script simultaneously this solves the issue. One side note is that it's kind to Riot servers as well - it's unlikely that you'll ever get two 429 errors in a row so they don't need to waste processing on requests that'll just be rejected.
But there are many other kinds of errors to handle in the API. Some kinds of errors are transient and will clear up in a few seconds anyway (500 and 503 are like this). Others will return the same result every time (400, 401, 404, and 422 errors are like this). For the transient errors I just try them again after the delay. I don't use exponential delays for those cause it isn't necessary.

Python APIs
===========

I took a look at the existing Python wrappers for Riot API briefly and felt that the documentation was a bit lacking so I didn't use them. It probably would've been better for the community if I'd forked their module and added documentation/etc. At first I was just in a rush to get *something* working. And now after developing for a while I have basically yet another API wrapper. Sigh.
To be fair though, it doesn't take a lot of effort to wrap a rest api so it's not that much effort wasted. I would've needed to spend all that time reading Riot docs on the field values anyway.

Compute and storage
===================

Heroku is handy for running periodic scripts with the scheduler addon. I'm using that for hourly processing. I use mongodb on MongoLab for storage, which is great for storing Json. After fixing my design issues I found that I'm hitting space quotas on MongoLab.
As a hack I delete all the stats, timelines, runes, and masteries for participants in matches. This helps but mongo doesn't actually free the disk space - it tries to reuse objects. So I don't get the space back until I run repairDatabase manually.
Even still, I'm running into issues again. MongoLab is migrating all free databases over to MongoDB 3.0 at the end of September, which allows for compression and should greatly reduce my usage.
Probably before then I'll have to strip the records down to their bare minimum so that I can keep crawling.

How well does it work?
======================

It works great except that I'm running out of MongoLab storage space. Otherwise I have about 54k players in the database and 83k matches (but only 53% have been looked up fully).
In any case, it's working well enough that I have a decent data set to use for machine learning and I'll post my early experiments to that end soon.
