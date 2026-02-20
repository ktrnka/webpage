---
layout: post
title: "Summary: Predicting win/loss for League of Legends"
date: 2016-05-19
---

<!-- KT TODO: This post was never finished. Contains placeholder text (`<description of champion selection>`, `<link to monte or saint>`, `<insert diagram>`, incomplete sentence). Review and complete or significantly trim before publishing. -->

Periodically I find that I need a quick project summary but I only have a long series of work-in-progress posts.

I'll cover the basics of the problem setup, what worked, and loosely why it worked. I'll focus on the common questions people ask me: what features were important, why is this problem important, do you have any tips for machine learning, etc. I won't cover the missteps along the way or the roundabout steps it took to learn; that's what the old posts are for.

Motivation
==========

I'm a big fan of professional League of Legends - every weekend I get to watch the best players in the world compete in a video game I play myself. It's not much different than watching ultimate frisbee or another team sport; matches involve player positions, complex strategy, professional commentary, coaches, million-dollar tournaments, star players, highlight reels, fantasy sports, corporate sponsors, commercials, and so on.

One of the main differences from a traditional team sports is that the 5 players on each side must pick which champions they will play from amongst 130 or so. In League each champion works very differently and the number of possible combinations in a 5v5 match is over 100 trillion. **<description of champion selection>**

Sometimes a professional comments that a team made a poor draft or even that they lost the game in draft phase. **<link to monte or saint>** I'd say it's more that the draft affects the probability of winning - say if a team makes a very poor draft maybe they only have 35% chance of winning. And if they're the worse team too then maybe it's more like 20% chance of winning.

Can I make a neural network that looks at the team/picks and tells me the probability of winning? If I could make it, then I could also write programs to help optimize the draft phase for pros or even help with my own amateur games!

Intro to League and e-sports
----------------------------

If you aren't familiar with these areas, these may help:

