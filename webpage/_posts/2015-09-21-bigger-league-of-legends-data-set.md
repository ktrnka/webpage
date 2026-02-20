---
layout: post
title: Bigger League of Legends data set
date: 2015-09-21
---

Background
==========

Riot granted me an app key so I can crawl a lot more data. The downside is that I had to re-engineer much of my system because I couldn't use free MongoLab tier with that much data. To give some ballpark sense, my mongo data directory is 46gb for 1.8 million matches and 1.2 million players.

The larger data set should lead to more accurate predictions of who will win. But first I want to check the distributions in the data in case anything's changed.

The old code started entirely from featured matches. The featured matches endpoint gives 5 matches which gets me 50 players. For each queued player I'd look up their most recent 20 games and add those matches. Then I'd also get a list of new players from those matches. And I'd repeat this over and over.

There were a couple more tweaks: I'd set a date for when each player's history should be refreshed by estimating when they'll have 20 new matches. And I skip 3v3, ARAM, or other games; I only crawl ranked 5v5.

The new crawling setup starts from featured matches but also crawls the endpoint of challenger and master leagues. Instead of loading their match history I use the new match list endpoint which lets me get their entire season 5 history at once and when I'm recrawling I can get exactly the new games. Beyond that it's the same just that I can crawl much more quickly. And I'm also looking up their current league too.

Game version
============

The majority of my old data was from when I started crawling: 5.14-5.16.

In the new setup it's pretty even from 5.5 to 5.16.

![Matches crawled by version]({{ "/assets/img/posts/wp/image-5.png" | relative_url }})

5.17 doesn't have much data because it was just released when I did this crawl. The blip in 5.7 is around when URF mode was released - maybe that increases ranked play as well?

Either way, I have a much more even distribution across versions than before.

Players by tier
===============

The old code figured out a player's league by the highest league they've reached in the past - this info is easily available in the match data for the game to set borders at the loading screen.

The majority of players were diamond but also many players are new and didn't have a value:

![Games by most common highest achieved season tier in old data set.]({{ "/assets/img/posts/wp/games_by_tier.png" | relative_url }})

The new data is a much cleaner distribution: many more players in platinum than diamond, gold than platinum, etc.

![Players by league in the updated data set.]({{ "/assets/img/posts/wp/image-6.png" | relative_url }})

This is similar to the distributions shown on [League of Graphs](http://www.leagueofgraphs.com/rankings/summoners-distribution) and [League of Legends Summoners](http://www.lolsummoners.com/stats). One of the interesting parts of those sites is showing the stats by division as well; you can see that division V typically has many more players than other divisions. That's because it's easier to be promoted a tier than demoted a tier.

![image (7)]({{ "/assets/img/posts/wp/image-7.png" | relative_url }})

The same trend is shown - there are many more players in gold V than silver 1, for instance. (The league labels got mangled a bit when exporting from google sheets, sorry!)

Blue side win rate
==================

Overall the blue side has a small advantage. In solo queue the blue side wins 50.5% of the time. Previously I saw that [it varies by league](/blog/2015/08/predicting-league-match-outcomes-first-week-of-machine-learning/) but wasn't statistically significant (read: possibly due to randomness). But now I have enough data that the trends are statistically significant!

Win rate by tier in solo queue
------------------------------

![Thick line is the win rate. Thin lines show plus or minus one standard deviation. Note that the axis doesn't go to zero.]({{ "/assets/img/posts/wp/image-15.png" | relative_url }})

For the curious, see note (1) on how the tiers are computed.

From platinum down to bronze the blue side has a win rate of 50.8% to 51.2% and those stats are roughly within a standard deviation of each other (not significant).

But then the blue side has a 48.5% win rate in diamond and 47.0% in masters! The change from platinum to diamond is significant and so is the change from diamond to master. The difference between master and challenger could just be randomness; there aren't enough challenger games to tell for sure.

Maybe breaking it down by division will help find what's going on?

![Thick line is the win rate. Thin lines show plus or minus one standard deviation. Note that the axis doesn't go to zero.]({{ "/assets/img/posts/wp/image-17.png" | relative_url }})

The entirety of the drop happens between platinum I and diamond 3, dropping from 50.4% win rate for blue down to 47.4% win rate. Each of those successive drops is statistically significant.

Possible explanations:

* Red side gets first ban and first pick. Maybe players don't take full advantage of this until around diamond III.
* The red side (higher elo) will tend to have more professional players from LCS. This is something I heard Heisendong say: At high level, some wins are determined based on which team gets LCS pros (like how at low level some losses are due to disconnects).

Win rate by tier in team queue
------------------------------

Last time I analyzed only 44 thousand games and about 14 thousand were team games. There wasn't really enough data to get a clear picture.

Now the trend for team games is clear.

![Thick line is the win rate. Thin lines show plus or minus one standard deviation. Note that the axis doesn't go to zero.]({{ "/assets/img/posts/wp/image-14.png" | relative_url }})

The changes from silver to gold, gold to platinum, platinum to diamond, and diamond to master tier are significant. There isn't really enough data for bronze to say and challenger data is so sparse that I didn't show it.

The closest published stat I could find was 52.8% win rate for blue side in team queue vs 50.9% for solo queue on [League of Graphs](http://www.leagueofgraphs.com/rankings/win-stats) but that doesn't show the effect of higher tiers.

There are two clear trends: 1) blue side has a bigger advantage in team queue than solo queue and 2) the advantage grows at higher rankings.

It seems to agree with professional results: overall 57% win rate for blue side and 59% in NA+EU Spring split 2015 according to [esportsfanz](https://esportsfanz.com/blog/red-vs-blue-how-serious-is-the-win-rate/).

The overwhelming advantage of blue side in team queue is likely due to first pick and ban. Like solo queue, players at platinum begin to take more advantage of first pick/ban and it escalates to master tier. The advantage in team queue is likely much greater because you're coordinating the draft strategy with your teammates. Furthermore, trading your pick is more effective with a team than with random solo queue players.

From what I can tell, the overwhelming first pick advantage is why OGN uses blind pick in game 5 of a best of 5: If the teams are so close that they make it to game 5, first pick advantage won't be the deciding factor of the entire match. (2)

Notes
=====

(1) To get the tier+division of a match I convert all players' current tier, division, and league points into their total league points. I filter out anyone that's division V with zero LP because I don't know what their level should be. Then I average and convert back from league points into tier, division, and leftover league points.

I need to improve this for team games by looking up the league of the team not just the individual players.

(2) There's a wealth of practice and information for regular draft but do they have enough analyst support for blind pick? How hard is it to practice challenger-level Zed vs. Zed play? That said both teams have the same challenges so it should still be fair.
