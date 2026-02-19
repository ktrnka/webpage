---
layout: post
title: latexdiff + version control = ???
date: 2010-11-28
---
In the past, I've used [latexdiff](http://www.ctan.org/tex-archive/support/latexdiff/) to show the changes between different versions of a paper.  But it's a pain to keep the old version around.  Or if I'm using a version control system I have to remember the right version number (and remember the commands to retrieve old versions and rename them).  For some reason, this past week I came across the [latexdiff manual](http://tug.ctan.org/tex-archive/support/latexdiff/latexdiff-man.pdf), which is just a nicely formatted man page.  But I noticed that latexdiff comes with other scripts... notably *latexdiff-vc*.  What does this script do?
latexdiff-vc combines latexdiff with a version control interface, and supports CVS, SVN, or RCS.  If you use something else like Git or Mercurial, don't fret!  It's just a Perl script, so it should be pretty easy to port.
Here are a few examples from the man page:

```
latexdiff-vc --svn -r file.tex
```

This compares file.tex against the most recent version in the SVN repository.  The *--svn* option might not be necessary though:  the documentation says it tries to guess the version control system. (I bet it checks to see if *.svn* exists)

```
latexdiff-vc --svn -r 29 file.tex
```

Same deal, but you can specify the version number to check.

It also has the --pdf option to run the output through pdflatex for you, which is nice.  Also, if you want to specify which version control system you're using but want to save keystrokes, there are wrapper scripts for each one:  latexdiff-svn, latexdiff-cvs, and latexdiff-rcs.

addendum
--------

This really helps simplify version tracking on single-file papers, but I haven't tested whether it works with the base latexdiff option *--flatten*, which follows *input* and *include* commands for nested documents.  Flatten doesn't do recursion anyway, and the nesting in my thesis and proposal goes a few levels (usually thesis.tex -> chaptername.tex -> chart/figure.tex).
The second note is that it needs to be easier to use version control with latex - easier to commit and easier to browse versions.  There are a number of tools out there for browsing svn, but ideally you need to tie commits into your editor.  I know Eclipse has good version control support (my software analysis buddies use that).  From talking to my labmate Dan Blanchard, it's pretty easy to setup commits in TextMate with macros or some such - I need to figure that out for TeXShop.
Finally, I vaguely recall that you could specify a date for Subversion and it'd retrieve the most recent version at that date/time.  It looks like the syntax is the same option as normal revision numbers, but requires special date formatting.  That'd be ideal - you could look up the date of your initial submission from email, then do latexdiff compared to that date.

### See also

* <http://www.jwe.cc/2012/02/workflow-with-subversion-and-latex/>
