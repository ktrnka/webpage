---
layout: post
title: "Predicting League matches: Are some matches more predictable?"
date: 2015-09-09
---

I've been working on improving the accuracy of my machine learning models and redesigning my software now that I have a much lower rate limit.

But I've been wondering whether some matches are more predictable than others. I'm sure it's true but I don't know what the trends are. Possibly lower skill players make more errors in pick/ban phase? Sometimes a game change makes a champion too strong and matches seem more predictable if one side gets them.

Setup
=====

I'm evaluating random forest classification with 10-fold cross validation. After making predictions and computing prediction accuracy I can analyze for correlations between accuracy and various properties (1):

* What's the accuracy in patch 5.16 vs 5.15?
* What's the accuracy at high skill vs low skill?
* What's the accuracy when certain champions are picked?

Just to be extra clear, I'm not looking at win rates. I'm looking to see **how well my model is learning in certain situations**. This will help me assess the strengths and weaknesses of my model and the features I'm using.

I'm testing this using random forests with hyperparameters that were good in previous tests. The results would probably differ slightly for gradient boosting trees and may differ more for logistic regression.

Game Version
============

Riot updates the game balance about every two weeks. Sometimes new champions are added and they may be too strong or too weak. Champions are tweaked and may become too strong or too weak. The most egregious recent change was 5.16 in which Skarner was nearly 100% banned or picked.

![Prediction accuracy by version]({{ "/assets/img/posts/wp/image-3_2.png" | relative_url }})

I dropped versions with fewer than 100 matches. Most of the data is 5.14-5.16 so those patches comprise most of the overall average. The big blips seem statistically significant unless I computed standard deviations incorrectly.

Some comments on what changed in some patches:

* 5.13: Devourer reworked (some junglers very strong now). Runeglaive buffed, making mid Ezreal even stronger. AP item overhaul making build paths easier. Tahm Kench released but very low win rate.
* 5.14.0.329: UI overhauled. Gangplank reworked, above average strength. Miss Fortune update (bot adc), brought up to average. Elise (jungle) buffed, becomes near 100% pick or ban. Ryze (top) nerfed, almost not played anymore. Runeglaive Ezreal no longer viable.
* 5.15: Fiora (top) reworked, underpowered at first and minor patch to improve her. Sivir (bot adc) ult nerfed.
* 5.16.0.342: Skarner (jungle) overpowered. A few strong top laners. Elise (jungle) nerfed. New items for tanks. Armor items reworked (generally armor lowered).
* 5.16.0.344: Skarner hotfixed to be less strong.

It's tough to summarize each patch in one or two sentences (the patch notes are several pages long and don't clearly indicate what each bug fix version number means). Originally I was thinking that patches with overpowered or underpowered champions would be more predictable. That's certainly the case with the Skarner patch. But it's not the case with the Elise patch.

My feeling overall is that the differences are fairly small. In general if my model were very good then probably any patch with major changes is hard to predict until we have enough data on the changing win rates. Patches with overpowered champions might be more predictable. Even if they're consistently banned this gives a small advantage to blue side in ban phase.

League tier
===========

Your ranked tier is a rough measure of overall skill level: bronze, silver, gold, platinum, diamond, master, and challenger. Are matches more predictable in bronze? In a previous post I saw a blue side advantage in low tiers and red side advantage in higher tiers.

If you aren't familiar with League of Legends one thing to note is that the number of players at each tier follows a sort of exponential distribution. See LoL Summoners' Global Stats (page no longer available) for instance. 27% of players are bronze, 42% silver, 20% gold, 8% platinum, 2% diamond, 0.04% master, 0.02% challenger.

Note that I'm still just using highestAchievedSeasonTier which is the max of all previous seasons and many players don't have a value. Also I have the median value for blue and red side separately so I only counted games where they were the same.

![Prediction accuracy by tier]({{ "/assets/img/posts/wp/image-41.png" | relative_url }})

Aside from platinum the others are all within about a standard deviation of one another. I don't even have a guess as to why platinum is less predictable; it has the most data of these groups.

Maybe when I look up their current season tier and crawl more data I can update this and get more accurate results. That should confirm the weird dip in predictability of platinum matches or show that it was an artifact of the way I was measuring.

Champion selection
==================

Do we better know the outcome when certain champions are picked? Many players feel some champions are really bad and the game is lost if they're picked (Teemo, Yorick, and Tahm Kench come to mind. Urgot used to be this way).

There are 126 champions and I can't graph that well. Plus it may lead to poor conclusions. Instead I'll look at the difference from average over the standard deviation, or the standard score. 2-3 standard deviations away from average is pretty significant. (2)

Here are the champions with the highest deviations in prediction accuracy from the average of 60.3%:

* Varus: 64.0% accuracy in 2,200 games (z-score 3.62)
* Nocturne: 63.7% accuracy in 2,116 games (z-score 3.21)
* Tahm Kench: 63.1% accuracy in 2,363 games (z-score 2.82)
* ...
* Kha'Zix: 58.1% accuracy in 2,829 games (z-score -2.40)
* Galio: 53.7% accuracy in 650 games (z-score -3.38)

Of these champions, Tahm Kench and Kha'Zix have pretty low win rates. Varus and Galio have win rates that are very dependent on the lane in which they're played.

One problem in analyzing this data is that the impact of champion picks is very dependent on the game version and individual player. If we have a few Varus mains with over 200 games played on him, they will likely have much higher win rates and lead to more predictable matches.

I don't feel comfortable drawing any conclusions from this analysis except to say that looking at individual champions alone clearly doesn't explain what my models are learning. In previous experiments I found that indicator variables for champion picks didn't help the model; it added too much sparseness and the model couldn't learn as well. So the models can't easily learn to predict outcome purely based on the champions.

Thoughts
========

It's tempting to draw conclusions that fit my intuitions with respect to predictability. But that would be biased interpretation of the data. I don't think my intuitions are upheld in this analysis with respect to predictability of game versions, predictability at different levels, or predictability in the presence of certain champions.

The conclusions could differ when I redo this with a much larger data set, especially when I get players' current tier rather than max tier from previous seasons.

What's next?
============

I redesigned much of my crawling and storage infrastructure to handle a much larger number of matches. It isn't optimized yet but I have full match data for 1.8 million matches and ranked stats for 94 thousand players. In the short term I'm regenerating my feature matrix to test machine learning with much more data and I'll report on the results of that.

I've also crawled each player's current tier/rank and I can experiment with features again once I experiment on the larger data set. I'll revisit feature engineering in general.

Beyond that I'll likely revisit hyperparameter tuning and then try out neural networks (there may be enough data to make use of them now).

And eventually I want to start focusing more on ranked teams - at a high level teams have match histories against one another which better mimics professional play.

Notes
=====

(1) I'm not saying features because I don't directly include the game version in the features (it was too sparse to be useful).

(2) I'm being cagey about claiming statistical significance because I'm doing multiple tests - the chance of one accidentally passing a significance test is reasonably high. I'm just doing a quick test to get a ballpark idea for now because I'll soon redo everything with a much larger sample size. At that time I'll look into doing statistical analysis that is more robust.
