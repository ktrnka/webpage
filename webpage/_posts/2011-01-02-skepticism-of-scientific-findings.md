---
layout: post
title: skepticism of scientific findings
date: 2011-01-02
---
[The New Yorker](http://www.newyorker.com/reporting/2010/12/13/101213fa_fact_lehrer) has an interesting piece on reproducibility in science, citing several biomedical studies that showed smaller and smaller effects over time in re-testing.  They also tests run by multiple groups where some found significance and some not.  Some researchers found huge effects and some not.
The unfortunate aspect of the article is the lack of hard data.  If we're talking about small sample sizes, differing results are normal and uninteresting. If we're talking about large samples, that's a different story.
I'll admit though, I came across it on Slashdot where it was entitled "Why Published Research Findings Are Often False", and that title bothered me.  If you can't reproduce someone's results, it could mean many things.  Furthermore, the word *wrong* is overly general.
I'll list several reasons why you may not be able to reproduce an NLP study.

* you're using different texts
  This may or may not affect the original results.  Sometimes methods are specific to a certain kind of text and it's not obvious.
* different preprocessing
  It could be as simple as a different tokenization method.  Or maybe one study removes certain punctuation and the other doesn't.  Take a step back for a second and ask yourself:  Is one method of removing punctuation always right?
* different implementations of underlying tools
  I'd be willing to bet that there are differences in the many available [support vector machine](http://en.wikipedia.org/wiki/Support_vector_machine "Support vector machine") implementations or language modeling toolkits.  I'd also bet that the differences could change the outcome of some studies.  There can also be differences due to the version.
* different algorithm implementations (due to lack of documentation)
  I still remember the first time I tried to implement an algorithm in a paper.  Before I started coding, I thought it was a great paper.  After I started coding, I realized they didn't document many important settings.  Many research papers are like this --- the amount of information necessary to understand the high-level idea is much less that the amount of information needed to re-implement someone's work.
  + different implementations can also be the result of mistakes.  For example, maybe an equation in the paper doesn't perfectly match the original because of a small mistake.  Enough small mistakes and it's not reproducible.
* varying implementations
  Sometimes results can take weeks to obtain.  If you make a slight change afterwards, you may not have time to go back and redo everything.  This may be poorly documented in the publication --- maybe they assumed that the change was irrelevant.
* if real users are involved, a whole host of problems could be the culprit:
  + Is there some [sample bias](http://en.wikipedia.org/wiki/Sampling_bias "Sampling bias")?  Are you only including eager participants?  Are you only including technophiles?  Are you soliciting participants in locations with a gender bias?
  + How are the instructions delivered to the participants?  Are there differences in the directions?  In the proctors' performances? Subtle differences can change your outcome.  For example, suppose the proctor from the old study encourages participants to use the system naturally and comfortably, but the new study's proctor asks them to completely utilize the system.  Even this simple difference can lead to large changes in the outcome.  But keep in mind, this isn't something that people will likely document.
  + How do you deal with outliers?  Sometimes there may be legitimate reasons to exclude data.  For example, suppose the participants are typing on a device and the device locks up.  You probably can't integrate the data, so it's gotta go.  Similarly, if someone decides to answer their phone during a study, that might be a good reason to throw out their data.  If someone's natural typing rate is abnormally slow or fast, you might consider removing it.  But you shouldn't remove data because it makes your system look really bad.  If you do that, you'll be chasing significance like the article mentions.

At the high level, if you can't reproduce something it means you didn't follow the original procedures exactly.  Most likely it means that the original procedures were inadequately documented.  In computer science, this becomes very clear once you try to code someone else's algorithm.  It's also possible that you misread the original procedures.
*Sources: [The New Yorker](http://www.newyorker.com/reporting/2010/12/13/101213fa_fact_lehrer), [PLoS Medicine](http://www.plosmedicine.org/article/info:doi/10.1371/journal.pmed.0020124), via [Slashdot](http://science.slashdot.org/story/11/01/02/1244210/Why-Published-Research-Findings-Are-Often-False?from=rss)*

### addendum

After thinking about it more, probably some of the negative tone is reactionary.  I bet that there are people who view scientific publication as the final arbiter of truth, and I can imagine being annoyed by that.  Unfortunately, there's no easy way to decide truth or not.  Scientific methods help a bit, but you still have to use your head.
