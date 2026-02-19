---
layout: post
title: Ensemble notes
date: 2015-11-23
---
I thought [probability calibration](http://scikit-learn.org/stable/modules/calibration.html) would be difficult but it's pretty easy. My ensemble code looks like this:

```
estimators = []

estimators.append(("nn", NnWrapper(dropout=0.5))
estimators.append(("gb", GradientBoostingClassifier(300)))

if calibrate:
  estimators = [(n, CalibratedClassifierCV(c)) for n, c in estimators]

model = VotingClassifier(estimators, voting="soft")
```

The only downside is that training the calibration-wrapped model is now going to run 3-fold cross-validation on the training data to learn the calibration. When predicting on new data it uses the calibrated probabilities from each of the three classifiers and averages them.
I ran several tests on the 200k x 61 dataset and found that calibration helps a tiny bit. But I also found that the results fluctuate much more than my non-ensemble classifiers even though I'm testing the ensemble in 5-fold cross-validation. (1)
Here are the raw numbers over 4 tests with and without calibration. Each of those tests is a 5-fold cross-validation run so the standard deviations are showing the variation between the different folds.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Without calibration | | With calibration | |
|  | Accuracy | Std dev | Accuracy | Std dev |
|  | 67.93 | 0.12 | 68.11 | 0.48 |
|  | 67.77 | 0.14 | 67.87 | 0.19 |
|  | 67.86 | 0.18 | 67.89 | 0.19 |
|  | 67.96 | 0.15 | 67.89 | 0.16 |
| Average | 67.88 |  | 67.94 |  |
| Spread | 0.19 |  | 0.24 |  |
| Runtime | 51.7 min |  | 95 min |  |

My first run with calibration was amazing: 68.1% accuracy is the best I've ever seen on this data! But it was a fluke. Also the standard deviation is very high, which likely means that one of the folds was accidentally very easy to predict. Although the average accuracy is higher with calibration it's almost entirely due to that one outlier.
Calibration about doubles the runtime as well. When I stop to think about it, it's running 3 training runs over 2/3 of the data instead of 1 run so it should be around double.
One cautionary note about CalibratedClassifierCV: It checks the numpy datatype of the output value and uses stratified cross validation if it's boolean or int. That's what I want. Luckily Pandas automatically set my output type to int64. If you're loading the data without Pandas be warned that numpy's default datatype is a floating point type which would lead to non-stratified cross validation. Non-stratified cross-validation can sometimes lead to bad evaluations especially if the output classes are sparse.
**Conclusion: Calibration helps a little but it's not worth the additional runtime.**

Isotonic calibration
====================

The default calibration is labeled as sigmoid but is really just feeding the output value of the base classifier into logistic regression. This is also called [Platt scaling](https://en.wikipedia.org/wiki/Platt_scaling).
[Isotonic](https://en.wikipedia.org/wiki/Isotonic_regression) calibration only uses the ranking of the probability value compared to other output probabilities. It's a more capable learner but prone to overfitting on small data sets.
I've only done one test with isotonic calibration so far and the accuracy was about the same but the standard deviation of accuracy across the folds was halved.
**Conclusion: Possible minor benefit from isotonic calibration. Need more tests.**

Hard voting
===========

I've been using soft voting which averages the probabilities of the individual classifiers. When you only have two good models it's the only option. I briefly tried including logistic regression in the soft voting ensemble but found that it was harmful.
However, I didn't try hard voting. Not all classifiers provide probabilities so hard voting is sometimes necessary. Another advantage is that I don't have to consider calibration.

|  |  |
| --- | --- |
| Model | Accuracy on 200k x 61, 10-fold |
| Hard voting: Neural network + Gradient boosting + Logistic regression | 67.57% |
| Soft voting: Neural network + Gradient boosting + Logistic regression | 67.53% |
| Soft voting: Neural network + Gradient boosting (previous best) | 67.88% |

Hard and soft voting with three classifiers are well within a standard deviation of each other. But they're well beyond a standard deviation lower than soft voting with the two best individual models.
I had a feeling hard voting wouldn't do anything magical but was curious if maybe there's some way I can use my less accurate models to improve the overall ensemble accuracy. It may be useful to use logistic regression in a soft-voting ensemble but I'd need to tune weights for each classifier.
**Conclusion: Not much different from soft voting except that it doesn't work with weighting.**

Thoughts and next steps
=======================

Overall I get the feeling that ensembles can get me that last fraction of a percent on a problem. In a competitive environment like Kaggle that can be the difference between top 50 and top 5. Also when you've run out of ideas for feature engineering it's another option for that last little bit of improvement.
Assorted ideas for further improvement:

* Run a grid search over weights in the 2-model soft voting ensemble
* Use the code for CalibratedClassifierCV as a guide to use logistic regression to combine models. I tried something like this before but didn't correctly train it like how CalibratedClassifierCV is implemented.
* Set up the ensemble so that different models can use different feature subsets. I'd like to have a model that uses the list of champions on each side but most models overfit that data (logistic regression is the exception). I think probably I need to migrate my code to [scikit-learn pipelines](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) to have an ensemble with different feature subsets.

Notes
=====

1. Clarification just in case: The evaluation is using 5-fold cross validation but inside each of those 5 folds CalibratedClassifierCV is splitting the training set into 3 folds.
