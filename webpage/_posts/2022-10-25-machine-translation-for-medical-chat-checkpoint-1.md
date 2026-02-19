---
layout: post
title: "Machine translation for medical chat, checkpoint #1"
date: 2022-10-25
---

At my previous job, we provided primary care in a text chat between doctors and patients. It was on-demand, meaning that patients could show up anytime and get in line to chat with a physician. Occasionally we had challenges when a patient didn't speak much English, for instance if they mainly speak Spanish.

So what can you do?

- You can switch to a phone call and dial in a translator. This is commonly done in traditional healthcare systems.
- If the situation is common and predictable, you can forecast Spanish visit volume and staff bilingual doctors.
- You can ask patients to schedule their visits ahead of time with Spanish-speaking doctors.

We'd sometimes talk about another option: Using machine translation to enable our English-speaking doctors to help Spanish-speaking patients. But we found that existing machine translation services just aren't good enough.

I've started looking into it now that I've got some free time. I've started with some literature, and I'm headed towards building a demo and API that could be forked.

This post will summarize what I've found so far and how I've changed my perspective as I learn. I hope it will help others build high-quality machine translation for the medical field, whether or not I'm successful myself.

This post covers a few topics:

1.  Literature in medical machine translation and user experience
2.  Domain adaptation for machine learning: I started a literature review but spent most of my time on the former topic
3.  Publicly available translation APIs: I looked into the big players (AWS, Google, Microsoft)
4.  A revised opinion on what medical machine translation should be

I hope you'll forgive me for putting too much into some sections and not enough into others. This is meant to be an early checkpoint.

### Machine translation in healthcare

#### [Can multilingual machine translation help make medical record content more comprehensible to patients? (2010)](https://ebooks.iospress.nl/volumearticle/13397)

They evaluated the translation quality of Babelfish on patient medical records. (Side note: Babelfish is a real blast from the past! I remember using it for Spanish class in the 90s!)

Generally the translations weren't understandable. The translations were especially poor with medical terminology and anytime the source sentences had complex grammar.

They also mention the Pan American Health Organization Machine Translation System (PAHOMTS), which was designed for English-Spanish-Portuguese. Unfortunately, it wasn't included in their evaluation because it didn't support all the language pairs they tested.

#### [Evaluation of Online Machine Translation by Nursing Users (2013)](https://journals.lww.com/cinjournal/Fulltext/2013/08000/Evaluation_of_Online_Machine_Translation_by.7.aspx?casa_token=NADejGKzfaUAAAAA:jvB-ZfxMgKGaQyIby6u5fckxaXEXZiMOb7ESk_VeHT95Y5qbrVlAw3_y3tsHQPpOZ0K8_Mhr-BLQVICnUZbvweT6)

This paper investigated machine translation of English nursing publications for Japanese nurses.

They did a survey by mail and got about a 50% response rate. That's a shockingly high number compared to surveys I've seen! I'm used to more like 5% or less.

Nurses rated Google Translate's English to Japanese translation quality poorly overall, but higher for usefulness than intelligibility.

Out of vocabulary words were a big issue. Some of the example words were regular words with many affixes like "preidentified" and "nonadherence". (Funny enough, as I write this Chrome thinks those words are typos.) Longer sentences also had worse scores which correlates with complex grammar, much like the prior paper.

#### [Exploring Local Public Health Workflow in the Context of Automated Translation Technologies (2013)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3900226/)

This paper surveyed healthcare professionals and includes many interesting excerpts.

For example, healthcare professionals often talk about the reading level of the translation:

> several LHDs emphasized the need for the document to be at an appropriate reading level and to convey the key message. Employees translated with this goal in mind and focused on lowering the reading level, adopting a conversational tone, and simplifying medical terminology which would be confusing for someone with minimal education

I wonder if that's a unique need for healthcare pamphlets, or if that would be desirable in chat as well?

Generally the healthcare professionals relied on manual translation though they sometimes used Google Translate to check terminology in a pinch. They had a lot to say about the importance of quality and quality control processes.

When they're not able to get translators for certain languages, they often just don't provide translated materials in that language at all.

They mention the HERE database, which might be a useful resource:

