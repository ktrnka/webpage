---
layout: post
title: Reading list for text classification, 2018
date: 2019-01-07
---

Motivation: Help new teammates come up to speed faster and ensure that we're on the same page.

### Text is a whole new challenge

I'm assuming that you have some familiarity with more traditional machine learning. For example, we might predict housing prices by number of bathrooms and square footage. This kind of data has a fixed number of inputs or features.

In text classification, the input to your model doesn't have a fixed length -- one document might be 100 words and another might be 1000 words. And the same model must work on both!

The other challenge -- the range of possible inputs is enormous. With even a small housing price data set we'd expect to see 99% of the range of possible values. Maybe our model will give bad outputs for rare outliers.

In contrast, a text data set will not even contain 99% of the words of the English language. Your model will be surprised with new words *very often*.

It certainly won't contain 99% of the possible sentences you can make in English -- maybe more like 1%. And worse yet, it won't even come close to sampling from all possible documents.

#### Summary

There are two core challenges in text classification that are unusual:

1. How do we convert a variable-length input (text) into a fixed-length input (list of numbers)?
2. How can we mitigate the [curse of dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality)? (we've only sampled 1% or less of the possible inputs)

### Reading list

This is going to be a very link-heavy post. I'm hoping to give you enough pointers for a nearly complete survey of the field or at least a good try.

#### Model architectures

Neural networks are overhyped. [Always start with a basic linear classifier](https://dl.acm.org/citation.cfm?id=2390688). In scikit-learn, this will often get 90% of the quality of a neural network with 1% of the effort:

```python
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegressionCV()
)
```

The authors of scikit-learn have done a wonderful job of making this easy and fast. And there are several useful parameters you can tweak if you want slightly better quality: ngram_range, min_df, sublinear_tf, and tokenizer/preprocessor options just to name a few.

To understand why this works so well you should learn about:

- [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- Why you should throw away rare words: At best they slow down training and at worst they lead to overfitting
- L2 regularization in the context of logistic regression/SVM
- [Cross-validation for hyperparameter tuning](https://stats.stackexchange.com/a/357761)
- Why [normalizing your inputs is important](https://stackoverflow.com/questions/4674623/why-do-we-have-to-normalize-the-input-for-an-artificial-neural-network) for gradient-based machine learning
- Ngrams: This helps understand the text better, but can lead to overfitting.
- Second-order optimization methods like L-BFGS: This is almost always a big improvement over first-order methods like stochastic gradient descent.

Practitioners are often unsatisfied with bag of words/ngrams because it seems so dumb. So I'll spend the rest of the post surveying reading for neural network approaches. You might be able to get a strong baseline in three lines of code and an afternoon, but it'll take much more to beat the baseline with neural networks.

The challenge of variable-length input isn't something we can ignore. There are roughly four options to learn a mapping from a text into a fixed-length numeric representation:

1. Bag of words or bag of ngrams
2. Recurrent neural networks, such as LSTM and GRU
3. Convolutional neural networks
4. Attention

#### Bag of words/ngrams

This has been the standard approach since the 90s. Any old textbook should cover Naive Bayes, for instance. These are a few recent papers in the area.

Wang, S., & Manning, C. (2012). [Baselines and bigrams](https://dl.acm.org/citation.cfm?id=2390688). In ACL.

Iyyer, M., Manjunatha, V., Boyd-Graber, J., & Daumé III, H. (2015). [Deep Unordered Composition Rivals Syntactic Methods for Text Classification](https://aclanthology.org/P15-1162). In ACL.

Li, B., Liu, T., Zhao, Z., Wang, P., & Du, X. (2017). [Neural Bag-of-Ngrams](https://pdfs.semanticscholar.org/0841/57df67618cae20de3c484d6477fd48601d46.pdf?_ga=2.127441229.1599049180.1524348587-1436306365.1524348587). In AAAI.

#### Recurrent neural networks

Around 2010-2013 the NLP community switched to recurrent neural networks for state of the art research. The community gravitated towards LSTM over vanilla RNN or GRU.

I don't have good citations from this time, but [this blog post](https://karpathy.github.io/2015/05/21/rnn-effectiveness/) and [this one](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) may help for a general introduction. There are certain core concepts that you should know if you intend to work with recurrent neural networks:

- backpropagation through time (BPTT) and truncated BPTT
- LSTM vs GRU vs plain RNN
- how to use them for classification (many-to-one)
- bidirectional models

One challenge was that they had *so many hyperparameters* and they took a long time to train. We didn't have good guidelines on how to configure them until this paper came around:

Longpre, S., Pradhan, S., Xiong, C., & Socher, R. (2016). [A Way out of the Odyssey: Analyzing and Combining Recent Insights for LSTMs](https://arxiv.org/abs/1611.05104).

#### Convolutional neural networks

Recurrent neural networks are often very slow, even with GPU acceleration. This motivated the field to explore convolutional neural networks, which is akin to moving a sliding window over the input. Researchers have found similar quality but they're 5-10x faster to train.

Yoon Kim. (2014). [Convolutional neural networks for sentence classification](https://arxiv.org/abs/1408.5882). In EMNLP.

Zhang, Y., & Wallace, B. (2015). [A Sensitivity Analysis of (and Practitioners' Guide to) Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1510.03820).

Conneau, A., Schwenk, H., Barrault, L., & Lecun, Y. (2017). [Very Deep Convolutional Networks for Text Classification](https://doi.org/10.1007/s13218-012-0198-z). In EACL.

#### Other notable approaches

These don't nearly cover the whole field, only the most impactful ideas I've seen and used.

Xiao, Y., & Cho, K. (2016). [Efficient Character-level Document Classification by Combining Convolution and Recurrent Layers](https://arxiv.org/pdf/1602.00367.pdf).

Zhang, Y., Roller, S., & Wallace, B. (2016). [MGNC-CNN: A Simple Approach to Exploiting Multiple Word Embeddings for Sentence Classification](https://arxiv.org/abs/1603.00968). In NAACL.

Wang, Z., Hamza, W., & Song, L. (2017). [k-Nearest Neighbor Augmented Neural Networks for Text Classification](https://arxiv.org/abs/1708.07863).

Yin, W., Kann, K., Yu, M., & Schütze, H. (2017). [Comparative Study of CNN and RNN for Natural Language Processing](https://arxiv.org/abs/1702.01923).

#### Transfer learning for NLP: Embeddings

Recall the curse of dimensionality: The input space is enormous so we only get to sample a tiny percentage of all possible texts. This makes generalization *very hard*.

Also note: *We're learning the meaning of all English words from scratch every time we build any model.* Wouldn't it be nice if someone just told us the meaning of each word? Humans just use a dictionary but to computers view a word as a location in a semantic space. We call this a word embedding or word vector.

There are two key components: The algorithm and the data. Several generous research groups have built word embeddings on a large collection of text and shared them. Typically researchers will start with one of these pretrained embeddings.

#### Traditional word embeddings

These are all unsupervised methods -- they process a large amount of text and search for the best way to compress the meaning of a word into a vector within the "compression algorithm" they use.

[word2vec] Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., & Dean, J. (2013). [Distributed Representations of Words and Phrases and their Compositionality](https://papers.nips.cc/paper/5021-distributed-representations-of-words-andphrases). In NIPS.

[GloVe] Pennington, J., Socher, R., & Manning, C. D. (2014). [GloVe: Global Vectors for Word Representation](https://aclanthology.org/D14-1162). In EMNLP.

[fastText V1] Joulin, A., Grave, E., Bojanowski, P., & Mikolov, T. (2016). [Bag of Tricks for Efficient Text Classification](https://arxiv.org/abs/1607.01759).

[fastText V2] Mikolov, T., Grave, E., Bojanowski, P., Puhrsch, C., & Joulin, A. (2017). [Advances in Pre-Training Distributed Word Representations](https://arxiv.org/abs/1712.09405).

Honorary mention: Principal component analysis

#### More advanced embeddings

One problem with word embeddings is that you can't always tell the meaning of a word out of context. Is "bark" talking about a dog or a tree? Also keep in mind that we're often using word embeddings just as a way to interpret the meaning of a sentence -- we'd really want sentence embeddings if we could get them.

These papers cover those two areas. All of them can be used to produce a vector interpretation of a sentence and some also provide a context-specific word embedding.

[doc2vec] Le, Q. V., & Mikolov, T. (2014). [Distributed Representations of Sentences and Documents](https://doi.org/10.1145/2740908.2742760). International Conference on Machine Learning.

Dai, A. M., & Le, Q. V. (2015). [Semi-supervised sequence learning](https://papers.nips.cc/paper/5949-semi-supervised-sequence-learning). In NIPS.

[CoVe] Mccann, B., Bradbury, J., Xiong, C., & Socher, R. (2017). [Learned in Translation: Contextualized Word Vectors](https://arxiv.org/abs/1708.00107).

[ULMFiT] Howard, J., & Ruder, S. (2018). [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146).

[ELMo] Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., & Zettlemoyer, L. (2018). [Deep contextualized word representations](https://arxiv.org/abs/1802.05365). In NAACL.

[BERT] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2018). [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805).

#### Lessons from other kinds of NLP

There are many uses for deep learning in natural language processing besides just text classification. The many subfields of NLP often push state of the art in unique ways that help us with text classification. Researchers in machine translation and language modeling use enormous data sets and have found many clever ways to speed up training, especially in industry research groups.

Greff, K., Srivastava, R. K., Koutník, J., Steunebrink, B. R., & Schmidhuber, J. (2015). [LSTM: A Search Space Odyssey](https://arxiv.org/abs/1503.04069).

Jozefowicz, R., Vinyals, O., Schuster, M., Shazeer, N., & Wu, Y. (2016). [Exploring the Limits of Language Modeling](https://arxiv.org/abs/1602.02410).

Gehring, J., Auli, M., Grangier, D., & Dauphin, Y. N. (2016). [A Convolutional Encoder Model for Neural Machine Translation](https://arxiv.org/abs/1611.02344). In ACL.

Hestness, J., Narang, S., Ardalani, N., Diamos, G., Jun, H., Kianinejad, H., … Zhou, Y. (2017). [Deep Learning Scaling is Predictable, Empirically](https://arxiv.org/abs/1712.00409).

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., … Polosukhin, I. (2017). [Attention Is All You Need](https://arxiv.org/abs/1706.03762). NIPS.

Gehring, J., Auli, M., Grangier, D., Yarats, D., & Dauphin, Y. N. (2017). [Convolutional Sequence to Sequence Learning](https://arxiv.org/abs/1705.03122).

Dehghani, M., Gouws, S., Vinyals, O., Uszkoreit, J., & Kaiser, Ł. (2018). [Universal Transformers](https://arxiv.org/abs/1807.03819).

#### Lessons from computer vision

Computer vision shares some core challenges with neural networks. The biggest difference is the input, which is often downsampled to a fixed size such as 224x224 pixels.

Both text and image classification tend to have two parts in their neural networks: an encoder which interprets the input and a classifier part which decides what to output. The encoder might be convolutional or recurrent and the classifier part is typically fully-connected. So although the lessons about the encoder may not translate between image processing and NLP, both fields face similar struggles with classification.

- [Dropout](https://www.jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf): Very good way to regularize
- [ResNet](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html), [DenseNet](https://arxiv.org/abs/1608.06993): There's an important concept called the credit assignment path (CAP). This is the path from the error to the weight you're trying to update. Learning is harder the longer this path is -- this is true in both neural networks and reinforcement learning. ResNet, DenseNet, highway networks, and skip connections are all ways to provide a shorter CAP to make learning easier.
- Neat ideas: Inception. This was complex but elegantly combines several ideas: within-network ensembling, decomposed 2D convolutions to reduce parameters, and some skip paths to shorten the credit-assignment path.
