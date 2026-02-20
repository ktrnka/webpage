---
layout: post
title: "Predicting League match outcomes: First week of machine learning"
date: 2015-08-25
---
*Edit 8/26: I meant to include learning curves but forgot. Added initial learning curve and final learning curve.*
Just a reminder, my goal is to predict the winner of a League of Legends ranked 5x5 game based on the pick/ban phase, including any player stats. This is an intermediate goal towards predicting the outcome of professional matches.
Before you read much further, decide on your own hypotheses: How accurate is good? How accurate is bad? Is 100% achievable? What would it mean? (Look back after reading more to assess your predictions.)
In the [previous post](/blog/2015/08/predicting-league-match-outcomes-gathering-data/) I described my infrastructure for building a database of players and matches from the Riot API. This one will describe the process of machine learning including the horrible failures.

Data and evaluation
===================

Once my crawling infrastructure was running semi-smoothly I started working on the machine learning infrastructure. At first I had about 20,000 matches crawled. As I went on I updated the dataset and it's now about 44,000 matches. The reason I updated the dataset during experimentation is 1) I goofed in my software design so that any time I needed to add new columns from the match data I had to reprocess all of my match collection and 2) 20,000 really isn't enough for good machine learning in this space. Now I'm keeping my data stable for a few days of experimentation then updating if/when I get significantly more.
For evaluation I'm using [10-fold cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#k-fold_cross-validation) so that all matches in the data set contribute to training and testing (but at different times - I'm never testing on my training data except to judge how much I'm overfitting).
I'm evaluating in terms of accuracy: the percent of the time that I correctly guess which side will win.

Problem setup
=============

Two-class classification is straightforward: the output is a simple yes or no. To convert this problem, I'm predicting whether the blue side will win.
The following is a graph of experiments from August 18-24. The left side is the oldest experiment and right side is the most recent.
![Accuracy over time]({{ "/assets/img/posts/wp/league_match_prediction_graph1.png" | relative_url }})
There was a terrible mistake in the middle and I wanted to hide it for the purpose of graphing, but I think it's important not to hide mistakes so that we can learn. Aside from that middle part there's a rough upward trend. I started off around 51-55% accuracy and now I'm achieving 61-64% accuracy.
I'll discuss these four phases separately:
![Accuracy over time in 4 regions]({{ "/assets/img/posts/wp/league_match_prediction_graph_annotations.png" | relative_url }})

Phase 1: Basics
===============

When starting out I do a few things:

1. Try to understand my data
2. Build a very basic set of features for each match
3. Test a few machine learning algorithms and tune hyperparameters

Exploring the trends
--------------------

I have a basic understanding of why teams win from playing the game. Overall I know that blue side has an advantage but that in ranked matches Riot puts the higher ranked team on red side and also gives them first pick/ban to balance out the blue side advantage. Also it's clear that certain champions have a higher probability of winning than others and it's dependent on the game version (changes every 2 weeks).
Overall let's look at win rate by side in this data:

Blue side: 50.6% win rate (in 43,905 ranked games)

