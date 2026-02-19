---
layout: post
title: MLOps Design Principles
date: 2023-02-16
---

There's a big difference between building a machine learning model that works on your computer, and making that model available for others to use. If implemented poorly, your users will be frustrated that your software isn't reliable. And it can take months to implement it well!

In this article I'll share the principles I've learned over the years in deploying models. It's meant for readers with basic awareness of machine learning and software engineering.

------------------------------------------------------------------------

### The basics

So you've got a model and want to integrate it into your product? It's probably not a one-time thing! You're going to need to fix bugs or release improvements! So you should think about having a process or system for updating models.

You're going to want it to be easy for your team. You also want it to be reliable -- your users won't be happy if the service goes down when you update! Those are the two key concerns: **minimizing defects and maximizing developer productivity**.

I want to first acknowledge the bigger picture before getting into machine learning: These concerns aren't specific to machine learning at all!

The DevOps movement is about breaking down harmful silos in organizations, and integrating the culture of writing software (dev) with culture of operating servers and networks (ops) to improve both productivity and reliability. I can't summarize the entire field here, but these resources can help:

- [The Phoenix Project](https://www.goodreads.com/book/show/17255186-the-phoenix-project): This is an entertaining read about a highly siloed, unproductive organization that improves.
- The annual State of DevOps Report: These reports are full of gems. They tend to be hosted on a different website every year so you'll have to search for it.
- [Accelerate](https://www.goodreads.com/en/book/show/35747076): This is a book version derived from the annual DevOps reports and it's well-worth a read.
- [The Google Site Reliability Engineering (SRE) handbook](https://sre.google/sre-book/table-of-contents/): This is another excellent resource for keeping your code running without downtime.
- I'd also recommend looking through the links in this [Reddit introduction](https://www.reddit.com/r/devops/comments/yjdscp/getting_into_devops/).

Although the foundation of DevOps is cultural, in practice DevOps often refers to the processes, skills, and tools used to deliver software rapidly and reliably. Unfortunately many software delivery tools do not work well for the delivery of machine learning models. Machine learning also faces unique challenges, such as training and evaluating models.

MLOps is about building and delivering machine learning code+models rapidly and reliably. While MLOps inherits the cultural principles of DevOps, in practice it also addresses special considerations in processes, skills, and tools.

------------------------------------------------------------------------

### MLOps Design Principles

These are lessons I've learned from deploying models at Swype, Nuance, and 98point6. I'll explain the problems that motivated each principle and how I've applied it since.

I find it's important to understand why you build software so that I can better adapt to new situations. That's why I'm writing up principles -- I've seen many people overly focus on tools without understanding the underlying reasons. And what's more, each company comes with different challenges so the existing solutions may not apply, even if the principles do.

One last word before I get into it -- I haven't "solved" this field by any means. This reflects my current understanding from a decade of industry experience and I hope to improve my opinions in the future.

#### Version the code and model together, or link them

Your newest model may not be compatible with old versions of your code. So if something goes wrong and you need to revert, you need to know both the model and code version to revert to.

Likewise, a code change may require you to retrain your model. That can be anything from changing your neural network architecture to updating your dependencies to changing your preprocessing. In some cases, the new code will crash when trying to load a new model. In other cases, it might successfully load a model but have worse performance.

At Nuance we had an extreme version of code-model dependencies. We produced a software development kit (SDK) for phone makers (OEMs) to build their own keyboards. We also provided language databases which had word lists and language models in them. Manufacturers often wanted the latent language databases, but were wary of upgrading the SDK version. (\*) So we maintained a giant compatibility table, listing the language database versions supported by all common versions of the SDK. In some cases, OEMs would use code from years prior and we couldn't convince them to upgrade. So when we'd plan changes to our model files, we often had to discuss whether it could degrade reasonably in most prior versions of the code.

That experience motivated me to make code-model compatibility easier to track at 98point6. We used tools like [data version control (DVC)](https://dvc.org/) which made it easy to track by storing models in S3 and linking model versions into git.

(\*) OEMs often just didn't have the time to update their integration for any breaking changes and often didn't even have the time to validate an update. That said, most were willing to accept [patch versions](https://semver.org/).

#### Atomic deploys and reverts

We don't want downtime while deploying or reverting our software. And because the code and data versions must be aligned, it's important to deploy or revert them as one unit. We don't want a temporary outage when one of them has deployed but the other hasn't yet.

This is easy if you package everything together, such as a Docker image or a mobile app. It's more difficult if the model is stored outside of the code package. But it can be addressed by naming models with their version and explicitly loading the model by version in your code.

I only bring up this topic because I've heard of many people deploying models by manually overwriting an old model version, which doesn't give us a nice way to deploy and revert.

Also note, there are similar DevOps challenges when deploying multiple components that must be kept in sync, such as a web service with a database schema change, or deploying a web service with infrastructure configuration changes. So if you're looking to learn more you may find inspiration in the best practices for those kinds of deployments.

#### Training and serving in the same repo

At 98point6 we tried having separate repos and a single repo for machine learning projects and I found that development is faster and less error-prone with a single repo.

When there are training-serving interdependencies, separate repos can lead to this:

> PR in training repo -> merged -> integrated into serving repo, only to find it doesn't work -> go back to the start

It's an incredible waste of time that just doesn't happen with a single repo.

One alternative would be to import code from the local copy of the training repo into the local copy of the serving repo. I've found that people tend to skip it and even when it's done it's sometime prone to copy-paste accidents.

The main downside of a single repo is that you need to implement multiple CI/CD pipelines in the same repo. That's easy in some CI/CD platforms and harder in others.

I've found a similar lesson in general software engineering, for instance when a frontend and backend are split across repos, or multiple tightly coupled backends are split across repos. One warning sign you might have this is when people make PRs just to see if something works in another repo.

Demos are also closely related. If you have a minimal frontend demo in the repo, it allows developers to test more easily *before* anything goes to a pull request or deployment. At 98point6 we had some repos with demos in the repo and others with demos in a separate repo. It was much faster and less error-prone to develop in repos that had built-in demos.

#### Single implementation of models

It's best to have a single implementation of the model that's used in both training and serving.

At Nuance we had a separate implementation in training in Python and production in C. The Python implementation trained the model and evaluated it on held-out data. The C implementation loaded the model and had some basic unit tests. Over the years, we discovered that the two implementations didn't handle some cases the same way (like the start of a sentence) and that meant that the production models were suffering degraded quality.

There are many ways to address this. TensorFlow Lite and PyTorch Mobile are for mobile apps. TensorFlow.js is for Javascript. And ONNX is a cross-platform, cross-framework file format with runtimes for many languages. That said, as I write this I'm learning that it [can be difficult to make your models compatible with ONNX](https://news.ycombinator.com/item?id=34799597).

If you can't share the model code, you should at least test that the two implementations behave similarly.

#### Review and approve your model releases

It's *very tempting* to only deploy models with better evaluations. That's a subtly flawed approach because your testing data may change. If your testing data changes, you don't know whether the numbers should go up or down. You might fix a bug in the testing data only to see that the metric was overly optimistic and now looks worse. Or you may update your testing data periodically and find that the distribution has shifted over time, which could make it easier or harder to get good metrics.

A human should review the evaluation report. If anything looks odd, they should review the model outputs on some standardized examples to spot anything that might not be detected in automated evaluation. Ideally you should have guidelines that the team can follow when doing this, and they can use their best judgement with your guidelines. If you use Github, I'd recommend the pull request process for this.

I learned this the hard way at Nuance. We periodically found quality issues in our testing data, such as the way it was preprocessed for Unicode, how duplicates were removed, or how language identification worked. It was particularly common for new languages with new data.

At 98point6 our model builds produced a training report and opened a pull request. If anything looked odd we could investigate it manually. This gave us the flexibility to change our testing data and the process to review our models. We improved it over time by developing guidelines for the team and putting them in the repo's pull request template.

#### Test, not too much, not too little

Testing is a complex topic that could take a whole article. If you haven't read it, I strongly recommend reading [Testivus](http://www.agitar.com/downloads/TheWayOfTestivus.pdf) first because that's my stance.

First off, I want to acknowledge that evaluating your model on held-out data *is* testing. It's often ignored when talking about testing but it's a key component of quality control for machine learning.

The challenge I experienced at Nuance and 98point6 was that we wanted unit tests that depend on the models, but the models change often. For example, the word predictions for "I am \_\_\_" might change when we improve our model. If we have unit tests that depend on those predictions, they will fail and someone will think they've broken the code when they haven't. If those tests are maintained, they'll be frequently edited and don't offer much value as tests.

So on to my guideline: Test that the model loads. Don't extensively unit test the model's behavior. You already tested the specific outputs against held-out data in a way that's much more robust than unit testing anyway. We adopted that stance at 98point6 and it was an improvement.

Side note: Design your code base so that you can unit test any business logic independently from your machine learning model. If you do that, the business logic tests will be less flakey, and they'll run faster too.

### Automate when possible

Reduce the burden on your devs by automating what you can, such as retraining models with new data or deploying a model once it's validated. Automate testing when you can.

Be cautious about automating too soon -- automation isn't always worth the effort, and it's also risky to automate a process before really understanding the challenges.

In cases where testing wasn't automated, I found that some devs would forget to run tests and push buggy code or models. Then it would disrupt another developer, who would think they broke something.

In cases where deployment wasn't automated, non-experts were sometimes afraid they'd break something and would wait for "the expert" to be available. That could lead to delays and moreover the culture felt unhealthy. It's better if everyone can deploy and only occassional issues need a specialist.

In cases where training wasn't automated and wasn't trivial, I found that one person would become "the training person". That puts an unfair burden on one person and makes the team less resilient, not to mention any delays if they take a vacation.

### Early ideas

These are a couple of design principles I'm entertaining, but not yet certain of.

#### Snapshotting dependencies

I prefer to leave dependencies unpinned when possible so that they're updated by frequent rebuilds. That way, we're getting minor patches pretty frequently. And if there are breaking changes we're exposed to them a little at a time rather than all at once in a big update.

I came to prefer this style of dependencies after pinning dependencies in repos at 98point6 and finding that it typically led to very outdated versions of libraries. Then when a crisis happened, it forced an upgrade of many dependencies all at once which led to delays in a crisis situation.

This sort of thing may vary by company, for instance if you have tooling to periodically test your code with updated dependencies, or if you have a strong culture around dependency updates.

In the context of machine learning, the model artifact may depend on certain installed libraries. Scikit-learn models can be sensitive to the version of scikit-learn and joblib, for example. They may just not load in a different version. So the version of those dependencies needs to be pinned in the serving code. You just can't take a chance with another version. And if you have automated testing of new version, it'll just fail unless you code it to retrain on certain dependency updates.

I also want to mention that saving your models with ONNX and other library-independent formats may fix this problem altogether for you, so long as you don't also have any preprocessing code that needs to be released to the service.

#### Use dependencies, not too many, not too few

It's generally good to use well-tested, publicly-available code instead of writing new code. For example, using PyTorch will be better than writing your own neural network library from scratch because it's highly tested and optimized.

On the other hand, I've seen code that goes overboard with dependencies that aren't strictly needed. Unfortunately, each dependency is an opportunity for a performance bug or security vulnerability. I found this was a problem in the Javascript ecosystem. As a result, projects which depended on Javascript would often trigger security scan warnings. At 98point6 I experienced this because of CDK in Javascript -- we'd go to deploy a minor update to an old service only to find that the Javascript dependencies of CDK had tripped the security scanner. Then we'd have to go figure out the update process.

In contrast, Swype and Nuance were on the extreme minimal side of dependencies. In my first two months I learned that we couldn't use standard template library (STL) in C++ because some of our customers required compilers without STL. So instead I wrote my own data structures which were certainly less tested, documented, and performant than STL. If I could do it again I'd explore other options.

There's another cost to dependencies -- it's more for new developers to learn. When you're adding more dependencies and complexity, it's good to double-check that the benefit will be worthwhile even for new teammates.

### What's next?

Thanks for reading!

[In the next post I walk through an example repo that shows MLOps for web services on AWS](https://medium.com/@keith.trnka/mlops-repo-walkthrough-90c7bd275f53). After explaining the repo I'll also audit it.

------------------------------------------------------------------------

### Appendix: Types of deployments

There are many different kinds of deployments and they affect MLOps differently. I'll provide a brief summary of how they differ here:

- **Web services**: Latency is a major factor to consider, and that leads to things like auto-scaling or geographic distribution. And don't forget that you're paying for that compute too!
- **Code packages**: Releasing your model and code as an importable package frees you from thinking so much about the compute environment. But your models may be integrated much slower than you'd like. Also, you may not get crash reporting.
- **Mobile apps**: Mobile devices vary widely in terms of compute and memory, which affects the kinds of models you can ship. You also don't have precise control over getting your update to everyone's phone, especially on iOS.
- **Analytics data warehouse / ETL**: If you update a model, should you re-run predictions on all old data? Or just new? How will you communicate that to your users? Software dependencies can be a challenge depending on your platform too.
- **Web frontends**: The available compute and memory varies widely across users. You also don't have full control over when they refresh and get updates by default.

I've worked with most of these except deploying models into web frontends. I'm sure there are other types of deployments with unique challenges as well.
