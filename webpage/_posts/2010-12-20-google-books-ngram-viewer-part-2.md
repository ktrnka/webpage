---
layout: post
title: google books ngram viewer (part 2)
date: 2010-12-20
---
Last week, I [covered](/blog/2010/12/google-books-ngram-viewer/ "google books ngram viewer") the release of the [Google Books NGram Viewer](https://books.google.com/ngrams).  Google's handy tool has received a lot of attention since then, which I'll attempt to summarize and I'll add some more information.

[Science](http://www.sciencemag.org/content/early/2010/12/15/science.1199644)
-----------------------------------------------------------------------------

The original article is available online through *Science*.  It's free with registration and the article isn't very long.  It focuses on showing cultural trends with this data and pushes the term *culturomics*.  I'll try to summarize most of the points.
For starters, they provide information on the collection of texts surveyed.  The Google Books project has digitized about 15 million books, and they picked about 5 million of them based on [OCR](http://en.wikipedia.org/wiki/Optical_character_recognition "Optical character recognition") quality and metadata. They note that periodicals were excluded, but I didn't even know those were a part of Google Books.  In any case, the 5 million books contain about 500 billion words, 361 billion of which are English.  In contrast, [Google popular 5-gram model](http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2006T13) was built using 1 trillion words of web data (which is considerably easier to obtain).  The 5 million books used for the project comprise about 4% of all books ever printed.
The ngram models can be used for a variety of studies, but one of the ones I found interesting was comparing "the Great War" to "World War I", which I reproduced using the web tool:
![Great War vs World War I]({{ "/assets/img/posts/wp/ww1.png" | relative_url }})
Unfortunately, this highlights one of the problems with Google's tool --- we would really like to compare "Great War" to "World War I" (uppercase i) OR "World War 1" (number 1) OR "First World War".  As far as I can tell, that isn't possible in the current system.
They move on to discuss the size of the general English vocabulary or lexicon.  However, non-words clog up the results somewhat (numbers, misspellings, etc).  Although numbers can be filtered automatically, misspellings can't.  Therefore they filtered a random sample.  They found that vocabulary nearly doubled from 1950 to 2000.
The authors compare their analysis of English vocabulary with dictionaries and in general conclude that dictionaries accurately survey common words, but struggle with some infrequent words.  In the end, they suggest that their analysis can be used by lexicographers to better find low-frequency words missing in the dictionaries and to better keep up with new words.
After analyzing vocabulary trends, they turn to trends in regular vs irregular morphology.  For example, consider *burnt* vs *burned* (shown under the Wired section).  They show several examples of the irregular -*t* replaced with *-ed* over time.  However, some words are shifting to favor the irregular form:  light/lit, wake/woke, and sneaked/snuck.  In using the online tool, it's difficult to reproduce these trends.  I suspect that they didn't just do a simple keyword query but tried those words in different contexts.
The article moves on to several similar "half-life" trends --- years, inventions, and people.  They find that these things are marked by a large, quick increase in frequency and then decay over time like a half-life.  For year trends, they look at the exact number (e.g., 1981).  For inventions, they group inventions by time.  For people, they use the full name (e.g., "Bill Clinton").
Some of the most interesting results come for people --- in modern times, the initial burst of fame is quicker and rises higher, but drops off much more quickly.  They also segregate by person type, showing the long-increase in fame of authors and scientists and the correlation between age and fame for actors and politicians.
Finally they survey censorship by querying names and comparing trends in English compared to German (for Nazi censorship) or English compared to Chinese (for [Tiananmen Square](http://en.wikipedia.org/wiki/Tiananmen_Square "Tiananmen Square")).
Overall, the article is worth reading, but it gives a strange vibe.  It's really a survey of possibilities using the Google Books NGram Viewer.

[Language Log](http://languagelog.ldc.upenn.edu/nll/?p=2848)
------------------------------------------------------------

The first half of Mark Liberman's post describes an interesting OCR problem --- in the past, an *s* looked much more like an *f* except when used at the end of a word.  He provides some excellent graphs showing that the OCR software saw an *f* up until the common glyphs changed, then saw an *s.*
He moves on to describe the problem of [word sense disambiguation](http://en.wikipedia.org/wiki/Word_sense_disambiguation "Word sense disambiguation") --- when you query for a word, say *C*, you get results for C as a computer language and results for C as a letter name (e.g., "Curtain C") among others.
The article concludes that researchers are in an awkward position.  We can process the ngram data freely, but we don't have access to the underlying texts (though with good reason).  But because of this, we can't correct things like the s/f problem, word sense disambiguation, part-of-speech based queries, and any of the other myriad analyses we might want to apply.

[Ars Technica](http://arstechnica.com/tech-policy/news/2010/12/history-of-computingin-handy-graph-form.ars)
-----------------------------------------------------------------------------------------------------------

The first article by Ars takes a look at Google's new tool in the context of typical computing arguments, such as Mac/PC, web browsers, operating systems, and programming languages.  The graphs are surprisingly sensible --- Netscape shows a distinct peak and fall, although I have a hard time viewing Netscape being nearly as "popular" as Safari/Firefox around 2007.  This shows part of the difference between real popularity and relative frequency --- books often mention Netscape in introductions, which tend to include historical notes.  Even if Netscape were to drop to zero usage, it'd still live on in historical accounts.  I would've really loved to see Ars pull some of their historical browser data for comparison.
The computer languages comparison is also interesting, but shows similar problems.  At the end of the graph (2007), Pascal is the most common keyword.  That said, there are several interesting trends --- we get to see the rise and fall of BASIC and the creation of several languages (Perl, Python, VB, Objective-C).
It's an excellent look at some practical modern examples, but the examples demonstrate the importance of critical analysis;  they only show frequency in books and need to be interpreted carefully.

[Ars Technica](http://arstechnica.com/science/news/2010/12/googles-digitized-books-provide-verbal-culturome.ars)
----------------------------------------------------------------------------------------------------------------

In a second article, Ars takes a closer look at the original *Science* text, citing many examples of correlation between frequency and real-world events (such as *slavery* around the Civil War).  They also include a graph from the original article, showing the relative frequencies of several foods over time --- steak/sausage as well as the more modern popularity of hamburgers, pasta, and sushi.
They conclude that the correlation of keyword frequency with real-world events can sometimes be surreal, but not everything shows correlation.  However, despite the lack of perfect matching to real-word events, this resource is a step in the right direction.

[Wired](http://www.wired.com/wiredscience/2010/12/cultural-evolution-google/)
-----------------------------------------------------------------------------

Wired covers the story from the perspective of our ever-changing culture and includes some discussion of the *Science* article that accompanied the release.  Compared to other coverage, they include several graphs from the original article --- burnt/burned in American/British English, popularity of several scientists over time, and popularity of several foods.
The graphs of burnt/burned in American vs British English are reproduced below.  In American English, *burned* becomes more common around 1855.  In contrast, British English prefers *burnt* until about the 1980-1995 range, when *burned* finally becomes more common.
![American English]({{ "/assets/img/posts/wp/burnt-american.png" | relative_url }})
![British English]({{ "/assets/img/posts/wp/burnt-british.png" | relative_url }})
 
Fortunately, they present it with a grain of salt --- although Google Books and the ngram viewer allow for excellent historical analysis, research using this resource is non-trivial.  Book writing is a skewed sample of language, and may not include useful data on certain topics, such as obscenity.

Summary
-------

Hopefully I've provided a better account of the original article as well as the coverage on several news sites.  In my opinion, you can perform many interesting studies with the Google Books NGram Viewer.  That said, you need to interpret the results critically and some analyses are limited because we can only use the 5-gram model.  Hopefully some aspects of the online tool will improve over time, such as groups of search terms.
