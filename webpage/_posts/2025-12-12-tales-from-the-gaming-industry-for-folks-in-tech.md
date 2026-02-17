---
layout: default
title: Tales from the gaming industry for folks in tech
date: 2025-12-12
---

After a year at Singularity 6 working on [Palia](https://palia.com/), I found myself answering the same questions from friends in tech: What's different about gaming? What's the same? This post shares many of the similarities and differences I experienced compared to other tech jobs.

## Background

My background with gaming goes back to my early childhood, as does my background with programming. I still remember playing Atari games and my first experiences with programming on the VIC-20. My first programming book was about gaming but I was too ambitious at the time. So I set that aside and learned programming on and off through high school.

I went to college at The College of New Jersey for computer science. I heard an exciting story there: A classmate got an internship in the gaming industry! But when I asked more, I found that they mostly fetched coffee for "real" developers. Not long after that, I started to read awful stories like the [EA spouse](https://www.gameqol.org/ea-spouse). So I set that dream aside.

Fast forward over 20 years: Most of my network is in healthtech or broader tech, and many people are curious about the gaming industry. After spending about a year at Singularity 6 working on Palia, I realized I had misconceptions about gaming that others might share too. This post covers topics that often come up in discussion, and focuses on my personal experiences rather than a review of existing literature.

## Crunch mode and Chaos

The gaming industry has a reputation for crunch mode: If a team is behind schedule and headed towards a deadline, people often work longer hours to try and meet their target. In many companies it happens by mandate from leadership, in other cases it happens from pressure, and other crunch is opt-in, often by passionate developers.

My impression from S6 and the [PsychOdyssey documentary](https://www.doublefine.com/dftv/psychodyssey) is that:

1.  It's popular to say "we don't crunch": The older generation of devs seem to say "never again" to the horrible experiences they had
2.  Crunching is less extreme than it was 20 years ago (but newer devs didn't experience the old crunch)
3.  Companies are trying to do better for employees but progress is slow

Also note that crunch isn't fairly distributed. QA might be the last step and they're pushed to crunch. Or junior engineers may be more susceptible to leadership pressure. Or people in key, understaffed roles may come under more pressure.

The question I've pondered the most is: Why do gaming companies seem to crunch more than tech companies, and is it avoidable?

This is what I've observed:

- Some chaos is avoidable
- Some chaos is unavoidable
- Crunching is a response to chaos, but not the only possible response

Let me give a few examples of avoidable chaos first, picking real examples that should be familiar to folks in tech:

- Someone interpreted a Slack message or offhand comment from leadership as an urgent command
- The game would support PC and Nintendo Switch, but the design requirements of Switch were not taken into account during initial development
- The game was intentionally designed to not be latency-sensitive, but a latency-sensitive feature was later added

I picked examples of communication issues because they're so common. In many of these cases, there wasn't enough communication or there was miscommunication. Another common theme is a refusal to prioritize, which is often a combination of communication and leadership problems.

Let me also give a few examples of unavoidable chaos. I'll start with one that's familiar in the tech industry: The team is working and runs into a surprise that needs to be addressed. That could be something as simple as learning that the plan will take much longer than expected, requiring adjustments to the schedule or plan. That's not to say that all surprises are unavoidable, many are, it's to say that all plans are susceptible to unknown unknowns.

The unknowns can be much more fundamental. When you distribute new software, you're certain to face surprises at launch. An example from Palia was that we had many more players in Europe than expected so we added European servers much sooner than planned, which took significant effort away from other efforts.

Gaming also has more unknown unknowns than typical tech work. A common challenge is developing a game or level only to find that it isn't fun. The tech industry equivalent is building a new product or feature only to find minimal engagement. We'd call this finding "product-market fit" while gaming talks about "finding the fun." But there's a key difference: in tech we're often solving a specific user need with established processes to validate solutions. In gaming, the user need is less specific (entertainment) and it's harder to incrementally iterate to success.

This uncertainty has real consequences. If "finding the fun" takes much longer than expected and the game development has a fixed budget, it can eat into the time to make the game polished and clean.

## Takeaways

- There are similarities between creating a new game and creating new products, but it's a bit harder to find the fun compared to finding product-market fit
- Chaos can be lessened in well-run companies, but there's always going to be some of it

## Internal use aka Dogfooding

Dogfooding (using your own product internally) is an interesting parallel across products and companies:

At [Swype](https://en.wikipedia.org/wiki/Swype), developers could easily load builds on their personal phones. And because we were using our phones so much, we could quickly find out if a new build was an improvement or had some rare bug. Keep in mind that our developers mainly spoke English, so we didn't catch as many bugs in other languages.

At 98point6, our software enabled an online visit between a doctor and patient. That was much harder to dogfood so people dogfooded far less (perhaps 1% of the amount I saw at Swype). Exploratory dogfooding was more reserved for dedicated times when we had multiple people available and had an area of the product we wanted to focus on. Even still, we weren't doctors so our dogfooding of the clinical software wasn't as useful as our dogfooding of the patient software.

At Singularity 6, dogfooding (aka playtesting) needed to be coordinated because it was a multiplayer online game. So we had scheduled weekly playtests for the whole company. Sometimes those playtests had particular themes like a new event, and other times they were less structured. At times downloading the right build was a challenge but that was much easier once we used Steam for internal distribution.

## Takeaways and opinions

Dogfooding is a valuable process in building high-quality software, but it has limitations to work around.

Ease of dogfooding has an effect on bug discovery:

- For Palia, it was much easier to dogfood PC rather than Switch so Switch needed more deliberate effort rather than informal dogfooding
- For Swype, it was easier to dogfood the Android builds rather than iOS

Bugs that affect developers are found more easily, and others are not as easily found

- Developers are often provided with high-end computers for productivity, but that leads to less discovery of performance issues on low-end computers
- Most developers have reliable internet, so bugs with unreliable connections are less likely to be discovered informally
- In many products, developers may only test in English, leading to a slightly more buggy experience in other languages

And just to be extra clear, I'm not suggesting that dogfooding is an alternative to deliberate, focused testing. It's complementary to many forms of testing and a key part of a suite of quality-improvement efforts. Beyond that, it's also a helpful effort to keep everyone in the company aligned with the user's experience.

## Distribution

Selling a game on Steam is comparable to publishing an Android app on Google Play. Both platforms take a ~30% cut of revenue, have some requirements about what you can publish, and provide some software libraries or services. In both cases you need to optimize your app for the store to make it more discoverable and drive growth.

Publishing an app on the iOS App Store is a bit more burdensome due to the manual review process. That can be good for quality and consistency, but the review process can also be inconsistent. We had some frustrating times at 98point6 when a bug fix was blocked because the App Store reviewer was flagging something from a prior version. That introduced delays and sometimes degraded the user's experience.

In the gaming world, publishing for Nintendo Switch is somewhat similar. They have a certification process similar in spirit to the iOS process, but it was a little slower and more involved. Also the certification rules required an NDA to access, which added another challenge.

Multi-platform distribution is very similar between gaming and non-gaming software:

- You're juggling the competing requirements of each platform. Some platform-specific work is essential and valuable (like controller button mapping conventions or optimized graphics settings per platform). But when possible, it's better to proactively design features to be compliant with all target platforms from the start. That said, this takes a lot of upfront work and effort early in development.
- You're trying to design a release cadence to balance the constraints of all platforms and that often is determined by the slowest platform to release on
- Backend APIs provide flexibility in release timing, but in gaming the complex interactions and subtle dependencies between client and backend can make it harder to safely change the backend independently. This was less of an issue in my non-gaming tech experience.

## Takeaways

- Distribution heavily influences release process optimization including the cadence of releases
- Discussion of "what goes in the client vs backend" should really consider release cadence more than it does

Both mobile app distribution and gaming distribution have their strengths and neither is fundamentally superior. Here are some practices worth adopting from each:

**From mobile app distribution:**

- The requirements are usually clear, and most of them are publicly available
- The certification process is pretty fast

**From gaming distribution:**

- Steam APIs are a value-add and can be used on other platforms
- Steam provides good discoverability

**Improvements for all platforms:**

- I wish cert requirements were public for all platforms (Xbox is good about this)
- I wish all requirements also included the intention not just the rule

## Competition and Market Dynamics

One of the biggest differences between gaming and traditional tech products is the level of competition and how easily users can switch. In B2B/SaaS, there's often significant friction to switching providers. Healthcare has regulatory and insurance barriers. But in gaming? If someone doesn't like your game, they can easily find something better to do with their time. The switching cost is nearly zero, and if you have a free-to-play game, players are even quicker to drop it.

Gaming is tougher than I've described so far:

- You might plan your game launch only to be eclipsed by a hit game launching around the same time
- You're not just competing against new releases but also competing against decades of amazing games
- You're not just competing against the same type of game, but many types of games
- For some players, you're also competing against other forms of entertainment not just gaming

## Takeaways

- I have a lot more respect now for game developers that succeed financially
- B2B/SaaS companies tend to provide far more stability than I previously realized

## Operations

I found it interesting to compare and contrast the operations of 98point6 (24/7 healthcare) to Palia (24/7 gaming).

At 98point6 we emphasized reliability and scrutinized our service availability. We typically ranged from 99.3% to 99.9% availability, with the variance driven by larger outages like third-party services going down for extended periods. For reference, 99.9% availability means about 9 hours of downtime per year whether planned or unplanned. In some years, just one or two bad outages could cause 9 hours of downtime.

In online gaming it's common to have scheduled downtime. That's a time when the game client may be updated, servers may be updated/restarted, and so on. When things went really well, that would only take 1–2 hours per week (~99% uptime). Coming from healthcare initially I scoffed a bit at the downtime but our tech stack required us to have downtime for coordinated updates across all clients and servers.

After seeing both in practice, I feel that predictability is often more important to users than availability. For example, in Palia our players expected downtime on Tuesday mornings and planned accordingly. It didn't bother most people. What bothered players was unexpected downtime and unexpected instability. Like when the 2 hour downtime turned into 6 hours and they couldn't play when they expected to.

## User feedback

The type and scale of user feedback varied dramatically across employers:

**At Swype and Nuance**

- A tiny number of bloggers and news sites would provide detailed feedback
- A small number of users commented on our forums, but overly biased towards English
- A large number of users gave app store reviews, but the reviews were rarely actionable

**At 98point6**

- Some patients provided feedback on app stores, but like Swype it was rarely actionable
- A smaller number of patients responded to our surveys with much more actionable feedback
- One time someone thanked me in person because our doctors might've saved their life
- Our doctors (also a part of the business) would provide feedback in person or in Slack

**At Singularity 6**

- When we first opened access in Aug 2023, we immediately had more hours of recorded gameplay on Twitch than we could ever hope to review. If we'd been able to review it all maybe we could've had repro steps for thousands of bugs but it was just impossible (note: someone please make a startup to create/update bug reports from Twitch)
- We were consistently drowning in feedback on Discord and Reddit. Discord was biased to be overly positive and Reddit was biased to be overly negative. Both were biased towards English feedback.
- Once we launched on Steam, we were drowning in feedback from Steam reviews. Steam reviews also enabled more feedback outside of English.
- There was enough culture around developer interactions that we had formal training for it.
- Many players responded to surveys as well.

I'm sometimes perplexed by the difference in feedback between 98point6 and Singularity 6. At 98point6 we saved our patients hours of frustration with the medical system, hundreds of dollars, and sometimes even saved their lives, yet the feedback was sparse. At Singularity 6 we provided entertainment and we were drowning in feedback. At times I despaired: Are people more passionate about entertainment than life itself?

I came to think of it differently over the years, seeing it as:

- With a larger user base, you have more passionate people and your time with feedback is sometimes taken over by the most passionate users
- Passion is somewhat proportional to the time investment. Someone might play Palia for 100 hours per year in contrast to using 98point6 for 30 minutes per year.
- Feedback is relative to expectations. With healthcare, you're expected to save lives and it's not a pleasant surprise. It's more of a surprise if you're expecting to wait and you don't need to. Sometimes those expectations are also unrealistic, like when patients expected antibiotics for viral infections.

## Brief additional observations

A few other observations worth mentioning:

- Developing in Unreal felt a lot like developing in Android Studio in terms of many aspects of the IDEs. I just wish that Blueprints (Unreal's visual scripting system) had a text version to diff in version control like Android layout files. It was frustrating to ask for review of a bunch of screenshots, especially for large Blueprints.
- Perforce (a version control system designed for large binary files) was frustrating in many ways, but we couldn't "just use git" due to lots of large binary files. That was familiar to my experiences in versioning ML models.
- The onboarding experience in gaming is often called FTUE (first-time user experience). There's a significant amount of effort put into that because games often have complex rules and mechanics to explain. Players aren't going to read manuals much so you need to incrementally teach them the rules in ways that are fun.
- There are some terminology differences in gaming, like studio = company, producer is something like a project manager, game designer is something like a product manager
- Gaming is often about delivering novelty and that may tend to push development into novel technology (which is often less reliable).
- A/B testing and user studies are most helpful AFTER you've found the fun or found product-market fit, less so before
- Working alongside artists, musicians, writers, and people with all sorts of skills is a lot of fun!

## See also

- [The software architecture of Palia](https://www.singularity6.com/news/software-architecture-of-palia)
- [Double Fine's PsychOdyssey documentary series](https://www.doublefine.com/dftv/psychodyssey)
- [Palia](https://palia.com/)