> We also specifically asked about use of the H.E.R.E. database, which is an online clearinghouse of public health education and health promotion materials in Washington State \[9\] and is a potential venue for LHDs in Washington State to post and borrow translated materials.

I wonder if I could use that to build a document-aligned parallel corpus? I haven't seen publications that learn from document-level alignment, but I bet it's doable.

#### [Translating Electronic Health Record Notes from English to Spanish: A Preliminary Study (2015)](https://aclanthology.org/W15-3816.pdf)

They simplify the words and grammar of sentences before doing machine translation. For example, they try to find the lay term for technical terms and expand abbreviations.

They train a Moses MT system from Medline translations, and also compared against Google Translate and Bing with and without simplification.

For evaluation, they use three de-identified EHR notes. That's not much data for evaluation but it's better than nothing. The main issue is that doctor notes are often specific to the author or hospital system, in both wording and document structure.

They found that simplification didn't play nicely with Bleu scores. It seemed to produce better translations but with worse Bleu scores.

Other notes:

- Commercial machine translation seems pretty reasonable for medical MT, even in 2015
- This might actually be reasonable for a commercial system even though it's a bit tougher to evaluate. HTER would be a better evaluation for an approach like this.

#### [Development of machine translation technology for assisting health communication: A systematic review (2018)](https://www.sciencedirect.com/science/article/pii/S1532046418301448)

This is an excellent meta-review of papers around 2006-2016. It had good things to say about PAHOMTS though unfortunately they couldn't include it because it was made before 2006.

They found that machine translation wasn't good enough to be used without professional translators though there were some areas in which it might be ok. I was very surprised to read that they saw no significant difference in the severity of errors made by Google Translate and human translators.

I believe this quote is describing a preference for adequacy over fluency, which I also noted in other publications:

> \[30\] found that users preferred the less accurate version of their system; imperfect translations that still avoid dangerous interactions were favored over more accurate but restricted interactions.

This quote resonates with my experience in building software for clinicians:

> Two studies also emphasized the need for a greater focus on design based on user needs rather than on technology-driven solutions

I enjoyed the read, though unfortunately there was only one system deployed in a clinical setting, and neural machine translation wasn't available yet.

#### [Leveraging SNOMED CT terms and relations for machine translation of clinical texts from Basque to Spanish (2019)](https://aclanthology.org/W19-7102.pdf)

Currently all clinicians in Spain are forced to work in Spanish, but they want to enable Basque clinicians to work in their native language. So they're building Basque-Spanish machine translation.

