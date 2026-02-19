---
layout: post
title: Synonyms for factoid search, Part 2
date: 2015-05-15
---
*The [previous post](/blog/2015/04/synonyms-for-factoid-search-part-1/) described the problem and attempted to find synonyms for Elastic Search using a thesaurus, Wikipedia redirect groups, and Bing's related searches.*

Problem recap
=============

We were adding a search box to ads to look up quick facts, initially focused on car ads. The big issue is that queries such as "ac" or "a/c" need to match a Json object containing only "air conditioner". Searches like "cost" need to match "MSRP" or at least "price".
![Toyota Prius Ad with Search Box](/assets/img/posts/wp/prius-ad.png)

Synonyms from WordNet
=====================

[WordNet](https://wordnet.princeton.edu/) is a great resource for word information in English. It's particularly good for nouns and indicates synonymy as well as hierarchy. For example, you can find that *tire* is a type of *hoop* or *ring*. And you can find synonyms, in this case just *tyre*. There's a [web version](http://wordnetweb.princeton.edu/perl/webwn) you can test out without needing to install/setup.
But it's much more complex than this: relationships such as synonyms or is-a (hypernym/hyponym) only have meaning between specific meanings, called word senses. The string *tire* has five senses in WordNet 3.1: 1 noun sense and 4 verb senses. The kinds of *tire*we care about for cars is the noun one. If we restrict just to nouns we can say that *tire* and *tyre* are synonymous in Elastic Search and that'll improve our search for British users.
What about a term like *mileage*? Looking up in WordNet online there are three senses:

1. mileage, milage (distance measured in miles)
2. mileage, fuel consumption rate, gasoline mileage, gas mileage (the ratio of the number of miles traveled to the number of gallons of gasoline burned)
3. mileage (a travel allowance at a given rate per mile traveled)

The senses are usually in order of most common to least common. Sense #2 is the one we want but it's not so bad to take all the synonyms of all senses {mileage, milage, fuel consumption rate, gasoline milage, gas mileage}.

Detour: Handling phrases
------------------------

WordNet has many phrases as well as single words. For instance, there's an entry for *air conditioning.* If we're generating synonyms for an air conditioning factoid it's better to use the phrase. However, *remote starter* doesn't have an entry.
I used a very simplistic approach that works for our data: if the full phrase isn't in WordNet, strip one word from the left and try again. If that's not found, strip another word and so on. Keep the leftmost words intact and generate alternatives just for the rightmost words. This works because we're working with noun phrases in English and there weren't many prepositional phrases.

Taking synonyms of all synsets
------------------------------

The simplest approach is to avoid [word sense disambiguation](http://en.wikipedia.org/wiki/Word-sense_disambiguation) and just join all synonyms. Like before I didn't have evaluation data so mostly I eyeballed synonyms and considered bug reports.
Input: air conditioning
Output: air conditioner
Input: heat
Output: heating system, ignite, oestrus, fire up, heating plant, inflame, stir up, heating, heat up, high temperature, passion, wake, heat energy, hotness, estrus, warmth, rut, hot up
Input: mileage
Output: mileage, fuel consumption rate, milage, gasoline mileage, gas mileage
Input: safety
Output: prophylactic, safety device, safe, base hit, rubber, guard, condom, refuge
Input: cost
Output: be, price, monetary value, toll
Overall the output is much better than previous approaches. Although *air conditioner* is useful, the stemming in Elastic Search would already handle it. Likewise for heat/heating.
And then there are frankly bizarre results if you consider the automotive domain, like *estrus* for heat. It's the sense of heat "applies to nonhuman mammals: a state or period of heightened sexual arousal and activity". Likewise in the automotive domain you probably don't need *condom* to be related to *safety*. But *rubber* related to *safety*? That might be good for rubber on the bumpers of the car... maybe.

Word sense disambiguation
-------------------------

The simplest approach to [word sense disambiguation](http://en.wikipedia.org/wiki/Word-sense_disambiguation) are the [Lesk-like algorithms](http://en.wikipedia.org/wiki/Lesk_algorithm): look for keyword overlap between the definition (called a *gloss*) and words in your domain. In this case I can group all keywords from our fact set for disambiguation. And for scoring I use cosine similarity.
Input: air conditioning
Output: air conditioner
Input: heat
Output: high temperature, hotness
Input: mileage
Output: fuel consumption rate, gasoline mileage, gas mileage
Input: safety
Output: (no synonyms)
Input: cost
Output: price, monetary value
The crazy stuff is gone but we've lost "safety device" for "safety", "milage" for "mileage", and "warmth" for "heat". Let's look at disambiguation scores for "safety".

1. safety (the state of being certain that adverse effects will not be caused by some agent under defined conditions)
   score=0.106600
2. condom, rubber, safety, safe, prophylactic (contraceptive device consisting of a sheath of thin rubber or latex that is worn over the penis during intercourse)
   score=0.065795
3. safety, refuge (a safe place)
   score=0.056980
4. base hit, safety ((baseball) the successful act of striking a baseball in such a way that the batter reaches base safely)
   score=0.032141
5. safety (a score in American football; a player is tackled behind his own goal line)
   score=0.000000
6. guard, safety, safety device (a device designed to prevent injury or accidents)
   score=0.000000

The sense we want is #6 but it has a score of zero meaning no overlap at all. "prevent", "injury", and "accidents" aren't anywhere in our list of car facts. Perhaps a corpus of automotive text would disambiguate to that sense.
Looking through old emails I found a great example of horrible WSD failure. We had tons of facts like "solar roof package" and it disambiguated "package" to "software package" leading to this unfortunate set:
solar roof package: solar roof software, solar roof
software program, solar roof computer software, solar roof
software system, solar roof software package, solar roof
package

Detour: Wolfram Alpha
---------------------

Later in the project someone pointed me to the Wolfram Alpha API because it provides a synonym service. The nice part is that you just specify the word. Another nice part is that you can test it via web search without setting up code for the API.
But I found that it's just giving back WordNet synonyms (as of 9/2014). There's no support that I saw for word sense disambiguation either. My best guess at their algorithm is that it iterates through the senses in order and tries to get 10 synonyms. But if it finds 9 and the next sense will add 3 it'll return 12 synonyms. I could replicate their synonyms closely from WordNet with a few slight differences:
For "interior" Wolfram Alpha filtered "Department of the Interior". For "heat" it filtered "estrus" and "oestrus". For "safety" it filtered the condom sense. It's plausible that the differences are due to WordNet version or that they have some additional filtering rules.
Another interesting bit is that their search is case-sensitive. "or" shows the real word and "OR" shows Oregon. "no" shows the regular word and "NO" shows nitric oxide.
Long story short I wouldn't recommend building a project on this service unless it's revamped. Just use the appropriate WordNet API for your language and it'll be much faster and more customizable.

Subjective issues aka bug reports
=================================

We had tons of issues because we didn't just need synonyms. I specifically remember feedback that "speed" didn't give 0-60 acceleration numbers. WordNet can't help too much because they aren't synonyms just closely related.
Another type of issue was common automotive acronyms like mpg, msrp, and a/c. "Cargo space" was another difficult one.
Colors were also difficult - searching for a specific color should show the list of available colors.
Occasionally we dealt with searches that didn't exactly have a keyword, such as "how much is it" but we addressed that with a question-answer type classifier.

Thoughts
========

The issues with WordNet can be loosely grouped:

* The info is in WordNet but my WSD is failing
* The automotive word sense isn't in WordNet (such as *hybrid*)
* Needed related words, not just strict synonyms
* Real language is more colloquial and involves abbreviations, acronyms, and informal variations

Collecting an automotive text corpus seemed to be the right direction. If we had thousands of users already I would have just mined the query rewrites from actual user searches much like Google. But that isn't sufficient to achieve traction with users, customers, or investors.
If we were searching documents rather than factoids I'd say we should ditch Elastic Search and adopt latent semantic indexing of some form. But the combination of factoid search and Elastic Search put us in a tight spot.
What did I need in a corpus?

* Domain-specific, preferably a method I could use on other domains if we started expanding from car ads.
* The stuff real people say, not just dictionary terms.
* Up to date with current automotive trends.

Next post I'll describe the approach: crawling automotive subreddits and using gensim to get LSA synonyms vs homemade pseudo-relevance feedback for synonyms.
