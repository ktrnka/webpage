
---
layout: post
title: nlp and statistical significance
date: 2010-12-07
---
Now that I'm done with my Ph.D., I can say that I wish I'd gotten a masters in statistics.  Or something.  You end up using it a lot more than you expect, and sometimes you need to do non-trivial analysis.  Either way, I learned a lot, though mostly I learned things the hard way.
background
Statistical significance is typically used in study situations.  For example, suppose you're interesting in analyzing the benefits of a text entry method, like say Swype.  You need a baseline, say T9.  I'm simplifying it a lot, but you'd have a group of people use T9 and a group of people use Swype.  You'd measure words per minute in both situations.  You find that Swype is say 15 words per minute faster on average.
But did that happen due to chance?  Maybe you had one or two really good people with Swype or one or two really bad people with T9.  Note that we're only considering the randomness of our sample (the group we used from the population).  If the Swype group is faster cause they were using performance-enhancing drugs, the numbers by themselves won't tell us that.
In a basic world, we label each group with the average words per minute and some value representing the amount of variation in the data (like standard deviation).  We use both values in deciding whether the difference could've just been chance.
Another way to look at it is to plot histograms of both data sets.  Use the same color and formatting for the bars of both data sets.  Is it hard or easy to tell which bars belong to which distributions?
p-values
When you test for significance, you usually end up with a p-value.  The p-value is the probability that you're wrong and the things you're comparing really are the same.  In some sense, the p-value represents part of the risk associated with believing there's an effect.
In terms of traditional explanation, you come up with a null hypothesis (the thing you're trying to disprove).  It might be that the true mean is zero, or that two distributions are really two samples from the same population. The p-value is the probability that the null hypothesis is true.
Now the strange part comes in.  Normally, researchers use a cutoff and anything above the cutoff is deemed significant.  Anything below the cutoff isn't significant.  Sometimes the symbol alpha is used to represent the cutoff on the p-values.  Typically we use the cutoff 0.05.  So we want 5% chance of error or less.
Now think about this:  suppose we do a test and have p = 0.001.  Suppose we do a test and have p = 0.049. Suppose we have a test and have p = 0.8.
I'm an advocate of reporting actual p-values when possible.  If something isn't significant, it may be close, which is saying a lot more than p = 0.5.  Or it may only barely be significant.  Or the chances that you're wrong may be more unlikely than winning the lottery.
For some interesting further reading, see [this article](http://feedproxy.google.com/~r/StatisticalModelingCausalInferenceAndSocialScience/~3/ZJV24YLvbFk/is_005_too_stri.html).  It also points out another interesting perspective - setting strict thresholds leads to conservative research.
not significant
If something isn't significant, why not?  You can imagine how stressful it can be in publishing when a significance test fails. If you're looking at it from a numbers perspective, either the means weren't different enough, or standard deviations were too high. It could be legitimate - maybe there really is no difference between your groups. Or maybe it's something you can address.
It could be that you didn't survey enough data points - if there's variation and the means are close together, it may take many data points to show significance.
It could also be issues in your experimental design.  If the conditions vary a lot, that can lead to more variation in your data.
practical significance vs statistical significance
With many data points, you can show statistical significance even with a 0.1% difference in means.  That doesn't mean that it'll help people in a meaningful way.  Or that the research was worthwhile.  It just means that you're allowed to say that there was a difference.
significance in NLP

* points are things like documents, not people.  You're essentially dealing with the variation due to one particular corpus (and potentially your methods).
* paired tests are easier to use, and are stronger tests of significance