They have [SNOMED CT](https://www.snomed.org/) in both Spanish and Basque. (It's a widely used medical ontology.) If I understood right, they generated synthetic parallel training data using predefined templates and populated the templates with SNOMED terms. They use the synthetic data to adapt general-purpose MT systems, mostly using transformer architectures.

They mention problems in translating drug names which surprised me. I'm guessing their transformer setup doesn't use anything to copy input tokens into the output. It should be fixable though!

I found it interesting that the synthetic training data wasn't really that fluent when you read it, but it was good enough to get the MT system working somewhat without any real aligned data.

I could see this approach being valuable even for English-Spanish. Even with a parallel corpus of medical English-Spanish, the corpus probably wouldn't have good coverage of all medical terminology. SNOMED has good coverage though, so it might be a good way to augment a true parallel corpus.

#### [Designing an App to Overcome Language Barriers in the Delivery of Emergency Medical Services: Participatory Development Process (2021)](https://mhealth.jmir.org/2021/4/e21586/)

EMTs in Germany need to provide emergency care in refugee camps with patients that don't speak German. This paper is about building an app with participation of everyone involved and it sounds like they came up with something pretty useful, though it doesn't involve much machine translation at all.

The paper wasn't that relevant for this project, but many of the lessons reminded me of my prior employer. These are a few examples:

- More senior EMTs tended to follow their experience rather than guidelines from their education.
- History-taking didn't go in a simple linear order or follow a predictable template.
- EMTs were excited about being involved in software development but they had to learn that there was limited development time and prioritization was necessary. The end result was largely positive.

They found that closed-ended questions like yes/no or multiple choice questions were valuable because the questions and answers could be translated ahead of time. That avoids the need to do live translation at all.

I didn't take away much for my MT project except that 1) it can be handy to verify quality using back-translation 2) in a real system, it's effective to find ways to rely on offline professional translation.

#### [Reliable and Safe Use of Machine Translation in Medical Settings (2022)](https://niloufar.org/wp-content/uploads/2022/05/FAccT2022_Reliable_and_Safe_Use_of_Machine_Translation_in_Medical_Settings.pdf)

This was a wonderful read and I'm not sure I can do it justice in a summary.

These are some of the key findings:

- Some people preferred phrase-based translation. Although it was limited, they could trust it more.
- Physicians sometimes use Google Translate when they don't have other options like when it's late at night and translators aren't available, or when they're worried that adding a translator will slow down their visit too much.
- It's helpful to repeat back what you heard to the patient to double-check your understanding.
- Clinicians mentioned that there's variable quality even with professional translators.
- Sometimes if a professional translation talks a lot longer than the physician, the physician would ask to clarify exactly what was communicated.
- There's a lot of discussion about risk and liability -- people don't want to use Google Translate for consent or something really critical, but feel ok with it for history taking and other low risk situations.
- Cultural differences could make translator-mediated conversation even more difficult, for example if topics more common in the US were somewhat taboo in the patient's culture.
- There were also issues with medical literacy -- Teaching the patient about their body is even harder with translation.
- Even some Spanish speakers would use Google Translate to translate specific words, like if they didn't know the medical term for something. That rings true with what I heard -- doctors that were Spanish-native speakers but not medically trained in Spanish may not know the terminology.
- Patients often just say yes to everything even if they don't understand, but will talk honestly with a non-doctor that's a native speaker. Doctors felt this was due to the difference in authority.
- Backtranslation was used to check quality.

So many of their findings resonate with my experience. The cultural issues surprised me though; I hadn't even considered that. And it was also surprising to hear some distrust of professional translators because they're often raised as the best option.

### Machine translation & User experience

I only read one paper in this area so far but it was so good I had to include it.

#### [Understanding and Being Understood: User Strategies for Identifying and Recovering from Mistranslations in Machine Translation-Mediated Chat (2022)](https://dl.acm.org/doi/abs/10.1145/3531146.3534638)

This is a fantastic paper on the user experience of MT-assisted chat with user testing.

They set up machine translation-mediated online chats between participants and had them try to accomplish various tasks. They were only able to read and write in their language and machine translation was used automatically.

Key insights:

- People don't always know when a mistranslation has happened, and assume one hasn't, so the two people sometimes both walk away thinking they've communicated successfully but they haven't!
- People try to adapt their writing to get more reliable translations -- for instance, simplifying their language and avoiding informal language. But in practice they would forget to keep doing this as the conversation went on.
- People often attribute weirdness or rudeness to the other person though it can be caused by the MT system.
- People that understand both languages sometimes are able to infer what the original must have been, even when they're not able to see the other language.
- Modern MT systems are quite good at fluency, but not as much at adequacy.

This part sounds right to me:

> MT-mediated communication has historically been designed to feel seamless and as close as possible to a chat with someone speaking the same language \[52\]. However, this seamlessness may actually make it more difficult for users to identify and attribute errors, and easier for them to forget that MT is in use

When I built software for doctors, it was important to make sure they understood how it worked and when it was reliable.

### Domain adaptation for machine translation

The most reliable way to tune a model to a specific domain is to find additional data, but there are approaches to get more mileage out of limited in-domain data or otherwise reduce the need to source data. I found that true in my thesis work as well as in industry roles.

#### [Unsupervised Domain Adaptation for Neural Machine Translation (Yang et. al., 2018)](https://ieeexplore.ieee.org/abstract/document/8546053?casa_token=V-K6VzcmEkwAAAAA:xfmgYBjKoAdOpqLUZ4zjZzMw4Yesmrok5zVnktsuuNP-T2vvmuRisyxLxLjf_F3SN6GlJZaeZQ)

I struggled with this paper. It seeks to do unsupervised domain adaptation but then uses aligned data to do it.

They use a generative-adversarial model:

- Generator: The machine translation model
- Two discriminators: 1) Domain classifier (is the output in the right domain) 2) Pair classifier (is the pair a translation)

Training:

