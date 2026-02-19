
---
layout: post
title: faking dynamic information display
date: 2010-10-28
---
Do you ever need to display a dynamically updating value on the web?  (And not have a lot of time?)  If we're talking about a basic daemon or long-running script, there's a quick way to address the problem:  periodically write the output to an html file.  The problem is that the user has to hit refresh.  But wait!  You can add a meta tag with the refresh option and have the page reload every second (or whatever interval you choose).
I used this cheap solution to have a "dynamic" display of the electric vehicles connected to our server in the [V2G project](http://www.udel.edu/V2G/).  I had a Java daemon that talked to the cars and to the regional transmission organization (in our case, PJM) and it did mostly what it was supposed to do, but I needed to show this to non-computer scientists.  In the end, it took maybe 30 minutes of my time and was probably the most appreciated aspect of my system.
The only thing to note is that you need to display when the page is outdated (sometimes the meta-refresh might break, or the daemon might die).  You can accomplish this by writing the unix time (seconds since epoch) and writing a little Javascript to compute the offset.
(I'd include code, but that project has restructured since I was last involved)
