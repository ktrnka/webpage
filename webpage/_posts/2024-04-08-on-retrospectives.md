---
layout: post
title: On retrospectives
date: 2024-04-08
---

I've had a number of conversations about retrospectives over the past few months, and until now I didn't have anything written that I could share.

This is written for leaders in software development, but I hope it'll help others too.

Keep in mind that retrospectives are most effective in organizations that dedicate time and energy to learning and improving. If you don't have that kind of support, I don't think retrospectives will help you as much.

If you're looking for a quicker read, I suggest [Postmortem Culture: Learning from Failure](https://sre.google/workbook/postmortem-culture/) for incident retrospectives and [How to run an effective retrospective](https://www.notonlycode.org/effective-retrospective/) for periodic retrospectives.

This post mainly describes my experience as Director of Data Science at 98point6. I was very fortunate to work under leaders that valued the long-term improvement of the team and the organization. I've also included some experiences from my time as a machine learning engineer at Singularity 6.

#### Types of retros

A retrospective is a review of how things have gone in the past, and a pondering about how to do better in the future. It can be done individually or as a group. It can be a formal meeting, formal document, or an informal conversation over coffee.

In the software industry there are different activities that I consider retrospectives:

- Team retrospectives, often periodically scheduled
- Project retrospectives, which may cross team boundaries
- Incident retrospectives, also called postmortems or outage retrospectives, that tend to happen after something bad happened

