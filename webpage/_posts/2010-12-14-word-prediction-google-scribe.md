---
layout: post
title: word prediction + ??? = google scribe
date: 2010-12-14
---

There's a South Park episode that spawned the quote "Simpsons did it."  In research, I'm starting to feel like we could say "Google did it."  I'm talking about Google Scribe, which brings word prediction (my research area) to the masses.

Google Scribe is a Google Labs project that adds predictive text entry to certain things (I think originally it was for Google Documents).  I've been trying out the Google Scribe extension for Chrome the past few days, which enables Scribe on any web text input.

user perspective
----------------

From the perspective of using Google Scribe, it's awkward and sometimes frustrating.  In editing my previous post, it would try and add a prediction after a section title and if I didn't click fast enough elsewhere Scribe would fill in the word.  Then I'd delete the prediction and try again.  I had similar experiences in editing text within a document, leaving half-completed words and extra words all over until I disabled it.

Scribe is much better in writing a document for the first time.  However, there were a few bad things that really undermine scribe:

* Scribe offers 10 predictions/completions most of the time.  While typing that means that a big part of your screen is changing every letter you type, making it really difficult to focus on typing.  Unfortunately, you can't control this in the options.
* The prediction list is formatted strangely --- the part of the word that you've typed so far is in a normal font and the completion is in boldface.  This means that the letters don't really align vertically or horizontally;  it's very difficult to tell the difference between similar words (especially those of similar length).
* While typing, there is a noticeable delay in generating the prediction list.  Honestly, I sympathize with Google here.  It could be the case that it's communicating with Google servers, because language models can take up a lot of space.
  + If they're communicating with servers for Scribe, I'd say they really need to compress a stripped-down language model into the extension.  There's some work out of Google on using 9-grams with pruning to fit in normal space requirements.  And tries are always fun.

research perspective
--------------------

The predictions offered by Scribe are good.  In the future, I'll try and measure keystroke savings with Scribe compared to some other options, maybe WordQ.  Though I'll probably have to compute it manually on a handful of texts.  I wonder which texts I should use?

Scribe offers multi-word prediction, which is very interesting (and can involve some complicated research).

suggestions
-----------

Fast typists need fewer distractions.  When using Scribe, I'd suggest two controls on the number of predictions. There should be an adjustable maximum list size.  For myself, I'd start off with something like three predictions max.

One step further would be to optimize Scribe for a single prediction --- probably this would be an ideal setting for fast typists.  The prediction/completion should be shown in-line without the drop-down menu. Unfortunately, you can't really use enter or tab to select the prediction.  Tab is already used for cycling between form fields.  And enter is already used to submit forms.  Maybe something like space bar?  But you'd need a delay in showing the prediction the first time, to allow for double-spaces after sentences.

The second suggestion is to use a probability threshold to control the accuracy of the predictions shown.  For example, if only the top two predictions are "good", I don't want to see the rest of them.

Also, the number keys are really awkward.  You can't really rest your hand on them while typing, so you need to move your hand to find it (which means you need to look down to the keyboard or risk a mistake).

Also, Scribe is much less useful for text field (single-line).  I'd suggest an option to disable Scribe for text fields, but leave it enabled for text areas (multi-line fields).

conclusions
-----------

Scribe might be useful for a slow typist, but it's far too slow and distracting for a fast typist.  That said, Scribe is a beta product;  in the future it might be more usable for fast typing.  Also, typists with RSI may benefit from reduced hand wear (at the expense of slower typing).

Note that these are real differences from a very slow typist, such as the expectation for augmentative and alternative communication.