Compare this to [League of Graphs](http://www.leagueofgraphs.com/rankings/win-stats), which shows 51% win rate for solo queue and 52.9% for team queue. They probably have more data than me and it's probably more balanced between different levels of play. I started crawling from featured matches and challenger/master so my data is likely biased towards the top levels of play.
But even then, given a game how do I decide whether it's diamond level or gold level? The Riot API doesn't provide this information. There are two methods:

1. In the match participant info, the highestAchievedSeasonTier tells you the highest tier they achieved in previous seasons, which is used for the loading screen borders.
2. You can look up the current league/tier each player is in. But you can't look up the tier they were at the time they played a game in their match history.

#2 is probably more accurate but adds a ton more server lookups so I'm using their highest previously achieved tier as each player's current level. Given each individual's ranking I combine them by taking the most common one. Sometimes that may mean the most common is unranked though. (1)
![Games crawled by most common highest achieved season tier]({{ "/assets/img/posts/wp/games_by_tier.png" | relative_url }})
Even though I started the crawl with current challenger and master players most of what I get are former diamond and platinum players and a ton of formerly unranked players.
How does it break down by solo queue and team queue? I prioritize team games higher when crawling but solo queue is more popular.
Solo queue: ~30,000 games
Team queue: ~14,000 games
So I have a good number of team games to hopefully learn different trends.
Looking at the blue side advantage by queue and tier:
![Blue side win rate by tier and queue]({{ "/assets/img/posts/wp/win_rate_tier_queue_fixed.png" | relative_url }})
I have zero master team games so that data point is missing. In solo queue there's an interesting trend where the blue side has more advantage at lower ranks and red side has advantage at higher ranks. In team queue the blue side is even or favored to win at all ranks.
I tested statistical significance between a few pairs like solo queue silver vs platinum but the difference wasn't significant. In other words, it's possible that the difference between any two pairs is just due to random chance. There's clearly something fishy and it's possible that more data would reveal a difference that can't be attributed to chance. Or it's possible that there's a better statistical test for this situation which is sort of a mixture of rank correlation with binomial distributions.

### Per champion win rates

It's common to analyze win rates by champion per patch. For just starting out I did by champions only. There are two ways to compute win rate and they led to different numbers:

1. From ranked summoner stats add up wins and losses
2. From matches add up wins and losses

I expected the same results but was wrong. What I found led me to this:
Total win rate from matches: 50.0% in 439 thousand instances (num matches \* 10 players)
Total win rate from summoner ranked stats: 52.5% in 2.9 million instances
At first I thought there must be a bug but didn't find any. I'm guessing that it's because my crawl is biased towards higher level players. For a player to reach diamond they had to have a higher than 50% win rate for a period of time and then stabilize at 50% once they reach their skill level. So their total history is over 50% win rate but their recent history should be around 50%. (2)
Win rates by champion look pretty sensible so I won't get into that.

Basic machine learning
----------------------

For machine learning we need to reduce each match to a fixed-size list of features. The features generally can be yes/no, numeric, or categorical. I started with the following:

1. Is this solo or team queue?
   1. 1 feature
2. What's the most common tier on each side?
   1. 2 features
3. One feature per (side, champion), for instance: Does blue side have Ahri? Does red side have Ahri? Does blue side have Annie? Does red side have Annie?
   1. 272 features

I started with three classifiers:

1. Random Forest: Easy to use and generalizes well especially with lots of trees. Flexible with feature inputs but can be slow.
2. Logistic Regression: Also easy, especially with numeric or yes/no inputs.
3. Gradient Boosting Trees: Kaggle competitions are usually won by a neural network or by gradient boosting trees. When I've used them they tended to beat out random forests but are slower to train.

My first 6 experiments were just variations on these three with some hyperparameter tuning, like the number of trees for random forests, min\_samples\_split for random forests, or the regularization constant for logistic regression. My conclusion from this was that gradient boosting wasn't helpful when random forests had the same number of trees and that logistic regression was comparable but much faster to train than both. Logistic regression with L2 regularization was better than L1. From then on out I stopped using gradient boosting and stopped trying L1 regularization in logistic regression.
I converted the highestSeasonAchievedTier to numbers like challenger=1, master=2, diamond=3, ... and took an actual average. At first I accidentally did integer division rather than floating point but when I used floating point division I found the results were slightly worse. Probably it's because it's allowing the classifiers to try and do comparisons that are too sparse.
I generated a learning curve with random forests to check whether I'm overfitting or underfitting.
![Learning curve for random forest classifier with 10 trees. Regularization params disabled.]({{ "/assets/img/posts/wp/learning_curve_orig_no_reg.png" | relative_url }})
It's the worst of both worlds! The gap between training and testing is enormous (overfitting). It's a little better if we set min\_samples\_split but still flat. So even regularization methods don't help. At the time I felt that we were also underfitting because additional data doesn't help but I was wrong - it's fitting the training data almost perfectly.
In a moment of desperation I tried enriching the feature space on the mistaken assumption that I also had underfitting. I felt that it's silly to just check if Annie is on blue side. Annie could be played mid or support or honestly some people probably play top/jungle/adc Annie (and probably would have lower winrates doing so). But unfortunately I'd removed the timeline data which indicates the lane each player is in to save space. Instead I tried just doing fields like Blue.Player1.IsAnnie, Blue.Player1.IsAhri, etc. At this point I also included the summoner spells - it's useful to know whether a support player selects ignite or exhaust for instance. So I had more columns like Blue.Player1.HasExhaust and so on. Instead of the 272 champion indicator features this is 1,260 champion features and 220 summoner spell features.
This was much worse! The summoner spells generally were used in the classifiers but the model was overfitting.
I went through some twists and turns in desperation and found that per-side champion indicators were better than per-side-per-player and the same trend held for summoner spells, so now I had Blue.NumFlash, Blue.NumIgnite, and so on. In other words, champion features were back down to 272 and summoner spell featured were reduced from 220 features to 22 features.
These tweaks took me from my initial 52.6% accuracy to 54.4% accuracy.

Phase 2: Elation, depression, and typos
=======================================

The second phase was about looking up each summoner's win rate history with the champion they're playing and their win rate history overall. So I had columns like Blue.1.ChampionWinRate, Blue.1.ChampionGamesPlayed, Blue.1.TotalWinRate, etc.
I knew I was cheating - the ranked stats may have been crawled after the specific match so it may be leaking the outcome of the match. Even with leaking info the accuracy was around 74%. (I'd expected higher)
Then I added some code to subtract out the outcome of the match in question when looking up win rate and played rates. **Unfortunately I had two variables named "won" and unintentionally subtracted 1 win every time so the models could deduce the outcome**. Still, I was fooled because subtracting it out decreased accuracy to 69% so it seemed like I'd solved the leakage of data.
I tried experiments for days but when I went to refactor some code, accuracy mysteriously dropped to 56%. Once I learned my issue I realized that also all the intermediate conclusions were invalid - why would the random forest use another feature if it already knows the outcome some of the time?
So I fixed the bug and started over from 56% accuracy.

Phase 3: Reality check
======================

Progress can be slow in feature engineering. If I had maybe 1000x more data perhaps I could throw this all into a neural network and avoid grinding away at it but I only have 44k data points.
This phase was a grind to work up from 56% accuracy to 59%. Then I updated my data and dropped back down to 58%.
For starters, the progress from 54% accuracy in phase 1 to 56% accuracy was solely due to each player's win rate. Previously I'd seen that having separate features per player made the data too sparse so I took the sum, min, and max to make features like Blue\_Champion\_WinRate\_Sum for the sum of win rates from player history on those champions (subtracting out the outcome of the match if appropriate).
Some of the experiments:

1. Total number of games played per player (combined with sum, min, max, and log of the sum). Helped a little
2. Breakdown of expected damage types (percent physical, magic, true damage)
   1. Note that this started to show differences between random forests and logistic regression. For random forests the actual number was best. For logistic regression it was better to have features like "top 20% most physical damage comps" or "top 20% most magical damage comps".
   2. This would be correlated with win/loss because it's easier for opponents to itemize defensively against a single type of damage.
3. Added win rate features from the total win rates of all players on the champions played (again combined with sum, min, max).
4. (Failed) Tried individual win rate on the champion divided by popularity. I was hoping to identify people that were good with rarely picked champions because they get an element of surprise. But it wasn't helpful.
5. Dropped all champion indicator columns. This gave me a good improvement and somewhat shocked me. What I learned is that with this amount of data it's much better to build in champion knowledge to aggregated stats like win rates and damage types. Including these columns causes the algorithms to overfit the training data more.
6. Revisiting hyperparameters. Random forests improved more with 500 trees but it's slow to train so usually I run with 100 trees.
7. Refreshed my data and lost 1% accuracy :( Part of the reason is that the player histories hadn't been looked up for all the new players yet.
8. Realized that I just added 5.16 data in which Skarner has over 60% win rate so I need to account for Skarner somehow.
9. Added the game version as a feature which was slightly worse.
10. Refreshed the data set with ~44k matches and added champion indicators back for slight improvement

Phase 4: Progress
=================

In previous experiments, champion indicators were a huge flop. They're just too sparse. When you think about champion indicators per side there are 126 features per side. If we consider that there are 6 bans, [(126 - 6) chose 10] is 116,068,180,000,000 different possible configurations of champions. That's **2.6 billion times more possible champion selects than the number of matches I have crawled**.
So I did what worked before: Compute a statistic per person then take a sum, min, and max. This time I precomputed a table of win rate per (game version, champion). If there was no data I looked up the champion overall win rate.
To compute this I had to move away from data from ranked stats endpoint which doesn't have version info. So I'm computing this over the set of matches I've seen and removing the outcome of the current match when looking it up.
This change got me from 58% accuracy up to 63% accuracy.
I got about 0.5% accuracy gain by dropping the champion columns and the game version columns. This has the nice bonus that training is MUCH faster with so many fewer columns.
When I think about the way random forests work, they compare a number to a threshold for floating point feature. So you can have a tree like:

```
if blue_winrate_sum > 0.55:
   if red_winrate_sum < 0.55:
      ...
   otherwise
      ...
otherwise
   ...
```

But that's a pretty dangerous game - there's no reason for the random forest to pick the same thresholds for each side.
So I decided to add diffs to allow it to directly compare win rates, like (blue\_winrate\_sum - red\_winrate\_sum). So now it can learn something like:

```
if (blue_winrate_sum - red_winrate_sum) > 0:
   ...
otherwise
   ...
```

Encoding some win rates this way got me up to 64%.
Here's the learning curve now:
![Learning curve showing the impact of more data. Regularization disabled. Ran this with 100 trees.]({{ "/assets/img/posts/wp/learning_curve_08_26.png" | relative_url }})
It's still overfitting but we're improving with more data. Removing or simplifying features is more likely to help. Filling in better default values is likely to help. Getting more data will help too.

Conclusions
===========

This post is too damn long.
Random forests are more accurate than logistic regression now, probably because they can represent combinations of features better. But until my most recent experiments, logistic regression was similar accuracy and faster to train.
My progress on this problem can be attributed to mostly feature engineering. Some of that comes from knowing about League of Legends and some of that is the constant struggle against data sparseness and overfitting. Although regularization helps to balance sparse data it's not nearly as effective as designing features that are less sparse.

Notes
=====

(1) This is an area I could likely improve in, by taking the most common non-unranked rank. I'm also considering conflating challenger and master cause players say there's little difference.
(2) Unfortunately I didn't notice this difference until somewhere around phase 4 so I used the ranked stats to look up champion win rates until then.

### Current features with feature importances from random forests

For the curious, here are the current features and the list of feature importances from random forest learning. My feature names are pretty bad so here's a rough legend.

#### Modifiers

Blue\_: Feature is for blue side
Red\_: Feature is for red side
Delta\_: Feature is the blue side value minus red side value
\_Sum: The sum of per-player values for red or blue side.
\_LogSum: The log of the sum of per-player values for red or blue side. This is used for number of games played usually because the difference between 100-105 games is very different than 5-10 games.
\_Min: The min of per-player values for red or blue side.
\_Max: The max of per-player values for red or blue side.

#### Values

MatchHistPatchWinRate: The win rate for (game version, champion), which is computed from match histories.
MatchHistWinRate: The win rate for (champion), which is computed from match histories.
TotalWinRate: The win rate for (player) for all matches in their ranked stats excluding the current match.
GeneralWinRate: The win rate for (champion), which is computed from ranked stats. (I'll try removing these features soon)
Damage\_true: Fraction of the team's damage that's "true" damage. This is computed by aggregating expected damage numbers per match for each champion.
Damage\_physical: Same but for physical damage.
Damage\_magical: Same but for magical damage
GeneralPlayRate: In general how often is each champion played. Percent of total games.
Played: The number of games played on the champion per player.
WinRate: Each player's win rate on their champ.
Combined\_WR\_LP: \_WinRate\_Sum \* \_Played\_LogSum
QueueType\_RANKED\_TEAM\_5x5: Is this team queue?
QueueType\_RANKED\_SOLO\_5x5: Is this solo queue?
Summoners\_Ignite: How many ignite spells were taken by the team? 0-5. Same format for other summoner spells.
Tier: Numeric value for challenger, master, diamond, platinum, gold, silver, bronze, unranked.

```
Delta_MatchHistPatchWinRate_Sum: 0.0783417150388
Blue_MatchHistPatchWinRate_Min: 0.0323549344068
Red_MatchHistPatchWinRate_Max: 0.0313488027432
Red_MatchHistPatchWinRate_Min: 0.0312881349164
Blue_MatchHistPatchWinRate_Max: 0.0306717664898
Delta_MatchHistWinRate_Sum: 0.0287678556769
Delta_TotalWinRate_Sum: 0.0276201874232
Red_MatchHistWinRate_Max: 0.0276070957926
Blue_MatchHistWinRate_Max: 0.0263995490777
Delta_GeneralWinRate_Sum: 0.0232490041282
Red_MatchHistWinRate_Min: 0.0215945236077
Blue_MatchHistWinRate_Min: 0.020329523968
Blue_Damage_true : 0.0189126204086
Red_TotalWinRate_Max: 0.0185370040173
Red_Damage_true : 0.018432428736
Delta_GeneralPlayRate_Sum: 0.0182740974154
Blue_TotalWinRate_Max: 0.0179750673806
Blue_Damage_physical: 0.0178206785779
Red_Damage_physical : 0.0176842953121
Red_Damage_magic : 0.0175138996467
Blue_Damage_magic : 0.0173994840467
Red_GeneralPlayRate_Min: 0.0159850121751
Blue_GeneralPlayRate_Min: 0.0157020093749
Red_Combined_WR_LP : 0.0150776361251
Red_TotalPlayed_Sum : 0.0141792367679
Blue_GeneralWinRate_Min: 0.0139296297018
Red_TotalPlayed_Max : 0.0138542469971
Red_TotalPlayed_LogSum: 0.0136744596289
Red_GeneralWinRate_Min: 0.0136513142511
Red_GeneralWinRate_Max: 0.0136279491338
Blue_WinRate_Sum : 0.0135539271417
Blue_TotalPlayed_Sum: 0.0134913754497
Blue_GeneralWinRate_Max: 0.0134111710295
Blue_TotalPlayed_LogSum: 0.0132455587734
Red_Played_LogSum : 0.0131352239828
Red_Played_Sum : 0.013119619869
Red_WinRate_Sum : 0.0130897656654
Red_Played_Max : 0.0129777766529
Blue_Combined_WR_LP : 0.0129752348834
Blue_TotalPlayed_Max: 0.0128538678549
Blue_Played_Sum : 0.011959672534
Blue_Played_LogSum : 0.0119042299448
Blue_Played_Max : 0.0116590197237
Red_WinRate_Max : 0.0111025449999
Red_GeneralPlayRate_Max: 0.0108553703343
Blue_WinRate_Max : 0.0107640266013
Blue_GeneralPlayRate_Max: 0.0106759217472
Red_Tier : 0.00791245927754
Blue_Tier : 0.00737769089121
Red_WinRate_Min : 0.00624995727823
Blue_WinRate_Min : 0.00624583713921
Blue_TotalWinRate_Min: 0.00541460174423
Red_TotalWinRate_Min: 0.00538417607259
Red_Summoners_Ignite: 0.00393322706347
Blue_Summoners_Ignite: 0.0036346189246
QueueType_RANKED_TEAM_5x5: 0.0025569841657
Red_Summoners_Exhaust: 0.00250370199147
QueueType_RANKED_SOLO_5x5: 0.00241526202611
Blue_Summoners_Exhaust: 0.00233453697897
Red_Summoners_Flash : 0.00172553159503
Blue_Damage_true_qcut5_(0.0331, 0.0424]: 0.00168115359604
Blue_Summoners_Teleport: 0.00168044078121
Red_Damage_physical_qcut5_(0.532, 0.59]: 0.00167882503717
Red_Summoners_Teleport: 0.00165874470876
Red_Damage_true_qcut5_(0.0329, 0.0424]: 0.00164035443627
Blue_Summoners_Flash: 0.00162409480129
Blue_Damage_magic_qcut5_(0.365, 0.425]: 0.00160973133415
Red_Damage_true_qcut5_(0.0424, 0.0585]: 0.00160545365344
Blue_Damage_true_qcut5_(0.0424, 0.0588]: 0.00159505732403
Red_Damage_magic_qcut5_(0.363, 0.423]: 0.00158946539755
Blue_Damage_physical_qcut5_(0.53, 0.589]: 0.00157602298871
Red_Damage_true_qcut5_(0.0256, 0.0329]: 0.00156570595649
Red_Damage_magic_qcut5_(0.298, 0.363]: 0.0015619551631
Blue_Damage_true_qcut5_(0.0259, 0.0331]: 0.00154027231206
Red_Damage_physical_qcut5_(0.59, 0.658]: 0.00149894639082
Red_TotalPlayed_Min : 0.00147979827299
Blue_Damage_magic_qcut5_(0.425, 0.492]: 0.00144937349364
Blue_Damage_physical_qcut5_(0.463, 0.53]: 0.00144713707292
Blue_Damage_magic_qcut5_(0.298, 0.365]: 0.00143075088626
Blue_Damage_true_qcut5_[0.00407, 0.0259]: 0.00142928172729
Red_Damage_magic_qcut5_(0.423, 0.491]: 0.00142108685736
Blue_Damage_physical_qcut5_(0.589, 0.658]: 0.0014153193219
Red_Damage_true_qcut5_[0.004, 0.0256]: 0.00139654834611
Red_Damage_physical_qcut5_(0.464, 0.532]: 0.00139123098978
Red_Damage_true_qcut5_(0.0585, 0.217]: 0.00135422801033
Blue_Damage_true_qcut5_(0.0588, 0.216]: 0.00133514872817
Red_Summoners_Ghost : 0.0012825018216
Red_Damage_magic_qcut5_[0.0439, 0.298]: 0.0012564652682
Blue_Summoners_Ghost: 0.00123342041717
Blue_TotalPlayed_Min: 0.00121063184839
Blue_Damage_physical_qcut5_(0.658, 0.932]: 0.00120105753152
Blue_Damage_magic_qcut5_(0.492, 0.85]: 0.00116191345092
Red_Damage_magic_qcut5_(0.491, 0.867]: 0.00115009507273
Red_Damage_physical_qcut5_(0.658, 0.92]: 0.00114326762739
Red_Damage_physical_qcut5_[0.113, 0.464]: 0.00112895810494
Blue_Damage_magic_qcut5_[0.0376, 0.298]: 0.00112384366323
Blue_Damage_physical_qcut5_[0.111, 0.463]: 0.00111729364361
Blue_Summoners_Barrier: 0.00104733673701
Blue_Summoners_Heal : 0.00103136162457
Red_Summoners_Barrier: 0.00101362007145
Red_Summoners_Heal : 0.000882613108646
Red_Played_Min : 0.000747445158982
Blue_Played_Min : 0.000717326533907
Red_Summoners_Cleanse: 0.000608349212887
Blue_Summoners_Cleanse: 0.000588182703567
Blue_Summoners_Smite: 0.000216492493282
Red_Summoners_Smite : 0.000174875332852
Blue_Summoners_Clairvoyance: 1.59854560378e-05
Blue_Summoners_Clarity: 1.07734826485e-05
Red_Summoners_Clarity: 7.13387206181e-06
Red_Summoners_Clairvoyance: 5.87287195701e-06
```
