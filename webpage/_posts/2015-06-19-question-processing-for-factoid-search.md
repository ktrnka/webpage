---
layout: post
title: Question processing for factoid search
date: 2015-06-19
---
Searchify was a project to enable quick factoid lookup on mobile advertisements. A full screen ad would have a search box and you could get quick answers without leaving the ad or even the app. Previously I've written about [building synonyms for automotive in Searchify](https://kwtrnka.wordpress.com/tag/searchify/).
One problem we faced is similar to web search: Will users prefer keyword search (e.g., "price") or full question search (e.g., "How much is it?")?
I'll cover this in three sections: 1) trying to get user data 2) separating questions from keyword search and 3) extracting useful info from full questions.

Will people actually enter questions?
=====================================

<!-- KT TODO: Repair the category links in the future -->
Previously we worked on [Swype](http://www.swype.com/); we're intimately familiar with mobile text input. Usually people cut corners and write short messages when possible. If you're typing then keyword search is easier. But if you're using speech recognition it's less clear. It'll recognize full sentences better and there may be a preference for full questions.
If possible it's best to look at data. But without a live system there's no data coming in. So I made a mock image of the system and used Mechanical Turk to solicit example searches. I iterated on this and learned several [tips for Mechanical Turk](https://kwtrnka.wordpress.com/category/mechanical-turk/)
![Mechanical Turk HIT for Toyota Prius Searchify ad]({{ "/assets/img/posts/wp/prius-hit.png" | relative_url }})
I tried to keep the directions short and tried not to lead users into giving questions vs keywords. I also ran a second version specifically asking for questions rather than searches.
This task was extremely informative. Notes:

* 10% of responses (101/991) were questions with general directions "What would you search for?"
* 98% of responses (646/658) were questions when users were specifically asked for questions. "Ask questions about a car ad"
* Some small percentage didn't follow the directions regardless of what I did. Things like blank fields, including "Toyota Prius" in the search, etc.

Unfortunately, this sample is biased towards people typing on a computer. We can't make definitive conclusions except that probably we should handle both keywords and questions.

Identifying questions
=====================

Full questions *sometimes* work in ElasticSearch because any [stopwords](https://en.wikipedia.org/wiki/Stop_words) are filtered out. But not all of the question words are in standard stopword lists. A word like "how" might be filtered but "much" not.
Keyword searches can be sent directly to ElasticSearch without processing. But any questions need to be preprocessed and the keywords should be sent to ElasticSearch. In other words, we need to first identify questions.
At first we just looked for a question mark, but people don't always enter one. Then we expanded to a list of unigrams/bigrams at the start of the search. I couldn't find evaluation numbers for this, but I remember there were a few unexpected cases like "car safety rating?" or "miles per gallon?".
We implemented a simple system so that we could spend our time on more important problems. In the context of a prototype this was the right decision. But if we expected to quickly scale to different domains and languages I would've set it up as logistic regression or another simple classifier.

Classifying questions
=====================

Given a question like "How much is it?" we need to know to look up the price. None of the words in the question clearly indicate this though.
The closest academic work we found was by Li and Roth, who provide their [question classification dataset online](http://cogcomp.cs.illinois.edu/Data/QA/QC/). The nice thing is that each question has a two-part answer type, like NUMERIC/money or NUMERIC/count. The unfortunate part is that the [answer types](http://cogcomp.cs.illinois.edu/Data/QA/QC/definition.html) don't cleanly align to our data.

Experiments on the Li and Roth data
-----------------------------------

Several academic publications use this dataset and achieve good accuracy. We unfortunately didn't have enough time to compete with such strong approaches but it gave us a reasonable upper bound on performance.
We used two very simple approaches to classify questions. In both we lowercased and tokenized the question roughly following Penn Treebank tokenization. We also added a period as the first token to handle start of question.
The first approach was to extract unigrams, bigrams, and trigrams from the question and use them as binary features in logistic regression using [scikit-learn](http://scikit-learn.org/stable/). This is extremely simple approach and would be more of a baseline in academic work.
There were concerns that this would be too slow or overfit the data so we also had a model that used the first word, two words, three words, four words of the question. The goal was to classify purely based on parts like "how much".
We split the data 80/20 and evaluated on the held out data. We also evaluated on the training data to help understand how much we're overfitting.

|  |  |  |
| --- | --- | --- |
| Two-part classes (50 classes) | On test data | On training data |
| Predict majority | 17.3% | 17.7% |
| Predict by first word only | 33.5% |  |
| Logistic reg on uni/bi/tri | 76.2% | 97.9% |
| Logistic reg on start of question uni/bi/tri | 56.5% | 62.5% |
|  |  |  |
| One-part classes (6 classes) | On test data | On training data |
| Predict majority | 22.9% | 22.9% |
| Predict by first word only | 50.4% |  |
| Logistic reg on uni/bi/tri | 84.0% | 98.3% |
| Logistic reg on start of question uni/bi/tri | 68.5% | 73.7% |

Even these simple approaches are significantly better than predict majority and predicting using just the first word. But they're clearly overfitting the training data: there's a big gap between accuracy on the training and testing data.

Domain adaptation to car factoid search
---------------------------------------

We also have a smaller corpus of questions for Searchify solicited from ourselves as well as Mechanical Turk workers. One quick test is to run the classifier on our questions.
Unfortunately we found a lot of questions labeled as HUMAN:individual. This is the most common question class in the Li and Roth data set so it makes sense for the classifier to default to the training set majority.
But those labels on our searches had 0% accuracy. Many others were labeled as DESCRIPTION:manner which was incorrect. Some classes were very accurate though, like NUM:count, NUM:date, NUM:money, NUM:period (period of time), NUM:volsize, and LOCATION.
We had someone annotate our question data for answer types and found a disconnect; many are yes/no questions but the Li and Roth data doesn't have that type. So we added a few answer types.
The second problem is that our annotator didn't use Li and Roth labels when appropriate, so some questions were assigned "number" without the second part label or "description". To address this problem, we ran the classifier from Li and Roth training data over our dataset and if the annotation was "number", we would find the most probable NUM:... label and relabel the data.
We also combined our data with the Li and Roth data but duplicated our questions to balance the size of the data sets. It's a cheap trick to make sure the classifier isn't skewed towards the Li and Roth data (which was the larger data set).
Even still, many errors remained. HUMAN:individual was always an incorrect classification. There were also problems in wording, such as "What's the curb weight?". This was annotated as a number but the classifier gave ENTITY:term (without domain adaptation) or description (with domain adaptation). The problem is that "What's the" in the Li and Roth data is usually asking for definitions or terms.
I didn't get the chance to do a nice evaluation because I was mostly dealing with bug reports like "how much does" should give NUMERIC/money and similar things. Things got hectic and I ended up shifting to extracting keywords.

Keyword extraction
==================

Ideally we need to extract keywords from the question and send them to ElasticSearch. For example, given "What type of engine does it have?" we want to search for "engine" or maybe "type of engine".
I did a proof-of-concept test to see if we could solve it with shallow methods:
1) Extract tail (the end of the question)
2) Extract middle
3) Inverse document frequency over the questions
(If I had to solve this again I might start with sequence labeling because it can represent more complex ways of extracting keywords.)
What I found was that the relevant keywords could be extracted successfully by each method:
Extract tail: 34/52
Extract middle: 43/52
IDF\*: 50/52
\* I can't figure out what IDF threshold I used so this may be optimistic.
Overall one thing I felt is that IDF had the potential to mostly solve the problem if we compute the IDF score over the set of example questions (we'd need to hold out data for evaluation though).
A few examples with the keywords we want underlined:
How much horsepower does it have?
What's the miles per gallon?
How many miles does it get per tank?
How big is the battery?
Note that there's some interaction in system design between question classification and keyword extraction. In the case of "How big is the battery?" we may not want the keyword "big" if the question type is NUMERIC/size.

Using the non-question data to help the question data
-----------------------------------------------------

When I started to write code to productize keyword extraction, I realized is that we wanted to convert the question data to be more like the non-question data.
So I tried another approach: What if I only extract keywords from questions that commonly appear in keyword searches? This worked surprisingly well!
There was one problem though: Toyota and Prius were often labeled as important keywords because they sometimes appeared in junky keyword searches. It helped to remove those.
Some examples of good labeling with this method:

```
what is the <terms>engine</terms> ?
what 's the <terms>gas mileage</terms> of a prius really ?
what is the typical yearly <terms>maintenance cost</terms> ?
what are the most <terms>common repairs</terms> for this vehicle ?
what are the details of the <terms>warranty</terms> ?
```

Even in the good cases sometimes the nuance of the question is lost. When asking what that real mileage is, they're saying that they doubt the official numbers. Similarly when asking for details of the warranty, they're asking for more than just the basic info.
Some examples of bad labeling:

```
how many people does this <terms>car</terms> seat ( is it a 2 door or 4 door ?)
how many cylinders does the <terms>engine</terms> have ?
how much horse <terms>power</terms> does it have ?
```

Sometimes the question isn't something you can easily ask in a keyword search (like the first one). In the cylinders case, our keyword data is just too sparse. In the third example, usually people spelled horsepower without a space so it wasn't identified.
More data would help this approach. If I could do this again I would've solicited more keyword searches from Mechanical Turk. If there were lots more time, formal evaluation would allow experiments in other approaches. I bet you could get far by indexing the keyword searches in LSI with gensim and using the questions to search the keyword database. Then send the best keyword search to the real ElasticSearch.

Conclusions
===========

This work was fun but we didn't put in enough effort to build a good question-handling system. Things we should've done to achieve good results:

* Design a superset of Li and Roth classes to cover our domain
* Annotate a larger data set for question types
* Sequence labeling for keyword extraction (but with so little data, the features may have needed to be more general than words)
* We didn't look into how to integrate this into the full system enough. For instance, any NUM question should boost up numeric results. NUM:money would just add keywords like "price" and "MSRP". This should have been all automated.