I have to thank [Postmortems vs. Retrospectives by PagerDuty](https://www.pagerduty.com/blog/postmortems-vs-retrospectives/) and [Post-mortems vs Retrospectives by Parabol](https://www.parabol.co/blog/retrospectives-vs-post-mortems/) for inspiring me to discuss both the similarities and differences between these different types.

### Team retrospectives

Team retrospectives are often scheduled periodically. Some teams run them at the end of monthly sprints, while other teams might run them a few times per year. They're a time to get together and assess how well the team has been working and seek opportunities to improve.

#### Things I've learned in team retros

I'll start with some examples of value I've gained from retros:

- Collaboration in machine learning is harder than I realized
- Not everyone understands the importance of user needs when building software
- There are many common, harmful behaviors in code reviews
- Many slowdowns and bugs are associated with splitting code into multiple repos. For example, in some situations developers were submitting a pull request, reviewing, merging, and deploying a backend only to find that it didn't work with the frontend.
- I learned how noisy our alarms became over time, which was partly caused by adopting a deployment library that had default alarms not appropriate for our services
- AWS is difficult for many engineers

#### Changes we made due to team retros

These are some examples of changes we made after learning more about the problems we faced:

- I put more effort into mentoring my team in how to use user feedback and data to build more successful features and products
- A healthy culture of code reviews is possible, but it takes deliberate effort and support from leadership. Examples:
- I shared my goals for our code review culture both verbally and in writing. It's more about leveling-up the team than it is about blocking "bad" code. I would also do some code reviews and I'd be explicit about when concerns were blocking approval (like patient safety issues) or when they were non-blocking suggestions to level-up.
- Sometimes large PRs happen despite our intentions to keep them small. When that happens I redirect the review to be a conversation about the design of the change first before diving into code. Big PRs are still hard but that gets things moving and focuses the reviewer on the big picture.
- We put deliberate effort into adjusting our alarms and reduced false-alarms significantly while also adding a couple alarms for the biggest safety risks
- When hiring additional engineers, I made AWS skills a priority
- As an individual contributor, when I see that certain kinds of development requires multiple sequential PRs across repos I advocate for merging repos

#### What's worked well, and what hasn't worked well

I like the "what's worked well and what hasn't worked well" framework in retros, and I'll use that framework in a sort of retro about retros.

**Things that worked well**

- When I was new to leading retros, I asked an experienced third party to lead the retro and afterwards we discussed further so that I could learn
- I recorded the retro meetings so that others can review it later as needed. This helped when not everyone could attend. It also helped in situations where a deeper cross-org issue came up. Be careful though: It can affect what people are willing to say.
- We've had better conversations when we discuss the problems before discussing solutions
- Retrium worked well for us because it allowed a smooth process of: Everyone write things to talk about, we group them all, we vote, then discuss the groups in vote order
- Things that have worked well as the moderator/leader:
- When I set a theme for the team retro, the team was more engaged.
- It helped to start the retro meeting with a brief 1-2 minute reminder of the purpose of the retro. In that quick overview, I'd share what we will talk about, what we'll try not to talk about, my role in the meeting, and so on.
- I made sure we heard from everyone, and also made sure we all understood any issues in enough depth. Put simply, my role was to get people talking in the right direction and to listen.
- Talking begets talking, so I tried to make sure everyone speaks at least once. This helped to survey the breadth of different issues.
- It's important to balance positive and negative sentiment. If it's all negative that can demotivate people. If it's all positive that usually doesn't lead to improvement. "What's going well" or "what's not going well" is a simple framework that ensures we discuss both.

**Red flags and antipatterns**

- Nothing's changed since last time: This could indicate any number of deeper problems, ranging from issues in leading the retro to issues in culture or incentives. Or it could be as simple as not having enough time since the last retro.
- A mad rush to discuss action items in the last 5 minutes of the meeting, and then the action items are not really actionable.
- One or two people dominate the conversation. This could be the result of many different things, for example unmet needs that come up or leaders that are new to leading retros.

#### Open challenges

These are some examples of things I haven't yet figured out, or that don't feel smooth yet.

- It's tough to limit bias in issues that cross team boundaries when they come up in a team retro.
- If you prioritize by voting, certain types of issues can be systematically missed, for example advanced AWS configuration issues. It might be valuable to discuss but often won't be selected if you're only prioritizing by votes. I recommend using your judgment to override the votes as needed in special cases like this.
- Sometimes it's tough to quantify a problem. For instance, if build times take 60 minutes that's definitely a problem but it's tough to compare against other things. It's good to work on some of these hard-to-quantify issues even if you can't measure them.

### Briefly mentioned: Project retros

I've had fewer experiences with cross-team project retrospectives but I've found them useful. For short projects there may not be enough time to really assess how the teams are working. For longer projects it's best to have retrospectives partway through the project so that you can improve the project.

One example was a project that was going slowly due to long round-trip time between teams with respect to IAM permissions for Sagemaker. When we talked about it in a retro, this led to the development of a test script that the infra engineer could use when iterating. That helped us reduce the number of round-trips between people on different work schedules.

The main challenge I've faced is that the projects that need retros the most are usually projects with the least predictable timelines. I'm optimistic that it'd help to schedule retros about a month after the project starts regardless of the expected project duration. If the project is still running, then you have a mid-project retro. If the project hasn't even really started yet, it might be valuable for leads to discuss planning and see if there's anything to improve. If the project is done already, great!

### Incident retros, aka postmortems or outage retros

Sometimes our software stops working as intended and it's unavailable for our users. In an industry like healthcare, an outage can harm patients' health. In commerce, an outage can mean a loss of revenue. We often call an outage an incident.

A degraded user experience might be classified as an incident as well, for example in healthcare our software may stop working with certain pharmacies but that won't affect all patients.

Responding to incidents can be personally disruptive and frustrating for anyone on-call. Before going on, if you've been on-call, I appreciate you. Thank you.

Once we've restored service for our users, it's common to review what happened so that we can learn from it. What we learn may help us prevent similar disruptions for our users, or it may help us improve our incident response to be less disruptive for the team. We call that review an incident retro, postmortem, or outage retro.

I've learned a lot from reading incident retros and I appreciate when people take the time to share their findings. I've also learned by leading my team to write them, and writing them myself.

#### Things I've learned from incident retros

- Almost all incidents were caused by code deployment. Code deployment happens when people are working so very few of them happen overnight. Some were caused by an unreliable external system and those issues could happen overnight.
- It's very hard to automatically detect situations where a small percent of the user base has a degraded experience.
- When we don't detect an issue right away, it's often harder to debug and it slightly increases the chance that it's detected at night.
- Many incidents are caused by code that is *harder to test*, such as authentication, infrastructure, or cross-repo changes.
- Employee turnover reduces the amount of complexity a team can manage effectively, even if the team size stays the same and has the same level of seniority.
- We often reach for a technical mitigation, but there are sometimes much faster non-technical mitigations like sending a message to users.

#### Changes I've seen from incident retros

- Increased automated testing
- Policy changes with feature flags
- Changes in when we deploy code
- Changes in third-party vendors
- Changes to alarms

Also, I've become more thorough in design review about authentication, cross-repo development, and pub/sub systems.

#### What's worked well, and what hasn't worked well

Worked well

- Incident retro documents, especially when shared broadly. It turns the incident into a learning opportunity for the entire organization.
- It's helpful to time-box the efforts on the incident retro document or else it can balloon into a large effort.
- Sharing the retro document back to the incident channel provides a feeling of conclusion and progress from a stressful experience.
- It's good to write down the incident timeline while it's still fresh in mind. Some people even write it down as it happens.
- It's helpful to approach the incident with curiosity, rather than assessing blame.

On the incident timeline specifically:

- There's often a delay between when the first user is affected and when engineers are aware of the incident. In some cases, that delay can be weeks. In other cases, it can be minutes. It's good to understand how impactful that delay is, so that we can decide how much time to spend on investigating the delay itself.
- In other cases, the team may become aware of an incident quickly after it begins, but may incorrectly assess the problem for a period of time and it may help us identify a communication issue to work on
- If there was a "bandaid" response followed by a full bugfix later, it's helpful to see that. Or if the team decided to ship a full bugfix, it can be useful to discuss whether a faster mitigation in the meantime would have improved our response.

Hasn't worked well

- Sometimes I've seen people push for a retro document too soon, before the first-responders have recovered from the incident response. In those situations the first responders delay or don't do the work, and experience additional stress beyond the incident stress

These are some antipatterns or red flags I've seen:

- Ineffective incident retros that don't lead to learning or improvements
- Time-consuming incident retros that drag on for a week or longer

#### Open challenges

- Sometimes the effort to get good data is major work. Whenever possible I try to get a "good enough" answer.
- If stakeholder communication was lacking in some way, it'd be nice to discuss that in a retro but the retro members may not even be aware of the problem. If I'm running an incident, when possible I follow up with stakeholders afterwards to solicit feedback.

---

### The bigger picture: Productivity and quality

I like to consider the team's total output over the next 2 years or so, where output means contribution to cost, revenue, or other key business outcomes. If we're thinking about a 2 year timeline, it's worthwhile to mentor, learn, and grow now so that we can deliver more in the future. The time frame also helps with prioritization: If an improvement would take 1 week to implement (optimistically) and it would save a few hours of time over the next 2 years, it's probably not worth it. I also find that perspective helps when thinking about the time I put into hiring efforts: It's absolutely worth the extra up-front effort in hiring to speed up the team over the next 2 years.

Through reading many incident retros and systems designs, I learned much more about overall quality and speed in software development. In many situations, we focused on the prevention of defects by comprehensive testing, whether human or automated. We sometimes prevented defects in code review too. Likewise we prevented defects in production by trying out our software in pre-prediction environments.

An orthogonal approach is to quickly mitigate defects when you detect them. That takes support in both detection and mitigation. In detecting defects, these efforts included automated alarms, operational dashboards, and ways for users to escalate issues. Detecting them sometimes involved analytics dashboards too. Mitigation efforts usually meant reverting a change or changing a feature flag.

I've come to believe that each project has a different return on investment between prevention vs detection and mitigation. For database schema changes, prevention is often more important because it's very costly to revert. Likewise, if reverting a deployment takes an hour and you're working on a critical service, prevention becomes more important.

That said, there are projects that are very hard to test thoroughly and realistically, such as server autoscaling. In those situations I focus more on monitoring and rollback efforts.

#### Double diamond

When leading retros, I like to use [the double diamond approach from user experience design](https://en.wikipedia.org/wiki/Double_Diamond_%28design_process_model%29):

Discuss the problems (or opportunities!)

- Breadth: Hear from everyone, all the challenges. Do not shut down ideas.
- Depth: Voting is a simple way to prioritize. Looking at data is another way. Discuss those challenges in depth.

Discuss potential solutions

- Breadth: Hear from everyone, all the ideas. Do not shut down ideas.
- Depth: Prioritize and dive deep on those ideas. Think about the expected benefit for users and the expected implementation cost.

I find that it's helpful to have separate meetings to discuss problems vs solutions. If they're discussed in the same meeting it's too easy to overrun the time for the first step and end with half-baked solutions.

When I was forced to choose between the two, I spent the full time understanding the problem. If the team is senior enough and has sufficient autonomy, once they understand the problem space they'll make it better. They just need a little help understanding the problem space.

---

### Additional reading

I did a brief literature review while writing this, and I'm sharing what I've seen along with a little commentary on each.

From Google SRE:

- [Google SRE -- Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/): I love that they emphasize postmortems as learning.
- [Example Postmortem](https://sre.google/sre-book/example-postmortem/)
- [Chapter 10 -- Postmortem Culture: Learning from Failure, Google SRE Book](https://sre.google/workbook/postmortem-culture/): Great read, including a comparison of two retrospectives (one good, one bad).

From PagerDuty

- [PagerDuty Incident Response Documentation](https://response.pagerduty.com/): Good links under "after incident"
- [Three analytical traps in accident investigation](https://www.youtube.com/watch?v=TqaFT-0cY7U): I agree with the point on counterfactual traps though I'm looking for a plain way to phrase it.
- [Anti-Patterns -- PagerDuty Incident Response Documentation](https://response.pagerduty.com/resources/anti_patterns/#getting-everyone-on-the-call): This has an excellent example of a retrospective in public. What we did, what happened, what we changed, and the impact of the change.
- [Effective Postmortems -- PagerDuty Incident Response Documentation](https://response.pagerduty.com/after/effective_post_mortems/): Good quick overview. They're particular about when to use the term "outage" which seems motivated by customer communication. Communication to stakeholders and customers is good to keep in mind, though I prefer statements like "10% of customers have degraded service." It'd be even better to be more specific about the degradation.
- [Getting Started -- PagerDuty Retrospectives Documentation](https://retrospectives.pagerduty.com/getting_started/): I agree that the facilitator should generally not express opinions.
- [Planning The Retrospective -- PagerDuty Retrospectives Documentation](https://retrospectives.pagerduty.com/planning/): I agree on the use of a timer to make sure each topic is covered, and setting the agenda for the first few minutes. I don't like the example agenda though; starting with metrics can anchor the entire conversation too much on what's easy to measure, not necessarily what's most important. Also I prefer to have the "good vibes" be a more key part of the retro itself rather than the ending.
- [During The Retrospective -- PagerDuty Retrospectives Documentation](https://retrospectives.pagerduty.com/during/): I agree with using voting to help prioritize and converge.

[Debriefing Facilitation Guide](https://extfiles.etsy.com/DebriefingFacilitationGuide.pdf) (Etsy): This is a great read. Highlights:

- This is absolutely worth reading if you're a facilitator because it teaches about how to lead the group.
- "The problem comes when the pressure to fix outweighs the pressure to learn" 1000% agree
- "You are like a traffic conductor, holding up a stop sign to things like blame and judgment, while giving behaviors like genuine, thoughtful inquiry and active listening the green light. Instead of traffic signs or flares, however, your tools are the types of questions you ask, and when you ask them."

Others

- [Incident 151 \| Heroku Status](https://status.heroku.com/incidents/151): They're clear about the severity of the outage and provide examples to understand it. I especially like the "Our Response" section and their three major lessons under Remediation.
- [Blame. Language. Sharing. \| Fractional by Lindsay Holmwood](https://fractio.nl/2015/10/30/blame-language-sharing/): The section on hindsight bias is useful, especially for junior engineers. I especially like running premortems with the predictions written down, then checking the predictions later so that we can learn to anticipate the future better.
- [Kitchen Soap -- The Infinite Hows (or, the Dangers Of The Five Whys)](https://www.kitchensoap.com/2014/11/14/the-infinite-hows-or-the-dangers-of-the-five-whys/): I agree that multiple factors always contribute to a problem, though I didn't interpret "The Five Whys" in the way they did.
- [STELLA report](https://snafucatchers.github.io/): Great quote: "Postmortems are not magic. They can be done well. They can also be done badly" YES
- [How to run an effective retrospective](https://www.notonlycode.org/effective-retrospective/): I love this one, and I might not have written my post if it had been longer.
- [Improving Postmortem Practices with Veteran Google SRE, Steve McGhee](https://www.blameless.com/blog/improve-postmortem-with-sre-steve-mcghee): Lots of great content here. The commentary on including names is unique and valuable.
- [Manifesto for Agile Software Development](https://agilemanifesto.org/): They put it simply: "At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior accordingly."

Collections of links

- [A collection of postmortem templates](https://github.com/dastergon/postmortem-templates)
- [danluu/post-mortems: A collection of postmortems](https://github.com/danluu/post-mortems)
- [awesome-leading-and-managing/Postmortems-Retrospectives.md](https://github.com/LappleApple/awesome-leading-and-managing/blob/master/Postmortems-Retrospectives.md): Great collection
