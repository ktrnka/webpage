---
layout: post
title: Lessons learned in 2022
date: 2022-12-30
---

At the end of each year, I like to reflect on my career and life. This post is meant to celebrate learning and growth, whether learning something new, or changing my mind as I gain more experience. I hope you'll also take time to notice and celebrate your own growth this year!

As I was listing things out, I didn't want anyone to feel like this is in any way a competition about how much you learned. So the list is just an assorted survey of topics that this audience may find interesting.

------------------------------------------------------------------------

### Machine learning

Genetic algorithms still have uses, even in the age of neural networks. I found them useful in an optimization problem that was difficult to represent as constraint programming and also difficult to represent as gradient descent. Using a genetic algorithm drastically shortened the time it took to get an algorithm functional enough to demonstrate.

Early in the year, I'd dismissed GPT3 and other large language models as hype and not interesting. I was wrong -- they're quite interesting and useful, even if they're *sometimes* overhyped. I've found them useful for writing and summarizing, and sometimes as an alternative for Google search. I find it helpful to think of them as "super duper fill-in-the-blanks algorithms". And related to that, prompt engineering is an interesting field. If you'd like to learn more, see [Learn Prompting](https://learnprompting.org/).

### Data science

Over the years I've used machine learning tools to do data analysis that can adjust for confounding variables. This year I also explored statistical methods for the same in the form of generalized linear models (GLM). I mostly used those methods to analyze whether a new product feature was having an effect on efficiency while controlling for confounders such as the practicing doctor, how busy the clinic was, the complexity of the patient's issue, other features, and so on.

I found that both machine learning methods in scikit-learn and GLM in statsmodels were valuable but have slightly different advantages. GLM methods will tell you things like "feature ABC changes visit duration by +0.1 to -0.4 minutes." Machine learning toolkits like scikit-learn on the other hand have advantages in preprocessing your data and dealing with messy data, even text inputs.

Regardless of the approach, I still haven't found a satisfying way to explain the results of either approach to a general audience, even after reaching out to more experienced folks for advice. For now I do two types of analysis: one that's more technical for myself and I use it to guide a more interpretable analysis for a general audience. Hopefully I'll learn a better way in the future.

### Software engineering

When designing a software system, the ease of local testing has a large effect on the amount of bugs and also the team's happiness. I had an inkling of this before but feel more strongly about it after reviewing 50-100 code bases for deployment safety.

[Pub-sub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) is more complicated than I previously thought. This year I saw two challenges in testing: 1) the order in which events are normally triggered can be critical 2) some pieces such as retries may be implemented by AWS and are harder to test. In the cases I saw, the order of events was not well understood and it led to bugs. Now that I've experienced the pub-sub pattern I'm better equipped to look out for reliability risks.

Healthy on-call alarms and notifications can be designed by asking questions such as: When would you want to be woken up at night? When could a notification wait until business hours? When would you prefer to periodically check dashboards, with full awareness that you will forget sometimes? What would the business impact be if all alarms had been disabled for the last 6 months?

### Leadership

Previously I thought that teams would be able to autonomously fix chaotic on-call rotations if only they have skill, time, and agency. This year I learned that teams also need a little nudge even if they have all those things.

Speaking with a small group that knows you is VERY different than speaking with a large group that doesn't know you. Your immediate team knows you and will give you the benefit of the doubt. In a large organization, many people do not know you and you may not have earned the benefit of the doubt yet. I felt that push me towards more "manager speak" when talking about company policy or roadmap. I suspect that many of the leadership flops I've witnessed in the past were the result of talking to a large audience the same as a small, high-trust audience.

------------------------------------------------------------------------

### Baking

This year a friend asked me about making bread from 100% whole wheat flour to reduce glucose spikes. I'd tried it once or twice before and it came out awful. This fall I took the time to read up more and practice, so now I see that it's possible to make good-tasting 100% whole wheat bread. The lessons are 1) use a lot more water than the equivalent white bread, and going by the dough texture is ok 2) add a hint of sweetness to balance it, such as cranberries 3) allow more proofing time than white bread. Hopefully the cranberries don't spike glucose too much.

I'd tried making bagels before with unsatisfying results. I'm not sure what I changed other than the recipe but I practiced a lot more this time and they came out very satisfying. As before, one key was to do a little more reading, and then practice every day until it's good. There's still more improvement to make but I found some ideas to try on /r/breadit.
