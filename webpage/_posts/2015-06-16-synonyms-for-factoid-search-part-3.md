---
layout: post
title: Synonyms for factoid search, Part 3
date: 2015-06-16
---

In the previous two posts I described 1) [our problem and initial simple approaches]({{ "/blog/2015/04/synonyms-for-factoid-search-part-1/" | relative_url }}) and 2) [WordNet-based solutions]({{ "/blog/2015/05/synonyms-for-factoid-search-part-2/" | relative_url }}). Now I'm finally writing up our best solutions: gathering a domain-specific corpus and learning word associations.

Quick reminder: The goal is to look up facts related to a car advertisement. But there's a huge problem in that the data only has one or two words per fact and people often use different words when searching. So we need a good source of synonyms or related words for the automotive domain.

*Note: This post was much longer than I expected :(*

Problems with previous approaches
=================================

The sources often lack the synonyms that we really need. I can't fix that with better ranking; the data just isn't there. The other problem is that both Wikipedia redirects and WordNet really need good word sense disambiguation and that's hard.

Scraping a domain-specific corpus
=================================

Goals:

1) Automated

2) Scale to other domains

The second goal is tricky: I wanted something that would work when we're dealing with ads for phones, drugs, homes, credit cards, etc.

There's a subreddit for almost anything. A quick search for auto subreddits shows /r/cars, /r/Autos, /r/MechanicAdvice, /r/Cartalk, and tons of manufacturer-specific subreddits.

So I wrote a reddit scraper using a Python module named [scrapy](https://doc.scrapy.org/en/latest/index.html). The setup was a bit involved:

1) Get scrapy installed. On Windows use [Anaconda](https://store.continuum.io/cshop/anaconda/) to make this easier

2) Run scrapy command to create a default project

3) Make classes for the items you want to scrape

4) Write a spider with starting URLs, rules to extract URLs that you want to follow next, rules to filter URLs to follow, and rules to extract the actual items from the pages

5) Add a pipeline to clean up the items (strip any leftover html, clean up whitespace, etc)

