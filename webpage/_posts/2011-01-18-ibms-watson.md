
---
layout: post
title: "IBM's Watson"
date: 2011-01-18
---
In case you haven't heard of it yet, IBM developed a deep QA system called [Watson](http://www.research.ibm.com/deepqa/).  They've had a medium-sized team working on it for about 4 years.  Among others is Jennifer Chu-Carroll, who received her Ph.D. from the University of Delaware under Sandee Carberry (who was part of my Ph.D. committee).
[youtube=http://www.youtube.com/watch?v=FC3IryWr4c8]
We'll have to wait until February 14-16 to see its actual performance, but the rumors say that it's very good. Good enough to have the news and blog sphere making SkyNet/singularity/etc analogies.  For example, see [the Atlantic Wire](http://www.theatlanticwire.com/opinions/view/opinion/World-Terrified-of-Jeopardy-Dominating-Supercomputer-6563) (which has many links).
IBM probably has some very interesting technology in there.  The speech recognition alone is impressive, especially recognizing names and their spellings. (This requires more than just an ngram model)
Deep natural language understanding is incredibly difficult and is never finished.  There will always be some awkward syntax that our programs can't parse/tag/etc.  Or an obscure idiom.  Or extreme cases of polysemy. For Jeopardy especially, there are difficulties in determining the "hole" that the answer leaves.  The answer isn't always an exact answer to a Who/What is type of question.
All that said, I'd like to view IBM's excellent work in context.  This isn't SkyNet.  It's a specialized QA system and it still makes plenty of mistakes.
For reference, I'm comparing Watson to the most basic baseline I can come up with:  I type the answer into Jeopardy with "wikipedia" in front.  Then I assume the top result is the answer.  To convert to a question, we could check the first paragraph for keywords, or do a Google battle "Who is X" vs "What is X", or use named entity classification.  (Someone might criticize about the Internet connection, but you could just download a data dump of Wikipedia)
For evaluation, all I have is IBM's YouTube video (unless I can find the real questions from the show).  There are 5 questions I could clearly hear in the video:

1. David Hume held this view that sense and experience are the sole foundation of knowledge.
   Question:  *What is empiricism?*#1 Google result:  *[Empiricism](http://en.wikipedia.org/wiki/Empiricism)*The interesting thing about this question is how to decide on the spelling *Hume*.  Would *Hume* even be in the lexicon?  If they're using a good corpus, yes.
   Probably part of what Watson is doing is using the less ambiguous parts of speech to query and build a more focused language model, which has a better chance of spelling it *Hume*.
2. After Germany invaded the Netherlands, this queen, her family, and cabinet fled to London.
   Question:  *Who is Wilhelmina?*
   #1 Google result:  *[Wilhelmina of the Netherlands](http://en.wikipedia.org/wiki/Wilhelmina_of_the_Netherlands)*
3. This US President negotiated the Treaty of Portsmouth, ending the Russo-Japanese War.
   Question:  *Who is Theodore Roosevelt?*
   #1 Google result:  *[Treaty of Portsmouth](http://en.wikipedia.org/wiki/Treaty_of_Portsmouth)*
   This one favors Watson greatly.  Even if we knew that it was a "Who is X" question, the top wikipedia person result isn't a US President.  If the search results were limited to US Presidents, I bet it'd work.
   It's possible that a simple pattern with the keyword *this* would be able to determine these types of restrictions:  All three answers so far use *this* to label the target.  Also, there are some speech recognition problems here.  I don't know if there are other spellings of *Portsmouth*, but there might be.  It may also be difficult to know to transcribe as *Russo-Japanese*.  The capitalization of *President* and *Treaty* may or may not have an affect on their processing, but it's a difficult decision if so.
4. A famous red-quaft clown or just any incompetent fool.
   Question:  *Who is bozo?*
   #1 Google result:   *[List of clowns](http://en.wikipedia.org/wiki/List_of_clowns)*
   First off, I've never heard of whatever word comes after red.  My first guess at the spelling doesn't occur in any dictionary I have, but none of my other guesses do either.  The closest the baseline method gets is if you use a space instead of a dash, a dictionary link is #3 for [bozo](http://www.dictionary30.com/meaning/Bozo).
   Secondly, I'd like to point out the interesting NLP here.  The answer is a noun phrase rather than a full sentence, which might suggest that a dictionary may be more useful.  In this case, I'd say that the first part isn't enough information to guess *bozo*.  Using both parts for different constraints might be necessary, which can make this quite difficult.
5. In REM's "It's the end of the world as we know it", two of the men with the initials LB.
   Question:   Pick two of:  Leonard Bernstein, Leonid Brezhnev, Lenny Bruce and Lester Bangs
   Question (Watson's):  *What is "I feel fine"?*
   #1 Google result:   [the song page](http://en.wikipedia.org/wiki/It's_the_End_of_the_World_as_We_Know_It_(And_I_Feel_Fine))
   #2 Google result:  [Lenny Bruce](http://en.wikipedia.org/wiki/Lenny_Bruce)
   #3 Google result:  [Lester Bangs](http://en.wikipedia.org/wiki/Lester_Bangs)
   Watson got this one wrong.  It's debatable whether my suggestion would get it right or not.  On one hand, you could say that it's reasonable to filter results that appear in the answer.  On the other hand, matching those pages might involve a little work.  I'll give the baseline half credit cause it's debatable.
   That said, I have to highlight some of the difficulty of speech recognition here.  Should you write "REM" or "R.E.M."?  Should you write "LB" or "L.B."?  How would speech recognition know that a song title is normally placed in quotes?  These things don't seem to matter to Google, but they could matter to IBM's deep QA.

IBM's Watson:  4/5
------------------

Baseline:  2.5/5
----------------

This is just an example; the evaluation set here is really too small to say much of anything.  That said, I'd like to point out that we can achieve decent results even with basic wikipedia queries.  We could probably do better with some simple additions:  using the *this* keyword along with NP chunking to find a category, classifying the answer by grammatical constituent, and filtering results that already appear in the answer.
Let me be clear:  IBM has put some excellent research into the development of Watson.  I can't say how good it is without knowing what it's doing, but there's definitely something there.  I decided to write a simple article like this to put Watson in perspective.  It's good, but definitely not the sort of thing I'd use SkyNet analogies for.
*Note:  If I can get a typed list of the full questions/answers from the shows in February, I'd be happy to evaluate this kind of simple baseline.*
