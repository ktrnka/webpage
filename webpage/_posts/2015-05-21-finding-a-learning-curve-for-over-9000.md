---
layout: post
title: Finding a learning curve for Over 9000
date: 2015-05-21
---

For Over 9000 I'm estimating the number of torrent downloads per show/episode at 7 days from release. If I have enough data I can compute that by interpolating points. But usually I need to extrapolate from the first few days of downloads.

I've focused on fitting log curves with scipy and I'm starting to get setup for more rigorous machine learning.

Learning curves
===============

Learning curves are a useful diagnostic to assess your model (see Andrew Ng Coursera [lecture link](https://class.coursera.org/ml-005/lecture/64)). If you're plotting training and validation error then you can see whether you're overfitting or underfitting. If you're overfitting, it can help to reduce the parameter space or add more data. If you're underfitting then you might need more features or a more complex algorithm.

Learning curves for extrapolating number of downloads
=====================================================

Unfortunately it isn't easy for my problem. Each episode is handled as an independent machine learning problem with usually 2-6 datapoints for training. But what I can do is assess prediction quality using the first 2 days of data, first 3 days, etc. I'm comparing multiple extrapolation functions so I can plot the error of each:

![***Note: Title is incorrect. This should say prediction ERROR not accuracy.***]({{ "/assets/img/posts/wp/learning_curve_basic_3.png" | relative_url }})

The three lines are each different curves fit to the data, where *x* is the number of days since the episode was released and we're predicting the number of downloads at that point in time.

* log function with 3 parameters (log 3p): b \* log(x + a + 1) ^ c
* log function with 1 parameter (log 1p): b \* log(x + 1) ^ 0.5
* asymptote function with 2 parameters (asymptote 2p): b \* x / (x + a^2)
  + *a* is squared cause I needed to force it to be positive

The y-axis shows the average error from prediction target: abs(y - y') / y. It's percent error over 100.

What does this graph show? Especially when we have fewer days of data to extrapolate from, functions with fewer numbers of parameters to fit are much better at predicting.

But when we have 7-8 days of data the testing data is used to train the curve fit and the trend is the reverse: the fit is better with more parameters (overfitting). This is what a normal learning curve shows but it's represented differently here.

![***Note: Title is incorrect. This should say prediction ERROR not accuracy.***]({{ "/assets/img/posts/wp/learning_curve_basic_3_labeled.png" | relative_url }})

In the past I had evaluated on at least 8 days of data to see how well each function was capable of fitting. But I mistakenly selected log3p, which is good at overfitting but poor at generalizing from very few days of training data.

Also note that log3p has 100% error at 1 day of training data. That's because scipy fails to fit a curve at all and the model defaults to predicting zero. Aysmptote2p also fails to fit the data sometimes too.

In the context of Over 9000 when the curve fails to predict you'll see "DLs at 7d: ???".

Backoff
=======

One easy way to solve this is to fall back to log1p when another curve fails to fit. Also log1p does a better job with less data anyway so when there are fewer points than parameters I also back off to log1p. That leads to these curves (y-axis scale adjusted):

![***Note: Title is incorrect. This should say prediction ERROR not accuracy.***]({{ "/assets/img/posts/wp/learning_curve_backoff1.png" | relative_url }})

Compared to the previous run many fewer tests are predicting zero. The functions with backoff do a much better job now. The reason they aren't identical to log1p is that the threshold is based on number of datapoints and there are sometimes 2-3 points per day.

Log3p+backoff isn't quite as good as I'd like in part because I set the cross-over point too low (4 points isn't enough). I'll investigate this more.

We've made great progress here: extrapolation from 3 days of data has gone from 25% error on log3p (used in production) to 14% with asymp2p+backoff.

But much of the progress is made in handling cases that previously failed to predict. To look into it, I generated histograms of the errors using [pandas](https://pandas.pydata.org/).

Here's a histogram of errors for log3p without backoff:

![model_scores_3_log 3p]({{ "/assets/img/posts/wp/model_scores_3_log-3p1.png" | relative_url }})

Over 30 episodes have no prediction at all so the prediction defaults to zero (100% error). Otherwise most predictions are under 20% error.

Now compare the asymptote 2p with backoff:

![model_scores_3_asymptote 2p backoff]({{ "/assets/img/posts/wp/model_scores_3_asymptote-2p-backoff.png" | relative_url }})

The asymptote function with backoff almost never predicts zero and the predictions it gives tend to have lower error. So the overall progress is both the result of fewer default predictions as well as lower error for non-default predictions.

Model combination
=================

Machine learning tells us that ensemble methods are very strong: you combine multiple models with different kinds of errors and the combined model will be better. One of the things I noticed in looking over the predictions is that the inverse function tends to predict too low while the log functions tend to predict too high. (1)

I've wanted to take the predictions of each model and use them as features for linear regression. As a first step I'll just average the predictions of log3p+backoff and inv2p+backoff.

![Note: Title is incorrect. This should say prediction ERROR not accuracy.]({{ "/assets/img/posts/wp/learning_curve_with_meta.png" | relative_url }})

Even a simple average gets us from 14% error at 3 days to 11%. Here's the histogram of errors at 3 days:

![Histogram of errors for average of the two functions]({{ "/assets/img/posts/wp/model_scores_3_average.png" | relative_url }})

There are fewer episodes with high error.

Weighting the training data
===========================

There's one trick I found in the [scipy documentation](https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.optimize.curve_fit.html): You can provide uncertainty weights on the data points. So you can force least squares regression to fit some points closer than others.

When we have a two-hump curve like some of the weird cases in the [previous post]({{ "/blog/2015/05/curve-fitting-and-machine-learning-for-over-9000/" | relative_url }}) it's important to prefer fitting the later data.

This is what I used for weights (Python): [1 / (x + 0.5) for x in x\_data]

The 0.5 is there to prevent divide-by-zero. The values are supposed to represent uncertainty, so lower means more weight in fitting.

![Note: Title is incorrect. This should say prediction ERROR not accuracy.]({{ "/assets/img/posts/wp/learning_curve_with_meta_dayweight.png" | relative_url }})

It's hard to compare to the previous graph unless you put them side by side (I like to open both, max the windows, then command-tilde really fast). Generally we're removing another 1-2% error, more with more data points.

Now at 3 days of training data we're a 10% error.

Conclusions
===========

It's great to be able to apply the regular rules of machine learning to this problem! It really meant I could approach it more methodically and begin to fix the overfitting.

I feel strongly that further improvement is possible, perhaps 5% error from 3 days of data.

The simplest improvement would be to poll the source data hourly rather than daily.

Custom regularization would be nice: Say if I penalize for parameters that deviate too much from typical values. Partially sharing data between different episodes of the same series would also probably help. In any case, tons more progress is possible but I'll take a detour to push these models to production first.

Notes
=====

(1) It's strange but some of the data looks to clearly have an asymptote so x / (x + a) is appropriate for that data. Other data clearly doesn't have an asymptote so a log curve fits better. Most data is somewhere between though.

(2) I made two mistakes originally. First, I was filtering the data to the first X days of data and sometimes that meant I only had one point: the fake point (0, 0) which isn't enough to learn from. It's also unrealistic: we never attempt to extrapolate a series until we have one real data point. So filtering that data gave a more realistic picture.

The second mistake was in the averaging function. I used numpy.mean which doesn't throw an error on 0 inputs; it returns NaN. Then I was putting the result into a pandas Series so when I computed the mean it was filtering NaN. That's why I originally had zero predictions with 100% error.
