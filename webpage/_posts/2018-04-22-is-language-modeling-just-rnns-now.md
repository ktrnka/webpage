---
layout: post
title: Is language modeling just RNNs now?
date: 2018-04-22
---

Language modeling is as much "just RNNs" as self driving cars are "just ConvNets." It's all the bits that you build on top of your function approximator, whether that's an ngram model or recurrent neural network.

### A little context

I was asked about this because my background is language modeling for text entry. My thesis work was in word prediction/completion for assistive technology and then I worked on mobile text entry for years at Swype and Nuance.

The field of language modeling has mostly switched from traditional ngram models to recurrent neural networks in the past few years. Traditional ngram models are basically giant lookup tables: How often did word *w* occur after the previous two words? Researchers work on how to deal with unknown sequences of words, trying to provide a smoother guess at the next word.

Recurrent neural networks on the other hand compute a smooth representation of the context and a smooth representation of each word and use that to predict. They're much better at generalizing and they can also look further back in the sentence.

They have some practical benefits as well: They have more explicit ways to encourage generalization such as dropout. They can take advantage of pretrained word embeddings (word2vec, glove, fastText) which even enables a degree of transfer learning. Memory usage is strongly bounded and predictable. And they take advantage of the more general machine learning community: Progress in optimization or parallel processing transfers between RNNs and other neural networks. And we can benefit from research such as LSTM or GRU.

That said, the benefit isn't free: They can take much longer to train. At large scale you sometimes see a swing in the other direction such as Google's [stupid backoff](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.324.3653) which just throws out the math and does something that's computationally scalable.

There are two themes to this post: 1) There are many problems that are about language modeling in general, not about ngrams vs RNNs 2) There are situations in which one approach or another is better.

Also note that my perspective is highly biased by text input. I'm more concerned with running language models on a phone than a server, unlike speech recognition or machine translation.

### Situational differences between ngrams and RNNs

Let's start with compare/contrast.

#### Vocabulary size and multilingual issues

Back at Nuance we tried using Mikolov's rnnlm toolkit but there was a hard max of 64k words in the vocabulary. That's reasonable for English (we had about 90k words) but NOT OK for any language with compounds like German and TOTALLY NOT OK for more inflected languages like Turkish, Hungarian, or Finnish.

Let's talk about German first. You can make a decent model with maybe 200k words in the vocabulary. In the ngram world, it's easy to use 200k words without performance issues. After all, it's just a giant hash table.

But that's more difficult for RNNs. In particular, the softmax becomes the limiting factor. With 500 hidden units you have a 501x200,000 weight matrix just for the output. One solution is to cluster the vocabulary and factor the prediction into [predicting the cluster first then the word](https://arxiv.org/pdf/cs/0108006.pdf).

