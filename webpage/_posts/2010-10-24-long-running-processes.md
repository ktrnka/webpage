
---
layout: post
title: long-running processes
date: 2010-10-24
---
Some of my simulations take a while to run, so I have a couple of servers that I ssh into and run them on.  But there are a host of little things I didn't know about at first:

* Running something in the background (*&*) still has a problem - the new process is tied to the shell's process.  So if you log out or your computer goes to sleep, the ssh connection is broken, which kills the shell and in turn the stuff you were running. However, you can address this problem with the *nohup* command, like so: "nohup perl blah.pl &".
* Sometimes I'm running a quick script but I don't want to open a new terminal window, and I forget to put & in there.  Don't fret! You can suspend the current process with CTRL-Z and then use the *bg* command to start the suspended process again, but in the background.  There's also a *fg* command for the foreground.
* It doesn't really hurt you to run in the background.  If you redirect the stdout/stderr (syntax for stderr is shell-dependent iirc), you can watch it stream by with *tail -f* on the file.  It'll show the file as it's created.  You stop it with CTRL-C.
* It's pretty easy to start stuff up and run it for an indefinite amount of time, but that causes some a human problem - if it takes 5-10 days to run, will you even remember in 10 days?
  + The option I'm using now is to have my scripts update an RSS feed when they're done.  Unfortunately, the Perl modules I found for RSS were a pain to install and the output wasn't readable (at least in Google Reader).  I ended up just writing a little Perl module to format my results and add a post to a blog of results.  The XML format is easy for basic RSS.  You can tell your program which part of the file to insert into using a comment.
  + In the past, I've wanted to use other options - you can write code to send a text message or make a phone call.  It's flashy, but really you don't need to be bothered when you're busy.  If you're already using an RSS reader for other things, you'll naturally see results when you have time to work.

That's it for now!  Though there are some open problems I haven't found good/easy solutions to:

* notification if your program hits the memory wall and starts paging
* notification if it's a shared system and someone else runs something demanding
* notification of crashes (this can't be done from within the program)
* more fluid updates - if testing on a particular corpus is taking a while, I'd like a status update once per day.  This could be addressed by writing an RSS-update function that exits early if it's been called in the last 24 hours.
