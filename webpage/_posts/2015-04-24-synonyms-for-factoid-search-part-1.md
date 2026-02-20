---
layout: post
title: "Synonyms for factoid search: Part 1"
date: 2015-04-24
---

*A while back I worked on a potential startup project called Searchify and needed to generate domain-specific synonyms. I'm finally getting around to writing that up but there may be some holes in my memory or notes.*

Advertising on mobile phones is a growing area but it's a mess. Suppose you get a full-screen ad for a car. Even if you're interested would you click on it? I wouldn't; it'll switch to a web browser, load for 20 seconds, and then I might not be able to get back to what I was doing.

The idea behind Searchify was to add a search box to the bottom of the ad. You could enter factoid searches like "price" and see a little popup with the info. You could star the factoid and then close the ad without losing your place in the app. Then come back to it later if you're still interested.

![Toyota Prius Ad with Search Box]({{ "/assets/img/posts/wp/prius-ad.png" | relative_url }})

On the backend we're searching against a Json data like this (1):

```json
{
 "Compass": "YES",
 "Clock": "YES",
 "Tire Pressure Monitoring System": "tire pressure monitoring",
 "Security (Standard)" : {
 "2 Stage Unlocking": "remote 2-stage unlocking",
 "Engine Immobilizer": "YES",
 "Power Door Locks": "remote power door locks"
 },
 "Mobile Connectivity (Standard)": {
 "Bluetooth": "YES",
 "Phone": "prewired for phone"
 },
 "Color": [
 "Super White": "F7F7F7",
 "Sea Glass Pearl": "ABBFC0"
 ],
 "MSRP": "$18000 - 25000",
 ...
}
```

The data was very noisy and required significant preprocessing: Extracting booleans, numbers, ranges, and lists from string data. Beyond that there's a degree of hierarchy so we grouped some information together to have a flat collection of documents.

But more to the point: **When someone enters "price" or "cost", how do we know to look up "MSRP"? When someone enters "red" how can we show color options? When someone enters "mileage" or "fuel efficiency" how can we show the MPG value?**

Contrast this with regular search: In document retrieval, a document mentioning price is likely to also mention MSRP or cost. For us there's often only a single keyword associated with a factoid. There's a very high chance that an arbitrary search will return zero results.

We need fuzzy search. Or put another way, we need to improve recall. In traditional information retrieval this might be handled by stemming, query expansion, and/or latent semantic indexing. (2)

ElasticSearch: solutions and constraints
========================================

