---
layout: post
title: Feature scaling is important, but not how I expected
date: 2015-10-21
---

Currently I'm getting up to speed with the [Keras](https://keras.io/) library for neural networks. After about a day and a half of effort I have a neural network that's tied with my best results ever for predicting the winner of League of Legends matches.

Keras doesn't provide exactly the same methods as a [scikit-learn](https://scikit-learn.org/stable/) model so I have to write some code to fit it into the cross validation and hyperparameter tuning frameworks. Then I'll have an apples-to-apples comparison.

I learned that feature scaling is critically important for Keras models. Some models won't even improve beyond random predictions without it! I knew that feature scaling was good for speeding up convergence but didn't think modern optimizers would suffer total failure without it.

If you aren't familiar with [feature scaling](https://en.wikipedia.org/wiki/Feature_scaling), it's just making sure that all your features have a similar range of values. The scaling I'm using subtracts the average value and divides by standard deviation so most values will fall in the -1 to 1 range after scaling (called standardization or a z-score). It's also possible to scale each feature so that the minimum is 0 and maximum is 1.

Feature scaling is important for machine learning models that use some form of gradient descent, like logistic regression and neural networks. In previous experiments I'd tried logistic regression with and without scaling and it had only minor impact though. However, I only ran those tests *after* finding a reasonable range of regularization constants to tune. Unfortunately I learned that hard way that the optimal regularization constant is radically different for scaled vs. unscaled data (1).

What I learned today
====================

* Optimal regularization constant (C) is dependent on feature scaling.
* Feature scaling speeds up optimization by about 6x (including the time to scale).
* scikit-learn has three optimizers: liblinear, lbfgs, and newton-cg
  + With feature scaling the three optimizers give almost identical results for each C value. lbfgs is consistently worse than newton-cg and lib linear but only by about 0.01%.
  + Without feature scaling, liblinear is consistently better than newton-cg or lbfgs. The best result from liblinear is about 0.02% better than the best from newton-cg and about 1.66% better than the best result of lbfgs. For my problem, 1.66% is about the gain I can get with a couple weeks of feature engineering.
  + lbfgs is drastically faster than newton-cg or liblinear
* [LogisticRegressionCV](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html) is about 2x faster than [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html) for lbfgs. The ratio is more dramatic if you're tuning over more than 10 C values because it initializes the weights for all instances closer to the optimum aka warm start.

### Tests within LogisticRegressionCV at 50k samples

* lbfgs: 0.2 min
* newton-cg: 1.0 min
* liblinear: 1.4 min

### Tests with GridSearchCV at 50k samples

It's tuning the same C values just doing it a different way.

* lbfgs: 0.6 min
* newton-cg: 1.7 min
* liblinear: 1.4 min

Note that GridSearchCV and LogisticRegressionCV are the same speed with liblinear because liblinear doesn't support a "warm start" in the optimization.

### Tests at 200k samples

* lbfgs LogisticRegressionCV: **1.2 minutes** [what I'm switching to]
* newton-cg LogisticRegressionCV: 4.8 minutes
* lbfgs GridSearchCV: 2.9 minutes
* liblinear GridSearchCV: 7.5 minutes
* liblinear GridSearchCV without feature scaling: **33.0 minutes** [what I've been using for weeks :( ]

**After these optimizations it's 27.5x faster.**

I didn't even try tests with 1.8 million samples. From memory that took about 3 hours for liblinear GridSearchCV without feature scaling and tuning 5 C values instead of 10. If the same speedup holds it should train in about 6.5 minutes.

I also checked the accuracy at the optimal C value for both. The fastest run found an optimum of 66.37% accuracy. The slowest (no feature scaling) found an optimum of 66.26% accuracy. So it's not that lbfgs is cutting corners here; we're actually gaining accuracy due to better optimization of C value with feature scaling.

Why does this matter?
=====================

When I'm trying out a new feature I don't know if it's useful or not. So I test it at 50k samples. But sometimes the feature isn't reliable in a small data set. I may find that it fluctuates the accuracy by 0.01 at 50k samples but gives a 0.2 gain at 2 million. Big improvements are clear even at 50k though; this is mostly helping me to quickly make decisions about small changes.

It really matters because speed of iteration is life. What I mean is being able to test ideas quickly.

Notes
=====

1. The optimal C value will differ when the useful features have radically different scales. It happens because the scale of the optimal weights is affected by the scale of the inputs and therefore affects the regularization value whether it's L2 or L1.
2. These tests tried 10 C values each. In my previous experiments I dropped it down to 4-5 values to try and speed up my experiments.
3. For all tests I used n\_jobs=3 on a quad-core cpu. They all use the exact same 10-fold cross-validation splits and the splitter is initialized with random seed 4.
4. Comparing LogisticRegressionCV and GridSearchCV is reasonable if you're only tuning the regularization constant C. If you're tuning other parameters like the max number of iterations or trying L1 vs L2 then you have to use GridSearchCV.