The more scalable approach is [hierarchical softmax](https://pdfs.semanticscholar.org/39eb/fbb53b041b97332cd351886749c0395037fb.pdf#page=255). It's not trivial but there are many [good variants](https://code.facebook.com/posts/1827693967466780/building-an-efficient-neural-language-model-over-a-billion-words/) and it's an area of ongoing research.

An older solution is to use a **mixture of ngram and RNN models**. You train the RNN for the most common words and interpolate with the ngram model. Or you backoff from the RNN model to ngram model when the RNN predicts OOV. I've seen these tricks many times from back when NNLMs were the hot research area so I'm not quite sure who to cite but [Mikolov et al 2011](https://www.researchgate.net/profile/Lukas_Burget/publication/241637478_Strategies_for_training_large_scale_neural_network_language_models/links/542c14960cf27e39fa922ed3.pdf) seems like a safe bet for RNNs.

The downside is that you're adding complexity. That's ok for your training code but maybe not if you have to implement this on a device. TensorFlow in particular has made great progress in this regard, supporting Android and iOS.

These approaches don't work well for highly inflected languages like Hungarian, Turkish, Finnish, and Korean. Nor does the plain ngram model for that matter. In these languages, you can't even store a word list with 90% coverage on a phone.

The most traditional approach is to split words up into morphemes and do a **language model over morphemes**. I vaguely remember a paper showing excellent improvements by interpolating a word model on common vocabulary with a morpheme-based model in the era of ngrams either for Arabic or Turkish. This would likely work even better with RNNs.

**Character-based RNN**: This works much better than a character-based ngram model though it may take some [extra effort](https://arxiv.org/pdf/1511.06303.pdf) to get it to [work well](https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/viewFile/12489/12017). The advantage is that it handles complex morphology all by itself. The disadvantage is that they don't work as well as word-based models for most languages.

Interpolate **short-list word model and open-vocab char model**: This seems like the natural progression from the previous two notes. I don't think I've seen this and the reason is that there may be better ways.

[Short list word embeddings and **predict word embeddings from characters** for OOV](https://arxiv.org/abs/1604.00788). It's a very elegant solution to the problem. I'm not exactly sure how you get true probabilities out of it but in the worst case you can use sampling.

#### Memory/disk size

Your model has to work somewhere. For apps, memory is a major concern: If you use too much it can slow Android down and/or your process gets killed and restarts often. In contrast to a server where you might have a 1gb model, on the phone you might have a 10mb model.

For an ngram model you have to get clever about pruning the least helpful ngrams and storing values in fewer bits. All of this takes manual effort.

It's much better in RNNs though; you can simply train them at reduced floating point precision from the start, which often speeds up training anyway. The number of parameters doesn't change during training so you can decide on your memory budget before even training it. And if you're doing hyperparameter tuning, it's pretty easy to optimize to balance size and accuracy.

#### Predicting in-order vs out-of-order

Plain language models are just giant lookup tables. If you want to change a word in the middle of the sentence it's about the same cost to recompute probabilities. For an RNN though you need to reprocess the whole sentence. In a keyboard this is a problem because you can click on any word. You *really* don't want to do processing proportional to sentence length when clicking on a word. I made that mistake once at Swype on a feature called Smart Editor, leading to slowdown in certain apps with long sentences.

#### First-pass vs second-pass decoding

This is common in big production systems like speech recognition. Often they have an enormous lattice of possibilities and want to prune that down to the likely ones. It's too big to use a slow model like an RNN though. So you use a very simple/fast ngram model like a bigram model.

Then on the second pass you use the better but slower model. This concept comes up in almost every large machine learning system to reduce latency/cost: Quick first-pass pruning with a high recall method followed by accurate second-pass with high precision method.

So even if you have a great RNN, you still need an extremely fast model for your first pass.

#### Software support

This is one that limited me. Our client-side code supported ngrams but not RNNs. We had a lack of engineers on the core code and generally the organization was risk-averse. In a new project or an organization with plenty of funding that's no prob though. And now there's TensorFlow.

#### Parallelization

Ngram models are easy to parallelize; the tokenization and counting are very suited for Hadoop and similar systems. RNNs have historically been more difficult to parallelize but there's been great progress in areas like asynchronous SGD and similar methods.

### Semi-situational

We're starting to move into topics that are general language modeling but with small differences between ngrams and RNNs.

#### Personalized language models

In applications like typing on your phone, there are huge gains from maintaining a language model that's trained iteratively from the user's text. I've seen results up to about 50% improvement, though at Swype on average it might've been more like 20% average and depended on how much you type. Here are a [couple](https://dx.doi.org/10.1109/34.56193) [classic](https://dl.acm.org/citation.cfm?doid=112405.112464) citations.

The easy way to handle this is to use an user-specific ngram model and a generic RNN and do a weighted average.

RNNs themselves just aren't fast enough to train on device. But you still have *some* options. For example, you could cluster your user population and use that as a feature for the RNN.

Even so, this isn't sufficient to adapt to the user's vocabulary. Most RNNs are word-based and trained with a fixed vocabulary in mind. If you want to add a new word like "schwifty" to the words that can be used as context or prediction, you need to retrain from scratch.

That leads me to another issue:

#### Not every language has spaces…

In English we might split on spaces and punctuation to get a list of words. This works well for many languages. Though it still leads to problems like "dataset" vs "data set". That little space between the words means that any word-based model will represent those two *very* differently.

Languages like Chinese, Japanese, Korean, and Thai are not so simple. They have clear concepts of words but don't use spaces. So you have a few options:

Build a word segmentation system and use it as preprocessing. This can work if the input isn't building up one character at a time. But I dislike it; it's introducing a source of errors just to try and reuse the same code as English. It's the kind of thing you do when you start in English and have to add Chinese in a rush later.

Option 2: Always process a lattice. This approach combines the word segmentation with the language modeling. It's easy to update every time a character is added. I also like it because the same idea works for conversion engines, such as romaji to kanji/kana in Japanese. Fundamentally it's about representing uncertainty in the input sequence.

Or you can use a character-based RNN. They aren't the same quality as word RNNs but probably better than relying on word segmentation.

#### Privacy of user data

Suppose that you've collected user data. You may want to update your ngram models with statistics from that data, but how do you protect privacy? For the vocabulary, one check is to see how many distinct users use a word. If it's just one user it might be private information like a password or social security number. But if 100 users use a word it's probably not private.

That's just the basics though. You run into the same issue at the ngram level. Suppose the data includes "the netflix password is tunafish". Each of those individual words may be used by hundreds of users but the sequence has only been used by one or two and you want to prevent that getting into a released language model.

With an RNN it doesn't store the actual words or phrases so it may seem safe. Recent research shows that RNNs can end up [memorizing secrets](https://arxiv.org/pdf/1802.08232.pdf).

### RNNs don't save you from this

#### What counts as a word anyway?

Someone's gotta decide what counts as a word. Short list of industry experiences:

1. Is your model case-sensitive? In English this can be debatable but in German some words differ only in capitalization.
2. Do you support accents? Are they optional, required, ignored? For instance, do you allow someone to enter fiancee or do they have to enter fiancée? This is considerably worse in Spanish; many users just give up on proper accents due to QWERTY keyboards.
3. Do you limit to formal words only or do you need common texting words, like lol?
4. Are lol, loll, and lolll the same word or different words?
5. Do you compensate for other weaknesses by removing confusables from the vocabulary? For example, removing *thee* from the vocabulary greatly improves typing accuracy. For swyping we had to remove "Getty" because people kept getting it instead of "get".

#### What counts as a language?

Are French and Canadian French different languages? I'm not asking the linguistic question but rather do we need one language model or two? If we want two, do we have enough training data for Canadian French to be better than using the other French model?

I'm optimistic about the future of language modeling with RNNs; there's been [some work](https://arxiv.org/abs/1611.04558) that uses a single model for all languages. It allows for better sharing across languages and enables machine translation between pairs of languages for which no aligned data is available.

#### Task-specific or task-independent models?

I've never seen a language model that was entirely task-independent. Meaning that I've always seen assumptions specific to speech recognition built into language models for speech, such as how numbers are represented. At Swype we ended up making tweaks specific to our task too.

But why stop there? You can train models specifically to improve your task. We could've had a language model that used more capacity on the confusable words and less on words that weren't confusable. That's an easy way to improve accuracy. Even something as simple as a perceptron can be used for [discriminative language modeling](https://dl.acm.org/citation.cfm?id=1218962).

#### Data quality

This comes up in almost any kind of machine learning and language modeling is no different. Let's suppose for instance that you're using web scraped data. Again these are industry experiences:

1. Filtering out porn and any other content the businesspeople worry about. If you're lucky you can have one classifier to do this but you might need a different one for each language.
2. Deduplicating content. There are almost always bugs in web scrapers that cause duplicates, which down the line leads to severe bias in language models. This can also unintentionally circumvent privacy filters.
3. Character encoding. Webpages sometimes indicate their encoding and sometimes provide misleading indicators of encoding. Another job for text classification.
4. Poor standards. Burmese has a Unicode definition but [Zawgyi](https://code.google.com/archive/p/zawgyi/wikis/WhyUnicode.wiki) is more common, which is a slight redefinition of certain codepoints. It isn't even a clean mapping; there are characters in both that can only be represented with combining characters in the other. Another example is [s-with-cedilla and t-with-cedilla in Romanian](https://archives.miloush.net/michkap/archive/2011/08/24/10199324.html).
5. Language detection. How do you even know you're crawling Tamil? There's a great Python module called langid these days that has a very long list. But one thing to worry about is that you're really identifying a language plus script. Serbian for example can be written in either Latin or Cyrillic script. Macedonian is written in Cyrillic and is related. If your language identifier only identifies Serbian in Latin script, you end up getting a mixture of Serbian Cyrillic and Macedonian identified as Macedonian.
6. Finding the right kind of data. Historically we use whatever kind of data we can find. Wikipedia is a good start but it's overly formal. If you train a text-entry system on Wikipedia you'll notice an abnormally high error rate around words like "I", "you", "me", which are some of the most common words in informal English. For text entry I found that Twitter was much better but introduced offensive content. You can try to filter out data with swears but inevitably you deal with multiword expressions like "die in a fire."
7. Removing formatting info. Usually this is easy but occasionally you spend a couple days fixing a rare html/formatting stripping bug.

### Closing thoughts

Language modeling is as much about RNNs now as it was about ngrams before. It takes considerably more effort than simply running an off-the-shelf toolkit. That said, our language models are now considerably better than they used to be.

#### Assorted other links

- [Exploring the Limits of Language Modeling](https://arxiv.org/abs/1602.02410)
- [On the State of the Art of Evaluation in Neural Language Models](https://arxiv.org/abs/1707.05589)
