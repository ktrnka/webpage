---
layout: post
title: Better predictions for League matches
date: 2015-11-04
---

I'm predicting the winner of League of Legends ranked games with machine learning. The models look at player histories, champions picked, player ranks, blue vs red side, solo vs team queue, etc. The last time I wrote about accuracy improvements my best was [61.2% accuracy with gradient boosting trees](/blog/2015/09/predicting-league-match-outcomes-week-2/).

Since then I've increased the amount of data from about 45,000 matches to 1.8 million matches. I've done analysis and the trends are [much more reliable](/blog/2015/09/bigger-league-of-legends-data-set/).

Experiments with 1.8 million matches are slow so I usually use 200k and sometimes 50k to test code. Almost always the trends in 200k are the same as 1.8 million but they run in minutes or hours compared to hours or days.

I keep a spreadsheet with the outcome of each experiment and notes that indicate the model used, features used, and any other tweaks. This graph shows the progress since the last post.

![Accuracy improvements Sep Oct 2015]({{ "/assets/img/posts/wp/image-18.png" | relative_url }})

The graph fluctuates so much because I sometimes test ideas on 50,000 matches. The models are worse but it allows rapid testing.

I also test multiple model types. It smooths out towards the end because I wasn't experimenting as much with weaker models. On this particular problem, gradient boosting trees and neural networks are clearly stronger than logistic regression and random forests.

Feature engineering
===================

Most of my progress came from feature engineering: getting from the starting point of 61.2% accuracy to 67.2%. I also ran the most experiments in this area: around 80 of 120 experiments.

The initial drop in accuracy was the result of adding additional matches but not fully updating the database of player histories. The players' ranked history stats were available for a smaller percentage of the data. Accuracy dropped to 58% even despite having 1.8 million matches.

After running a full crawl of all player ranked stats the problem was solved and gradient boosting trees were up to 62.3%. That's 1% higher than the previous best just from having more data.

Previously I dropped features with low weights in the models because they're making the data more sparse. When you have a small dataset, you can get small but good improvements by dropping these features. There wasn't anything particularly special about these features; they're just mins and maxes of individual player features by team. Adding these features back increased from 41 to 53 features and had accuracy gains: gradient boosting improved from 62.3% to 62.4%. Logistic regression improved from 60.7% accuracy to 63.3% which is the new best.

The next big change was looking up each player's current rank (e.g., Silver 1, 50 LP). In previous experiments I only used their ending rank from the previous season because it's easy to access. I had to write a new crawler and let it run over a weekend to fetch every player's current league, division, and points. I converted that to a single numeric value and added features for the average rank of each side and a diff to make them easier to compare (1).

This was very successful, achieving 65.8% accuracy with logistic regression and 67.1% with gradient boosting trees.

I also extracted the role each person played within the team. A standard team comp has the following five roles: solo top lane, solo mid lane, solo jungle, bottom/marksman, and bottom/support. With these assignments we can compare the player on each side of the matchup: do we expect blue side or red side to win in the mid lane? What about jungle? And so on.

Unfortunately the data is extremely messy for the lane/role assignments. I put a lot of effort into making sensible default values but it still needs more work (5).

After all that work though, logistic regression and gradient boosting trees only improved by 0.1%.

I also revisited indicator features for the champions played on each side and the summoner spells selected. This increases the number of features from 61 to 331 and usually makes the models overfit. I only ran a small number of tests with logistic regression but found on the 200k dataset that it improved accuracy from 66.3% to 66.5%.

Neural networks
===============

Feature engineering is good but once you run out of ideas it's good to try different model types and hyperparameter tuning. I'd been meaning to use neural networks but they aren't supported in scikit-learn (2).

