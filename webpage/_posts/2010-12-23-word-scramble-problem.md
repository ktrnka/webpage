---
layout: post
title: word scramble problem
date: 2010-12-23
---

*Sorry for the delay in posting something --- I'll be more active again once I get over this cold.  Here's something from my Drafts folder in the meantime.*

The word scramble problem seems to crop up every few years or something.  [Brain Oddities](http://www.ritholtz.com/blog/2010/12/brain-oddities-irrelevant-spelling/) has the recent version. We took a look at the problem in our NLP class in 2003, and I wrote a program that worked for basically any word it's seen in training.  It doesn't even use a complicated model or anything.  And the number of words encountered in training is much less than the vocabulary of a normal adult.

Some comments on the newest take:

* The text is a little offensive... I don't think it has much of anything to do with general intelligence.  I wouldn't say someone's smart for being able to read it, or unintelligent for not being able to read it.
  + I think instead, I'll consider the title to refer to *sarmt* people, which I'll interpret to mean English speakers.
* The article says that the arrangement of internals letters is irrelevant to comprehension.  In some sense, I understand.  But I'd say that the ease/speed of reading can have effects in how fully you interpret the message.
* The comments have some excellent points
  + Longer words are more difficult (slower) to read in this scheme.
  + Instead of a random scramble, just reverse the interior letters.  It's much harder to read than random scrambling.
  + Many of the observations can be modeled using a basic ngram model along with a word list.
  + rastafasta links an excellent [youtube response](http://www.youtube.com/watch?v=TNStNUizxhE).  It gives a more realistic assessment of things.
* In all likelihood, it might be best to suggest that a [noisy channel model](http://en.wikipedia.org/wiki/Noisy_channel_model) of typing/etc is what's going on.  Here are some examples of related things:
  + email/paper typos
    Even if something is misspelled, you can usually figure it out right?  Based on the context in the sentence, the type of misspelling, and previous words in the same document.
  + printing errors
    In mass market paperback books, you tend to get pages with parts of the ink missing.  But you can still read it based on the parts of the words that are present and the context.
  + handwriting
    Here's a fun experiment:  Find someone you know with poor handwriting.  Ask them to write about something technical.  Have someone that know the technical terms read the writing.  Have someone that doesn't know the terms (or doesn't use them often) try to read it.  I tried this with my advisor's handwriting and used my sister to read it, comparing to what I read.  The results were hilarious.
