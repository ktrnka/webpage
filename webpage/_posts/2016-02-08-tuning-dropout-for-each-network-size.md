
---
layout: post
title: Tuning dropout for each network size
date: 2016-02-08
---
In the [previous post](/blog/2016/02/switching-from-deep-to-wide/) I tested a range of shallow networks from 50 hidden units to 1000. On the smaller dataset (50k rows) additional network complexity hurts: It's just overfitting. On the larger dataset (200k rows) the additional complexity helps because the amount of data prevents the network from overfitting.
But I learned from the [Stanford CNN class](http://cs231n.github.io/) that I made a mistake: It's bad to view network complexity as regularization, instead it's better to pick the most complex you can and tune dropout (and/or L2). I'd amend that to say that it's bad if you have excess compute resources. If the pace of experimentation is limited by runtime then reducing the network size may be a good way to achieve both regularization and experimental efficiency.
Just as a reminder this is a part of my [ongoing project](https://kwtrnka.wordpress.com/tag/league-of-legends/) to predict the winner of ranked matches in League of Legends based on information from champion select and the player histories.
Here's the graph from last time, showing that added network complexity is harmful on a small dataset. I kept the default of 0.5 dropout.
![Shallow NN hidden units on 50k dataset](/assets/img/posts/wp/shallow-nn-hidden-units-on-50k-dataset.png)
The hidden layer config is shown on the x-axis as Python tuples; this graph is a series of experiments all with a single hidden layer of varying widths.

Tuning dropout for each network size
====================================

I replicated the test but stopped at 600 units; it takes increasingly longer to train the wider networks and I was running several times more tests than before. Let's start with tuning dropout separately for each hidden layer size:
[caption id="attachment\_1488" align="alignnone" width="4818"]![Scaling number of units with and without dropout tuning on 50k dataset](/assets/img/posts/wp/scaling-number-of-units-with-and-without-dropout-tuning-on-50k-dataset.png) The hidden layer config is shown on the x-axis as Python tuples; this graph is a series of experiments with different numbers of hidden units in a single hidden layer. This was run with 10-fold cross-validation and the following dropout values were tested: [0.4, 0.5, 0.6, 0.7, 0.8].[/caption]Now we see a different trend: when tuning dropout in conjunction with the network size, the added capacity doesn't lead to overfitting. If anything it improves accuracy slightly then plateaus.
It's also interesting to see the trend more consistent but that could be the result of taking the max over 4 tests. I'm not sure how to assess that independently.
Also note that the best dropout value I tested for 200-600 is 0.8 (the max value I tested). Higher values may have been better but I didn't have time to test more.

Weight initialization
=====================

I replicated these tests with the he\_uniform initialization (the default is glorot\_uniform). Last time I saw benefits from he\_uniform but didn't test thoroughly.
![he_uniform vs glorot_uniform across network size with and without dropout tuning](/assets/img/posts/wp/he_uniform-vs-glorot_uniform-across-network-size-with-and-without-dropout-tuning.png)
The dashed lines show the results without tuning dropout - he\_uniform is generally an improvement. It's isn't any more consistent than glorot\_uniform though (previously I was thinking it might be).
When we tune dropout for each network size (solid lines) they're almost identical. Looking into the best dropout values per size, the tuned values for he\_uniform tend to be lower values of dropout. It still transitions to 0.8 for the larger networks but not until network size 300 in contrast to 200 for glorot\_uniform. Another way of looking at it: The default 0.5 dropout is closer to optimal for he\_uniform and therefore it fares better when dropout isn't tuned.
I can only guess at the cause... probably the additional randomness in initialization with the He correction is starting the network off with additional diversity. Dropout itself is forcing diversity so maybe we don't need to force it as much.
All that said, I'm happy to have learned more: Although He initialization is important for deep networks with ReLU, for shallow networks it's a minor improvement. But depending on the test it may appear to be an improvement if dropout isn't tuned because it changes the optimal value of dropout.
 
