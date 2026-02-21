---
layout: post
title: "scikit-learn 0.17 is out!"
date: 2015-11-16
---

Scikit-learn 0.17 adds features and improvements that might help me:

* stochastic average gradient solver for logistic regression is [faster on big data sets](https://github.com/scikit-learn/scikit-learn/pull/4738)
* speed and memory enhancements in several classes
* [ensemble classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html) that supports hard and soft voting as well as hyperparameter tuning of the components in grid search
* [robust feature scaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html) does standard scaling but excludes outliers from the standard range

The full changelog is [here](https://scikit-learn.org/stable/whats_new.html#version-0-17). I've been testing the changes to see how they'll impact my work in predicting match winners in League of Legends.

Stochastic average gradient
===========================

Like lbfgs and newton-cg, sag supports warm\_start so it works well in conjunction with LogisiticRegressionCV to tune the regularization parameter.

First I tried on the 200k match dataset with 61 features. I repeated the tests for better accuracy.

| Solver | Training time | Accuracy |
| --- | --- | --- |
| lbfgs | 0.5 min | 66.59% |
| lbfgs | 0.5 min | 66.59% |
| sag | 1.7 min | 66.60% |
| sag | 1.8 min | 66.60% |
| newton-cg | 2.4 min | 66.60% |
| newton-cg | 2.6 min | 66.60% |

sag is faster than newton-cg but still about 3x slower than lbfgs. It does eke out that last 0.01% accuracy though.

sag is designed for large data sets so I also tried on the 1.8 mil x 61 dataset:

| Solver | Training time | Accuracy |
| --- | --- | --- |
| lbfgs | 7.2 min | 66.07% |
| sag | 45.8 min | 66.07% |

It's over 6x slower and achieves the same accuracy. Maybe sag's benefit really shines on datasets with a large number of features: sklearn team testing used 500 features and 47k features.

**Conclusion: Staying with lbfgs.**

Other performance
=================

The patch notes briefly mentioned speed and memory improvements in random forests and gradient boosting.

RandomForestClassifier
----------------------

Tried this on the 200k x 61 dataset:

| Version | Training time | Accuracy |
| --- | --- | --- |
| Random Forest 0.16.1 | 14.1 min | 66.34% |
| Random Forest 0.17 | 13.7 min | 66.39% |

The training time and accuracy fluctuations could just be differences due to randomization; random forests tend to fluctuate more than other methods from test to test. In the worst case, it doesn't seem that much has changed. In the best case there are slight improvements.

**Conclusion: Random forest is about the same, but I didn't test memory usage.**

GradientBoostingClassifier
--------------------------

Gradient boosting trains much more slowly than other methods so I started on the 50k x 61 dataset. I ran some tests multiple times to be certain of the results.

| Version | Training time | Accuracy |
| --- | --- | --- |
| Gradient Boosting 0.16.1 | 7.6 min | 66.08% |
| Gradient Boosting 0.16.1 with feature scaling | 8.8 min | 66.10% |
| Gradient Boosting 0.17 | 11.0 min | 66.17% |
| Gradient Boosting 0.17 | 11.6 min | 66.34% |
| Gradient Boosting 0.17 with feature scaling | 11.7 min | 66.14% |
| Gradient Boosting 0.17 with feature scaling | 11.7 min | 66.17% |
| Gradient Boosting 0.17 presort=False | 14.0 min | 65.94% |
| Gradient Boosting 0.17 max\_features=auto | 11.2 min | 66.19% |

Gradient boosting is clearly slower in 0.17 and generally a tad more accurate. The default presort setting is good for runtime and accuracy. Feature scaling doesn't really help. Adjusting the max\_features setting seems to help a touch (should reduce variance and improve training time).

I also tested on the 200k x 61 data:

| Version | Training time | Accuracy |
| --- | --- | --- |
| Gradient Boosting 0.16.1 | 43.9 min | 67.66% |
| Gradient Boosting 0.17 | 62.3 min | 67.75% |

Again it's slower but more accurate. I've [opened a ticket](https://github.com/scikit-learn/scikit-learn/issues/5808) and right now it's under investigation. It sounds like a change in the error computation may be the culprit.

**Conclusion: Gradient boosting 45% slower but a little more accurate, fix is being investigated.**

VotingClassifier
================

In [the previous post](/blog/2015/11/better-predictions-for-league-matches/) I described possible directions to get from 67.9% accuracy up to 70.0% and suggested that an ensemble of the best classifiers may be a fruitful direction but may take a bit of time to code.

Well, two things changed. First off, I found [a great guide](https://sebastianraschka.com/Articles/2014_ensemble_classifier.html) on making an ensemble in scikit-learn. I implemented a simple ensemble and improved my best results from 67.9% accuracy to 68.0% accuracy by a soft-voting ensemble of gradient boosting and neural networks. It's not as much as I expected but it's progress.

The second change is that scikit-learn 0.17 added [VotingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html), implemented by Sebastian Raschka (who wrote the guide and implementation I found earlier). I ported my ensemble code to scikit-learn and it works great (though I had to change my neural network wrapper to return two columns rather than one for binary classification).

That said, I wish it had a flag to perform [calibration](https://scikit-learn.org/stable/modules/calibration.html) of the probabilities of the individual classifiers. I'm currently looking into calibrating but not finding that it helps; gradient boosting has more skewed probabilities than neural networks which leads to more weight on gradient boosting. That's an unintentionally good decision: putting more weight on the stronger classifier.

**Conclusion: VotingClassifier is easy and works like a charm.**

RobustScaler
============

In general using the robust scaler seems like an easy solution to save time in preprocessing your data.

I tried it with logistic regression because it's so sensitive to feature scaling. But after several tests **I didn't find any difference in either scaling+training time or accuracy.**

Thoughts
========

I bolded the main point of each section so I won't summarize. But I like the direction the scikit-learn is taking.
