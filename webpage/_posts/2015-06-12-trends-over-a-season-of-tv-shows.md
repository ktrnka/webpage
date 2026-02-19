---
layout: post
title: Trends over a season of TV shows
date: 2015-06-12
---
If I plot the number of downloads per episode over the length of an anime series, are there interesting trends? I'm using the data and estimation methods from [Over 9000](http://www.over9000.me/) and graphing the number of downloads for each episode 7 days from when the torrent is available.
I'm also showing a shaded region to indicate potential error in the estimate: When we extrapolate from only a little data then it's less reliable.

Winter 2015
===========

I picked out some of the top shows of the season to investigate.
![Parasyte - the maxim](/assets/img/posts/wp/parasyte-the-maxim.png)
![Tokyo Ghoul A](/assets/img/posts/wp/tokyo-ghoul-a.png)
![Aldnoah Zero](/assets/img/posts/wp/aldnoah-zero.png)
![Log Horizon 2nd Season](/assets/img/posts/wp/log-horizon-2nd-season.png)
![Death Parade](/assets/img/posts/wp/death-parade.png)
![Durararax2 Shou](/assets/img/posts/wp/durararax2-shou.png)
The data is quite messy, partly because I was working out the kinks during the Winter and couldn't re-scrape any old data with updated code. There's a drop in the middle of the season for several shows that seems to be a bad bug (since fixed). Aldnoah.Zero has a couple weird data points for episodes 1, 4, and 7 even though the show started at episode 13 in the Winter. Similarly, this was the second season of Log Horizon and there was a tiny amount of data for episode 11 which was season 1.
Even ignoring some of those blips the data isn't very consistent. I'd expected them all to have a downward trend - losing some percent of viewers every week. But only some shows look that way.

Spring 2015 (ongoing)
=====================

![DanMachi](/assets/img/posts/wp/danmachi.png)
DanMachi is an interesting case because there's very little drop-off in viewers as the show progresses. Some ups and downs that may just be noisy data.
![Seraph of the End](/assets/img/posts/wp/seraph-of-the-end.png)
Seraph of the End has a very smooth curve - it seems consistent with my guess that people try out shows for a couple episodes before deciding to watch the whole season.
![Fate Stay Night - Unlimited Blade Works](/assets/img/posts/wp/fate-stay-night-unlimited-blade-works.png)
![Fatestay night Unlimited Blade Works (2015)](/assets/img/posts/wp/fatestay-night-unlimited-blade-works-2015.png)
First off, my code didn't merge all of the torrents for Fate/Stay UBW correctly so there are two groups here. The difference is that one of them was linked up to a page for 2nd season and the other was linked to the first season page. Both seasons are 12 episodes and you can see that the first graph has the bulk of the data starting at 11-12. This happened because I had just started scraping in January so I only barely caught the end of Fall 2014 season.
Regardless, the interesting thing is that there's no drop-off between episode 1 of second season and episode 2 (in the top graph that's ep 13 and 14). This may be a fundamental difference in a show that's split into two quick seasons.
The other interesting trend is that it's getting more downloads in 7 days as the season goes on.
![Shokugeki no Souma](/assets/img/posts/wp/shokugeki-no-souma.png)
This show looks "normal": early drop off then leveling.
![Kekkai Sensen (Blood Blockade Battlefront)](/assets/img/posts/wp/kekkai-sensen-blood-blockade-battlefront.png)
There's very little ep 1-2 dropoff here and a strange blip at episode 7.
![Highschool DxD BorN](/assets/img/posts/wp/highschool-dxd-born.png)
Another strange trend but overall downward. The data looks correct for episode 1 but I don't know why it'd be so much lower.
![Plastic Memories](/assets/img/posts/wp/plastic-memories.png)
Normal downward trend.
![Arslan Senki (2015)](/assets/img/posts/wp/arslan-senki-2015.png)
![Arslan Senki (The Heroic Legend of Arslan)](/assets/img/posts/wp/arslan-senki-the-heroic-legend-of-arslan.png)
Arslan Senki ended up with two entries even though it's the same show. That happened because google search linked one to the 2015 version and the other to the 90's series. The show tends to lose viewers each week with less of a plateau than other shows.
![Ore Monogatari](/assets/img/posts/wp/ore-monogatari.png)
Another drop-off between episodes 1 and 2 then slow decline.

Rough trends
============

Shows roughly lose downloads/viewers from one episode to the next. More people stop watching early on, probably they're just checking it out to see if they'll like it or not.
But the data is quite noisy, especially any older data. And certain shows buck the trend - DanMachi for instance retained almost all its viewers and Unlimited Blade Works gained viewers over time.

Can we predict ratings?
=======================

It's great when people rate shows on sites like [MyAnimeList](http://myanimelist.net/)but it's a small percentage of the viewers and many wait to rate until the show is over. It'd be great if we could use the shape of the curves to indicate how good a show is.
I looked at the data from 6 shows in Winter and 7 shows in Spring as a proof of concept experiment. I manually picked the first episode of the season and the last episode with reliable data. Then I computed the percent of viewers that stayed all the way through.
Separately I found the ratings for each show on MyAnimeList and correlated with viewer retention. The Google Sheet is available [here](https://docs.google.com/spreadsheets/d/1cAZqNIEnNJPm-ab6F8tRBZDjgT2oABC_qkfU_Kjmsfk/edit?usp=sharing).
![Scatter plot of retention vs MAL rating](/assets/img/posts/wp/image-3.png)
There's some correlation there but the Pearson correlation value is only 0.59. Viewer retention clearly isn't everything.
What about correlation with the total number of downloads for the last episode? That's only slightly better at 0.63. Correlation with the downloads of the first episode is 0.61 (that's better than retention).

Looking into Winter and Spring separately
-----------------------------------------

What if we analyse completed shows and ongoing shows separately? I didn't expect it but they exhibit drastically different trends.

### Winter

The most correlated value with ratings is retention, with a coef of -0.08. That's so low that there's really no correlation at all.

### Spring

The most correlated value is retention (percent viewers from first ep still watching at last). This has a correlation coefficient of 0.80!

What does it mean?
------------------

**Viewer retention isn't predictive of a show's eventual rating. But it's very predictive of the show's rating while it's still airing.** I suspect people that stop watching give low scores while the show is airing but when it's finished a much larger group of people give true ratings.
So we haven't learned how to assess show quality by torrent downloads but we've learned something about what the ratings mean for still-airing shows.

Notes/Caveats
=============

1. I would've preferred to use Spearman correlation over Pearson because I didn't expect a linear relationship between retention and ratings. But I didn't see an easy way in Google Sheets.
2. I half expected the graphs to be pure noise but some of them are noise-free. It seems that noise-free graphs may be achievable. But there may be trends I don't understand yet, such as the impact of v2 releases or delays.
