---
layout: post
title: nlp and statistical significance
date: 2010-12-08
---

I wanted to jot some notes on statistical significance as a follow-up to the evaluation post.  But I tried to write for a wider audience, and it ended up being huge and incomplete.  In this post I'll describe some of the oddities of using statistical significance for NLP research, and maybe at a later date I'll write a primer on statistical significance.

Traditional significance testing might be something like the following scenario.  You have two different groups of people and you're measuring the difference between them with some metric.  You want to know if the difference is significant or "real".  Normally one group is a control or baseline group - it's just a normal group, nothing special.  The other group usually has some sort of change applied (some hypothesized improvement).

That's the idea for traditional testing - you're trying to decide if the differences in the means could really just be due to variation of the subjects.  In NLP, instead of subjects, you might have documents.  The before/after groups are the same set of documents with a baseline method and improved method.  Here you're concerned with the variation due to your method.  Maybe it's better on some documents but really bad on some others.  In this case, it could be that the overall difference you see can be explained by chance.

That said, if you can apply a paired test, you should.  The idea of a paired test is that you convert your two sets of data into a single set of improvement scores.  You might just be taking a difference.  I'll make one note though - you should consider your particular data and decide whether you think the absolute difference or percentage difference is more important.  Which is more consistent across documents?  It can be the case that it's easier to achieve significance with one or the other.  But it's bad statistics to just run both and pick the better one, so you have to decide ahead of time.  If you're wondering why it's bad - there are probably hundreds of ways to compute significance.  If you run them all and pick the most favorable, of course your results will seem significant.

In general, you should use paired tests when you can because they're stronger.  But paired tests really show some of the strangeness in significance testing for NLP:  Some improvements are unable to decrease performance (such as adding an extra last stage in a backoff language model).  That means that the paired distribution is all or mostly all positive.  So your mean is positive and the standard deviation is such that the distribution covers mostly positive examples.  In this case, significance is somewhat trivially accomplished.

Another thing to note is that significance testing is strongly affected by sample size.  In this case, the number of documents.  In my own work I've seen this.  In tests with many documents, significance is easy to achieve even if the improvement is small.  In tests with few documents, it can be much more difficult to achieve significance.

Research in NLP is interesting in that it can have user studies as well, which follows a more traditional analysis.  Studies with humans are substantially more complex though.  For example you have learning effects - even asking someone to perform the same task twice probably won't have the same outcome.  Everything from the environment to the way you communicate and explain things to subjects can affect your results.

I'll give some examples of how you can perform statistical significance in some situations.  Note that I predominantly have experience with paired t-tests, but in general you'd want to consult someone more experienced if it's important.

* unadaptive word prediction
  The prediction of each word in a document is (more or less) independent, so you can take individual words as your unit to measure over.  In this case, significance should be trivial (unless you have large variance) because you have a huge sample.
* adaptive word prediction
  The prediction of each word depends on previous words in a document, so you have to take documents as the smallest independent unit.
* parsing
  In traditional parsing, the processing of each sentence is independent of every other sentence.  In this case, you can take sentences to be your unit of measurement.
* part of speech tagging
  Normally you process each sentence independently.  Words aren't processed independently though, so the smallest unit of independence is a sentence.
* text classification
  If you're classifying documents, then documents are your smallest unit of independence.

In any case, statistical significance can be useful for NLP depending on the situation.  In some cases, it's not very informative and in other cases it can be helpful to identify if a benefit varies too much.  All that said, here's my advice for grad students - take a decent stat class while you're still taking classes.
