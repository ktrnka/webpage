---
layout: post
title: Switching from deep to wide
date: 2016-02-02
---
In the [previous post](/blog/2016/01/gains-from-deep-learning/) I found gains by adding a second hidden layer. But I accidentally found even better results with wider networks of a single hidden layer. I've done more systematic experimentation and wanted to share. Just as a reminder this is a part of my ongoing project to predict the winner of ranked matches in League of Legends based on information from champion select and the player histories.

On the smaller dataset (50k rows) increasing the size of the network is harmful: it's just overfitting. This is probably a part of the reason why I originally decided to stay with a small network but I'll show that this conclusion doesn't apply to the larger dataset.

![Shallow NN hidden units on 50k dataset]({{ "/assets/img/posts/wp/shallow-nn-hidden-units-on-50k-dataset.png" | relative_url }})
*The hidden layer config is shown on the x-axis as Python tuples; this graph is a series of experiments all with a single hidden layer of varying widths.*

I began to replicate this test on the larger dataset and unfortunately found that my training code doesn't scale. It works relatively well for networks of under 500 hidden units but slows down more as it scales. Normally the 200k dataset takes 4x longer to train than the 50k dataset. In this situation however, I suspect it's the full-batch training that's scaling nonlinearly and I suspect that it's because of the matrix of 200k x 500 weights.

But I learned this the hard way: It took perhaps 12 hours to train all sizes on the 50k dataset with 20-fold cross-validation so I expected around 48 hours for the 200k dataset. After letting it train for an entire week I gave up.

In short I've changed my training:
* Old: 100 epochs in batches of 1024 followed by 100 epochs of full batch training
* New: 100 epochs in batches of 1024 followed by 100 epochs of batches of 5000

In the graph below I separated the two training methods but it doesn't seem to matter much.
![Shallow NN configurations on 200k dataset]({{ "/assets/img/posts/wp/shallow-nn-configurations-on-200k-dataset.png" | relative_url }})

The trend is unsteady especially considering the standard deviations but it's reasonably consistent. When I first tested wider networks I tried 250 and 500 units, which got 68.2-68.4% accuracy. Those results were probably just outliers. Even so, the wider networks fare quite well (considerably better than the deeper networks I tried last time).

If it's one thing I've learned it's that nothing quite goes the way you plan. After starting these experiments I've begun following along [Stanford's CS231n class on convolutional neural networks](http://cs231n.github.io/). One of the things Andrej said is directly applicable: rather than tuning the network size to the data, pick the biggest that you can and tune dropout.

It makes sense: Increasing dropout will sort of shift the excess capacity for learning over to ensembling. But I'm also not entirely happy with the added training time of the larger networks and that may slow down my overall experimentation. On the other hand, thinking about it this way is directly analogous to the way you tune regularization for logistic regression so it simplifies code a little. I tested 50 and 250 units on the 50k dataset in conjunction with tuning dropout and found the same accuracy for both network sizes once dropout was tuned for each one. Maybe this weekend I'll try replicating the network size graph on the 50k dataset in conjunction with dropout tuning.

Another thing I learned from the class is that the Keras models suggest an incorrect weight initialization, or at least it's incorrect in conjunction with ReLU. The default is glorot\_uniform but it should be he\_uniform or he\_normal. Both kinds of initializations compensate for diminishing variance of the activations as you stack layers but the Glorot ones are only correct for sigmoid and tanh activations. In ReLU initially about half of the activations will be zero and the He versions compensate in initialization so that the variance of activations doesn't vanish as you go down the network (which is a problem because the gradients will be very very small and the initial updates too small).

![Neural network initializations over 3 dropout settings and 2 network configurations on 50k dataset.png]({{ "/assets/img/posts/wp/neural-network-initializations-over-3-dropout-settings-and-2network-configurations-on-50kdataset.png" | relative_url }}) Experiment on 50k dataset of dropout [0.4, 0.5, 0.6] x 3 initializations shown above x 2 network configurations: (50,) and (50, 50)
The truth is that I didn't expect it to matter at all with shallow networks but it's a reliable improvement. In some ways switching from glorot\_uniform to he\_uniform is more important than tuning the dropout param.

Since this test I've added the initialization test to many of the configuration experiments on the 200k dataset. Generally he\_uniform has a more stable trend from one configuration to the next and is usually better than glorot. I haven't tested enough configurations to know whether the degradations from Glorot are due to outliers or not.

One brief note: I think the class examples used glorot\_normal and he\_normal. Not really sure why uniform is better but I'd guess that it has better symmetry-breaking properties.

Next steps
==========

* Replicate the network size scaling graph in conjunction with tuning the dropout. I'm hoping to see that it's flat or slightly increasing.
* Replicate scaling graphs with he\_uniform to see if it really is more consistent from one configuration to the next.
* Get this working on GPU - I spent a few hours but found that it's challenging to get CUDA installed under Windows or at least, a version of CUDA that Theano can use. I looked into TensorFlow instead but that's actually less supported than Theano.
* I've been focusing too much on tuning the individual models I think.... it'd be great to get back to feature engineering.
* I've been meaning to update the datasets for season 6, which started a few weeks ago. Lots has changed in the game: Champion select is done in a way where you're more likely to get the role you want. There are tons of champion and item changes. And team queue for 5v5 is gone - now you can queue up as 2-5 people in the same queue as solo but it tries to match the teams or subteams in addition to the players.
  + I've been avoiding thinking about this because it's enough of a change in data that my intuitions from this data may not transfer 100%. And I have to do more engineering work, in particular the player history stats need both season 5 and season 6 information.

Probably I'll take a break so I can catch up on homework for the Stanford class.
