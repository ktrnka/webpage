---
layout: post
title: Software engineering estimates and League of Legends
date: 2015-03-27
---
*This might only make sense to players of [MOBA](http://en.wikipedia.org/wiki/Multiplayer_online_battle_arena)-style games.*
There's been renewed debate lately over time estimates in software engineering such as the [no-estimates debate](https://medium.com/backchannel/estimates-we-don-t-need-no-stinking-estimates-dcbddccbd3d4). It's incredibly hard to estimate how long a new feature or bug fix will take.
And it baffles people when you don't know how long it'll take. I prefer to say "It'll take 3-4 hours if things go according to plan, but could take 1-2 weeks depending on how things break." I've had to explain over and over, which probably means my explanation is not good enough. This time I'll try an analogy with [League of Legends](https://leagueoflegends.com).

"I need a ward at their red buff asap"
======================================

In some ways, making a software change is like trying to get a deep ward in the enemy jungle. There are many possible outcomes:

* (Best case) You run there, drop the ward, and run out. It cost you maybe a minute plus 100g.
* You run by a stealth ward in the process. Your ward is cleared out when you leave and you need to do it all over again. And you lost time and gold that you needed for other tasks.
* You get killed by the enemy jungler. So it costs you extra time and feeds gold. It also increases risk for the rest of the team.
* You get caught by enemy jungler and try to run. You barely make it to a teammate and then 2 more enemies pop out and you both die. You lose even more time, transfer even more gold, and give up more map pressure.
* And plenty of worse cases...

In all the bad cases you need to try again and there's chance of the second attempt failing as well.
So you can't say exactly how much it'll cost you to ward. The cost of the best case is very clear. But there isn't a clear bound on just how badly it could go wrong.
Warding isn't always this dangerous and similarly software isn't always so unreliable.

Reducing risk in League of Legends
==================================

You reduce risk in League by gathering information. If you can see all five enemies on the map, you make a good guess about whether it's safe to ward or not. If you watch the people moving in and out of lane, you guess where the stealth wards are. And so on. Your understanding makes it more predictable.
In League there's are maybe a few dozen ways your task can go wrong but you can eliminate many of them by gathering information and reasoning about what's possible.

Reducing risk in software engineering
=====================================

Unlike League, you generally have vision (access) to all the source code. In theory you could have a perfect understanding of how the software works. But that's rarely the case.
Usually I've worked at an intersection of complex systems. They may span hundreds of thousands of lines of code, span multiple programming languages, been written by 50-100 people many of whom are gone, etc. Although you have visibility into the code, you may not have *complete understanding*of it. For instance, you may assume an index variable starts from 0 but it's starting from 1. Or you may assume that a function has no side-effects only to find that it sometimes does.
The better you understand the system, the tighter your estimates can be. It's unlikely that you'll ever have 100% understanding of the full stack so improving estimates is a lifelong process.
Unlike league there are probably hundreds of ways a seemingly simple task can go wrong because the tasks themselves are more complex.

Back to software estimates
==========================

Rough estimates are often necessary. But it's problematic when an estimate is turned into a hard client commitment. It's better when both sides of the table understand that estimates are really a range and that there are almost countless ways that software can break and take more time.