- Pre-train the MT model on out of domain data
- They try to adapt something trained on formal language for informal language
- Results look similar to other methods for domain adaptation that are supervised

The core idea of a domain discriminator makes sense, and could be trained from monolingual data which is much easier to obtain.

#### [MetaMT, a Meta Learning Method Leveraging Multiple Domain Data for Low Resource Machine Translation (Li et. al., 2020)](https://ojs.aaai.org/index.php/AAAI/article/view/6339)

They start with a general-purpose transformer model with pretrained word embeddings and byte-pair encoding (BPE).

They learn a transformation of the word embeddings to adapt to each domain. It looks like they compute domain-specific embeddings as a weighting of "base" embeddings from the top 10k general words.

My read on this paper is that it's trying to allow for fine-tuning on a small corpus without overfitting by drastically limiting the number of parameters that can be fine-tuned.

They achieved decent improvements over standard fine-tuning.

The general approach makes sense to me -- find or create a small number of parameters to domain-adapt in fine-tuning. That's been my experience in domain adaptation to the medical field as well; that it's helpful to carefully limit the number of free parameters to prevent overfitting.

### API review

I haven't found a medical machine translation API. I'd guess that one of the big cloud vendors will make one eventually but they haven't yet.

#### [Amazon Web Services Translate](https://aws.amazon.com/translate/)

AWS has a machine translation API for general purpose language. It offers some customization:

