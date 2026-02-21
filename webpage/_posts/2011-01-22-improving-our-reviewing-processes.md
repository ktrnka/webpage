---
layout: post
title: Improving our Reviewing Processes
date: 2011-01-22
---

It looks like the new issue of CL Journal is out today, and Inderjeet Mani has [an interesting Last Words article](https://www.mitpressjournals.org/doi/abs/10.1162/coli_a_00046) about reviewing.  It's only 4 pages, but I'll summarize it and then comment.

summary
-------

### Problems with Reviewing

* Lack of qualified reviewers
  There are many examples of good papers being rejected or poor papers being accepted.  Mani brings up an example of a rejected paper that won a best paper award the next year.  Part of the problem is that the field is increasingly specialized - most people work on very specific problems.  The current solution to finding reviews is informal, based on who you know and good reviewers from past experience.
* Lack of quality control
  This section title has a little mismatch with the text.  The text focuses on the issue of limited time - we can't have quality reviews without significant time investment on the part of the reviewers, yet reviewers are already strapped for time.

### Finding Qualified Reviewers: An ACL Reviewer Database

A proposed solution to the lack of qualified reviews is a central ACL database.  The database would be updated for all ACL-related conferences/journals with the reviewers' information.  This may sound like a privacy concern to some, but Mani points out that most conferences already publish such lists (though admittedly without some of the proposed information:  number of papers reviewed and interests).

Mani proposed additional information to help in the reviewer selection process:  specialist/generalist, prolific/occasional, and skill level.  Beyond this, he suggests that we might be able to calculate a reviewer's impact factor to provide assessment of the reviewer (the type of number used to judge publications/journals), which would be:

(how many journals and conferences a given reviewer has reviewed for) / (how many articles in those venues were reviewed by any reviewer)

He suggests that normalization by subfield may be necessary also.

### Encouraging High-Quality Reviews

Mani brings up the idea of open reviewing using the [British Medical Journal](https://www.bmj.com/) as the prime example.  In this and other journals, the reviews are made public.  Thus the quality of the reviewing can have a real effect on reputation.  He notes some problems though, such as a tend towards more conservative reviews.

The second interesting part is that some journals ([Biomed Central](https://www.biomedcentral.com/) and [Atmospheric Chemistry and Physics](https://www.atmospheric-chemistry-and-physics.net/)) provide access to the history of versions of a paper in addition to their reviews.  I can only imagine how instructive this would be for a young researcher.

The final suggestion is to train reviewers.  Maybe the reviewers tried, but forgot to review a certain aspect of a paper.  Or maybe they didn't provide clear suggestions for improvement, etc.  British Medical Journal is mentioned again - they provide PowerPoint presentations to train reviewers.  One of Mani's suggestions is to potentially require some short online reviewer training (somewhat akin to human subjects training I imagine).  Open reviewing ties into this:  Open reviews could form the basis of an example-based training program.

comments
--------

First off, the problem is interesting.  Why are we focusing on it now?  Reviewing has always been time consuming and error-prone.  If I had to guess, I'd suggest that people are talking about it due to articles about scientific review in mass media.  I know Ars Technica has written about scientific review many times in the past few months.  It's tough to say whether we're at a breaking point where reviews have become so demanding and unreliable that we need to change... or whether it's just perception.  Either way, I think the system could use an update and it's good at times to relentlessly pursue better science.

The first comment I had is "What is a qualified reviewer?"  One interpretation is that you are (potentially) qualified to review in venues that you've published in.  But I think Mani means qualified for a particular paper.  Suppose there were a hypothetical paper submission about using methods A and B to solve problem P as part of a task T.  [An example](https://aclanthology.org/D07-1118/) might be using a [Markov model part of speech tagger trained on Penn Treebank] and [the EM algorithm] to solve the problem of [domain adaptation] for [biomedical part of speech tagging].  Now here's the question:  Are you qualified to review such a paper without any BioNLP knowledge?  What about without knowledge of domain adaptation?  What about without knowledge of HMM taggers, but BioNLP knowledge?  It's a bit unclear.  Then there are other issues:  Some people are qualified and don't know it (or the program chair doesn't know it).  And some people are unqualified and don't know it.  So who decides?  (I didn't mean to come off as ranting; it's just a fundamental question that I felt was vague)

The reviewer database could be good.  Though I have to wonder if ACL/NAACL/EACL would use anything short of the full database.  In this case, it's feeding ACL reviewers from other conferences, which is probably a good idea.  I wonder if it'd keep up with increased submission rates?  Mani mentions a 24% increase in submissions from ACL 2008 (Columbus, OH) to 2009 (Singapore).

If we're thinking about this in terms of algorithm design, it might be safer to require each author to review one paper.  One small concern is that authors might reject everything in trying to get their own work accepted, but I doubt that would happen (especially if we move in the direction of open reviews).  Who knows, reviews might even be faster or better because you're placing yourself in the shoes of the people reviewing your work.  I'm sure there are some problems with it, but it's an idea to consider.

On a side note, I'm surprised that they haven't tried to make better use of younger researchers.  I haven't written my own ACL/NAACL/EACL full paper yet, but they haven't asked me to review and it seems like they're in a pinch to find reviewers.  This reminds me of some faculty I've known that mostly pass off the reviewing task onto their students anyway.  In the cases I've observed, the students write a much more thorough review anyway, because they haven't learned to value their time and they're afraid of doing a poor job.  Something like this could even be pushed into doctoral programs.  If a paper you review is accepted, lead a discussion on it.

I don't know how I feel about open reviewing.  It could be good, but it feels too much like "Do the right thing or I'll burn you!"  Publication history might be nice, but I don't know if I'd be comfortable with it.  Sometimes my first submission has a few embarrassing typos (real-word errors, accidental extra word, etc).  Also, if I saw a paper that was revised three times before a final accept versus a paper that was revised once, would that affect my perception?  Would I view the latter paper (and author) as better and the former as something salvaged and molded into something barely passable?  I'm not sure, I just think it merits further thought and discussion.

The idea of reviewer impact factor is interesting, but I don't think it's something we can measure.  We're trying to measure how much their reviewing helps the field, right?  The act of reviewing alone isn't enough, you need some sense of review quality.  Instead I'd say it's more important to see if the review led to many improvements in the final submission (for accepted papers) or whether it led to improved papers in the future (for rejected papers).  It's not practical to measure, but I think that's what we want to get at.

Reviewer training is something I partially agree with.  I strongly agree with the idea that reviewers need more than the simple review page they're given.  Depending on the conference/software, the review categories may be explained well.  Or they may be over-explained, leading reviewers to only skim them.  At the same time, the scoring scale is often unclear.  What does a 5 or 1 for novelty really mean?

At the same time, the problem of reviewing is partly due to lack of time.  Adding training makes the lack of time worse.  Instead I'd suggest self-paced additional help.  Maybe in the review site, try to have video game-like help tooltips as you go from one page to the next?  Simple things like tooltip-based help in the review site can work wonders.  It's not annoying and in your face, but is available for very little effort when needed. Also, if ACL goes with a training program, it might be worthwhile to consider YouTube videos instead of PowerPoint.  I'm always surprised at just how many excellent tutorials are on YouTube.

Also, I'd suggest working review training into graduate programs somehow.  What better time to train researchers?  (Though I have to point out that this is similar to teaching - there's an expectation that a Ph.D. can teach, but it's not a part of most Ph.D. programs.)

I like to think about reviewing as an economics problem.  From the reviewer's perspective, it costs you time and energy.  You might potentially consider opportunity cost if a paper isn't interesting.  Your time is already a limited, high-value resource.  What's the benefit to the reviewer? Satisfaction that they've *maybe* made the field better and another item in your CV.  The *maybe* part is the killer - doubt.  Maybe someone else would've done the job just as well?  As far as your CV, there isn't distinction between quality of reviews.  If anything, this encourages the young researcher to perform many quick/poor reviews rather than taking the time to write good ones.

There needs to be a benefit.  Because of human nature, it should be a concrete, short-term benefit.  Maybe the best [log n] reviewers get free or reduced conference registration.  Or even some small iTunes/Amazon credit.  It's a little longer term, but best reviewer awards can work wonders.  Or it can even be something as simple as "if you come to the conference, you get an extra drink ticket".  Or the best reviewers are given a better chance to pick only the papers they want next time.

You can frame the benefit as lack of humiliation in an open reviewing system, but people seem to respond better to an actual benefit rather than lack of punishment (I've been reading Don't Shoot The Dog recently)

Finally, I'd suggest that a quality user interface removes many of the burdens from the user:

* What if the review system automatically found and linked all of the citations for you?  That's one less step of going on Google Scholar/etc if you need to dig something up.
* Suggested missing citations - could we use text similarity and similar citations (minus similar authors) to detect recent work that should be potentially referenced?  (This might not even need to be part of such a system - it's one of the ideas I'd love to implement for Google Scholar)
* I forget who it is, but someone in ACL wrote a script to use text similarity to suggest reviewers (using publications from the reviewers).  I'm not sure if that's still in use, but it might ease the problem of finding appropriate reviewers.  The main thing is that it would need to provide a concise reason for each suggestion so that the program chair can tell whether it's similarity based on the methods, subfield, or just writing style.
* Could text overlap (minimum distance edit) and potentially similarity be used to highlight the truly novel contributions of a paper compared to the author's prior work?
* (not UI) Would better guidelines in CFPs help?  For example, imagine saying something like "We welcome results-focused papers, but papers lacking any linguistic intuition are often rejected."  It might help to have guidelines for several different types of papers (incremental improvements vs high-risk research, numbers focus vs linguistic focus, guidelines on task-specific components)
  + I bring this up because not all reviews cost the same amount of time.  If you're determined to write a good review, reviewing a poor paper takes significantly longer than a good paper.  For example, papers written in poor English can take minutes just to decipher individual sentences (even syntactically; not fitting the semantics into the article).  Similarly, poorly explained methods or motivations can make it very difficult.  Mentoring programs help a lot with English, but not much with the latter.

*Note:  Sorry for writing too much.  I feel like half of the problem is that we need more and better ideas, so I wanted to put it all out there.*
