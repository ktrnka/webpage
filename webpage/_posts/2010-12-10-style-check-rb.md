
---
layout: post
title: style-check.rb
date: 2010-12-10
---
I'm very interested in tools to help write papers, specifically automatic proofreaders.  I've noted a couple before, namely [After the Deadline](/blog/2010/10/after-the-deadline/ "After the Deadline") and [Grammarian Pro X](/blog/2010/11/grammarian-pro-x/ "Grammarian Pro X").  I recently came across the tool [style-check.rb](http://www.cs.umd.edu/~nspring/software/style-check-readme.html), which helps proofread LaTeX documents.  It doesn't really have a name per se, just the filename style-check.rb.
This isn't the same type of tool as its production counterparts;  it's simply a Ruby script written by [Neil Spring](http://www.cs.umd.edu/~nspring/) at the University of Maryland, who seems to have struggled with some similar issues in proofreading latex documents.
The core of the checker is a set of various regular expressions.  If any regex is found in the source document, it spits out an error message like a compiler.  The format of the errors is such that editors like emacs and other programs can jump to the error in the source document.  (His webpage shows it in an emacs context).  Here is some of the basic output on the dirty testing file:

![style-check.rb on test-dirty.tex](/assets/img/posts/wp/screen-shot-2010-12-10-at-4-00-18-pm.png)

The test-dirty example shows the basic error messages.  If you run with the -v flag, it'll also explain each error. Below is a snippet from that.

![style-check.rb on test-dirty.tex with verbose output](/assets/img/posts/wp/screen-shot-2010-12-10-at-4-08-11-pm.png)

I decided to run it on the conclusions from my thesis, and it produced a long list of errors.  Some of the issues are things that don't bother me (using an em-dash "---" with spaces on either side).  Some of the issues are debatable, like for instance it doesn't like the phase "in general" or the word "utilization".  It also complains about many of my \refs:  "Table, Figure, and Section refs should have a non-breaking space".  I'm guessing it means that you don't want to allow LaTeX to end a line between "Table" and the table number (so use a dash for nonbreaking space).  That's a good trick to know.
I get the impression that some of the errors are very specific to a certain style of author.  I'll probably go edit the rule files (they're just big lists of human-readable rules) and remove the ones that don't really bother me.
It seems like the author added rules anytime he had to make changes more than once.  Based on the readme, it seems that he also made rules to help bring co-authored papers into his style.
For general usage, I'd recommend this to anyone with mild tech savvy that uses LaTeX for publishing.  The best use of the program will result from removing rules that give too many false-positives and adding rules specific to 1) your field 2) your writing style 3) your co-authors' writing styles.  It's very applicable to people who use emacs.  I can manage to get it to run in TextMate too, but I haven't figured out how to make it parse the output so that I can double-click to see errors.
(Side note:  copying output into WordPress is a pain;  I don't see a font size tool anywhere and copy/paste is messy with line endings.)
