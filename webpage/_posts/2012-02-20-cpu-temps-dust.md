---
layout: post
title: cpu temps + dust = ???
date: 2012-02-20
---

Recently I built a new system for myself and as usual I bought a tube of thermal paste.  Now what do I do with it?  Typically I let it sit in the closet for another 3 years, then wonder whether it loses its magic, then order a new tube anyway.

But this time is different!  I decided I'd take my old system, measure CPU temp under idle/load, then clean it and check CPU temp again.  Then the next time I think about how much I hate dust, I'll have some numbers.

Setup/Background
----------------

Relevant hardware (thanks to the magic of Newegg's history):

* AMD Athlon 64 X2 5400+ Brisbane 2.8GHz (with the packaged cooler, but with Arctic Silver 5 instead of the prepackaged thermal pad)
* MSI MBOX K9N6SGM-V
  (yeah I was lazy and used a barebones)
* Age/usage/environment:  3.5 yr, of which 3 years were heavy usage in an ordinary carpeted area.

Testing:

* Monitored CPU core temperatures with [CPUID HWMonitor](https://www.cpuid.com/softwares/hwmonitor.html)
* Idle:  Booted the computer and let it sit while watching CPU temp.  Recorded when it stabilized.
* Load:  Ran [Prime95](https://www.mersenne.org/freesoft/#newusers) for 30-60 min, then watched for a while and recorded stable temp.

Before
------

Here's a shot of what we're working with:

![Dusty case interior]({{ "/assets/img/posts/wp/mobo-ground-zero.jpg" | relative_url }})

Our main targets are the case fan and the CPU heatsink/fan (HSF).  Here are the two sides of the case fan:

![Dirty case fan (interior face)]({{ "/assets/img/posts/wp/case-fan-dirty-int.jpg" | relative_url }})![Dirty case fan (exterior face)]({{ "/assets/img/posts/wp/case-fan-dirty-ext.jpg" | relative_url }})

The really yucky side is the exterior-facing side.  That dust was sandwiched between the fan and the grill on the back of the case.

Now for the heatsink/fan.  I'll just show the one photo of them apart:

![Dirty heatsink/fan, separated]({{ "/assets/img/posts/wp/hsf-dirty.jpg" | relative_url }})

Take a look at the top view in the first picture.  I bet you didn't expect to find that much fur between the fan and HSF!  I sure didn't!

The Cleaning
------------

Skip this section unless you really want to see how I cleaned it.  On the off-chance that you want to do this, here are the "tools" I used for cleaning.  I don't suggest doing this if you're not comfortable assembling the computer.

* rubbing alcohol
  Windex would probably work fine too but I've never tried that for removing thermal grease.
* cotton balls
  You might be able to get away with paper towels.  Sometimes I did that for really big surfaces.
* q-tips
* a bowl with some soapy water

To reapply the thermal paste, I also used a razor blade that came with a scraper.  I wish I still had some flexible double-sided razors, but the inflexible single-sided was good enough.

### Case fan

Nothing too special here.  I started with cotton balls and rubbing alcohol and did two passes to get most of the dust off.  Then I switched to q-tips to get into the nooks and crannies.

### CPU Heatsink/Fan

I separated the fan from the heatsink as shown above.  Then I disassembled the heatsink - separated the harness from the metal and took the bracket out.

For the heatsink itself, I cleaned the old thermal paste off the bottom with rubbing alcohol and cotton balls.  It took several passes to get all the paste/residue off.  I made sure that I got it down to the point where I could run my finger on it with no visible residue.  After all, I wouldn't want the old paste interfering with the new.

Then I had to deal with the dust.  For this, I filled a bowl with hot water and a little dish detergent.  Not too much or else it might leave residue.  Just enough to get the dust off easier.  I sloshed the heatsink around for a little while then checked - it cleaned up quickly.  Then I had to let it dry overnight.

I cleaned the other plastic and metal parts the same way.

The CPU fan was much like the case fan, so I handled it the same - one or two passes with cotton balls and rubbing alcohol, then a pass with q-tips and rubbing alcohol.

### CPU

Like with the heatsink, I used cotton balls and rubbing alcohol to remove the thermal grease on top.  But I was much more careful with the CPU - I don't want thermal grease getting on any pins or connectors.  I used q-tips with just a little rubbing alcohol on the edge of the CPU and was careful not to let any of it drip.

### Other

I also cleaned many of the capacitors and such in the CPU area.  I doubt it has a major effect, but for the CPU heat to dissipate, I want the surrounding air to be dust-free and cool.

Also, I really don't want to accidentally sneeze while reseating the HSF and get some dust sandwiched in the worst possible place.

After
-----

I can write all I want, but the pictures tell the story.  HSF first:

![Clean heatsink top]({{ "/assets/img/posts/wp/hs-clean-top.jpg" | relative_url }})![Clean CPU fan bottom]({{ "/assets/img/posts/wp/cpu-fan-clean-bottom.jpg" | relative_url }})

Case fan:![Clean case fan (exterior face)]({{ "/assets/img/posts/wp/case-fan-clean-ext.jpg" | relative_url }})

Mobo (it was tough to get in there with my bear-sized hands so it's not as clean as I'd like):

![Clean motherboard and case]({{ "/assets/img/posts/wp/mobo-clean.jpg" | relative_url }})

The replacement thermal grease was also Arctic Silver 5, but it was a newer tube.

CPU Temperatures
----------------

The temps are recorded as Core0/Core1.  If it was fluctuating in a range when stable, I recorded the range.

Dusty:

* Idle:  60/58 C
* Load:  94-96/97-100 C

Clean:

* Idle:  50-53/48-51 C
* Load:  79/74 C
  *I'm guessing that thread affinities caused the core0/1 temps to be reversed here.*

So there you have it.  Dusting reduced idle temps by 7-10 C and reduced load temps by 18-21 C.

The lower temperatures won't get me much unless I decide to overclock.  On the other hand, if I had let it get much dustier, higher load temps would probably trigger a shutdown.

Discussion
----------

In retrospect, I measured sloppily.  I should've measured min temps at idle and max temps at load.  It would've also been good to measure how long it takes to return to idle temps when I stop Prime95.

Ideally I would've liked to clean different components independently and measure the effect on CPU temps.  I could've cleaned the case fan and case area first to see what that does.  Ideally I'd like to see the difference between just cleaning HSF and reapplying the thermal grease to see if there's any benefit to replacing 3.5 year old grease.  But that's impractical.  In the end I was lazy and just did one full pass of cleaning.

I didn't give the replacement thermal grease any time to cure.  Maybe the temps would drop another couple degrees if I allowed for curing time.

I've never used compressed air for dusting.  I know many people do, but it only seems like it's pushing dust around in the case.

See also
--------

* AnandTech's CPUs and Overclocking Forums (now dead)
  It's been a long time since I've been interested in overclocking but lurking here is a decent starting point.
