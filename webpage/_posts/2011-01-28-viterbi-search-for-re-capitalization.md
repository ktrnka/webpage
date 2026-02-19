
---
layout: post
title: viterbi search for re-capitalization
date: 2011-01-28
---
Last week I mentioned that I was working to [restore the capitalization](http://kwtrnka.wordpress.com/2011/01/21/title-case-pos-tagging-nnp/ "title case + pos tagging = nnp") of graph titles.  At the time, I was using Google's trillion word unigram model to disambiguate case.  But it didn't work quite right.  It seemed like an improvement over just lowercasing them, but you'd end up with words like *Spring* or *Jobs* capitalized all the time.  It became clear that some additional information was necessary.  There are three candidates for additional information:

1. the immediate context of the word
   This lends itself to higher-order ngrams. For example, consider *Stocks Spring Back*. Based on *Stocks*, we can decide that *Spring* refers to the action rather than the season.
2. the accompanying article
   It's likely that the text of the article containing the graph would have the proper case more often than not. This should work fine with unigrams, though higher-order models probably can't hurt much. There's one major problem though: We don't have article text for most graphs. Some graphs don't even go with an article.
3. topic-based methods
   Hopefully some of the words in the title are relatively unambiguous. We could take those keywords and run a Google search (or any relevance-based method), then build a tailored language model weighted towards the top results. The downside is that this is a lot of work and may or may not work.

I've focused on #1 so far and used Google's bigram data with a [Viterbi search](http://en.wikipedia.org/wiki/Viterbi_algorithm "Viterbi algorithm") to help disambiguate. How does that work? We consider all possible re-capitalizations of each word (we use the Google unigram model to produce these sets). Then we use the Viterbi algorithm to find a good sequence. Here's a little example for the title *THE ECLIPSE OF SUN*:

{ THE, The, the } => { ECLIPSE, Eclipse, eclipse } => { OF, Of, of } => { SUN, Sun, sun }

Each word is replaced with a set of alternate casings. Normally in this type of process we'd first transition from a start-of-sentence symbol to the *THE* set and at the end transition from the *SUN* set to an end-of-sentence symbol. But we don't have accurate start/end data for the format we want to produce, so we omit that. (Though I should note that we implicitly use a not-start-of-sentence symbol before the *THE* set. It's tough to say whether an end-of-sentence symbol would be helpful.)
The resulting capitalization is much more consistent than the unigram method: We don't have (seemingly) random words capitalized. Most of the time the casing is excellent. But it turns out that this method has some fatal flaws:
Consider the title *ACTIVE USERS*.  Our initial candidates set for *ACTIVE* is ranked by the unigram model.  It comes up with these probabilities (using engineering/scientific notation):

* ACTIVE:  1.4 e-6
* Active:  2.2 e-5
* active:  4.7 e-5

So it prefers the lowercase form by about a factor of two. Then we consider all of the possible forms of *USERS.* I'll only show the top candidate that gets linked to each.

* USERS:  ACTIVE => USERS  (smoothed transition probability:  8.6 e-4)
* Users:  Active => Users  (smoothed transition probability:  1.7 e-2)
* users:  active => users  (smoothed transition probability:  5.7 e-3)

I haven't shown quite enough digits, but the end result is that *Active Users* is assigned a probability of 3.69 e-7 while *active users* is assigned a probability of 2.63 e-7. Therefore the method prefers *Active Users.*
Why did this happen? Surely *active users* is more common! Nope! The lowercase title occurs 341,302 times compared to 677,703 for the title case one. There's a good lesson in using real data.
However, it doesn't necessarily have to be that the wrong case is more common because of the nature of the data. Another example title is *FOR RICHER & FOR POORER.* Although *for* is about 25 times more common than *For*, the transition from *for* to *richer* is about 20 times less probable than *For* to *Richer*. Then when we get to the ampersand, the transition from *Richer* is more likely. In this case, the probability of the history maybe could've helped us, but the wrong transition was more probable even though it was less common.
This happens because a huge number of words occur after *for*, but a much smaller number occur after *For*. I'd speculate that this reflects a more restricted ngram model learned from titles and such on the web.
I'll try one more simple idea before moving on to processing the titles that have accompanying text.
