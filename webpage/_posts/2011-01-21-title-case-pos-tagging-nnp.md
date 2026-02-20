---
layout: post
title: title case + pos tagging = nnp
date: 2011-01-21
---

This year I plan to make up for lost time in publication; while finishing my dissertation I was still doing research but didn't get around to publishing it.  Now I'm in the process of doing that and I thought I'd also take a look at some work from my early days of grad school.  At the time I didn't know which ideas were publishable or not.

The work is from the SIGHT project, which seeks to infer the author's communicative intention in the design of information graphics.  The project grew from Stephanie Elzer's thesis, who worked with bar graphs.  Since then, Rich Burns has worked in expanding it to grouped bar charts and Peng Wu has worked with line graphs. Seniz Demir worked in actually generating textual descriptions for blind users.  I believe everyone in my lab has worked on the project at some point in time, though not all for thesis work.

Way back in 2003 or so, I worked on the project in trying to integrate the natural language information in graph titles, but I found there were a lot of problems in graph titles.  (I also did several interesting analyses, which I hope to redo on newer data and publish)

That said, we've used keyword methods before, but I'm interested in part of speech tagging the titles as a precursor for more interesting analysis.  Actually I tagged them back in 2003 with Brill's tagger.  The big problem is the case of the titles:  Many are all uppercase or title case, so the tagger labels everything as proper nouns (NNP/NNPS).  At the time, I lowercased the titles, which worked reasonably well but really isn't the way to go.  Here's are some example titles:

* ON THE REBOUND?
  lowercasing works just fine here
* GERMANS MISS THEIR MARKS
  lowercasing messes up the part of speech for "Germans"
* SOUTHWEST'S BIG COST ADVANTAGE
  similar situation
* GDP
  lowercasing is generally bad for this

Now several years have passed and I'd like to beef up the work and try to publish.  But I figure I should do a better job than lowercasing the titles, so I've embarked on a quest to fix those darned titles.  This post will document some of the ups and downs of today's coding session.  I haven't gotten around to reading some of the articles on fixing the casing, but I'll get there soon.  I wanted to code up some ideas before I forgot them and also it feels good to program after so long.

My first idea was to check the Google language model I have and see whether the uppercase or lowercase form of each word is more common.  (I'd love to check the accompanying article text, but I don't have that for the graphs I've looked at so far)  Also note that I can't really just load it into memory, so I have to scan the titles and build a list of word forms that I want frequencies for.

That led to some interesting problems:

* some words are simply more common in the incorrect casing:
  + Total > total
  + Quarterly > quarterly
  + Sales > sales
* Google's tokenization method means zero-frequencies for certain tokens:
  + LONG-TERM
  + COVERAGE...
  + MOUNT...
  + TELECOM'S
  + ...THE

The second problem is easier so I solved that first.  But I can't just throw away the punctuation.  I need to make sure that I've left the title intact aside from capitalization.  So I temporarily removed punctuation on the edges of tokens while re-capitalizing.

But that's not enough.  I handle the possessive case ('s) specially if it's not in the Google data, which helps. Then I also have to consider splitting hyphenated words if they aren't in Google's data.  After all that I need to reassemble the string so that it matches the original, just with different casing.

I should also mention another problem I ran into (that I found funny).  Originally I created equivalence classes (like stemming) for title words by lowercasing them all.  If case information is unreliable, anything with the same lowercase form is a candidate casing.  However, I had the title "Ups and Downs", which turned into "UPS and Downs".  In this case, it's just that we're not sure if it should be "Ups" or "ups", which I have to fix.

The problem of unigrams is a pain though.  I'm working on addressing it by doing a [Viterbi search](http://en.wikipedia.org/wiki/Viterbi_algorithm), where for each word I consider all alternate casings from the Google unigram data, but use Google bigrams to find the best path through the graph. I doubt bigrams enough will solve the entire problem, especially for single-word titles.  But I bet they'll do better than pure unigrams.  Also, you have to consider some titles that require some topical awareness to fix, such as "THE NEXT BOOM":  Does it refer to "next" or "NeXT"?  Ideally we'd have the accompanying article text to help with that.

Maybe I'll write about it again when I see what Viterbi with bigrams can do for me.
