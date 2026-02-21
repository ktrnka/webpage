---
layout: post
title: "Predicting League match outcomes: Week 2"
date: 2015-09-02
---

I've continued to log my experimental accuracy in predicting League of Legends matches (see [part 1](/blog/2015/08/predicting-league-match-outcomes-first-week-of-machine-learning/)) and this graph picks up from where I left off last time (around 64% accuracy).

![Experimental accuracy part 2]({{ "/assets/img/posts/wp/image-4.png" | relative_url }})

When I hit 100% I learned I had data leakage. Then it dropped back down after fixing the leakage problems. (1) Also note that the cyclic patterns in the graph happen because I run random forest, then logistic regression, then gradient boosting trees most of the time. If I could do it again I'd make a different column in the spreadsheet for each one.

Gradient boosting trees revisited
=================================

Early on I tried gradient boosting trees but they didn't perform well. They also take a while to train so I stopped experimenting with them. Now that the overall accuracy was decent I decided to revisit them to see if I did something wrong.

While random forests were getting 64.7% accuracy and logistic regression hit 61.6%, gradient boosting trees were 82.5% accurate. Clearly something was wrong.

Data leakage 2.0
================

The easiest way to debug the problem is to inspect the models. I can't actually view all 100 trees in gradient boosting, but I can check out the feature\_importances\_ field of the learned model. They give scores for how much each feature contributes to the overall model. At the same time I can check the feature\_importances\_ in the random forest model and the array of weights for logistic regression. If gradient boosting is clearly learning to cheat and the others aren't, I can compare to see which features are more important in gradient boosting.

The big difference was that gradient boosting trees heavily relied on the win rates computed from match history. There was one set of features for win rate by champion and one set for win rate by champion and game version.

I removed those two sets of features and accuracy was believable again: around 58-59%.

What was the leakage? I never found all the leaks but I found two issues:

There was an issue in the per-player statistics from the [ranked stats endpoint](https://developer.riotgames.com/api/methods#!/1018/3452). I didn't realize but it can only provide stats on a per-season basis and it defaults to the current season. Some of the matches in my database are from SEASON2014 but the stats are SEASON2015. So when I subtracted the match outcome from the win rate, that was incorrect for 2014 matches.

The second issue was another misunderstanding. Say the ranked stats indicate that you played Morgana 1 time and won 0 times. The timestamp indicates that these stats were computed on Monday at 5pm GMT. Now say we process a match you played Morgana on Monday at 4pm GMT and won. This is inconsistent with the ranked stats. Previously I'd make sure neither value could subtract lower than 0 but really if it's inconsistent I shouldn't adjust either the wins or total games played (what I'm doing now).

How could this happen? The match data is being updated in a live database. The ranked stats seem like they're from a Hadoop job. Probably the data is copied over from the live database to Hadoop for batch processing periodically. Then a giant job is used to recompute ranked stats now and then, which may also have some processing time. Even if they're using the same database (say HBase) then the list of matches would be fixed at the start of processing and the timestamps may be set at the end.

The strangest thing is that fixing these two problems increases the accuracy of gradient boosting to almost 100%. So the features more cleanly represent leakage somehow. I couldn't figure out how but decided I should compute match history statistics chronologically anyway.

Aside: Diagnosing by decision tree images
-----------------------------------------