Our system was designed around [ElasticSearch](http://www.elastic.co/guide/en/elasticsearch/guide/current/index.html) which provides lowercasing and [stemming](http://www.elastic.co/guide/en/elasticsearch/guide/current/stemming.html). Lowercasing will help if a query is "msrp" and we have "MSRP". Stemming will help us if we have "power windows" and the search is "window options". ElasticSearch also offers built-in spell correction which can improve recall of real-world searches.

[ElasticSearch synonyms](http://www.elastic.co/guide/en/elasticsearch/guide/current/synonyms.html) allow us to address the problem of "price" vs "cost" vs "MSRP". You can specify a mapping of original terms to a set of replacements.

ElasticSearch doesn't provide default synonym sets so we experimented with many options. In this post I'll focus on the initial experiments which failed to varying degrees.

Moby Thesaurus
==============

[Moby](http://onlinebooks.library.upenn.edu/webbin/gutbook/lookup?num=3202) is a large, free thesaurus available at Project Gutenberg. It's a large comma-delimited file with a word and possible synonyms. Seems like the perfect option for a 15-minute experiment!

In a first-day situation you don't even have evaluation data for synonym generation. You don't have evaluation data for your search system either. So I ended up generating lists of synonyms and eyeballing. That evaluation is only good for comparing systems of very different quality. (3)

Input: air conditioning

Output: adiabatic absorption,adiabatic demagnetization,adiabatic expansion,aerage,aeration,air cooling, ...

Input: heat

Output: John Law,Le Mans,a transient madness,abandon,activate,agitate, ...

Input: mileage

Output: account,aesthetic distance,allowance,assessment,bill,blackmail,blood money, ...

Input: safety

Output: aegis,arm guard,assurance,backstop,buffer,bulwark,bumper, ...

Input: cost

Output: afford,amount,amount to,bereavement,bring,bring in,budget, ...

The words skew towards extreme recall because thesauruses are meant to help writers. The lists sometimes contain useful terms such as "range" in "mileage", "amount", "expense", "price", and "sell for" in "cost".

This data might be useful in conjunction with aggressive filtering. But in many cases it lacks the synonyms we want so I gave up on it.

An old version of Roget's thesaurus is also available through Project Gutenberg. But the file format isn't meant for programming and it's much smaller than Moby.

Wikipedia redirects
===================

Wikipedia will redirect you to the correct page if you type a similar word or phrase. The "Fuels", "Feul", and "Chemical fuel" all redirect to the page for "Fuel". The page for "Seattle Sounders FC" has redirects for "Seattle MLS", "Seattle MLS team", "Sounders FC", "Seattle Sounders", etc. The redirect structure can be used to extract realistic synonyms even for things that wouldn't appear in a dictionary.

Here's [a good post on the process](http://www.behind-the-enemy-lines.com/2013/02/wikisynonyms-find-synonyms-using.html) with a web demo system and they provide a [web API](https://www.mashape.com/ipeirotis/wikisynonyms) to query redirect-based synonyms. The main problem with this process is that you need a word list ahead of time. If you have a corpus for the domain you can easily generate them all (though it takes a while). But let's get to some examples!

Input: air conditioning

Output: Air conditioning, Air conditioner, Air-conditioning, Air Conditioning, Air-conditioner, ... Central air, ... Cylinder unloaders, ... Air con, ...

Input: heat

Output: (fails because it's is a disambiguation page)

Input: mileage

Output: (fails because it's a disambiguation page)

Input: safety

Output: Safety, Safely, Safty, Saftey, Testing for safety

Input: cost

Output: (fails because it's a disambiguation page)

Overall many queries fail because Wikipedia uses a disambiguation page and we don't know which is most appropriate. We really need to do word sense disambiguation to use this but I was hoping to avoid it.

In general it failed to generate synonyms for most terms. And I began to see issues due to the domain: "windows" would be listed with "Microsoft Windows" (including all version numbers of Windows). The redirect groups tend to group all possible synonyms even when there isn't a disambiguation page.

I did one follow-up experiment on this. I took the union of all redirect sets in disambiguation pages. That clearly added way too much irrelevant junk. Then I ran web searches like *cars windows* (112 million pages) vs *cars "windows computers"* (213 thousand pages) and used the ratio of counts to help filter out terms not in the automotive domain. Although that was helpful the lists were reduced to almost nothing.

Bing related searches
=====================

Bing sometimes provides a list of related searches on the results page. Scraping it probably isn't a good idea but if it's useful enough maybe there's a paid API or publications that explain the methodology.

Input: air conditioning

Output: Central Air Conditioning, Home Air Conditioning, Heating and Air Conditioning, Mitsubishi Air Conditioning, Air Conditioning Prices, Air Conditioning Repair, Air Conditioning Installer, Home Air Conditioning Troubleshoot

Input: heat

Output: Heat Energy, Heat Movie, Rondo Traded to Heat, Rajon Rondo Trade to Heat, Rajon Rondo Miami Heat, Miami Heat, Miami Heat Players, Define Heat Energy

Input: mileage

Output: Mileage between Locations, Mileage from City to City, MapQuest Mileage, Driving Mileage Calculator, 2014 Mileage Calculator, MapQuest Mileage Distance, IRS Mileage Allowance, IRS Gas Mileage Reimbursement 2015

There are some interesting bits there but clearly the intent is for query refinement: taking a general search and helping the user to be more specific. Not useful for our needs.

What's next
===========

This will probably take 2-3 more posts to cover:

* WordNet, Wolfram Alpha
* Corpus-based methods
  + Building a domain-specific corpus by scraping reddit
  + Latent semantic analysis
  + Pseudo-relevance feedback
* Issues in testing, other scrawled notes

Footnotes

(1) The real data was messier and more verbose but I condensed it to fit in a blog post.

(2) My information retrieval knowledge is outdated. Maybe Latent Dirichlet Allocation is popular and/or derivatives of word embeddings from neural network language models.

(3) I should've discussed evaluation more. I eyeballed synonyms of 30 popular car features. After getting started it's important to transition from a quick, subjective evaluation to a more rigorous test. But that involves even more challenges.
