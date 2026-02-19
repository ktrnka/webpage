
---
layout: post
title: ParseTreeApplication on Github
date: 2013-02-19
---
It's tougher to blog or publish articles in a professional research and development role; most of the work isn't public. If I'm not careful, side projects get the "leftover" time in my schedule.

ParseTreeApplication
====================

Periodically people send me thanks or feature requests for ParseTreeApplication, a tool I wrote years ago to draw and compare parse trees.  Like so:

[![high attachment - Keith is using the telescope to see the man.](http://kwtrnka.wordpress.com/wp-content/uploads/2013/02/parse-high.png)](http://kwtrnka.wordpress.com/wp-content/uploads/2013/02/parse-high.png)[![Low attachment - Keith is seeing a man, who has a telescope.](http://kwtrnka.wordpress.com/wp-content/uploads/2013/02/parse-low.png)](http://kwtrnka.wordpress.com/wp-content/uploads/2013/02/parse-low.png)

I rarely get the time to implement a feature request, but I've taken a step to help:  [ParseTreeApplication is now on Github](https://github.com/ktrnka/ParseTreeApplication)!  You can download the source and build it in [Eclipse](http://www.eclipse.org "Eclipse (software)") without much trouble.  Also, I've added some examples of how you can use the ParseTreePanel in an external Java application/applet under [src/edu/udel/ktrnka/pta/examples](https://github.com/ktrnka/ParseTreeApplication/tree/master/src/edu/udel/trnka/pta/examples).
The executable jar is now in the github tree under [releases](https://github.com/ktrnka/ParseTreeApplication/tree/master/releases).  There aren't any real differences from the previous release but the jar is a bit smaller from compression.

Shifting to Eclipse and Github
==============================

I made this small application in 2003-2004 or thereabouts on a [Sun Ultra](http://en.wikipedia.org/wiki/Sun_Ultra_series), possibly the 30.  Oh and it was in a campus building with roaches that was shortly demolished and eventually replaced with a parking deck.  What with the low-power machine and all, I didn't use Eclipse.  I used a text editor and a makefile.  I didn't use packages cause it added work in that setup.  I unpacked the library jars and repackaged them into my jar.  It's embarrassing by any sort of professional standards.
Migrating to a semi-modern setup was easier than I expected.  The only tricky part was getting Eclipse to include the help file in the jar (tell it to include the resource folder as source).
For source control, I'd previously used.... Dropbox.  I can't even keep a straight face while saying it.  But it followed me from computer to computer and kept 30-day revisions which was enough.  Switching to github wasn't too painful.  It would've been completely painless but my config is a messed up; I have Github for Windows setup correctly and Git Bash setup for another github account.
