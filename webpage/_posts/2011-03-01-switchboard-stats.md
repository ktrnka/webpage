
---
layout: post
title: Switchboard stats
date: 2011-03-01
---
I've been using the [Switchboard corpus](http://www.isip.piconepress.com/projects/switchboard/) for years and I recently gave a talk in class with some statistics, including simple tests to compare Switchboard to a background corpus. In this case, I used Google's Web 1T unigram model for "general purpose statistics". I'll include and discuss the interesting graphs, but the full slides are online [here](http://www.cis.udel.edu/~trnka/CISC889-11S/lectures/switchboard.pdf).
The first big test was to classify words into a set of word shapes and compare. Before looking at the graph below, consider the ambiguity: Is "A" title case or all caps? What is "JetBlue"? What about "T3"?
![percentage of word shapes](/assets/img/posts/wp/word-shapes.png)
Note that this is a partially cleaned version of Switchboard from my work with augmentative and alternative communication. Speech repairs and annotations are mostly removed.
The prevalence of lowercase words in Switchboard shouldn't come as much of a surprise. In addition to spoken conventions, the subject matter is restricted to specific topic prompts and the speakers don't know each other. So the percent of proper nouns is probably small. The list of topic prompts is available in "ATTACHMENT 2" in [LDC's documentation](http://www.ldc.upenn.edu/Catalog/readme_files/switchboard.readme.html). For example, "Find out what kind of fishing the other caller enjoys. Do you have similar or different interests in the kind of fishing you enjoy?" I can't imagine many proper nouns with that, but maybe more with the baseball topic.
You can also see some other trends in Switchboard transcription and Google 1T conventions. Switchboard transcribes numbers spelled out (e.g., "nineteen eighty eight"). Google's model splits up words with hyphens so those are rare or non-existent in 1T data. I'm curious what sorts of things fall into the *other* category though.
Note that the symbol category uses regex character class \pS, which matches Unicode chars that are indicated as symbols. But I haven't done much testing with it yet.
The second graph compares the distribution of pronouns in each corpus. For starters, Switchboard is about 10% pronouns compared to maybe 1% for the Google 1T web data. However, this graph is only within those percents.
![distribution of pronouns in Switchboard vs Web 1T](/assets/img/posts/wp/pronoun-distributions.png)
The distributions make some sense - Switchboard's much higher percent of "I" comes at the expense of other words. If you think about the situation, when would the speakers use he/she? I'm a bit surprised that "they" is higher in Switchboard though.
I repeated the same analysis for a list of contractions. The percent in web data is surprisingly low (0.0002%) for my list compared to Switchboard (4.5%), but I took a look at the distribution within the group here.
![distribution of contractions](/assets/img/posts/wp/contractions-details.png)
You'll probably have to enlarge the image to read it (sorry!). Also, the rarity of contractions in Google 1T affects the analysis somewhat.
I'd guess that *it's* and *that's* are generally non-referential (*that's unfair! it's going to rain*). You might think that normalizing by the number of contractions overall could hide some trends - maybe *it's* and *that's* are about the same percent overall in the corpora. But this isn't the case - *it's* is about 0.86% of Switchboard tokens but only 0.00000055% of Google 1T.
Looking at the documentation for the 1T model it says that tokenization generally follows Penn Treebank tokenization, which separates *'s* and *n't* as separate tokens. But then how on earth are tokens like *it's* even in Google's 1T? It's bizarre. So I'll leave you with the top few results of the 1T model for *'s* and *n't*.

### n't

```
isn'ta  3276867
wasn'ta 1641021
can'tI  657682
aren'ta 352813
don't   338047
Don'ts  315740
didn'tI 258163
havn't  249372
don'ts  224515
don'tI  222961
ain'ta  147897
con't   143638
can't   138521
dosen't 135393
n't     127065
...
```

### 's

```
's      2988704364
It'sa   2893295
it'sa   2605456
there'sa        1263361
There'sa        883982
MBA's   792778
...
```

final words
-----------

*isn'ta* is more common than *isn't* and also more common than *n't*. I don't know what to make of that. I'm stumped. Even if you do a Google Battle between *isn'ta* and *isn't*, *isn't* wins at about 1.6 billion pages. Yet *n't* is only 127 thousand words and *isn't* is 46 thousand.
*Note (3/4):  Because of the number of page views, I went back and edited this again to improve the writing.*
