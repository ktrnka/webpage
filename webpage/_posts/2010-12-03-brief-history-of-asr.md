---
layout: post
title: brief history of ASR
date: 2010-12-03
---

This is the first part of a two-part article on evaluation in natural language processing.  For the first part, I'd like to focus on Fred Jelinek's ACL Lifetime Achievement Award, which has a corresponding publication in *Computational Linguistics* entitled *[ACL Lifetime Achievement Award: The Dawn of Statistical ASR and MT](http://www.aclweb.org/anthology-new/J/J09/J09-4004.pdf).*

His article tells the story of automatic speech recognition (ASR) over the years.  The beginnings are interesting biographically; Jelinek started in information theory at MIT, then tried to switch to linguistics during grad school, but wasn't allowed to.  When he interviewed at Cornell, another faculty member wanted to work with him in applying information theory to linguistics.  But by the time he arrived, that faculty member had moved on.  So he spent ten years on information theory before starting to work with IBM on speech recognition.

I can't say how encouraging his story is for me.  I wish I'd read it last year while struggling with style adaptation, or as a younger grad student (though it hadn't been written yet).  Even now as I look for jobs, it's encouraging to think that even Fred Jelinek took a winding path to explore his interest in linguistics.

Back to the story, ARPA had a competition in speech understanding in the 70s.  The best of the systems was the Dragon System, which used hidden markov models in contrast to what seems to be more rule-based systems.  Both the best and second best systems were made by grad students at CMU, which I find interesting because CMU still has an excellent group in speech recognition.

At IBM, they built a markov model that reflects the grammatical structure of a sentence (very differently than part of speech MMs).  They formulated the problem using the noisy channel model, which estimates the likelihood of the sequence of words separately from the likelihood of the acoustics based on the words.  They used relatively artificial sentences spoken in a very controlled environment for evaluation.

In the late 70s, they focused on better estimation of the likelihood of a sentence.  Their experiments used a 5,000 word vocabulary, showing the roots of ASR in restricted environments.  They were hoping to model language in a way that reflects grammar, and one of their linguists provided the quote:  "Don't worry, I will just make a little grammar."  At the time, such a statement may have seemed reasonable.  However, over the years we've seen that parsing is very difficult.  The IBM team ended up with a trigram model and had to go about the difficult task of smoothing the model.

Some of the later notes are very interesting - they used Katz' backoff at some point and also tried several methods using decision trees, but decided that the additional complexity of decision trees wasn't worth it. They hoped to use part of speech information, but found that it wasn't helpful.  (I wish I'd known this before - several researchers present it as a benefit.  I still think there's a good way to combine word and POS information.)

Another part of the picture is the problem of corpora.  If maintained by a commercial organization, prices for data might be too high.  But people needed a standard testbed.  These needs led to the creation of the Linguistic Data Consortium, which now hosts hundreds or thousands of different corpora from varying sources and containing various annotations.  The formation of Penn Treebank in particular pushed researching in parsing and part of speech tagging forward.

If you're a student of language modeling or struggling in a young academic career, I strongly suggest reading the paper.  It's short and a great pick-me-up.

 

This article gives a great overview of the history of language modeling, and shows some of the progression of NLP overall.  Older designs were often based on simplified tasks and tended to be rule-based or require knowledge bases.  When more data became available with the LDC and the Internet, the field moved to evaluation-heavy methods.

In the next piece, I'll explain my perspective on the role of evaluation in NLP.  I'll also try to highlight many of the difficulties of evaluation.
