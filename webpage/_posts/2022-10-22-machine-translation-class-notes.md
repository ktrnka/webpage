---
layout: post
title: Machine translation class notes
date: 2022-10-22
---

I'd like to build a machine translation system for English-Spanish medical chat. But first, I need to brush up on machine translation.

I took the [Coursera class on machine translation](https://www.coursera.org/learn/machinetranslation) and read many of the papers they reference, particularly in areas that I wasn't familiar with. I've summarized many of them below with notes on how the papers may help in medical MT.

I enjoyed the class -- It covers a good range of topics including modern methods like BERT.

### Evaluation methods

#### [Bleu: a method for automatic evaluation of machine translation (Papineni et. al., 2002)](https://aclanthology.org/P02-1040.pdf)

This paper introduced Bleu scoring, the most common evaluation metric for MT. It's a geometric mean of ngram precision ranging from ngram length 1-4. They also add a length factor to penalize translations that omit details from the source, and a factor to penalize repetitive but common ngrams.

They evaluate the proposed metric by correlation with human judgements on translation quality, finding that their method is well correlated with humans.

Although this isn't a human rating of quality, it's a useful proxy. The key things that make the proxy useful are:

- Doing document-level metrics rather than sentence level metrics to avoid multiplying by zero or having unreliable ngram precision metrics.
- Using multiple reference translations or at least multiple translators even if there are single references, which mitigates problems in measuring exact matching of words and ngrams.
- All systems are ranked using the same metric, so even though Bleu has limitations those limitations affect all systems similarly.

I had heard criticism of Bleu scores for years in grad school, for instance that Bleu was just some ngram metric and had little to do with useful, well-formed translations. But now that I've read it, the paper is well aware of the challenges and makes an effort to build a reasonable proxy for human judgments.

I bet this paper inspired the Workshop on Machine Translation (WMT) shared task on evaluation metrics, which is a competition to design the metric that's best correlated with human judgements. The subsequent paper reviews come from this shared task. I have to say that it's inspiring to see such dedication to build the best approximation of human judgements on translation quality!

#### [MEANT: An inexpensive, high-accuracy, semi-automatic metric for evaluation translation utility via semantic frames (Lo and Wu, 2011)](https://aclanthology.org/P11-1023.pdf)

Metrics like Bleu capture fluency well, but don't do a great job of capturing adequacy. On the other end, there are metrics like Human-mediated Translation Error Rate (HTER) which capture adequacy very well but are time-consuming to measure.

Side note: In HTER the experts make "the minimal number of edits so as to make the MT output convey the same meaning as the reference translation".

Here's a brief definition of fluency vs adequacy:

> Fluency measures whether a translation is fluent, regardless of the correct meaning, while Adequacy measures whether the translation conveys the correct meaning, even if the translation is not fully fluent. ([Snover et. al., 2009](https://aclanthology.org/W09-0441.pdf))

The MEANT paper is seeking to find a middle ground between expensive, high-quality metrics like HTER and cheap, lower-quality metrics like Bleu. They're also seeking to make something simple and easy to understand.

They measure agreement on who did what to whom, when, and why, etc, in other words agreement on semantic frames. Although semantic frames seem technical, they were able to use minimally-trained people to annotate the semantic frames.

They found that it's an improvement over existing metrics for adequacy and close in quality to HTER but much cheaper. They also double-checked the semantic frame annotation and found that the annotation quality was good despite limited training. They then tried automated semantic role labeling and MEANT still works well, just not as well.

The paper's premise seems to be based on single-reference Bleu, and the Bleu authors seem to prefer multiple references. I wonder if multi-reference Bleu would be a sufficient measure of adequacy? Even if so, it might be too expensive but I'm curious.

MEANT might be a useful option for medical machine translation because many papers describe the importance of adequacy in the medical area (to be summarized in a subsequent post).

#### [Fitting Sentence Level Translation Evaluation with Many Dense Features (Stanojevic and Sima'an, 2014)](https://aclanthology.org/D14-1025.pdf)

The authors create a machine-learned metric by trying to predict human judgments of translation quality. One problem they note with metrics like Bleu is that word ngram features are very sparse which can make it less reliable, especially for short documents or sentence-level evaluation.

They design many of their features to be less sparse, for example character ngram overlap between reference and candidate. They also include word ngram overlap features. I found it surprising that they also included recall features -- the Bleu paper specifically mentioned that they couldn't use recall because of multiple references. Maybe multiple references fell out of favor over the years due to the cost? This paper also includes complicated features about word order changes, using permutation trees (PET) but I didn't understand how those worked.

These features are fed into a linear model to predict human ratings. They compared it against METEOR and found that their method (called BEER) was generally better across language pairs. They used Kendall Tau for evaluation, which surprised me a bit because others all used Spearman or Pearson correlation. Maybe it's because of the learning-to-rank approach?

The character and word features were the most valuable, then PET, then function words, then fluency, and so on.

I like the core idea of using ML with non-sparse features. Though I bet it could've been improved with *some* sparse features like word translation edit rate (TER) if the model has appropriate regularization.

Another thing I like about the BEER work is that it could be applied to other quality judgements. For example, in a MT-mediated medical chat we might want a metric like diagnostic accuracy, and could use the BEER work to approximate that instead of imitating generic MT judgements.

#### [CharacTer: Translation Edit Rate on a Character Level (Wang et. al., 2016)](https://aclanthology.org/W16-2342.pdf)

This paper is aimed at evaluation in morphologically rich languages -- word-based approaches don't work so well in those languages. To use the phrasing of the BEER paper, word-based features are too sparse.

They're extending the translation edit rate (TER) metric to work at the character level. This is how they describe TER:

> The most related work is the widely applied TER metric (Snover et al., 2006), which evaluates the amount of necessary editing to adjust a hypothesis so that it is accurately equal to a reference translation. Compared to the Word Error Rate (WER), TER introduced a shift edit on top of the Levenshtein distance, since in many languages different sequence orders are allowed.

They create a character-level edit distance metric called CharacTer, that uses word-level alignment with character edit distance. The word-level alignment was found to be necessary for runtime performance.

They found that it often outperformed other metrics. One of their key improvements was a modification that could be applied to other metrics as well -- to normalize by the hypothesis length rather than the reference length.

I like that it's a simple way to measure similarity to the reference and it doesn't need anything language-specific for morphology. It felt like they did manual hyperparameter tuning and I'd prefer automated tuning, but that's a minor point. Also I wonder why a character-based method like chrF3 didn't meet their needs? Is 3 too short of an ngram?

### Upgrades to the noisy-channel model

Classic statistical machine translation follows a noisy-channel model approach, common also in other fields such as speech recognition, optical character recognition, typing on mobile phones, and many other applications. The two papers below are improvements over the noisy channel model for machine translation.

#### [Minimum Error Rate Training in Statistical Machine Translation (Och, 2003)](https://aclanthology.org/P03-1021.pdf)

In this approach, called MERT, the source model (LM) and channel model (translation) are simply inputs (features) into a log-linear model.

It's not as simple as learning a classifier for the correct translation though, because the correct translation often isn't in the n-best list of candidates. So traditional approaches don't apply. Instead, they optimize each parameter separately using a line search.

They come up with pseudo-references in the n-best list to treat as gold standard using metrics such as Bleu to select the best pseudo-references.

In general they find that you should use the same metric for pseudo-reference selection as the system evaluation. Unfortunately, this means that some of the progress is coming from optimizing to the metric rather than a general-purpose improvement in translation. Similarly, they had an interesting comment that using mWER favored shorter translations while Bleu and NIST metrics favored longer translations, and I take that as a cautionary lesson that there are some biases baked into the metrics. On the other hand, it means that when better metrics are created, MERT can be used to optimize to the better metric.

#### [Tuning as Ranking (Hopkins and May, 2011)](https://aclanthology.org/D11-1125.pdf)

This is a follow-up to MERT. They're seeking to build a feature-weighting model like MERT that scales better to thousands of features.

Their metric is called pairwise ranking optimization (PRO). They use a ranking framework, so it takes n-best lists with Bleu scores (or other scores) and learns a model to predict which of a pair of candidate translations has the higher score. They compute features of each candidate translation, take the difference, and the differences are the input to the model. Once trained, the model can be used to sort n-best lists.

Generally the evaluation scores are similar or better than MERT while being significantly faster. And they were able to scale to thousands of features successfully. They also find that it's more reliable that MERT: When doing repeat training, there's much less variation in the results with PRO than MERT.

They also explore how to sample each n-best list and how many source sentences as well. They had an interesting footnote about sampling: They only pick pairs with sufficiently different Bleu scores because they're trying to learn the difference between bad and good translations, not learn the difference amongst good translations.

### Next steps

I'm working to write up a literature review for medical machine translation (actually this post was originally a section, but it felt different enough to split out).

There were also some longer publications that I haven't read yet, like the summaries of the WMT shared tasks. That's on my list.

I'd also love to find a retrospective on two decades with Bleu scores, or another recent summary of translation metrics.
