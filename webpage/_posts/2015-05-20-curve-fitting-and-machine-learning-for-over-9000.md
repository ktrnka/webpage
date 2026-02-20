---
layout: post
title: Curve fitting and machine learning for Over 9000
date: 2015-05-20
---

One of my current projects is [Over 9000](http://over9000.bitballoon.com/), a visualization that shows which anime series are currently popular. I get the data by scraping a popular anime torrent site every day and come up with a single number that represents the popularity of a show.

The number I use is the average number of downloads per episode, interpolated or extrapolated to 7 days since release.

Current approach
================

Each episode of each show is processed independently; I'm treating this purely as a curve-fitting problem. Typically I get one datapoint per day per episode. If the episode's been out for more than 7 days then I interpolate. Otherwise I use scipy to fit a, b, c in this equation:

downloads *= b \** log*(*days\_since\_release *+ a) ^ c*

For more info on the background see [previous post](/blog/2015/02/projecting-the-number-of-downloads-for-torrents/).

Problems
--------

Occasionally during development I'd get 3-4 different datapoints at hour intervals. When they were very close to the release date the equation would fit a nearly vertical curve and estimate downloads in the trillions or more. But after it got another day of data the estimate would stabilize to something more reasonable. As a hack I put in a rule that the estimated downloads at 7 days couldn't be more than double the current downloads.

The evaluation was problematic also. I'd estimate downloads at 7 but I didn't actually have evaluation data, so I'd interpolate between the closest two points.

Machine learning problem
========================

I'll continue to predict each episode independently. When an episode has been available for 4 days typically it means I have 3 data points. And I also add a fake point of 0 downloads at the release date.

This is somewhat different than a regular regression problem in a few ways:

1. Much less data. We'll normally have 2-6 training examples (number of downloads on a given day)
2. Extrapolation not interpolation. In a normal regression problem, the prediction has a value similar to those seen in training. But in this problem, we're predicting a larger value than any seen in training.
3. Multiple parameter sets. Each episode has one parameter set; we're really learning hundreds of models.

#1 means that we want a model with pretty high bias. We want to force the system to only consider hypotheses in a limited range. Fitting a curve is a great approach: the above curve has only 3 parameters (similar to linear regression with 2-3 features).

When I was struggling with crazy predictions I should've stopped and thought about it: the model was fitting the training data well but giving terrible performance on the testing data. It's overfitting!

There are many solutions to overfitting but in one way or another they're reducing the hypothesis space: 3 variables is too many when we have so few training samples.

Aside: Remember linear algebra?
===============================

In the distant past I had to solve systems of equations. When there was only one variable you just move the parts around to solve. When you have two variables you needed two equations. And even then they couldn't be multiples of one another. Three variables, needed three equations. Obligatory [Wikipedia link](http://en.wikipedia.org/wiki/System_of_linear_equations).

That said, typically it isn't possible for find parameters that perfectly fit this data. Real data is noisy. So using a solver isn't the right approach but I should've remembered the basic principle that you need at least N equations to solve for N parameters.

Sometimes scipy.curve\_fit throws errors when there's fewer training examples than parameters. Sometimes not. In cases when it doesn't, it extrapolates very poorly.

Mistakes were made
==================

I picked the function above because it was able to closely fit a complete download curve. This was a horrible mistake.

In a regular machine learning problem you'd plot a learning curve to show the quality of your system on training data and on testing data. And you'd pick the best model on testing or development data. The best model for your training data is probably overfitting and won't generalize well.

Simple solution
===============

When trying to learn a model, if it has 4+ datapoints I use the 3 param equation. If not I use a 1 param equation that works pretty well:

downloads = *a* \* log(days\_since\_release + 1) ^ 0.5

That only requires one non-zero data point to fit and doesn't get too crazy. This solution is pretty similar to backoff in language modeling: fall back to a model that generalizes better when you lack data.

Fixing evaluation
=================

Another issue is what we're testing against. It used to interpolate the downloads at day 7 and use that to evaluate. But then I'm chaining errors from the interpolation into my evaluation.

The real problem with that is that I'm drawing a straight line between the closest point before 7 and closest point after 7. But the true data isn't a straight line so I could be penalizing a model for a correct prediction.

Now I search for any data points between 6.5 and 7.5 days since release and use those are testing data.

Looking at weird data
=====================

Sometimes we fit the data poorly because we pick poor parameters for our model.  Other times it's because the model can't represent the data.

In experimenting with various models I found that a small number of episodes had download curves that couldn't be fit well by any of my models. In the development data it was 8/398 episodes, about 2%. It's interesting to look at them:

![Aldnoah Zero, Episode 21. It's tough to see but the first 3 days follow a log curve (just a much smaller one).]({{ "/assets/img/posts/wp/aldnoah-zero_21.png" | relative_url }})

![Gundam G no Reconguista, Episode 24. Another interesting one and again it looks like a smaller log curve started off at first then a bigger one is added.]({{ "/assets/img/posts/wp/gundam_g_no_reconguista_24.png" | relative_url }})

![Knights of Sidonia Season 2, Episode 2. This clearly looks like two curves added.]({{ "/assets/img/posts/wp/sidonia_no_kishi_daikyuu_wakusei_seneki_2.png" | relative_url }})

Looking over them I'd say that probably a less popular fansub group is occasionally doing an earlier release than the more popular one. Or it's plausible that the show had a really good episode and tons of new fans started watching a few days later. It's also plausible that there was a processing bug and I was missing data for the first few days. But I'd expect that to be only missing data for a single day.

Here's a normal curve for reference:

![Naruto Shippuuden, Episode 408. What a smooth curve!]({{ "/assets/img/posts/wp/naruto_shippuuden_408.png" | relative_url }})

Wrapping it up
==============

Sometimes a machine learning problem is staring you right in the face but you just don't recognize it. Also it's interesting to run into a problem that's difficult with ordinary classification or regression.

Next steps
==========

* Improve evaluation framework
* Make something similar to learning curves
* Finalize the new equations
* Explore linear regression using predictions from each equation as features