Generally you can follow the [tutorial](https://doc.scrapy.org/en/latest/intro/tutorial.html). Tips:

* Use [scrapy XPath selectors](https://doc.scrapy.org/en/latest/topics/selectors.html) to pick the parts of the HTML you want to process. When possible prefer to extract content based on CSS classes and ids. Figure out the XPath you need by right-clicking in Chrome and doing "Inspect element"
* Be strict about only following "Next" links and links to detail pages. I had bugs where it'd follow links to "Previous" which had a different URL so it fooled scrapy into visiting the page again (normally the framework will track sites it's visited and only visit once). I also had bugs where it'd follow links to different sort orders and just lead to cycling the same content.
* Set a DOWNLOAD\_DELAY to 1 sec or more. This ensures that you aren't hitting their servers much.
* Decide whether you want a depth-first search or breadth-first. They have memory tradeoffs but depth-first tends to go off into weird deep sections of the internet. See [this](https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order).
* When running your scraper from the command line, you can store the scraped items as Json which is great for downstream processing.
* I used the HTML stripper from [NLTK](https://www.nltk.org/) (nltk.clean\_html). It's higher quality than writing your own.
* If I could do it again I'd probably spend a day and see if I can set up two levels of Kimono scrapers to accomplish something similar.

For this project I really just need a collection of documents. I wasn't sure at first whether I wanted each comment to be a document or each thread so I made sure I could experiment with both. So I have a file format like:

```json
{"title": "Thread 1 title", "url": "https://blah", "body": ["Post 1", "Post 2", ...], "links": ["https://...", "https://...", ]}
{"title": "Thread 2 title", "url": "https://blah", "body": ["Post 1", "Post 2", ...], "links": ["https://...", "https://...", ]}
...
```

With a rate limit of about one page per second I let it run for about a day and got ~100mb worth of text.

Checking data quality
---------------------

This is likely a topic for a dedicated post but don't assume that you have clean data. Some simple checks I did for this project:

* Read through the actual Json for 20-30 minutes. I always end up finding duplicates, cut off content, bare URL lists, and other weirdness. It's counterintuitive in a world where we focus on automation but it's worth it.
* (NLP-related) Tokenize the text and make a unigram distribution. Inspect it any time it'll change.
  + Are common words at the top like the, a, an, I, you, and? (Don't read into it too carefully cause the specific order is domain-dependent)
  + Is capitalization reliable or unreliable? (doesn't matter if you lowercase)
  + How is your tokenizer handling words like "it's", "your's", "don't", "I'm"?
  + In the automotive domain, I check that all the terms I need are in there, such as Toyota, Prius, car, cars, truck, trucks, engine, hybrid, mileage, milage, safety, air bag, etc.
  + If there are any weird words in the top 100, search the actual Json. They may come from duplicate documents that result from a scraping bug.

Using domain-specific corpus for filtering
==========================================

One of the early things I tried was to filter the Wikipedia redirects and WordNet synsets by how frequent the terms were in the reddit automotive corpus. It's simple and effective but ends up filtering the lists a bit too much.

Filtering WordNet
-----------------

```
color: colour
security: protection
option: choice, alternative
grey: gray
warranty: guarantee, warrant, warrantee
```

They're pretty good but I couldn't use examples from the previous post. Almost all of those lists were empty after filtering!

Filtering Wikipedia redirects
-----------------------------

```
security: the security, securities, security systems, marketable, securing
option: options, configurable
grey: gray, dark gray, grayish, greyish
warranty: warranties, lifetime warranty, warrenty, car warranty
```

Similar to WordNet we're getting most of the bad synonyms out. It's clearly more precise with filtering but the lists are much smaller. And it doesn't solve the problem of missing the words we need.

Synonyms from latent semantic analysis
======================================

A common solution for finding synonyms came from information retrieval research in the 90's. The rough approach is to build a giant matrix of word counts per document, apply singular value decomposition, then drop the least important dimensions.

Using the resulting decomposition in information retrieval is called [latent semantic indexing](https://en.wikipedia.org/wiki/Latent_semantic_indexing). Usually when it's applied to synonyms it's called [latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis). And more broadly it's a machine learning technique called [principal components analysis](https://en.wikipedia.org/wiki/Principal_component_analysis).

The result is that you get three matrices: mapping of terms to semantic dimensions with weights, weights for the dimensions, and a matrix mapping documents to semantic dimensions. For synonyms you can use the term-to-semantic-dimension matrix to compute semantic similarity. (1)

Previously I tended to stay away from LSI/LSA because they use compiled tools with little documentation. But we found a great Python module called [gensim](https://radimrehurek.com/gensim/), which provides a nice wrapper around LSI/LSA as well as related approaches like LDA and word2vec.

There are a couple really nice things about using LSA:

1. No word sense disambiguation (2)
2. Continuous similarity scores between terms, can set a threshold to tune precision vs recall

We treated each Reddit thread as a document because the comments were too short to learn useful cooccurrences.

To look up synonyms I make one "document" for each word in the vocabulary. Then I used gensim's LsiModel and MatrixSimilarity to "search" for the most related terms for any input.

Examples
--------

I didn't run the exact same terms as previous tests in my old emails sorry! I'll just pick a few examples.

```
black: matte, stain, vinyl, plasti, plastidip, paint, ...
color: colors, blue, colour, repaint, wrap, ordered, vinyl, vin, painted, ...
windows: tint, tinted, va, dark, pink, darker, glass, windshield, ...
security: bedroom, house, steal, thief, stolen, theft, ...
wheels: rims, bbs, diameter, offset, spokes, locking, ...
doors: door, sedan, coupes, coupe, pillar, hatchback, sedans, hatchbacks
tires: tread, tire, rears, michelin, rubber, sidewall, compound, rotated, ...
prius: environment, hybrids, insight, priuses, viewed, hybrid, unplugged, ...
```

They're excellent with a few caveats:

1. When I don't recognize a word I can't tell whether it's an acronym or just a term I don't know
2. Sometimes it's unclear why words are related, such as "viewed" for prius or "pillar" for doors.

Side track: Using web crawl
---------------------------

Reddit is great but somewhat limited. So I tried taking all the outbound links from the reddit auto crawl and doing a general web crawl to build up a larger corpus. Unfortunately a ton of the links were used car sites or detailed manuals. I went through the process of training LSA and generating synonyms but they had lots of general terms mixed in randomly. So I didn't continue the investigation.

Side track: LSI vs LDA
----------------------

Latent dirichlet allocation (LDA) seems to be more common than LSI/LSA these days. We only very briefly tried it and the results weren't much different with the exception that you could get a clean summary of each topic in the model. With LSI/LSA the topics are less defined by particular dominant words and more defined by patterns of cooccurrence so the groupings aren't human readable.

Using LSA synonyms in ElasticSearch
-----------------------------------

Even though we have similarity scores between pairs of terms, ElasticSearch is a boolean synonym-or-not type of system. So we had to pick a threshold for similarity (around 0.35 seemed good). And our generated synonyms aren't symmetric but ElasticSearch synonyms are.

Side track: Issues in the overall system
----------------------------------------

Unlike web search, sometimes in factoid search it's best to return no results. For example we had an issue where a query for "sunroof" would return the info for "technology package". This happened because there was no information at all for sunroof, certainly no "sunroof": false in the data and happened because "sunroof" and "package" were often mentioned together in the corpus. We didn't have a good solution for this except to set the synonyms threshold to be more restrictive.

This would've been a good area for further work had Searchify continued.

Alternate approach: Pseudo-relevance feedback
=============================================

The relevance feedback is another technique from information retrieval. Imagine a thumbs up/down button on each search result. If you did that, then the system can redo the search to prefer good documents and penalize bad documents. Some of the background is in the [Rocchio algorithm](https://en.wikipedia.org/wiki/Rocchio_algorithm).

An interesting tweak is pseudo-relevance. The system assumes that documents with good scores are mostly good and documents with bad scores are mostly bad. Then it finds words that occur more in good documents than bad, adds them to the query, and redoes the search.

It can also generate lists of related terms. We'd search our set of documents for a term, say "color" and assume the top 20 documents are relevant. And assume all other documents are irrelevant to "color". Then we compute the probability of each word in those two sets and take the difference in probabilities.

What we get are scores like "paint" is 0.005 more probable in documents related to "color". Some old debug output:

```
color color: 0.0094 he: 0.0055 paint: 0.0050 blue: 0.0041 his: 0.0029 bmw: 0.0028 interior: 0.0021 guy: 0.0017 laguna: 0.0015 he's: 0.0015

price price: 0.0076 sell: 0.0046 dealer: 0.0032 me: 0.0032 dealers: 0.0027 selling: 0.0025 they: 0.0024 them: 0.0023 then: 0.0023 dealership: 0.0022

cost tax: 0.0062 cost: 0.0044 we: 0.0037 parts: 0.0035 pay: 0.0033 taxes: 0.0022 shop: 0.0020 us: 0.0019 price: 0.0019 by: 0.0018

engine engine: 0.0326 starter: 0.0045 check: 0.0044 timing: 0.0038 battery: 0.0036 belt: 0.0030 when: 0.0027 start: 0.0027 may: 0.0024 light: 0.0020

transmission transmission: 0.0285 fluid: 0.0203 shop: 0.0028 filter: 0.0027 change: 0.0026 drain: 0.0024 fill: 0.0022 flush: 0.0021 tell: 0.0021 do: 0.0020

cargo truck: 0.0069 people: 0.0042 trucks: 0.0036 drive: 0.0028 haul: 0.0026 because: 0.0023 when: 0.0022 had: 0.0018 we: 0.0016 need: 0.0015

space park: 0.0094 next: 0.0066 parking: 0.0045 door: 0.0043 parked: 0.0030 do: 0.0027 traffic: 0.0025 lane: 0.0025 splitting: 0.0023 see: 0.0022

efficiency torque: 0.0059 speed: 0.0039 engine: 0.0022 highway: 0.0021 rpm: 0.0020 horsepower: 0.0016 we: 0.0016 low: 0.0015 drag: 0.0015 high: 0.0013
```

Some of those common terms are really inappropriate so I weighted by inverse document frequency to fix that:

```
color blue: 0.475 seca: 0.368 laguna: 0.352 green: 0.166 reminds: 0.160 countach: 0.156 black: 0.134 racing: 0.129 metallic: 0.129 paint: 0.124

price kbb: 0.493 trade: 0.305 credit: 0.262 offers: 0.233 told: 0.196 dealers: 0.189 negotiate: 0.185 promise: 0.174 sell: 0.172 me: 0.168
 (kbb = Kelley Blue Book)

cost parts: 0.797 shop: 0.634 labor: 0.561 he: 0.257 bearings: 0.251 vanos: 0.248 shops: 0.248 labour: 0.241 charge: 0.234 struts: 0.222

engine starter: 0.462 battery: 0.275 firing: 0.188 bay: 0.170 mclaren: 0.169 timing: 0.156 crank: 0.155 coil: 0.145 spark: 0.135 bolts: 0.135

transmission fluid: 0.820 flush: 0.140 filter: 0.119 drain: 0.118 pan: 0.112 atf: 0.103 shop: 0.101 hydraulic: 0.100 fill: 0.096 transmissions: 0.094

cargo truck: 1.000 trucks: 0.809 haul: 0.592 hauling: 0.302 people: 0.280 tow: 0.277 fit: 0.274 bed: 0.245 utility: 0.233 towing: 0.191

space park: 1.000 splitting: 0.815 lane: 0.638 cones: 0.611 traffic:
 0.490 parking: 0.482 parked: 0.287 next: 0.253 ding: 0.245 cart: 0.228

efficiency torque: 1.000 rpm: 0.871 drag: 0.697 mpg: 0.689 highway: 0.682 gearing: 0.645 engine: 0.590 epa: 0.492 force: 0.419 pushrod: 0.390
```

Side track: Using multiword queries
-----------------------------------

When looking up synonyms for "sun roof" we could use a bigram-aware IR engine for pseudo-relevance feedback. This would prefer documents that have "sun roof" rather than "sun" and "roof" in different parts of the document.

This improved synonyms for phrases but unfortunately there wasn't a way to use it in ElasticSearch synonyms. We could've used it in the overall system by running an ElasticSearch query against the web crawl data first and then expanding the original query before sending to the fact database. However, this would add an additional search to the latency of the system. (May have been quick enough but we didn't get to look into it.)

How I'd improve more

We stopped working on Searchify a while back but I thought it'd be nice to lay out what I saw as the path forwards in generating synonyms for ElasticSearch.

* Make a gold-standard evaluation of the synonym component. Get human annotated data from tasks on Mechanical Turk. Something like "Which of these words is most related to X when talking about cars?"
* Compare results from LSA, LDA, word2vec, pseudo-relevance feedback. Tune any parameters (such as the number of topics)
* Train a combination approach. This tends to be effective in machine learning and may be a way to combine general-purpose synonyms in WordNet/etc with domain-specific synonyms from LSA and pseudo-relevance feedback.
* Once the system was live we could have mined the data for query reformulations: When you search for "price" then get no results and rephrase to "MSRP" that could be used as part of the synonym engine.

What's next?
============

I'll do one more post about Searchify and the text classification component for queries like "How much is it?" or "How big is it?"

Notes
=====

(1) Calling it semantic similarity is a bit misleading. You're computing something more like "How often do these terms appear in documents with the same words?"

(2) For us this is helpful but it can be bad if you need to differentiate between different senses of a word. It's a common problem with co-occurrence methods.
