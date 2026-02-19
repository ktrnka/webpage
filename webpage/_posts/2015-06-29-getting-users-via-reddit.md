
---
layout: post
title: Getting users via Reddit
date: 2015-06-29
---
It's tempting to focus purely on the engineering or research of a project. Hmm tempting isn't the right word... it's the default approach. In a typical software engineering or research job, you're trained to leave other aspects of the project to marketing/business/etc.
However for side projects the entire solution is your responsibility. That means not just making a great product but also acquiring customers or users. And even making a great product involves graphic design, user feedback, support, and other areas outside of a research-and-development role.
So last week I tried plugging [Over 9000](http://www.over9000.me/) on Reddit to grow the user base and learn more about achieving traction.

What I did
==========

I made a thread in [/r/dataisbeautiful](http://www.reddit.com/r/dataisbeautiful/comments/3avzno/popular_anime_shows_by_downloads_per_episode_oc/) and [/r/anime](http://www.reddit.com/r/anime/comments/3aw9ru/over_9000_automated_ranking_of_current_popular/) with a link and short description tailored for each subreddit. /r/dataisbeautiful has 3.4 million subscribers and /r/anime has 288k. After making the two threads I emailed some friends and asked them to upvote. My goal was to get enough upvotes to get onto the default/hot list for each subreddit for a few minutes. Or at least to stay on the first page of the new list for a while. I monitored comments for a few hours and replied to any questions quickly.

Feedback
========

There were unfortunately no comments on /r/dataisbeautiful. I was hoping someone would have a good idea of how to make better use of my data.
The comments on /r/anime were useful and the biggest bug report is that shows are sometimes split into two. I'm working on a solution for that.

Data
====

I'm using Google Analytics and it shows some interesting trends. First up are page views for June 2015:
![Page views by day, peaking on 6/23](/assets/img/posts/wp/image.png)
I made the Reddit threads on 6/23. Before that I'd been getting at 0-80 pageviews per day. But the Reddit threads produced 533 views on 6/23 and 131 on 6/24. Since then it's back to regular levels but there are no days with zero views.

Demographics before Reddit
--------------------------

One of the difficulties in using Google Analytics is that much of the traffic is fake. 14% of the traffic is from fake referrals (see [this](http://viget.com/advance/removing-referral-spam-from-google-analytics)).
Looking over the flow, 98% visit the front page then leave.
Geographically most the traffic is from the United States but also some from China, Japan, Germany, and Brazil and a little from other countries. Location is not set for 24% of sessions and those sessions have average duration 0 sec (probably web bots). Here's the [raw data](https://docs.google.com/spreadsheets/d/1W7r6QKulbF6hzlaa25Pma27Ud5GXEiNklUjN3fGR8eE/edit?usp=sharing).
![Map of the page views before Reddit](/assets/img/posts/wp/image-1_2.png)
99% of visits are from desktop over this time period. The only 3 visits from mobile were all from my own phone.

Demographics after Reddit
-------------------------

Fake referrals make up only 4% now!
96% of visits view the front page and leave (down from 98%). That means more users are visiting the Winter 2015 or About pages (but only a few).
Geographically the distribution has only 7% unset locations (vs 24%). The United States is 51% of sessions (vs 34%). English-speaking countries follow the US: Canada, UK, and Australia. Maybe Reddit is biased more towards English-speaking countries? [Raw data link](https://docs.google.com/spreadsheets/d/15tYNTU2zDOuYKOmC_zFURdli_q9W5bTR81hnfJJNBp0/edit?usp=sharing).
![Map of page views after Reddit](/assets/img/posts/wp/image-2_2.png)
The device demographics from Reddit are different: only 72% from desktop (vs 99%). 23% from mobile and 5% from tablet. I'm glad the site is responsive to device size!
In browsing the data I saw that Google Analytics tracks page load speed:

main page: 2.45 sec (that's horrible!)
winter2015: 0.45 sec
about: 0.00 sec

When I look at pre-Reddit numbers they're all 0 sec. The slow load of the front page is due to external CSS/JS which is fast for repeat users and slow for new users. Although the resources are hosted in CDN, Materialize isn't popular enough that new visitors already have it cached. Likewise my own CSS isn't going to be in cache for new visitors. In the future I'll try inlining these.

If I could do it over again
===========================

* I'd track how many referrals came from each subreddit. If I remember correctly you can add a param like utm\_source=blah to the referring URL to do that.
* I'd solicit more friends in advance to keep the threads trending for a little longer and try to get them in sync to upvote at around the same time. Once the thread is off the first page it's basically dead.
* I'd look up more ways to get a post onto a subreddit front page.