- Set the formality of the translation ([Reference](https://docs.aws.amazon.com/translate/latest/APIReference/API_TranslateText.html))
- Provide a list of terminology translation overrides. This is meant for things like brand names, which are sometimes real words but often shouldn't be translated. It's just a flat list. In theory this could be used to do some customization for the medical field, but in the API spec it said they can only have 256 entries total. ([Reference](https://docs.aws.amazon.com/translate/latest/APIReference/API_TranslateText.html))
- Active Custom Translation: Provide a [domain-specific parallel corpus for domain adaptation](https://aws.amazon.com/blogs/machine-learning/customizing-your-machine-translation-using-amazon-translate-active-custom-translation/). This is only supported for batch translation which has response time in minutes to days, so it's not really appropriate for live chat. Also the cost is about 4x more per API request.

I also looked into self-hosted machine translation on Sagemaker, but the templates are a bit outdated now ([custom seq2seq model in Sagemaker](https://docs.aws.amazon.com/sagemaker/latest/dg/seq-2-seq.html)).

#### [Google Cloud Translate](https://cloud.google.com/translate)

Google Cloud has three translation solutions:

- Translation API Basic: This is basically Google Translate as we know it
- Translation API Advanced: This adds support for additional document types, batch translations, and customized models. The only customization I saw was terminology overrides like AWS had, which they call glossaries.
- AutoML Translation: This trains your own MT system so it's meant for more customization.

The AutoML Translation option looks like it could work well for medical machine translation. It starts from a prebuilt Google neural machine translation then adapts to your data. And both the base model and AutoML model are shown in the evaluation reports!

#### [Microsoft Azure Cognitive Services Translator](https://azure.microsoft.com/en-us/products/cognitive-services/translator/)

Azure looks to have good options for [custom models](https://learn.microsoft.com/en-us/azure/cognitive-services/translator/customization) as well.

You can provide document-aligned data and it'll pair the sentences for you! This would be great because I ran into a couple potential document-aligned data sources.

> The system can also use monolingual data in either or both languages to complement the parallel training data to improve the translations.

I wonder if they're doing back-translation for pseudo-parallel data, or including a language model on the target side, or both? Regardless, it may be significantly easier to build a moderately large corpus of patient-facing medical text in each language.

#### Thoughts on APIs

It looks like Google Cloud and Microsoft Azure both have good options for building medical machine translation models. That said I'm not sure if the base models are the best available ones or not. I'm sure there must be a Bleu score comparison of APIs somewhere that I just haven't found yet.

The Azure API sounds easier to work with, because you can provide document-aligned data and also monolingual in-domain data.

### Survey of commercial MT-mediated chat

As I was editing this post, I stumbled into several commercial offerings for seamless translation of live chat and other customer support. For the most part, the companies integrate with existing customer service platforms such as ZenDesk, Salesforce, and so on, and enable a company to staff customer service agents in one language with automated translation into the language of the customer.

KantanAI has [some information online](https://kantanmtblog.com/2021/04/28/kantanstream-meets-the-challenge-of-big-data-and-wins/). They mainly act as a plugin to existing customer service tools and do seamless translation. The translation is human-in-the-loop -- many messages go through machine translation but many others are sent to quick-response professional translators. That builds up a data set for them and over time should enable a much better MT system.

Unbabel also has some information online such as [case studies of deployments](https://resources.unbabel.com/case-studies/farfetch-elevates-customer-support-agent-experience-with-unbabel). I found the post interesting because the highlights from the customer sounded so similar to priorities in workforce management in healthcare, like the effects of reduced reliance on hard-to-hire people. The writing suggests that turnaround time is occasionally a problem, so maybe it's more for email support rather than live chat, or live chat in an overstaffed center that already has non-instant response times.

The other companies only had an option to book a sales demo; I didn't see any details online.

These companies don't mention HIPAA or healthcare so that's a non-starter for any real application in the US.

I also saw mentions of [iTranslate Medical](https://blog.itranslate.com/news/itranslate-medical/) but I wasn't able to try it out. The only working medical translation app I found for Android is [Care to translate](https://play.google.com/store/apps/details?id=com.siv&hl=en_US&gl=US), which is a phrase board of common phrases.

### What medical machine translation could be, revised

This section is a combination of what I've learned from papers with what I know from experience. If you know of apps like this, or think it couldn't work, let me know!

Key principles:

- Doctors and patients often know some of each other's languages, and sometimes know a lot of one another's language.
- Users don't need a black-box (seamless) translator, and publications suggest that a black-box translator is actually harmful.
- Doctors and patients should have some visibility into the workings of the system to understand when to trust it. And FDA guidelines also push for this as well, for example see [the summary of Sept 2022 guidelines for clinical decision support software](https://www.fda.gov/medical-devices/software-medical-device-samd/your-clinical-decision-support-software-it-medical-device).
- Doctors may see dozens of patients per day while patients typically have two visits per year. So doctors will have much more experience with the system than patients, and that may lead to different needs for each user.
- Adequacy is more important than fluency in actually getting things done.
- When appropriate, it's best to rely on offline, professional translation.
- Physicians are intelligent and motivated, and also they bear nearly all liability for errors.

I've often found it's effective to focus more on assisting doctors rather than automation itself. So I wonder, would it be better to **teach doctors to work effectively in Spanish**? That would keep physicians "in the driver's seat" and would support doctors that know Spanish but don't know medical terms.

This is a somewhat big pivot from how I was originally thinking, and I'll have to read up on user experience for language learning apps like Duolingo. For now though I can summarize my experience as a Duolingo user who's furiously studying Japanese for a trip:

- It progresses you from easy to hard both in terms of concepts and software support
- The app uses spaced repetition to encourage you to retain information
- When it uses a word you've never seen before, it's highlighted and encourages you to click on it
- You can click on words and it'll show the translation for the word and also the phrase it's in

Back to my MT project, I imagine physicians would progress through a level system with light gamification:

1.  Initially, the physician reads and writes in English. When they're reading, it shows the patient's Spanish with English MT output from multiple complementary systems.
2.  When the physician is reading, they'd be able to click on English words to see the aligned Spanish and definitions. Likewise they could click on the Spanish words to see alignment and definitions. This would be a weak signal to indicate proficiency (but it can't be the only one). Words that are likely "new" to the physician are highlighted like Duolingo to encourage them to read the definition. Over time that would become more rare -- maybe one or two new words per chat.
3.  The physician progresses to read Spanish more reliably so the English translations are hidden by default. They would need to click to see the translations. This click data is used as a weak signal on their proficiency with words/phrases.
4.  There's a separate progression for writing proficiency. They'd initially write in English, see multiple Spanish translations with English back-translations, and select the one they prefer.
5.  After a while, the physician writes some messages in Spanish with appropriate spell/grammar-check and sees multiple back-translations to review.
6.  The physician eventually writes mostly in Spanish but the back-translations are hidden by default. They can click to review back-translations, which is used as a weak signal on proficiency and medical importance.

I don't have it all figured out though -- there's a huge gap on the writing side between steps 4 & 5. I don't have many ideas for how to incrementally learn writing while chatting with the patient, except maybe leaning on standard phrases or templates.

The UI would use small icons for simple quality checks:

- Golden checkbox: The (source, target) pair appears in a database of professionally-approved translations.
- Green checkbox: The target back-translates exactly to the source.

I suspect you'd see more checkboxes if you use short, simple sentences so it would "train" users to adjust a little to the MT system without needing to consciously think about it so much.

The same concepts would apply to the patient's experience, but patients wouldn't have a leveling-up system of language proficiency. So patients would get multiple translations, ability to see alignment, definitions, and lightweight quality signals.

It's important that the patient and physician are working cooperatively to communicate:

- Show the doctor's language proficiency to the patient so that they can adapt as needed
- Augment the text chat with emoji reactions like Slack
- Make it easy to request clarification on a word or phrase, in addition to a dictionary lookup

More technical notes:

- Use multiple, complementary systems when possible, one phrase-based, one NMT at least. Also be sure to include an accent-insensitive one because it's very common to omit accents when typing Spanish on mobile.
- Add drug names to do-not-translate lists, or use a copy mechanism.
- Off the shelf APIs probably don't provide alignments for their translations in the output, so that idea may be harder to implement.

In a commercial setting, I imagine more would be needed:

- Physicians would need an "emergency button" if they feel unable to provide high-quality care, which would escalate the case.
- We'd need quality improvement processes, such as professional translators that review chat logs with physicians and help them to improve. Ideally they'd be able to thumbs-up/thumbs-down a translation which would improve the training data.
- I'd also imagine there would be much more reliance on standardized content, but I probably won't get to that in a demo.

Advantages of a teaching approach to MT:

- Doctors and patients are better informed about whether to trust the system
- It could be "partially enabled" for Spanish-speaking doctors that don't remember medical terms
- It would create a more multilingual workforce, which makes staffing easier (forecasts don't need to be as precise, more options for trading shifts, etc.)

Disadvantages of a teaching approach to MT:

- Doctors tend to be very busy and time-sensitive. Would there be enough doctors willing to slow down a little to learn Spanish?
- There's more to implement and maintain -- there are multiple MT integrations and integration with translation dictionaries. The alignment code would be yet another piece to maintain.
- Showing multiple translations and backtranslations may take a lot of screen space and add cognitive load, compared to seamless MT.

Additional concerns:

- Learning vocabulary is one thing, but doctors would also need to learn verb conjugation, gender agreement, grammar, etc. How could we help?
- How to make it easier to build rapport? That might just be tough in a text-based system.

Despite the downsides I think it'd be an improvement over seamless MT-mediated chat. The real question is whether I could build something good enough that some clinicians would prefer it over phone translators.

### Next steps

Writing this up took more time than I expected, and I hope that you'll help me correct mistakes and fill in any gaps.

Beyond this, I've got to 1) read more 2) start trying out existing APIs 3) build a data set 4) look into bilingual dictionaries. It'd be nice to play around with the actual transformer implementations too, once I have some reasonable baselines.

#### Reading wishlist

- UX for language-teaching apps like Duolingo
- UX for MT-mediated chat -- find and read more
- Try out PAHOMTS and/or read about it
- Best practices for corpus-building -- I suspect that I may need to build a small in-domain corpus for this effort, and I could learn from the way large corpora are built.
- Machine translation models for dialogue -- Most MT research is about sentence translation, but I bet there are possible gains from iteratively translating a conversation as a document. For example, a word might be ambiguous in one sentence but not in a previous sentence.
- Simpler approaches to domain adaptation
- Read about the user experience of Facebook's M messenger -- I believe they released MT-mediated chat a while back but I haven't heard anything since
- Read through [https://machinetranslate.org/](https://machinetranslate.org/)
- Skim this year's WMT proceedings if they're available

#### Data

The data sources I saw mentioned so far:

- Medline has translated abstracts
- WMT has a medical English-Spanish track, I think I saw in WMT 16?
- The HERE database of translated pamphlets in WA (and there must be other similar ones!)
- SNOMED/ICD ontologies with synthetic data generation for complex terminology

There must also be some medical webpages that are translated, and I bet there are papers on how to scrape those for parallel texts.
