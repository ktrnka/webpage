
---
layout: post
title: Mechanical Turk tips for beginners
date: 2015-02-20
---
I've been using Amazon's Mechanical Turk for side projects, whether it's for annotating data, generating short-form content, or evaluating subjective quality.  When I started I had several misconceptions, found a lot of great info, and learned many lessons the hard way.

Misconception 1: Cheap work
---------------------------

I'd first heard about MTurk through academic papers where people would pay $0.01-$0.05 per task.  The part I remembered was that it was cheap and quick.  But that's not quite true: you're paying people for work and much of the workforce tracks the effective hourly wage of your tasks.  If you pay very little, most people will skip your tasks.
Usually it's best to estimate the completion time of your task and pay at least minimum wage. I'll admit that I don't know what that means for countries other than the US though.
Simple recipe for setting reasonable pay for $8/hr:

1. Make tasks in the sandbox and do them yourself.  Measure average time per task.
2. Set real task pay to $8/hr \* 2 \* your average completion time.
3. Run a mini batch (say 20) with real workers at this rate.
4. Update the task pay to $8/hr \* average completion time in mini batch.

Misconception 2: Spam, spam everywhere
--------------------------------------

I'd heard people complain about spammers - workers randomly clicking buttons or typing garbage to complete tasks faster.  And researchers build complex systems of reviewing to combat it.  This is a half-truth.  You can get quality results by requiring masters qualification (default) or 98-99% approval rate with 2000+ tasks completed (cheaper, similar quality).  People also suggest limiting to US/CA only and I do that but haven't evaluated how important it is.

Misconception 3: Cheaper than doing it yourself
-----------------------------------------------

Let's assume that you're paying $6/hour and you're a researcher making $50/hour.  Suppose that you have 800 news article titles that you want reviewed for spelling and grammar.  On average say it takes 20 sec to review one article title.  If you're focused on it and doing them in batch maybe it'd take an expert 10 sec per title.
So if you do them all yourself it takes 2.2 hours, effectively $111.11.
Or you could create an MTurk task and the workers complete it in 4.4 hours total, effective $26.67.  But it takes you 2 hours to get the data files setup, write the directions, figure out how much to pay, test, and revise the design. So the total cost is really $126.67. Effectively you lost money because of the time spent setting everything up and "debugging" the task. That said, you may have learned new MTurk skills along the way and it might've been more interesting.  So it may have been worthwhile.

### Caveat: Not all tasks are possible to do yourself

Suppose you're asking turkers to look at two designs for a website and tell you which one they prefer.  Each person has a different opinion so it's not possible for you to do it yourself.  Or maybe you could ask 10 people on the street but it doesn't give the same statistical reliability as 300 opinions.
Opinion-type work can't be done yourself.

Links
=====

[TurkerNation](http://turkernation.com):  Forum with lots of helpful people, great place to get tips and tricks.  Focused more on the worker side but there are enough requesters to answer almost anything.
<http://turkernation.com/showthread.php?21352-The-Myth-of-Low-Cost-High-Quality-on-Amazon-s-Mechanical-Turk>
<http://blog.echen.me/2012/04/25/making-the-most-of-mechanical-turk-tips-and-best-practices/>
<http://mechanicalturk.typepad.com/blog/2013/07/hit-critique-design-tips-for-improving-results-.html>
[Best practices (official)](http://mturkpublic.s3.amazonaws.com/docs/MTURK_BP.pdf): Very useful.
[TurkOpticon](https://turkopticon.ucsd.edu): Where workers go to review requesters.

What next?
----------

I'll start writing down some of the tips I've learned.