* [What is League of Legends? By Riot Games](https://www.youtube.com/watch?v=BGtROJeMPeE) (2015, 5 minutes) - Covers the game basics, targeted for new players. Doesn't discuss professional play.
* [Beginners guide to League of Legends e-sports](https://www.youtube.com/watch?v=IYMcKzMl7CY) (2014, 6 minutes) - Covers e-sports in general with a focus on League, targeted for people without a League background that are watching pro games for the first time.
* If you prefer to read, ESPN has [an excellent article](http://espn.go.com/espn/story/_/id/13059210/esports-massive-industry-growing) about the scale of e-sports in contrast to traditional sports.
* ESPN also ran [a fantastic article](http://espn.go.com/espn/feature/story/_/id/13035450/league-legends-prodigy-faker-carries-country-shoulders) about superstar player Faker, comparing him to Michael Jordan and Tiger Woods. It's written for a general audience.

 

 

Questions to answer:

Challenges in working on pro matches: Not much data due to patch changes. Team rosters change often enough. Data not available via API. Give examples from Oracle's Elixir.

Why is this hard?
-----------------

I'd like to focus on pro matches but there isn't that much data - maybe 50-70 games per week but the game is modified every two weeks. Furthermore, there isn't an API to easily get the information about all pro matches in all regions.

So instead I'm focusing on something more achievable: crawling the Riot API for ranked online matches to build a fairly large data set that I can learn from. If I'm successful in this task I can transfer pieces of the learned models to help predict pro matches.

Most players analyze a match in terms of which champions were picked on each side. This is actually quite challenging for machine learning - there are about 163 trillion possible matchups with 130 champions and Riot adds a few more every year. For reference my largest dataset is 2 million matches so we have an extreme data sparseness issue.

What's more is that the exact matchup will play out differently depending on the players. Even if the picks are identical, what if you're playing that champion for the first time? What if you've played that champion 100 times? Your performance also has an element of general skill too, such as reaction time, knowledge of the opposing champions, knowledge of strategy, and so on.

Problem setup
=============

What can we do and

Engineering
===========

This is the pipeline I have now:

<insert diagram>

Match and player stubs are crawled from the Riot API. That's done as a Python script on Heroku and populates a MongoDB running on mLab (about 1-2gb). When I have enough data, I run a script on my local machine to fetch the full details for matches and players into a MongoDB running on my laptop (about 50gb).

From there I generate a feature matrix (about 200mb). This is a rough feature matrix with almost all of "building blocks" features. The script for actually training and testing models does the work of converting distributions into min/max/average, standardizing features, taking diffs, converting to indicator variables for quartiles in some cases, dropping bad features, and so on.

Commentary: The script that generates a feature matrix from MongoDB takes a while; it needs to process about 50gb. Its output is more like 200mb. This design allows iteration on fine-tuned improvements of the features without having to reprocess the full data set.

Machine learning
================

Process and tools
-----------------

Loosely I cycle through a few different types of tasks. This is basically what you'll see in Kaggle winner interviews:

* feature engineering
* different types of models (random forest, SVM, etc)
* hyperparameter tuning
* reducing training time
* data analysis - when is it predicting well or poorly?

I tracked most of my experimental runs in a Google Sheet and that way I could plot accuracy over time very easily and take very brief notes about hyperparameter tuning and/or feature engineering.

For the overall project I used Trello to help prioritize experiments and that worked reasonably well.

Feature engineering
-------------------

### Feature customization for tree-based modeling

Random forests and gradient boosting are based on decision trees. For continuous valued inputs they propose many possible thresholds on the feature and test candidate splits that way. However, this easily leads to overfitting. In theory you can retune your regularization to compensate, say with a max\_depth for trees, min\_samples\_leaf, min\_samples\_split, etc. But then your process requires more frequent retuning if you're adding/removing features. Instead I felt it was easier for some features to simply use pandas.qcut to discretize a real-valued input in a few levels (like what percent of the team is magic damage). In practice this was very cheap to compute and provided the regularization I wanted. The downside is that this kind of feature engineering is less applicable to weighted approaches like logistic regression and neural networks.

The second kind of feature engineering for tree methods was to compute diffs. For example, I had a feature for the total number of games played by red side and the same feature for blue side. A tree can't compare two variables directly; it would need to learn two levels of the tree and you'd need to get very lucky for it to work right. Instead it's easier to just add some diff features.

Logistic regression
-------------------

Logistic regression with L2 regularization forms a strong baseline for classification. Notes:

* Be sure to scale your features; this has a strong benefit to training time and sometimes affects accuracy
* Tune your regularization parameter. In scikit-learn, LogisticRegressionCV will do this for you very efficiently. Usually it's not too sensitive to the number of C-values tested; 10 was fine for me.
* L-BFGS was radically faster than the other solvers in scikit-learn with the same accuracy, enough so that I'd suggest to anyone to try a few solvers and compare speed vs accuracy

Another benefit is that logistic regression is very consistent. The other methods I used were all much more sensitive to randomness. Because it's so fast I recommend running it in addition to your main model at all times if only to simplify feature debugging.

Gradient boosting
-----------------

Gradient boosting aka gradient-boosted decision trees are something like random forests, but use the idea of boosting to start with a very basic simple tree and iteratively correct and refine the model. In contrast, random forests make no attempt to fit the data more tightly than the individual models; it's just that the average of the individual models is more accurate and robust.

Early on I tried gradient boosting but it was slow and not accurate. Later when I tried it for a second time I learned that the default parameters were very suboptimal for my data. For a while they had similar accuracy to my neural networks and were a little simpler (but training was slower). Tips:

* Tune learning rate and optionally the number of trees. The optimal learning rate for my data at 300 trees is around 0.22. Generally I'd get better models with more trees but training time increases linearly and the accuracy improvements diminish.
* Set some value for min\_samples\_leaf or min\_samples\_split so that the trees can stop learning earlier. This also has some regularization benefits.
* max\_depth didn't matter much when setting min\_samples\_x
* Subsampling at 0.9 helped accuracy slightly and sped up training slightly
* I found it was a little helpful to set logistic regression as the initial model for gradient boosting but it wasn't well documented so not worthwhile overall

I used gradient boosting because it was easy in scikit-learn but after I got used to neural networks I found that the neural networks would run in maybe 5 minutes vs gradient boosting 30 minutes and the NN would have similar or better accuracy. On the other hand, gradient boosting plays nicely with multiple threads/jobs in a grid search but neural networks don't. And even despite all this, the gradient boosting model was still useful when ensembled with the neural net.

Neural networks
---------------

I'd previously used neural nets only for classwork. In practice you have a few options in Python. You can code it manually using numpy, Theano, or TensorFlow but that takes time and you have to test/debug everything. I used Keras which is just a wrapper for those backends and provides a sklearn-like interface for neural nets. If I had to do it all over again maybe I'd try skflow because I ended up writing scikit-learn wrappers around Keras models so that I could use scikit-learn grid search.

All that said, I learned a ton of practical lessons that you don't get in classes as much:

* ReLU was much better than sigmoid or tanh activations, even for networks with a single hidden layer
* dropout is very useful
* maxout is supposed to help in conjunction with dropout but I didn't have any experiment in which maxout showed improvement
* he\_initialization is important with ReLU. For a short network like mine choosing he vs glorot had an interaction with the optimal dropout parameter; max accuracy was the same with both but he gave better results with the default 0.5 dropout.
* Deeper networks gave improvements but I had to retune the networks to get the benefit. Wider networks gave even better improvements than deep models for this task.
* Even a small about of L2 was harmful which surprised me
* Gaussian noise on the inputs was harmful on this problem
* Early stopping was harder to use than I expected. With the default Keras settings it would stop far too early. I had to set the patience value pretty high and even then it tended to hurt

Overall my neural networks were clearly the best individual models but took more hyperparameter tuning than the other models. But some of these were general lessons such as ReLU so I think on the next problem I tackle, I'll jump to NNs sooner.

Ensemble methods
----------------

I tried ensembles but generally regretted it. In a Kaggle competition it's natural because you're forced to generate CSV files of your predictions and you have all the old ones around to ensemble, so doing ensembles of 10-100 models is very cheap.

But in a sklearn setting when you're retraining the whole ensemble it really slows down training. In the end my feeling is that it's useful for last-mile improvements but should be avoided until then.

Tips:

* You can ensemble even two classifiers if they have probability scores. This was successful between gradient boosting and neural networks
* Probability calibration helps a little but it's a pain in the ass cause it adds another layer of cross-validation. If you're doing calibration anyway it's the same computational cost as stacking, which is better anyway.
* My favorite was logistic regression with a little regularization on the output probabilities. My second favorite was linear regression on the output probs. I prefer logistic because those models tended to have lower standard deviation in cross-val tests. Either way you need to use cross-validation to get held-out predictions from the base models to train on so it's slow.
* Guess-and-check on a linear combination of output probs is prone to fitting on the dev/test data and honestly it's not a good process. In the end it was easier and less stressful to do nested cross-validation in stacking.
* On the small data set I noticed that ensembling was much more helpful and it's probably because the models were tuned to fit the larger data so they overfit the small data. So then I tried to encourage the models to diversify by overfitting on the large data to get a better ensemble but it wasn't helpful.

In the end, ensembles on the 200k data set gave fairly small accuracy improvements. On the other hand, they reduced the standard deviation of the cross-validation which means that they're behaving more predictably. That may be very important in an industry setting. But they're also slow so pick your poison.

High-level conclusions and tips
===============================

The future
----------

I'll probably come back to this project again now that I've had time to learn other things. Things I'll need to look into:

* Full data update
* Mastery points by champion is available now which is better than the number of games played in the current season in ranked queue only
* Use GPU for the NN (now I'm used to that)
* Switch to a better system for logging experiments, like saving into mongodb or something
