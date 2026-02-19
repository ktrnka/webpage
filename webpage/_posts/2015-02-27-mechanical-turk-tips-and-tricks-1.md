---
layout: post
title: "Mechanical Turk: Tips and Tricks 1"
date: 2015-02-27
---
Spend some time as a worker
---------------------------

You'll make better tasks if you understand the worker's perspective. If you're planning on using MTurk for a long period of time spend an hour here or there just doing tasks. You'll quickly learn that many tasks have broken Html, poor rendering, are too long, pay poorly, etc.

Make sure the layout size is big enough
---------------------------------------

Few things are more annoying than having the HIT with a second set of scroll bars because the layout height was set too small. And luckily that's easy to test.

Test/proofread your HIT
-----------------------

Nobody gets the HIT perfect the first time. So create your HIT and:

* Try it yourself in the sandbox. Any pain points?
* Ask a friend to view it in the sandbox or just share in dropbox. Any confusion points?
* Make a test batch with real pay (~5% size) and add a comments box for feedback on the HIT. What are people saying?
  + You can leave the comment box in for your real batch but note that it will increase completion time a little (which leads to lower effective pay or higher cost).

Also use this process to set a decent price for your HIT by averaging completion time and computing at $6-10/hour.

The cycle of rejections
-----------------------

Sometimes workers get sloppy and you need to reject their work. In this case the pay is refunded. But Mechanical Turk is setup in a way that makes it very adversarial:

* The worker lost time and their approval rate is lowered. Once it's below a 97-98% many jobs will not be available anymore and they won't be able to make money effectively.
* If the worker thinks the rejection is unfair, they might discuss via email. Or you may just get a negative TurkOpticon review. Or they may post on popular Turker groups like TurkerNation, Reddit, etc.
  + Either way this leads to a smaller worker pool you can use. (And eventually will drive up the amount you need to pay to get timely results)
  + Be sure to explain your rejection to help avoid this.
* If the work is particularly bad you might block that worker, but it has even more adverse effects on the availability of tasks (not just yours!).

So you're faced with a dilemma: If you reject people too much you're increasing the chances of a negative post/review. When you're starting out and have only 1-2 reviews that's a big deal.
If you don't reject borderline/bad work enough then everyone will have 99% approval rate and you won't be able to filter bad workers anymore.
This leads to related issues as well. Say a worker accidentally hits enter with the forms blank. They email you their results and ask that you don't reject. If you accept it, you add their results manually and approve. Or you reject. But it may take a minute to add to your data manually and another minute to respond to the email. MTurk doesn't allow you to edit the data on the server though, so you need to remember to add after the data is all downloaded. Someday if you download again you'll need to add manually again (if you even remember).

What happens when pay is too low
--------------------------------

You may not get all tasks completed. Very few people will do your HIT so it'll fall off the first page of HITs before anyone willing will see it. If you're a popular requester someone may follow you via TurkAlert but until then "most recent" is how people will discover your HIT.
Even if it's completed, HITs with low pay will take much, much longer to complete.
You're also likely get negative reviews on TurkOpticon which will decrease the number of workers you get in the future.
