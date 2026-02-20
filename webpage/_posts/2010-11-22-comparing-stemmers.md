---
layout: post
title: comparing stemmers
date: 2010-11-22
---

Natural language understanding typically involves a huge chain of processing and errors can happen anywhere, then get propagated to your system which operates at the top of the stack.  I'll give an example from my thesis work - adapting a language model to the style of text:

* style adaptation
  + depends on:  our Markov model part of speech tagger
    - requires:  part of speech tagged corpora
      * uses:  Stanford maxent tagger
      * uses:  sentence tokenization
      * uses:  word tokenization
    - depends on:  tagging of unknown words
      * depends on:  morphology
      * depends on:  available context

That's probably a simplification, but you can see that if we screw up sentence tokenization, the error will propagate, especially because taggers are designed for complete sentences (due to training on Penn Treebank). Then because the Stanford tagger messed up our training data, *our* tagger in the language model will mess up, which can affect both normal predictions and the ability to adapt to style.  Though I feel that errors are rare, this highlights the importance of putting effort into things like tokenization, corpus cleanup, and text normalization.

Stemming
--------

One of the tools that gets used in NLP (especially NLU) is [stemming](http://en.wikipedia.org/wiki/Stemming) - removing the suffix from words.  For example, reducing *combinations* to *combin*-.  Depending on the software you're using, it may give the root form *combine* or just the pure substring *combin*.

### Porter's stemmer

The most common stemmer I've seen is Porter's stemmer, which is a rule-based stemmer for English (though it has been adapted to other languages).  I believe the implementation I use is the Perl module [Lingua::Stem::En](http://search.cpan.org/~snowhare/Lingua-Stem-0.84/lib/Lingua/Stem/En.pm) along with a wrapper module for ease-of-use.  Porter's stemmer has been criticized many times over the years, because it sometimes comes up with crazy stemmings.  That said, Porter's stemmer can be useful for some tasks.  For example, I used it in computing document similarity scores - when the documents being compared are very short, stemming can increase the overlap that you see.

### PC-KIMMO

Alternatively, people sometimes use a more principled morphological analysis, PC-KIMMO.  PC-KIMMO is a C version of the KIMMO software, which is a two-level morphological analysis.  It includes some basic part of speech information in the analysis, so you might be able to come up with something like *test + PLURAL = tests*.  The main drawback of PC-KIMMO is that it's a pain to use in Perl - you can write a wrapper to call the C program, but it's slow to call the program all the time.

One of the really interesting aspects of PC-KIMMO is that it's basically parsing the inside of a word.  So the program returns a set of parse trees for a word.  Although this usually means suffixes, I think it can parse prefixes too.

The downside of parsing is that it might be ambiguous.  For example, it might not be sure whether to parse *stirling* as some unknown word with *-ing* or a whole word.  Another good example of ambiguity is *cation*.  It may also be uncertain about the part of speech, such as *tests* as a plural noun versus third person singular verb.  The bottom line is that if you want to use PC-KIMMO for stemming, you need to make a way to disambiguate (I've just used a majority vote in the past, which works reasonably).

Another downside of PC-KIMMO is that it partly depends on an internal lexicon.  I'm a bit unclear on how the lexicon affects parsing, but PC-KIMMO does differently on known vs unknown words.

The bright side is that the parses from PC-KIMMO are typically excellent.

Comparing stemmers
------------------

The motivation for comparing stemmers was to evaluate stemmer quality for Emily Hill's research.  Ideally, we want to answer the question *How good is Porter's stemmer compared to PC-KIMMO?* To do this, we would need a gold standard of stemmings, but we don't have that.  We could easily compute something like percent agreement, but does it even make sense?  Suppose we're stemming *comparing* and Porter's returns *compar* but PC-KIMMO returns *compare*.  Is that agreement or not?

Instead, I wrote a tool to facilitate subjective analysis. I'll show an example and explain how to interpret it:

```
           word   shared in set   PC-KIMMO only   Porter's only
--------------- --------------- --------------- ---------------
           know            Know        knowable          knowed
                          Knows       knowingly
                           know     knowingness
                        knowing
                          knows
```

In general, the analysis treats stemming as the process of defining equivalence classes.  In this example, Porter's stemmer has an equivalence class *{Know, Knows, know, knowing, knows, knowed}*.  In other words, Porter's stemmer reduces all these words to the same stem.  The set for PC-KIMMO is *{Know, Knows, know, knowing, knows, knowable, knowingly, knowingness}*.  How would we view the overlap between an arbitrary pair of sets?  We represent it as the intersection (*shared in set*) and the two exclusive sets *PC-KIMMO only* and *Porter's only*.

Which tool fares better?  In this case, I'd say *knowable*, *knowingly*, and *knowingness* should be grouped with *know.* I have no idea what *knowed* is though, but in the absence of contextual information, I'd choose to group it with *know*.  In this case I'd conclude that both PC-KIMMO and Porter's made mistakes, but the output of PC-KIMMO is better.

How do we choose which sets to compare?  We iterate over all words we've stemmed and look up the set for the word in PC-KIMMO and Porter's and make a table like the above, hence the *know* in the leftmost column.  I seem to recall that I couldn't figure out a better way to display all the data (though with hyperlinks and such you can make it a bit easier).

One of the interesting problems is trying to extend this to *n*-way comparisons of stemmers, though the only other stemmer I know of is a biomedical stemmer written by Manabu Torii, an alum from our department.

I'll post the Perl script I used to generate this when they bring my server back online (caveat:  I have to remember too).

addendum
--------

I cleaned up the text a little bit for clarity, and while doing that I realized that it may be possible to automatically obtain a type of gold standard for stemming.  You can go in the reverse direction using most modern dictionaries - they list alternate forms of a word.  The main drawback to this approach is that it's evaluating stemming quality for proper English, and natural texts tend to do their own thing.
