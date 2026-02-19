---
layout: post
title: Wolfram on Watson, etc
date: 2011-02-02
---
As the semester approaches my free time and energy have been dwindling, so I'll probably be terse for a while.
I recently came across [a critique](http://blog.stephenwolfram.com/2011/01/jeopardy-ibm-and-wolframalpha/) of IBM's Watson by Stephen Wolfram of [Wolfram|Alpha](http://www.wolframalpha.com/).  He has some interesting things to say about the task and Watson, but I'll focus on the rough baseline they crafted.
They took a random sample of Jeopardy clues from a database of 200,000 and fed it as input to various search engines. Then they counted the number of times the answer/question could be found in 1) the top page result (either title or full text) or 2) the first page of results (either titles or text snippets). Sites specifically about Jeopardy were excluded.
The short story of the data is that Google fares best in both setups. Interestingly, Google and Bing are almost tied in the first task (first page only), which matches the recent controversy of Bing using Google's top ranking. In contrast to [my baseline](/blog/2011/01/ibms-watson/ "IBM's Watson"), they find that Wikipedia search performs poorly (though I'm guessing they're using the on-site search rather than Google on the Wikipedia domain). In contrast, if they only use the title of the first search result, they correctly solve 20% of the clues. This is much closer to my baseline.
Wolfram notes that they're only approximating a baseline. It can't actually do Jeopardy. You'd need a way to decide upon a single answer based on the results and then transform it into the appropriate question. A real system also needs some sort of confidence score. It needs to know when to answer and when not to.
On a side note, the baseline given seems like the precision of the average human (60%) and Ken Jennings (79%), but this isn't really a fair comparison, because the proposed baseline doesn't have a way to decide not to answer.
The best part of the article for me:

It's yet another example of how something that seems like artificial intelligence can be achieved with a system that's in a sense "just doing computation" ...

Artificial intelligence is like a magic show. You're pretending to do something insanely difficult (or impossible), and because it's done well enough the audience can't tell the difference.
Another interesting note is that he's really advocating Wolfram|Alpha's approach - curated knowledge. I doubt that's free, but I wonder whether OpenCyc or OMCS would be useful?