Random forests and gradient boosting trees are both collections of large numbers of decision trees (I'm using 100-500). It's too hard to just look inside. But I can take a single decision tree and visualize that.

Scikit-learn fortunately has [a function](https://scikit-learn.org/stable/modules/generated/sklearn.tree.export_graphviz.html) to export a graph file of the decision tree. Then you can plug it into [webgraphviz](https://www.webgraphviz.com/) if it's small enough or render locally. Unfortunately the trees get so big that they crash renderers. Even with max depth of 5 it's a very horizontal image:

![decision_tree.dot]({{ "/assets/img/posts/wp/decision_tree-dot1.png" | relative_url }})

Second aside: While trying to make a graph fit on this blog post I started lowering the max\_depth and found that actually decision trees aren't completely crap they just overfit horribly with default parameters in sklearn.

Aside: What may have worked
---------------------------

There were predominantly two features that were used. I could have tried learning a decision tree on only those two features and dumping it out. Or plotting a decision surface.

Also, it feels like it's learning to implicitly diff the features and check that two numbers are 1 different when there was leakage because it wasn't something logistic regression was able to learn.

Regenerating the data with win rates computed chronologically
=============================================================

Although it nags at me, the specific bug isn't important. Computing all match-history-based info can be done iteratively as I generate the data if I generate matches chronologically. I process one match then update the win rates for that patch and those champions and move to the next match. Leakage isn't possible when computing it this way (at least for the match history features).

This brought be back down to 57-58% accuracy for random forests and logistic regression. I tried decision trees for prediction out of curiosity and they're around 52-53% with these features. (2)

Using backoff for sparse win rates
==================================

Win rates are just like language modeling probabilities (my background is language modeling). You're computing the probability of an outcome given some conditional information like the champion selected, game version, and/or player. As you use more parameters the data gets very sparse. Often there's no history of a player's win rate on a given champion.

Previously I would default these values to 50%. But now I explicitly set a backoff/fallback value. When computing the player's win rate on a champion, I back off to the aggregate win rate on that champion (both from ranked stats). The most basic form is when the player's data is empty the value should be the more general one. But actually it's even better to handle sparseness such as only 2 games played for champion\_i, player\_j.

So I combine the primary feature and secondary feature based on how sparse the primary feature is.

primary weight = num games played / (num games played + crossover)

secondary weight = 1 - primary weight

The crossover parameter is the number of games at which the two are averaged equally. Through experimentation I found that 10 worked better than 5 or 20. With enough games played the value will default to the primary one (player+champion) but when there are a few games it will nudge the more general value (champion only) towards the player's history. When there are no games at all it'll seamlessly back off to (champion only).

This got me to 60% accuracy with random forests and logistic regression. Gradient boosting trees reached 62.5%.

Lesson learned: Very sensitive to having ranked stats available
===============================================================

Now that the data is extracted chronologically I can compute other features, such as the player's current winning or losing streak. So I regenerated the data with winning and losing streaks.

The numbers dropped down to about 58% accuracy. I played around some more and found that it was 58% even without the new features... the ongoing data crawling from the backend had changed my data and my numbers were lower.

After poking around I found that tons of player ids were queued up to have their ranked stats pulled in for the first time. So I halted the ongoing crawling and wrote a script to do a one-time crawl of ALL players. This took half a day but when it finished and I found that random forests and logistic regression were back up to 60% accuracy. Gradient boosting was about 61.2%.

It's a good thing that I learned that accuracy is so sensitive to fetching ranked stats to compute player win rates. But it's also a shame because it means my system needs full coverage of that long list of players, which takes a while.

Beyond this I reduced my features from about 52 to about 42, which speeds up training and very slightly improves accuracy by making the models more general. Mostly I dropped several \_min and \_max aggregate features.

What's next?
============

Currently I'm working on two initiatives:

1. Which matches are more predictable? I'm trying to break down prediction accuracy by player skill level, game version, etc to understand the value of what I'm building.
2. Riot approved my app key so I can query much faster. At the same time I need to drastically reduce data stored on MongoLab so I'm refactoring to store just skeleton info in MongoLab like match ids, player ids, timestamps, and player rankings. And I'll cache Riot API lookups in a mongo instance on my own machine running mongo 3 for compression. So far the refactor is going well but it takes time.

Notes
=====

(1) I'm calling it data leakage but specifically I mean that the features used to represent the problem unintentionally contain a feature that's derived from what we're trying to predict. For instance, when I subtract out the result of the match from the win rates that can leak information if I do it incorrectly.

(2) I later found that decision trees can do reasonably well with hyperparameter tuning. With default params I got around 52% accurate. With a little tuning I got 58.5%. Compare to 60.4% for logistic regression with slight tuning.