After surveying Python neural network libraries I found that almost all of them use [Theano](https://en.wikipedia.org/wiki/Theano_(software)) on the backend sort of like how scikit-learn uses numpy. I really didn't want to write the NN code manually in Theano. [Lasagne](https://lasagne.readthedocs.org/en/latest/index.html) provides shorthand functions to create network layers but doesn't help with the optimization. [Keras](https://keras.io/) is much closer to scikit-learn in that it provides an easier interface and you pick from multiple optimization methods. And I don't need to understand Theano at all to use it. So I went with **Keras**.

At first I tried replicating logistic regression as a sanity test. A neural network with sigmoid activation and no hidden units is actually just logistic regression. Unfortunately I couldn't get similar accuracy to scikit-learn logistic regression no matter what I tried. I got 62.2% in Keras vs 66-67% in scikit-learn logistic regression. When I tried using the ReLU activation function instead of sigmoid I could get 65%. I also tried tanh but that got 64.3%. I never figured out why I couldn't reproduce it and moved on. (3)

Neural networks are sensitive to hyperparameters just like most other algorithms. But you could say they have many more hyperparameters: the number of layers, layer widths, regularization, dropout, maxout, maxnorm, optimizer algorithm, optimizer settings, activation functions, and so on. The easiest way to test would be scikit-learn's GridSearchCV or RandomizedSearchCV. Unfortunately Keras models aren't compatible so you need to write a scitkit-learn class that wraps the Keras model ([code here](https://gist.github.com/ktrnka/81c8a7b79cb05c577aab)). I made many mistakes in doing it before finding this [note](https://scikit-learn.org/stable/developers/#rolling-your-own-estimator). It's pretty janky; it uses introspection to decide which members of your class are hyper parameters for get\_params and set\_params (hint: anything ending in underscore is excluded). Keras has a scikit-learn wrapper also but it doesn't look like you can run a grid search over layer sizes with it.

Ranting aside, I can run grid searches over different network configurations, dropout settings, activation functions, etc.

I was able to get to 67.4% accuracy (new best) after two days with Keras using a neural network with one hidden layer of 75-100 units, 0.5 dropout, and ReLU activation function. Since then I've tried tons of experiments which I'll summarize:

* Adding a second small hidden layer is harmful. I was comparing 61 input -> 75 hidden -> 1 output vs 61 -> 75 -> 5 -> 1. From watching the run it's fitting the training data much better but generalizing much worse. I couldn't find any dropout settings that would compensate for the overfitting enough.
* Maxnorm: [Literature](https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf) shows that it's helpful in conjunction with dropout but I didn't get any gains at all.
* Maxout: [Literature](https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf) shows bigger gains than maxnorm in conjunction with dropout but I could only just barely get it to have the same score by ensuring that it wasn't increasing the number of parameters in the model (i.e., for maxout 2, use half as many hidden units)
* 0.5 dropout seems best. When I increased features from 61 to 331 the best dropout was like 0.8 (which is more or less allowing it to ignore all the extra features). I only put the dropout layer after the hidden layer. I may have tried a dropout layer after inputs but found it didn't help.
* I found best results by doing mini batch with about 1000 matches per batch followed by full-batch training.
* Used Adam optimizer cause I saw a talk that said it's best/easiest.
* I tried adding a GaussianNoise layer on the input with 0.1 noise but it was slightly harmful.
* I ran many experiments on early stopping not shown in the graph but was unable to find any settings that gave the same accuracy. However, I did learn that [Keras early stopping](https://keras.io/callbacks/#available-callbacks) can only use val\_loss or val\_acc; it can't stop on training loss. Also, the code works incorrectly if stopping on accuracy; it stops if the *minimum* doesn't decrease for the specified number of epochs but with accuracy we want the max to increase.
  + To get reasonable results I had to set the patience value pretty high (20 epochs).
  + The best I could do with early stopping was 67.3% accuracy in 3.6 minutes vs 67.45% accuracy in 7.0 minutes without it. So about a factor of 2 faster but not as accurate. Probably good for quick tests though.
  + For accuracy stopping I tried modifying the Keras class to handle accuracy correctly but it didn't seem to work well (maybe stopping on accuracy is fundamentally bad).

After all that tuning I couldn't beat 67.4% on the 200k dataset and couldn't beat 67.0% on 1.8m.

Gradient boosting with init
===========================

Gradient boosting decision trees start from a base classifier and correct the errors in the model with each new tree. It starts from predicting the majority class by default but you can supply a full estimator to use as default.

I tried a test with using logistic regression as the base and found that it helped slightly (67.1% -> 67.3%). It was a huge pain though due to lack of documentation but [Stack Overflow saved me](https://stackoverflow.com/questions/17454139/gradientboostingclassifier-with-a-baseestimator-in-scikit-learn).

The only issue is that it doesn't seem to work with multiple threads so mostly I don't use it. But it seems less sensitive to hyperparameter tuning.

Model types: odds and ends
==========================

I tried support vector machines briefly and learned why nobody uses them anymore: O(n^2) runtime so they just don't scale. I'm sure there are ways around it. You could run the kernel on log n carefully selected points but scikit-learn doesn't have that.

I also tried elastic net, which is logistic regression with both L1 and L2 norms. I vaguely remember benefits with this for maxent language models. But it didn't improve over L2 logistic regression and the implementation in scikit-learn was harder to use in cross-validation.

Revisiting hyperparameter tuning
================================

I hadn't tuned the parameters of gradient boosting trees like I had for neural networks because they're slow. But I've been going back through gradient boosting and random forests to reassess the hyperparams. My goal is to improve runtime and hopefully improve accuracy a little.

### Gradient boosting trees

My previous hyperparameters for gradient boosting trees were very suboptimal. After tuning I improved from 67.1% to 67.9% (best results yet). The important settings were the learning rate and number of trees. I'd set the learning rate to 0.9 (very poor choice) and tree to 100 to match the random forests. The best settings were around 0.2-0.25 learning rate and 300 trees. Possibly I had set the 0.9 learning rate from hyperparameter tuning when my data set was leaking the test info and I got 90-100% accuracy. The default learning rate of 0.1 was poor.

I also found tiny gains from subsample 0.9, which helps reduce overfitting. I tried subsample at 0.5 and 0.75 but that was awful. Subsample 0.9 should speed up training slightly so I'm using that now. I also found small gains by tuning min\_samples\_leaf down to 10 from 20. (4)

### Random forests

I also tried tuning with random forests and found that I was using too few trees so upped that from 100 to 150. I was hoping to find the "elbow" in the graph of accuracy vs number of trees but it's smoother than I'd like:

![Accuracy vs number of trees in random forest]({{ "/assets/img/posts/wp/image-19.png" | relative_url }})

I have no idea why there's a blip at 100.

I also tried re-tuning min\_samples\_leaf and min\_samples\_split; higher values reduce overfitting and speed up training. I didn't see much gain. I'm using min\_samples\_leaf 7 and min\_samples\_split 50.

Conclusions
===========

I re-trained and tested the best settings on 200k matches with 5-fold cross-validation with 3 threads:

|  | Accuracy (200k) | Training time |
| --- | --- | --- |
| Gradient boosting trees | 67.7% | 43.9 min |
| Neural networks | 67.4% | 7.3 min |
| Logistic regression | 66.6% | 0.6 min |
| Random forests | 66.3% | 14.1 min |

I'm not sure why gradient boosting lost 0.2% from previous runs but the hybrid with logistic regression gets 67.9% (not listed above) so I'm not too worried.

I might have to try a scikit-learn wrapper for [xgboost](https://github.com/dmlc/xgboost). I've seen Kagglers have better success with xgboost than with scikit-learn and it's supposedly faster.

Below are the best results to date in one table. The runs on 1.8 million matches aren't necessarily with the same hyperparams as the corresponding 200k tests because it takes so long to rerun.

|  | 200k matches | 1.8m matches |
| --- | --- | --- |
| Gradient boosting trees | 67.9% | 67.7% |
| Neural networks | 67.4% | 67.0% |
| Logistic regression | 66.6% | 66.1% |
| Random forests | 66.3% | 66.2% |

So what's next? Unfortunately the ranked season ends next week and there are massive overhauls for season 6. Especially with ranked team builder queue, I expect that more players will get their best role so matches will be less predictable. I'd really like to hit 70% accuracy but I'm running out of time before everything changes.

Things that might help:

* Crawl normal (unranked) game stats. Sometimes a player doesn't have ranked stats for a champion but has stats from normals that could at least show whether they're new to the champion or not. This would take a couple days to code and a few full days of crawling. I'd guess 0.1-0.5% gain from this.
* Ensemble of classifiers. Unfortunately I didn't see a wrapper for this in scikit-learn so I haven't tried it yet. Gradient boosting trees and neural networks are learning in a very different manner so they should combine well. I'd guess 0.3-1.0% gain from this though it would be more complex than majority voting.
* Improve team queue prediction. I'm using the solo queue ranking of the players and adding them up but I should look up the team ranking. I could also start tracking the win rates of pairs of teams, which may capture strength or weakness of team strategy. I'd guess 0.1-0.3% gain from this.
* Make my own ELO score. I could easily make an ELO score that's updated as I generate the dataset. This wouldn't have any data leakage problems like current rank but if I have lots of players that only show up in a few games then it won't be stable. I'd guess 0-0.2% gain.

Extra: Predictability tests
===========================

It's good to understand when your models are doing well and poorly. I looked at this [before](/blog/2015/09/predicting-league-matches-are-some-matches-more-predictable/) but there weren't too many interesting trends. I've changed my tests in three ways:  logistic regression instead of random forests (for speed), full 1.8 million matches instead of 44k, and using the players' current league/rank to tell the level of the match instead of their rank in previous season.

![Predictability by league]({{ "/assets/img/posts/wp/image-20.png" | relative_url }})

The black line is is overall average and the thin blue lines show plus or minus one standard deviation around the main blue line. Generally lower leagues are much more predictable. There isn't a statistically significant difference between silver and gold or master and challenger, but the difference between bronze and silver is significant, gold vs platinum, platinum vs diamond, and diamond vs master.

It's probably because there are more errors in pick/ban phase at lower ranks that players haven't learned yet. And also high level players are more capable of playing all roles reasonably whereas lower rank players might play only one role well.

![Predictability by version]({{ "/assets/img/posts/wp/image-21.png" | relative_url }})

This shows the prediction accuracy of the model by game version. I removed all game versions with a low number of matches. The standard deviation for most versions is around 0.2%.

The trend worries me. It's completely unlike what I saw on older data (basically flat). It likely means that the features for current league are partially revealing the outcome of previous matches. Unfortunately the Riot API doesn't provide a player's historical ranking so it's not possible to look up their ranking at the time they played a past game. I could drop the feature but it's useful. Or I could recrawl each player's league every day but I don't have enough cloud storage to store that.

Notes
=====

(1) Logistic regression has no trouble comparing two features but it's more effective in tree-based methods to add a diff feature.

(2) This recently changed.

(3) I should have tried an absurdly high number of iterations. Structurally the models are the same and I set the regularization and feature scaling the same but the optimizers are different. If I did it all over again I'd test scikit-learn's SGD implementation to compare directly to Keras SGD in addition to a very high number of iterations.

(4) Generally I like this setting because it reduces overfitting and also speeds up runtime. min\_samples\_split and min\_samples\_leaf interact a bit though.

(5) First off, the lane/role fields are sometimes empty or may have a lane (bottom) without the role (carry vs support). If the fields are empty I pick the most common lane/role in the data. If lane is present but the role is missing I fill that in with the most common role for that lane and champion. Even still sometimes the data is wrong and lists the support as a second mid lane. This could be better solved by using a classifier to clean up the data but that's a bigger project. So sometimes I get matches where one side has bot/support and the other side doesn't. In this case I look up the win rate of that champion as bot/support. If both supports are correctly tagged then I'll look up the win rate of that matchup (e.g., Morgana bot support vs Blitzcrank bot support).
