---
layout: post
title: parse trees + visualization = ???
date: 2011-01-14
---
There have been many points in my research career when I realized that I would understand the problem better if someone had visualized my data somehow.  Usually, that means I write some simple visualization that's close enough to quickly answer my questions about the data.  For example, I've [compared stemmers/lemmatizers in a simple way](/blog/2010/11/comparing-stemmers/ "comparing stemmers") to help understand the differences.  It isn't the prettiest visualization, but it's enough to quickly learn something new.
Back when I was working in an older lab (maybe 2003-2004), my labmate Rashida Davis had a problem with a parser.  For certain sentences, it'd return as many as 50 different parses.  Part of the problem was that the grammar was developed a long time ago (and had some unfortunate ambiguities).  Another part of the problem was that the grammar had many feature structures in addition to plain constituent labels.  Being the generous guy that I am, I decided to write a Java program to draw the parse trees and help to compare them.  (Unfortunately, I had no sense of the complexity of the parse trees when I started out)

parse tree application
----------------------

This led to a publicly available program, [parse tree application](http://www.cis.udel.edu/~trnka/pta/), which does the work of drawing and comparing various kinds of parse trees.  Part of the motivation was to help compare trees for a friend, but another part of the motivation was to make it easier to have nicely drawn parse trees in publications.  So the output can be saved as EPS, PNG, or JPG.  I had to take some extra effort to get EPS output, but I wanted vector graphics suitable for LaTeX.  Also, if you're on a Mac, you can print and save to PDF.  I seem to remember being able to edit the EPS output nicely in Inkscape.
![example parse tree](/assets/img/posts/wp/demo_example1.png)
By default, the constituents are drawn as close to their children as possible.  In rare occasions, this can lead to rendering ugliness, but you can select a different rendering preference from the right-click menu if you'd like. Also note that the application has no understanding of what different constituents are; you can use whatever label/tag set you want.
That said, the original goal was to compare parse trees.  I've shown the classic prepositional phrase attachment problem below with the compared rendering.  To produce this, you first have to draw the trees that you want. Then minimize any trees you aren't interested in.  Then select "Compare non-minimized trees" from the "Compare" menu.
![The telescope was used by Keith to see the man.](/assets/img/posts/wp/comparison_example1.png)
![Keith saw the man who was holding the telescope](/assets/img/posts/wp/comparison_example2.png)
I thought about the visualization for a while.  I could highlight the differences with color, but that was hard on the eyes at times.  Or I could bold the text in the different parts, but that changes the shape of the image somewhat.  I decided to grey the similar parts so that it's easy enough to ignore if you want.  Also, this works regardless of color blindness and doesn't change the shape of the image.
The application also renders a few other options:  Shallow parses and trees with feature structures.  Here's an example shallow parse:
![shallow parse](/assets/img/posts/wp/example_shallow.png)I don't have a lot of good examples of trees with features, but they can include things like number/gender agreement, verb tense, and other lexical features that are propagated around the parse.  Here's one of the monster parse trees that came out of ICICLE.  You'll have to click on it to see any real detail.
![monster parse tree](/assets/img/posts/wp/example_huge.png)
In any case, I can't imagine trying to draw this manually for a paper, even less when you're trying to see where the ambiguity lies in a set of 50-100 of these.  (Though admittedly, I don't know if I can imagine wanting to publish such a huge tree in a paper)

input format
------------

The input can either be XML or Lisp.  I prefer XML, where the elements (tags) are the constituent labels and the features are attributes on each element.  Shallow parses are detected automatically (if multiple words are children of a "leaf" constituent).

Spaces are significant here.  Sometimes you might want a constituent label that isn't a valid XML element name.  In this case, use some extra syntax:

```
<constituent label="+S">+s</constituent>
```

Here's an example shallow parse with features:

```
<S><NP AGR="3s" ROLE="SUBJ">The dog</NP> <VP><V AGR="3s">ate</V> <NP AGR="3s" ROLE="OBJ">the cat</NP></VP></S>
```

I'm not a fan of Lisp, but if you have a tree as a Lisp s-expression, here's what it might look like:

```
(S (NP (PRP I ) ) (VP (V wore ) (NP (DT a ) (NN hat ) ) (PP (P with ) (NP (DT a ) (NN ribbon ) ) ) ) . )
```

The application can also load XML files that are sets of parse trees, or even sets of sets of parse trees.  Though you'll want to download the application and look at the help document for that.
The design as an application maybe isn't the best:  You download and unpack a zip file and run the one jar.  I wish I had packed everything up as a single jar, but I wasn't sure about the licensing issues involved with doing that for the eps include I used.

conclusions
-----------

The [parse tree application](http://www.cis.udel.edu/~trnka/pta/) is a step in the right direction for more quickly visualizing output/etc in NLP.  But it's still very involved to quickly determine the differences in a large set of parse trees.
