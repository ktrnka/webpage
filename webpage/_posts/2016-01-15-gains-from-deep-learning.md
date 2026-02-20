---
layout: post
title: Gains from deep learning
date: 2016-01-15
---

Back from the holidays! I've finally made some progress with neural networks, particularly a deep network. This is a part of my ongoing project to predict the winner of ranked matches in League of Legends based on information from champion select and the player histories. [Previously](/blog/2015/12/ensembles-part-2/) I'd been working on ensemble methods, but concluded that they're more of a last-mile improvement.

First off, what is deep learning? It's any neural network with 2 or more hidden layers.

Deep neural networks in conjunction with convolutional layers are the reason machine learning has made so much progress on face and object detection. They're also responsible for large improvements in speech recognition over the past decade. More recently language modeling has seen large improvements due to recurrent neural networks. (2) That said there's a ton of variation in deep learning so we use the underwhelming definition "any neural network with 2 or more hidden layers".

**What changed for my problem?** I revisited an assumption I had: That subsequent layers are modeling higher levels of abstraction and therefore it makes sense to reduce the number of units in deeper hidden layers. I tried a network that was 56 inputs -> 75 hidden units -> 5 hidden units  -> 1 output. This is consistently worse than 56 inputs -> 75 hidden -> 1 output. At the time I concluded that deep learning wasn't applicable for my problem. After all, neural networks don't dominate all kinds of machine learning problems.

Why revisit my assumption? I was reflecting on my future over the holidays and wanted more practice with deep networks; they're taking over industry and I keep thinking "I wish I could do that!" Had I been busy with something else or not been reflecting I may have never tried this.

Deep networks
=============

As usual I started development on the 50k dataset because it's fast. I did a quick first test then expanded my search to include the following configurations. I'm only listing the configuration of the hidden units because the input and output layer sizes are determined by my feature matrix (55 inputs, 1 output).

* 75 hidden: 66.49% +/- 0.65%
* 75 hidden -> 75 hidden: 66.34% +/- 0.56%
* 30 hidden -> 30 hidden: 66.19% +/- 0.55%
* 20 hidden -> 20 hidden: 66.04% +/- 0.54%
* 75 hidden -> 5 hidden: 65.99% +/- 0.53%
* 10 hidden -> 10 hidden: 65.98% +/- 0.61%

The network with two hidden layers of 75 units each does surprisingly well, enough to make me question my previous judgment on a network of 75 and 5.

I was surprised that the smaller networks didn't do so well; my thought process was that a deeper network with a similar number of parameters might have an easier time learning. The 30->30 network has 2,610 weights in the model compared to 4,256 for the 75 network. In contrast the 75->75 network has 9,900 parameters. (1)

I ran some of these configurations on the 200k dataset and finally achieved gains over the 75 unit network!

![Accuracy vs network configuration]({{ "/assets/img/posts/wp/accuracy-vs-network-configuration.png" | relative_url }})

That's a great improvement over the previous best neural network on this dataset. Furthermore it's competitive with gradient boosting which tends to get around 67.8%-67.9% accuracy.

Additional experiments
----------------------

I tried additional **network configurations** 100 -> 100, 100 -> 75, and 75 -> 75 -> 75.  The results seem slightly improved on the 100 -> 100 and 100 -> 75 networks and much worse on 75 -> 75 -> 75.

I tuned the **dropout parameter** in the range 0.4-0.6 and then again 0.4-0.51 (default 0.5) on the 75->75 network. The trend isn't a smooth curve so I'm hesitant to draw conclusions. The sheer amount of variation worries me. If nothing more, higher values seem to be worse.

![Accuracy vs dropout]({{ "/assets/img/posts/wp/accuracy-vs-dropout.png" | relative_url }})

