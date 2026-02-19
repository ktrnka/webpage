---
layout: post
title: "Machine translation for medical chat, checkpoint #2"
date: 2022-11-18
---

I've made some progress since my [previous post on machine translation for medical chat]({% post_url 2022-10-25-machine-translation-for-medical-chat-checkpoint-1 %}), and this is a second checkpoint.

This post covers two topics:

1.  (Short) Notes about Google Translate and Duolingo for Japanese
2.  (Long) What I've learned so far from trying to build a prototype of MT-mediated chat

### Notes from Tokyo travel

I visited a friend in Tokyo for a week and my Japanese proficiency is *extremely limited*, mainly coming from [Duolingo](https://www.duolingo.com/) and the little I remember from anime. While I was there, I kept up with my Duolingo practice and relied heavily on [Google Lens](https://lens.google/), which translates text in images.

Google Lens was great, and was fast with offline models. It was particularly good for translating signs, such as those in parks or tourist areas. Or even signs in elevators. It was good but not great for translating menus at restaurants, for instance it could show me that the fourth item on the menu was pork kimchi monja, but I also really needed to know how to pronounce the kanji because I don't know the word for pork. Fortunately my buddy knew the word so it worked out. (Side note: If you enjoy food, I thoroughly enjoyed Tsukishima monja street)

We also tried out the speech translation feature of Google Translate, which expects you to alternate between the two languages and decides when to switch with silence detection. We found that it was cool but it took practice to ensure that it didn't switch languages too soon.

Also, now I better appreciate the challenge of translating sentences with drastically different word order. I'd known that it was hard for machine translation systems but surprised to find that it's really hard for me too! When I had to translate in Duolingo with a lot of word reordering, I'd often forget a whole phrase of the sentence. The classic Duolingo one would be something like "I go to work around 9am every day" which becomes something like "every day am-9-oclock-around-at work-at go". If I had to say that a *particular* person was going to work around then, I'd *definitely* forget to translate that part.

Even if you can translate the sentences correctly, being in Tokyo made me realize that there are expected customs in Japanese, and machine translation won't take care of those. For instance, it's common to say "itadakimasu" after food arrives but before eating, but in English I think we usually just start eating if everyone's food has arrived. It makes me think that maybe translation of dialogue isn't as simple as translating sentence by sentence.

**Takeaways for my machine translation project:**

- Even for a well-understood low-risk situation like tourism, there's still plenty of room to innovate on the user experience
- I feel more confident that there's a need for dialogue translation or perhaps cultural translation

---

### A prototype of MT-mediated chat

It's time to build a prototype! I find prototyping helps me uncover assumptions and challenges that I'm not even aware of. Also, I just miss coding a bit!

I built it using Google Colab, which is a Python notebook system that's free and easy to use for scripting. It's not ideal for user interface prototyping, but I figure I can use it for a while then transfer my code to something else.

#### User interface development

Originally I started with a simple demo of a Spanish message from a patient and a separate demo of a message from an English doctor, and I used sentences that I knew were realistic from my time working in healthcare. Here's what the Spanish→English direction looked like:

![Early prototype of Spanish to English, using txtai for translation]({{ "/assets/img/posts/mt-chat-2-spanish-to-english-early.png" | relative_url }})

Unfortunately *my* Spanish isn't good enough to generate medical Spanish, so I mostly used Google translate from English. There's a risk that the Spanish I'm using for the patient is unrealistic.

For the English→Spanish direction I additionally showed the back-translation:

![Early prototype of English to Spanish, using txtai for translation]({{ "/assets/img/posts/mt-chat-2-english-to-spanish-early.png" | relative_url }})

After a few days I switched to a chat-like user interface so I could translate a whole dialogue rather than individual turns. I found that I learned MUCH more about the limitations of MT-mediated chat by doing this. This is what a few turns of dialogue looks like:

![Second prototype, showing both Spanish to English and English to Spanish, with txtai translations]({{ "/assets/img/posts/mt-chat-2-full-dialogue.png" | relative_url }})

I used pure HTML, CSS, and Javascript to ensure that it could work inside of Google Colab. It's not ideal, but I found it was good enough for me to learn a lot.

There are three main components in the demo, and I'll write a section on each:

1.  The actual translation
2.  If you click any Spanish word, it shows a bilingual dictionary for the word
3.  Translation quality assessment using backtranslation

Each of the three sections will describe what I did and the challenges I ran into.

#### Full example (links)

For full examples, follow these links:

- [Example chat with only txtai translations](https://www.dropbox.com/s/8upccc9ajq0qqcr/medical-mt-demo-txtai.html?dl=0)
- [Example chat with txtai, Google, Azure, and AWS translations](https://www.dropbox.com/s/vh9z9va6b8y4tz8/medical-mt-demo-all.html?dl=0)

If you have a few minutes and some English/Spanish proficiency, I recommend reading through and clicking around to get a feel for the limitations.

### Machine translation providers

I worked with four off-the-shelf machine translation systems, three of which were discussed in my previous post:

[**txtai**](https://neuml.github.io/txtai/pipeline/text/translation/) is a Python library for semantic search that uses [Huggingface](https://huggingface.co/) models under the hood for machine translation. It's very easy to setup, and downloads the models for your language pairs seamlessly in the background. It tries to automatically select the best-performing Huggingface model for your language pair, which is a nice feature but unfortunately it doesn't tell you which model it's using.

**Google/GCP Translate** is a standard in translation. The API is pretty bare-bones though. I didn't see any customization options. It took me longer than other services because I'm not as familiar with GCP's concepts and terminology.

**Amazon/AWS Translate** is another option. I'm familiar with AWS concepts so it was easy to setup. The API offers a bit more customization than GCP, like setting the desired formality of translation. Also, I realized that the do-not-translate list is passed in with the text to translate, so the limitation on the number of terms wouldn't be the problem I previously thought.

I found **Microsoft Azure Translate** easier to setup and use than GCP, partly because they have a very simple way of doing access keys and you don't need to install a big Python library to use it. Also it turns out that they have an API for a bilingual dictionary too!

#### On ensembles

I included multiple translation providers for the ensemble benefit -- if different systems make different kinds of errors, when you look at multiple options you can often figure out the best output. *Sometimes* the systems differed in a way that helped me find the best translation. But usually all four systems provide very similar translations, so the ensemble idea wasn't as useful as I'd hoped.

#### On translation quality

I noted some of the translation problems I saw but keep in mind that these are anecdotes and it'd be better to do a proper study when possible.

- There was sometimes ambiguity around formality, such as how to translate "pee". I've observed many doctors use "pee" rather than "urine" to be informal with patients. I'm not sure what the best translation in Spanish would be though -- most systems translated it "orina" and one "pis". Ideally the user interface would help me verify the translation of formality better.
- I also observed that incomplete sentences became complete sentences when translated and back-translated. Maybe the API setting in AWS Translate would help.
- "Clear out" turned into "clean" in Spanish and that's not *quite* the same meaning when talking about clearing an infection out of your system -- that's the exact kind of thing I'd like to help doctors investigate in the user interface, but I haven't figured out how to do definitions of phrases properly.
- As far as I can tell, the Spanish word for cranberry and blueberry is the same, "arándano". In the context of cranberry juice that's probably ok; I don't think blueberry juice is common but it could be a little ambiguous and the English speaker might not even know.
- One time, a translation system simply dropped an entire sentence! I've heard that neural machine translation can do that, but it's the first time I've seen it.
- The acronym UTI was processed strangely. It's a common acronym for urinary tract infection. Some systems would translate the acronym to "infección del tracto urinario", others to "ITU", and others left it as "UTI". There was even one system that did this translation: UTI (en) → UTI (es) → ICU (en). UTI is definitely not the same as ICU!

Fortunately none of the issues I saw would've made a big difference in the outcome of the dialogue.

I was pleasantly surprised that no system had issues with terminology like Macrobid or nitrofurantoin (the generic drug name for Macrobid), or locations like 4th and Pike. I was expecting that I'd need to do a lot more work for drug names. That said, Macrobid is a *very* common drug so it's not the best test. I should test with less common medications.

### Bilingual dictionaries

I felt that it was important for doctors to be able to easily look up definitions of each word so I made the Spanish words clickable:

![Inline word translations for reference]({{ "/assets/img/posts/mt-chat-2-word-translations.png" | relative_url }})

In this case, with a little bit of Spanish knowledge I can tell that quema is probably from a verb quemar, and probably "me quema" is like saying "it burns me".

When available, it'll also have definitions, sometimes for multiple word senses:

![Inline word translations with definitions]({{ "/assets/img/posts/mt-chat-2-word-definitions.png" | relative_url }})

But that makes the display very long, and I had to cut off the screenshot after just two definitions (WikDict has four senses of parecer!).

It was tougher than I expected to find machine readable bilingual dictionaries. These are the four I tried:

- [**Word2Word**](https://pypi.org/project/word2word/): This is a Python library that's easy to install and provides words that are correlated between two languages. The words aren't usable as definitions but the coverage is pretty good.
- [**WikDict**](https://www.wikdict.com/) **/ Wikitionary**: [Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page) is a multilingual dictionary similar in spirit to Wikipedia. It's possible to extract a bilingual dictionary from it, and that's what WikDict provides. It also provides a machine-readable version in sqlite and xml. I used the sqlite version. One challenge is that it doesn't have good coverage of conjugated words, so I needed to use a lemmatizer to get good coverage. I used [Spacy](https://spacy.io/) to do lemmatization in Spanish, and had mixed results (it couldn't lemmatize as often as I'd like). I also found that it has *some* phrase pairs in the database, though I couldn't figure out when I could count on them. One advantage of WikDict over others is that it provides a dictionary definition. That said, for the demo I needed to run the definition of the Spanish words back through machine translation to get a translated definition. At first I felt uneasy about relying so much on MT, but the phrasing of dictionary definitions tended to be simple and the translations were pretty good.
- **Azure Translate**: Azure was the third option I tried and became my favorite. It has good coverage and doesn't require lemmatization. The main downsides are 1) it doesn't include definitions 2) you can only query the API with 10 words at a time, which takes a bit of extra coding.
- [**BabelNet**](https://babelnet.org/home): This was the last dictionary provider I tried. I was hopeful because it sounds like WordNet, but found that it had far too many senses for each word and I didn't see any easy ways to do word sense disambiguation (WSD). There's a field for frequency, but it was the same value in all entries. There's also a way to get a gloss (definition) which could be used for WSD, but that takes one extra API call per sense and the API is limited to 1000 calls per day.

I wish I had a more reliable source of definitions because it seems like the definitions, even when translated, convey the connotation of the word better than a simple bilingual word list.

I also feel that the user interface needs work, both to make it easier and more compact.

### Automated quality checks using backtranslation

In my [previous literature review]({% post_url 2022-10-25-machine-translation-for-medical-chat-checkpoint-1 %}), I found that backtranslation was a common method used to assess translation quality, both in the context of MT-mediated chat and also in the context of healthcare. So I wanted to make it easy to use backtranslation for quality assessment, not just for manual review but also automated review.

I started off by measuring the cosine similarity of word bigram distributions between the source and back-translation, but found that it would often give very low near-zero numbers.

I did a quick literature search and found [(Rapp, 2009)](https://aclanthology.org/P09-2034.pdf), which builds an automated metric using backtranslation to assess the quality of machine translation. They found that it was possible to build a metric on backtranslation that correlated with human ratings. They introduce a new metric OrthoBleu that's like Bleu but uses character trigrams -- it led to a usable metric that doesn't require a reference translation! Keep in mind that they're testing English-German MT, and character ngrams might be particularly helpful there at scoring partial credit with German compounds, so it may not address issues in all language pairs.

I approximated OrthoBleu using cosine similarity of character trigrams between the source and back-translation. I also added a start of message and end of message token to ensure that there would be at least one character trigram (and to slightly improve the metric, maybe).

Originally I showed the exact score, but felt that it gave a false appearance of precision. And what does it even mean to have 0.85 cosine similarity? Is that good? Bad? So instead I made up four quality cutoffs: 0.2, 0.5, 0.75, 0.9. There isn't any scientific basis for these, just a gut feel from the kinds of scores I saw. Ideally I'd prefer to calibrate them to the 25th percentile, 50th percentile, etc. And I'd love to add a 5th level of quality bar if (source, target) pair appears in a professionally-vetted translation table.

As I worked with this more, I noticed some issues:

- If the Spanish text didn't have proper **accents**, that caused problems because the back-translation would often have proper accents. In my example chat, I typed "Si" for yes even though it should be "Sí", but it's easy to tell from context that it means "yes", not "if". Unfortunately, the back-translation metric gave full score to the MT system that translated it as "if" (incorrect) and zero to the MT systems that translated as "yes" (correct).
- It also had problems with English → Spanish → English if the source English had **contractions** because the MT systems rarely produced contractions in the back-translation. I'm guessing it's because 1) Spanish doesn't have the same kinds of contractions as "don't" 2) MT systems are trained on more formal language. In the end it meant that any source English with a contraction got lower back-translation scores for all systems.
- Sometimes MT systems would also add **punctuation** as appropriate, like a period at the end even if it wasn't in the original. This doesn't make the translation bad, but slightly reduces the automated score.

Overall, a quality score feels like a good direction but this particular quality score doesn't feel reliable enough for real medical practice.

### Ideas that didn't work out (yet)

I looked into a number of other directions briefly but couldn't get them to work in time:

- Publications point to the Pan American Health Organization Machine Translation System (PAHOMTS) as a good classical translation system. I reached out to PAHO but there aren't licenses for research use.
- I was originally thinking that if multiple translation systems agreed, the translation was probably good. But the translation systems very rarely agreed on the *exact* translation unless the input was very short.
- Another thought was to hide the additional translations in the cases when they agreed, but it can be tricky to get dynamic user interfaces right so I didn't pursue that further (yet).
- I wanted to render word alignment in the user interface so that doctors would verify the way highly important words are translated, but haven't tried that yet.
- I found that AirBnb does translation of pages, but it looks like it's human in the loop translation and it's not realtime. They might have translation of chat messages but I didn't find any publications about it.
- It would've been nice to use Spacy part of speech tagging to filter dictionary definitions, it just takes a bit of extra work to align the Spacy tags to each dictionary's POS tags.
- I really need a way to do definitions of phrases, though that again points more towards using word alignment. I frequently found even for myself that I needed to verify phrasal verbs, and it was pretty slow to do so I often didn't do it.
- I really wanted to have photo avatars for each user and each MT system to make the chat more skimmable. It would also enable users to develop cognitive associations between MT system avatars and levels of typical quality.

### Challenges & Takeaways

It makes sense to use multiple translation systems, but the current user interface takes up too much screen space to be practical. I'm skeptical that there's any way to show the output of four systems in a way that doesn't slow doctors down though.

An automated quality score is useful, but it needs to be more focused on adequacy and less focused on fluency to be trustworthy.

The lack of accents in informal Spanish will likely be a bigger problem than I expected for practical use. I'll probably need an accent-insensitive MT system.

The integration of translation dictionaries was a useful direction. It's even handy for me while developing the system. The main limitation is that I didn't find a good way to include phrase definitions. I think word/phrase alignment is the most promising idea to handle this.

On the bright side, off the shelf translation systems did better than I expected with medical terms.

### Next steps

I'm going to pause for a few days to reflect and consider my options.

I feel that the goal should be a system that's much more compact, but I don't know what would work to get there. I wish it were easier for users to verify the quality of translations. And I haven't made as much progress as I'd like in helping users to understand how the translations are generated.