Based on [a tip from Yann LeCun](http://www.cs.nyu.edu/~yann/talks/lecun-ranzato-icml2013.pdf) I tried setting the **error function** to binary cross entropy rather than mean squared error (MSE). The results were wholly worse: There was no configuration in which it was better. I tested this in conjunction with dropout experiments and found that the models trained with MSE had accuracy in the range 67.4-68.1. Binary cross entropy training had accuracy 66.9-67.2.

I increased the **number of training epochs**, thinking that deeper networks need more time to converge. Previously I was running 100 epochs in batches of 1024 followed by 100 epochs of full batch training. I also tried 200/200 and 300/300. Generally the 200/200 runs were an improvement and the 300/300 runs were worse.

![Batch spec ((100, 1024), (100, -1)) means 100 epochs in batches of 1024 followed by 100 epochs in matches of max size (full batch).]({{ "/assets/img/posts/wp/accuracy-vs-training-iterations.png" | relative_url }})

It seems that iterating more on a deep network is just overfitting. So I tried **[early stopping](http://keras.io/callbacks/#earlystopping)** based on 10% held-out validation accuracy with patience 20 epochs. If accuracy doesn't improve for 20 epochs it stops. In theory this should fix any issues with the 300/300 epoch training but it failed; early stopping was generally worse overall. I found this surprising cause I've heard Geoff Hinton say that early stopping is a sort of free lunch - you're speeding up training and preventing overfitting at the same time.

![Accuracy with and without early stopping]({{ "/assets/img/posts/wp/accuracy-with-and-without-early-stopping.png" | relative_url }})

During the experiments I came to realize that due to **randomness** in initialization and training (dropout) there will always be some outliers in a batch of results. If I run 20 tests of the same model there's a good chance one or two will have top-notch accuracy and one or two will perform horribly. So I've become more skeptical of results and I'm recording not just accuracy but standard deviation of the cross validation more often. I'm also tending to look more at the distribution of results while tuning other hyperparameters (the graphs above are like this).

As I was writing this up I came to see that the shallow network with 100 hidden units was a little better than the 75 unit network. It's funny because I used to use 100 units normally and reduced to 75 to speed up experimentation. I tried a shallow network with 250 hidden units and found that it got 68.42% (best ever) so now I'm going through much more thorough testing of wider shallow networks.

Odds and ends
-------------

Before holidays I ran a few more tests with ensembles. First I tried encouraging diversity in the ensemble. My thinking was to tweak the settings so that the individual classifiers would each overfit. So I reduced the min-samples-split setting in gradient boosting and reduced dropout in the neural network. It didn't help  though.

I also tried adding logistic regression and random forests as components in the stacked ensemble. When testing on the 50k dataset, logistic regression improved the accuracy of the ensemble to get best results. Adding random forests to the ensemble hurt performance. Funny enough, when stacking with linear regression it assigns random forests a *negative* weight. I'm amazed that they're *that*bad.

Before I'd gotten into deep networks I revisited the activation function. In Keras you can pick ReLU, sigmoid, or tanh. I picked ReLU after initially finding it vastly better than sigmoid. In retesting I found that ReLU was vastly superior to both sigmoid and tanh for the hidden units. The results were pretty close for the output unit.

Thoughts
========

Stepping away from the problem and coming back to it gave me a fresh perspective and helped make progress, especially by retesting assumptions.

Next steps
----------

* Thorough evaluation of shallow networks. Tests of hidden layer size are in progress.
* Tune the learning rate. I haven't touched the default learning rate at all.
* Revisit maxout now that I have deeper networks

Notes
=====

1. Due to dropout maybe I should think of each layer as about half the size?
2. I'm grossly simplifying. Probably none of the progress would've happened without GPU-accelerated linear algebra. Or without better learning techniques for deep networks (rprop/rmsprop, adam, tweaks on sgd). Or without the massive increase in training data (NNs not as useful for small data). It's tough to choose but I'd also include dropout, maxout, LSTM, GRU and ReLU as part of the neural network renaissance.
