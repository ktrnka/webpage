---
layout: post
title: "Machine translation for medical chat, checkpoint #3"
date: 2022-12-15
---


This is another literature review, but this time with more papers and pictures!

------------------------------------------------------------------------

### Machine translation for medical chat, checkpoint \#3

This is another literature review, but this time with more papers and more user interface pictures.

[Last time I posted](/2022/11/18/machine-translation-for-medical-chat-checkpoint-2.html), I was prototyping different user interfaces for machine translation-mediated chat and hit a wall. Since then I've been reading papers to get ideas. I read papers already in my queue, explored the citation graph around those papers, and I also tried [Elicit](https://elicit.org/) to expand my search more.

I was mainly looking to read about user interfaces for machine translation but included other areas as they came up:

1.  User interfaces to improve understanding of MT-mediated communication
2.  User studies of MT-mediated communication
3.  Computer-Aided Translation (CAT) tools -- This is a field just for tools to support translators, and I read a few papers about interactive machine translation (IMT) that might be useful for writing
4.  Healthcare machine translation -- I found more to read about MT in healthcare too!

I'll go through papers in chronological order within each category. Sometimes I read them out of order, and I apologize if that makes the reading more difficult. I'll include as many user interface screenshots and complete citations as I can. And also, I'm trying ChatGPT to help convert my raw notes into readable summaries.

I'll share my thoughts as I go, and afterwards summarize what I think are the most promising directions for the future.

I hope this article will be helpful to others that are looking to improve machine translation for healthcare.

------------------------------------------------------------------------

### User interface design for comprehension

This grouping largely has self-contained user interface experiments.

#### Leveraging uncertainty visualization to enhance multilingual chat

Collins, C., & Penn, G. (2006). *Leveraging uncertainty visualization to enhance multilingual chat.* Proceedings of the CSCW

The researchers presented a visual representation of the most probable parts of the lattice of a statistical machine translation system. The weight of each arc in the lattice is proportional to the probability of its corresponding translation. Initially, the visual representation may be confusing to interpret, but once the idea is understood, it is fairly easy to read and provides insight into the ambiguity of the translation process.

![Collins & Penn lattice uncertainty visualization]({{ "/assets/img/posts/mt-chat-3-uncertainty-lattice.png" | relative_url }})

In addition, the researchers propose a novel approach for dealing with out-of-vocabulary (OOV) words. Rather than simply leaving these words untranslated, they suggest searching for images of the OOV words on Flickr and displaying the images alongside the untranslated words. This approach offers a unique way to handle OOVs and provides additional context for the reader.

The visual is too complex for the chat interface in my project. I haven't seen many challenges with OOVs, but the idea of linking to a secondary database for complex words might have potential if OOVs are a problem.

#### Automatic Prediction of Misconceptions in Multilingual Computer-Mediated Communication

Yamashita, N., & Ishida, T. (2006). *Automatic Prediction of Misconceptions in Multilingual Computer-Mediated Communication*. Proceedings of the 11th international conference on Intelligent user interfaces

This paper focuses on the role of machine translation in facilitating communication between people who speak different languages. The study found that misunderstandings are common in such interactions, and that both parties may think they have successfully communicated when in fact they have not.

The researchers make a distinction between stated misconceptions, which are related to mistranslations, and unstated misconceptions, which arise from assumptions made by one or both parties. They also discuss the potential use of lexical chains, which are sequences of words that are related in meaning, to help identify misunderstandings.

I didn't understand all of the paper. In particular, it is unclear how the researchers are annotating misconceptions and measuring the success of their methods. The core idea seems to be that people often switch topics when they do not understand each other, and it can be detected using lexical chains.

Overall, the study raises the possibility that misconceptions caused by machine translation can be automatically detected in certain kinds of chat.

In doctor-patient communication, typically the doctor leads the conversation and the patient follows. I don't think the method of lexical chains would help identify situations in which the patient misunderstands the doctor, but may identify situations in which the doctor misses some information from the patient. Unfortunately that would be a special-case solution for only one type of miscommunication; I'd prefer to find a more general-purpose solution.

#### Evaluation and Usability of Back Translation for Intercultural Communication

Shigenobu, T. (2007). *Evaluation and Usability of Back Translation for Intercultural Communication.* International Conference on Usability and Internationalization

The researchers in this study explore the use of back-translation as a feedback mechanism to improve machine translation. They argue that simply providing back-translation is not enough, and that the user interface (UI) must also be designed carefully to enable users to easily identify and correct mistakes. (I agree!)

In their experiment, the researchers used back-translation in a non-native speaker (NNS) machine translation (MT) scenario, where the back-translation was used as a feedback loop to help the author revise their original input. They found that the quality of the back-translation was highly correlated with the quality of the forward translation, although the back-translation was on average 20% worse.

The researchers also developed a real-time translation system that attempts to identify parts of the input that are "translation unstable" and highlight them to the user. However, they do not provide much detail on how this is done. They found that the approach worked well for Japanese-English translation, but not for Chinese or Korean.

![Backtranslation stability highlighting]({{ "/assets/img/posts/mt-chat-3-backtranslation-stability.png" | relative_url }})

In my project, it may be possible to use multiple back-translations with different pivot languages to help identify "translation unstable" parts of the input.

#### picoTrans: An Icon-driven User Interface for Machine Translation on Mobile Devices

Song, W., Tanaka-Ishii, K., Finch, A., & Sumita, E. (2011). *picoTrans: An Icon-driven User Interface for Machine Translation on Mobile Devices*. Proceedings of the 16th international conference on Intelligent user interfaces

The researchers present a novel approach to machine translation using icons and hierarchical categorization. The system is designed for non-native speakers of Japanese, and allows users to select from a range of pre-defined icons to communicate their intended meaning. The icons are organized into a hierarchy of categories, making it easier for users to find the appropriate icons for their needs.

![picoTrans icon-driven UI]({{ "/assets/img/posts/mt-chat-3-picotrans-icons.webp" | relative_url }})

While the idea of using icons for communication has potential, there are some challenges with the approach. For example, the hierarchical categorization of icons may be difficult for users to navigate. Additionally, it may assume the user has awareness of Japanese verb conjugation.

Overall I found it interesting but didn't take away implications for my work.

#### Can Indicating Translation Accuracy Encourage People to Rectify Inaccurate Translations?

Miyabe, M., & Yoshino, T. (2011). *Can Indicating Translation Accuracy Encourage People to Rectify Inaccurate Translations?* International Conference on Human-Computer Interaction

The researchers in this study conduct user testing to evaluate the quality of automated machine translation. They use BLEU scores on back-translations to assess the accuracy of the translations.

The researchers tested three different indicators of translation accuracy: percentage, a 5-point scale, and a 3-point scale. However, the scales were presented in words rather than visual aids, which may have affected the results. The study focused on Japanese translation.

The researchers also had users attempt to repair inaccurate translations. They found that the 5-point scale was the preferred indicator of translation accuracy, but that the indicators did not significantly affect users' judgments of the accuracy of the translations.

(Rapp, 2009) found that BLEU wasn't good at measuring back-translation quality, so this isn't entirely surprising. It's also possible that the translators would've been thorough regardless of the user interface.

#### Same Translation but Different Experience: The Effects of Highlighting on Machine-Translated Conversations.

Gao, G., Wang, H.-C., Cosley, D., & Fussell, S. R. (2013). *Same Translation but Different Experience: The Effects of Highlighting on Machine-Translated Conversations*. Proceedings of the SIGCHI conference on human factors in computing systems

The researchers in this study explore the use of highlighting to improve the user experience of machine translation. Their hypothesis is that highlighting certain words in the translated text can make it easier to understand and increase trust in the translation. For example, in the case of the poorly-translated sentence "Was in Beijing on a six point document send out," highlighting the keywords "Beijing" and "six o'clock" might make it easier to infer the intended meaning, which was "Need to send this document out by six o'clock Beijing time."

To test their hypothesis, the researchers conducted a user study comparing no highlighting, human-selected keyword highlighting, and random highlighting. The study involved Chinese-English machine translation (presumably using Google Translate) and had users engage in MT-mediated chat to complete brainstorming tasks.

![Keyword highlighting brainstorm study]({{ "/assets/img/posts/mt-chat-3-keyword-highlighting.png" | relative_url }})

The researchers found that keyword highlighting was rated as the most clear, while random highlighting was less clear than no highlighting. They also found that participants had a slightly higher impression of their conversational partner when keyword highlighting was used.

Overall, this study provides some evidence that highlighting can improve the user experience of machine translation.

The examples show nearly-unintelligible English translations. Would it still be helpful with better quality translations from modern MT models?

#### Agent Metaphor for Machine Translation Mediated Communication

Shi, C., Lin, D., & Ishida, T. (2013). *Agent Metaphor for Machine Translation Mediated Communication*. Proceedings of the 2013 international conference on Intelligent user interfaces

The researchers in this study explore the use of machine translation in a conversational agent scenario. I wasn't able to understand the paper fully.

They propose a system in which the agent uses BLEU scores on back-translations to determine when to intervene and suggest that the author repair the message. One finding of the study is that "using machine translation almost doubles the participants' effort" which is worth pondering.

#### BBN TransTalk: Robust multilingual two-way speech-to-speech translation for mobile platforms.

Prasad, R., Natarajan, P., Stallard, D., Saleem, S., Ananthakrishnan, S., Tsakalidis, S., … Challenner, A. (2013). BBN TransTalk: Robust multilingual two-way speech-to-speech translation for mobile platforms. *Computer Speech & Language*, *27*, 475-491. doi:10.1016/J.CSL.2011.10.003

The researchers in this study developed a machine translation system for use in military communications, specifically in the context of the Pashto language. The system is designed to be used in a star trek communicator type of device, and incorporates a number of features to minimize errors and improve the user experience.

One key aspect of the system is the use of confirmation strategies, such as requiring the user to confirm the output of the automatic speech recognition (ASR) before it is sent to the machine translation (MT) and text-to-speech (TTS) components. The researchers also incorporate a number of other techniques to improve the quality of the ASR, including a large vocabulary and the use of a high-quality grapheme-to-phoneme (g2p) dictionary.

The user experience was designed to be simple and intuitive, and meant to support eyes-free communication. Press YOU for push-to-talk for yourself, HIM for the other person. There's a way to review what it heard, and also it'll start speaking the translation after a delay. If you don't like it you can just push YOU to start over.

The researchers explored the use of back-translation and quality estimation (which they call confidence estimation) to improve the MT component of the system. They found that back-translation with METEOR scoring was not as effective as a confidence measure based on translation consistency, but that both approaches were useful. I think they set a threshold on the score for the system to ask the user to repeat themselves.

I enjoyed this paper -- It presents a complete system with a range of research. In addition to the research I've summarized, they also dealt with challenges in speech recognition and machine translation as well.

I don't think the details are applicable to MT-mediated chat in healthcare though. At a high level though I'm inspired by how simple their system is.

#### Improving machine translation by showing two outputs

Xu, B., Gao, G., Fussell, S. R., & Cosley, D. (2014). *Improving machine translation by showing two outputs*. Proceedings of the SIGCHI Conference on Human Factors in Computing Systems

The researchers in this study conducted a user evaluation of a machine translation interface that provides both the original and translated sentences. The study involved a Mandarin-English translation task, and included a number of quotes from users to provide insight into their experiences with the system.

One quote mentioned that the dual translations were not useful when they were too similar. Another quote mentioned the potential usefulness of the system when the machine translation is not of high quality, such as in Russian-English translation.

![Two outputs dual translation UI]({{ "/assets/img/posts/mt-chat-3-two-outputs.png" | relative_url }})

My notes on this paper are very limited; I read (Gao et al., 2015) first, which is a very similar paper. (Xu et al., 2014) focuses more on summarizing feedback from users.

#### Enhancing machine translation with crowdsourced keyword highlighting

Pan, M. H., & Wang, H. C. (2014). *Enhancing machine translation with crowdsourced keyword highlighting*. Proceedings of the 5th ACM international conference on Collaboration across boundaries: culture, distance & technology

Pan and Wang (2014) examine the use of crowdsourced keyword highlighting to improve machine translation quality in the user interface. The authors find that while highlighting can be beneficial, it only has a significant impact on difficult sentences when the highlighters are bilingual.

These results suggest that highlighting may not be a reliable method for improving machine translation in healthcare settings. I had been considering having doctors underline important words and propagate those underlines in the translation. However, that's similar to the failed monolingual tests so I'm less confident it would work.

#### Designing User Experience for Machine Translated Conversations

Surti, T. (2015). *Designing User Experience for Machine Translated Conversations*. Proceedings of Machine Translation Summit XV: User Track

The researchers in this study conducted a user evaluation of a speech-to-speech translation system integrated into Skype. The system was developed around 2014 and involved two people speaking in different languages, with the system providing real-time translations for both participants.

The researchers were surprised to find that user complaints about the system were focused more on the user interface than on the translation quality. Users found the experience chaotic and overwhelming, with four voices (two people and two translations) often speaking simultaneously. The authors suggest using audio ducking, which adjusts the volume of the less relevant audio stream, to improve the user experience in these cases.

Additionally, users reported frustration with the perceived slowness of the system. The authors explain that this was due to the system only starting the translation once the full utterance had been received, rather than providing partial translations as the user spoke. They suggest adjusting the settings for pause duration and partial translation to improve the speed of the system.

Overall, this study provides some interesting insights into the challenges and user experience of speech-to-speech translation systems. I don't think there's applicability to my work though.

#### Two is better than one: Improving multilingual collaboration by giving two machine translation outputs

Gao, G., Xu, B., Hau, D., Yao, Z., Cosley, D., & Fussell, S. R. (2015). *Two is better than one: Improving multilingual collaboration by giving two machine translation outputs*. Proceedings of the 18th ACM Conference on Computer Supported Cooperative Work & Social Computing

The researchers in this study explored the use of multiple machine translation outputs in MT-mediated chat. They used two different MT systems (Google and Bing) for Mandarin-English translation, and compared the results to using English on both sides and using only one MT system.

The researchers conducted a user study with a task-based scenario involving navigating a map. They found that using two MT systems was better than using one or using English on both sides. In some cases, the use of two MT systems was nearly equivalent to using English.

![Two MT systems chat (Google + Bing)]({{ "/assets/img/posts/mt-chat-3-two-systems-chat.png" | relative_url }})

One surprising finding was that participants did not report a higher workload when using two MT systems, and in fact reported a lower workload compared to using one MT system. However, the workload was still higher than using English on both sides.

One limitation of the study is that the two MT systems used in the experiment did not produce particularly high-quality translations, which may have contributed to the effectiveness of the approach.

In my work, I explored showing multiple translations in the user interface from different translation systems. Unfortunately, the translations from modern MT systems were often very similar so there may not be as much benefit. I also found it challenging to design user interfaces that could work for both the reading and writing side of communication, and having multiple translations plus back-translations on the writing side took up too much screen space.

#### Beyond translation: Design and evaluation of an emotional and contextual knowledge interface for foreign language social media posts

Lim, H., Cosley, D., & Fussell, S. R. (2018). *Beyond translation: Design and evaluation of an emotional and contextual knowledge interface for foreign language social media posts*. Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems

The researchers in this study explored the use of multiple techniques to enhance the translation of social media posts. They used named entity recognition to identify words that could be linked to Wikipedia, added a display showing the sentiment of the translated post, and extracted sentiment themes from the posts. The study focused on Facebook profiles in other languages.

![Emotional context with sentiment and named entities]({{ "/assets/img/posts/mt-chat-3-emotional-context.png" | relative_url }})

The researchers conducted a user evaluation of the enhanced translation system and found that it was perceived positively by users. Users reported that they were able to comprehend posts better using the enhanced system, and were more willing to engage with the posts (e.g. liking them). However, there was no significant effect on the desire to socialize or make friends with the poster.

The researchers also found that the enhanced system slightly reduced cognitive load, compared to using only the translated text.

In my project, there could be benefits to integrating health information in this way, especially if it's professionally translated in multiple languages. Doctors might perceive Wikipedia links as too risky, but there may be translations of Mayo Clinic or other trusted resources available.

#### Three Directions for the Design of Human-Centered Machine Translation

Robertson, S., Deng, W. H., Gebru, T., Mitchell, M., Liebling, D. J., Lahav, M., … Salehi, N. (2021). *Three Directions for the Design of Human-Centered Machine Translation*.

Robertson et al. (2021) discuss the challenges of machine translation and propose three directions for future research in human-centered machine translation. These include helping users craft good inputs, helping users understand translations, and expanding interactivity and adaptivity. They ran a social media survey and also ran a pilot test of TranslatorBot.

![Three directions for human-centered MT]({{ "/assets/img/posts/mt-chat-3-three-directions.png" | relative_url }})

One key idea is that translation tools should be able to identify messages that are difficult to translate and provide strategies to adjust the text. For example, TranslatorBot will warn users if their message is very long or if they use words that are unstable under backtranslation.

Another important direction is making it easier for users to understand the translations. This could include using quality estimation models to help users assess the accuracy of the translation, and providing easy access to backtranslation and bilingual dictionaries.

Finally, the authors suggest exploring ways to make machine translation more interactive and adaptable. This could include allowing users to prioritize the accuracy of certain words or phrases, and utilizing contextual information such as chat history to improve the quality of the translations. These ideas could be useful for designing the user interface of a healthcare chat system.

Overall it's a good read! For my project, they suggest several ideas along the same direction I'm headed:

- Could we use back-translation to estimate stability? I need to read (Mehta et al., 2020)
- Integrating a bilingual dictionary or Wiki links for sensemaking
- Users in healthcare need adequacy more than fluency, could we tune a MT system for that?
- Are there ways to integrate chat history?

#### Bridging Fluency Disparity between Native and Nonnative Speakers in Multilingual Multiparty Collaboration Using a Clarification Agent

Duan, W., Yamashita, N., Shirai, Y., & Fussell, S. R. (2021). Bridging Fluency Disparity between Native and Nonnative Speakers in Multilingual Multiparty Collaboration Using a Clarification Agent. *Proceedings of the ACM on Human-Computer Interaction*, *5*. doi:10.1145/3479579

In this study, researchers tested the effectiveness of a new automated speech recognition (ASR) and text-to-speech (TTS) bot designed to assist non-native speakers (NNS) in communication. The bot uses word frequency analysis to identify and interrupt the conversation to ask for clarification on words that NNS are unlikely to know.

Three conditions were tested in the study: the use of the ASR/TTS bot, a "dumb" baseline version of the bot, and no bot at all. The results of the study showed that the ASR/TTS bot was effective in helping NNS communicate more evenly with native speakers (NS), and that even the baseline version of the bot was useful at times.

Participants in the study reported several benefits of using the ASR/TTS bot, including that it allowed NNS to ask for clarification without feeling embarrassed or self-conscious, and that it helped to bridge the gap in understanding complex words. Additionally, the bot's interruptions would sometimes "buy time" for NNS to try and understand the conversation before NS moved on.

Interestingly, the researchers also found that exposure to the ASR/TTS bot caused NS to change their behavior in subsequent sessions, making them more aware of their vocabulary choices and more likely to explain or avoid complex words.

In my project, the core idea of asking for clarification of complex words might make sense, similar to (Robertson et al., 2021)'s TranslatorBot.

Additionally, I like the study's approach of placing the burden of clarification on the speaker rather than the listener (who is already struggling). I could imagine more focus on writing tools rather than just trying to support the reader. I also like how the authors were aware of social dynamics and wanted to alleviate stress from the non-native speakers because they were already stressed. In a healthcare chat setting it might be similar to place more burden on the doctors to have effective communication rather than just giving patients a way to look up definitions of words. Although my solutions are unrefined in this area, I agree with the perspective of unburdening the disadvantaged party.

#### Backtranslation Feedback Improves User Confidence in MT, Not Quality

Zouhar, V., Novák, M., Žilinec, M., Bojar, O., Obregón, M., Hill, R. L., … Yankovskaya, L. (2021). Backtranslation Feedback Improves User Confidence in MT, Not Quality. *NAACL-HLT 2021-2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Proceedings of the Conference*

Zouhar et al. (2021) examines the effectiveness of using backtranslation to improve the quality of machine translation. The authors find that while backtranslation increases user confidence in the translation, it does not necessarily improve the quality of the translation itself.

The authors also experiment with paraphrasing and quality estimation to improve translation quality. They found that paraphrasing also increases user confidence in the translation, but it actually leads to decreased translation quality. They didn't find a benefit from quality estimation, though it's possible that the quality estimation method was too simple to be useful.

Overall, the paper shows that user confidence in a translation interface is not necessarily correlated with improved translation capabilities. This is an important finding for the design of future studies.

Although the paper raises doubts on several approaches, I remain optimistic that there may be a way to use backtranslation to improve user comprehension or to improve authoring for non-native speakers. I'm less optimistic about quality estimation after reading the paper though.

#### Beyond General Purpose Machine Translation: The Need for Context-specific Empirical Research to Design for Appropriate User Trust

Deng, W., Mehandru, N., Robertson, S., & Salehi, N. (2022). *Beyond General Purpose Machine Translation: The Need for Context-specific Empirical Research to Design for Appropriate User Trust*. arXiv preprint arXiv:2205.06920

This paper was very similar to "Reliable and Safe User of Machine Translation in Medical Settings" (Mehandru et al., 2022). But it added many citations on user interfaces. This paragraph is worth quoting:

> Researchers have also designed and evaluated interfaces that provide additional information other than the back- translation, such as two different translations \[15, 61\], highlights of key words \[14, 26\], emotional and cultural context \[26\], and numerical indications of translation quality \[34\]. Lab studies suggest that additional information can improve message recipients' perceived understanding without increasing the mental workload \[14, 15, 26, 61\], but it is not clear from these studies whether users' perceived understanding aligns with their actual understanding of the intended meaning \[43\]. In other words, we do not know whether these interventions help users appropriately calibrate their trust in MT, or whether it promotes trust indeterminately even when translations are incorrect.

It seems to argue against (Robertson and Diaz, 2022) to some extent, suggesting that seamful design for MT may not help users to identify poor translations.

The above quote seems to say that it's a hopeless quest, but I disagree. The field has experimented with many approaches and had limited success in building a high quality human+computer system. I suspect we're in need of a paradigm shift rather than more research of the same type, and I feel even more confident that a paradigm shift to language learning has a chance at being effective.

------------------------------------------------------------------------

### Other user studies

These papers didn't explore user interface changes; they sought more to understand the challenges in MT-mediated communication.

#### Machine translation vs. Common language: Effects on idea exchange in cross-lingual groups

Wang, H. C., Fussell, S. R., & Cosley, D. (2013). Machine translation vs. Common language: Effects on idea exchange in cross-lingual groups. *Proceedings of the ACM Conference on Computer Supported Cooperative Work, CSCW*, 935-944. doi:10.1145/2441776.2441882

In this study, researchers explored the impact of machine translation on communication productivity and comprehension, comparing brainstorming in English to brainstorming in native language with machine translation. The study found that while machine translation can improve productivity of ideas, it can also lower comprehension.

![Brainstorm study MT vs common language]({{ "/assets/img/posts/mt-chat-3-brainstorm-study.png" | relative_url }})

This trade-off may be acceptable for certain applications, but could be problematic in others where comprehension is critical like healthcare.

In my project, I'm aware of the challenge and I've been working to support better comprehension, whether through multiple translations or integrated bilingual dictionaries.

#### Multilingual Chat through Machine Translation: A Case of English-Russian

Şahin, M., & Duman, D. (2013). Multilingual Chat through Machine Translation: A Case of English-Russian. *Meta*, *58*(2), 397-410. [https://doi.org/10.7202/1024180ar](https://doi.org/10.7202/1024180ar)

This paper explored the use of machine translation in English-Russian communication. The authors found that the MT-mediated conversation worked surprisingly well, with about half of the messages being translated perfectly and the majority being accurate and intelligible.

The authors remained positive and optimistic about the future of MT-mediated communication despite any challenges, though they did express some concern about using it in high-stakes situations like healthcare. Overall, their tone was much more positive than other works in the field.

#### Multilingual Communication via Best-Balanced Machine Translation

Pituxcoosuvarn, M., & Ishida, T. (2018). Multilingual Communication via Best-Balanced Machine Translation. *New Generation Computing 2018 36:4*, *36*, 349-364. doi:10.1007/S00354-018-0041-7

This paper introduces the concept of "quality of message" (QoM), which considers not only the quality of the machine translation but also the writing proficiency of the author and the reading proficiency of the reader.

The authors used this concept to determine the best language for participants to read and write in, in three conditions: all English, all native language with machine translation, or a best-balanced approach. They found that the QoM of a message had a relationship with the likelihood of a conversation breakdown, and that generally, the less variation in QoM, the less variation in talkativeness.

The findings of this study suggest that the QoM concept could be useful in determining when a doctor should switch from writing in English to writing in the patient's native language, or from reading in English to reading in the patient's native language. It also suggests that patients with limited English proficiency may be more forthcoming with their doctors when chatting in their native language even with machine translation.

#### Opportunities for Human-centered Evaluation of Machine Translation Systems

Liebling, D. J., Robertson, S., Heller, K., & Deng, W. H. (2022). *Opportunities for Human-centered Evaluation of Machine Translation Systems*. 229-240. doi:10.18653/V1/2022.FINDINGS-NAACL.17

This paper discusses the use of machine translation in healthcare and highlights the need for better metrics to evaluate its effectiveness. The authors emphasize that a machine translation system is more than simply the machine translation model. The success of a machine translation system includes not only the quality of the model but also the quality of the user interface for the goal it's addressing.

They also emphasize the importance of adequacy in task success, despite the traditional focus on fluency in metrics like BLEU. METEOR and COMET are suggested as adequacy metrics.

> There is growing evidence that MT is widely used in high-stakes contexts such as healthcare (Vieira et al., 2020)

That's an interesting change of perspective -- It's not a question of whether we can make machine translation useful or not. It's already being used, and our work could make it safer.

Overall this is a good summary paper to read.

#### Understanding Cross-lingual Pragmatic Misunderstandings in Email Communication

Lim, H., Cosley, D., & Fussell, S. R. (2022). Understanding Cross-lingual Pragmatic Misunderstandings in Email Communication. *Proceedings of the ACM on Human-Computer Interaction*, *6*. doi:10.1145/3512976

This paper presents a detailed study on email miscommunication between native and non-native speakers of English. The findings showed that it is generally better for non-native speakers to use English instead of machine translation, as their messages are received more positively and their intentions are conveyed more accurately. The study also found that providing information about the speaker/writer can be helpful in improving communication, potentially due to a "humanizing" effect.

The results showed that length of time spent in an English-speaking country was relevant for the communication of politeness intentions but not for other factors. The non-native speakers in the study had relatively high TOEFL scores, at the 92nd percentile.

In my project, this has me wondering when NNS_EN \< NNS_TR. Below what TOEFL score would it be better to translate? Above what TOEFL score would it be better for patients to write in English with supporting technology?

The work on showing the name and background of the participants also got me thinking about ways to help the patient and doctor see one another as people more, even in a chat medium. Even simple things like clear photos of each might help. Or a quick introduction, which sadly is often skipped in a rush, but this study suggests that it might help the conversation make it through any challenges.

------------------------------------------------------------------------

### Computer-Aided Translation (CAT) tools

I found a number of papers meant to aid translators in writing translations, and they may be relevant in making user interfaces for text entry in healthcare chat.

#### Target-Text Mediated Interactive Machine Translation

Foster, G., Isabelle, P., & Plamondon, P. (1997). Target-Text Mediated Interactive Machine Translation. *Machine Translation*, *12*, 175-194. doi:10.1023/a:1007999327580

This paper was an early exploration of the use of interactive machine translation (IMT), focusing on word completion using both the source sentence and partial translation. The authors faced some challenges in combining the probabilities correctly and in accessing the translation model probabilities. They also found that the translation model was effective for nouns, verbs, and open-domain words, but the regular language model was better for closed-domain words, making it difficult to combine the two effectively.

The authors proposed a method for preventing re-translation using an "anti-cache" and showed that IMT was possible with 1997 technology. They concluded that IMT was a better fit for the needs of skilled translators, as it allowed for more control and flexibility in the translation process.

#### Using word alignments to assist computer-aided translation users by marking which target-side words to change or keep unedited

Espla, M., Sánchez-Martínez, F., & Forcada, M. L. (2011). *Using word alignments to assist computer-aided translation users by marking which target-side words to change or keep unedited*. Proceedings of the 15th Annual conference of the European Association for Machine Translation

Espla, Sánchez-Martínez, & Forcada (2011) proposes using word alignments to assist computer-aided translation users by marking which target-side words to change or keep unedited. The authors used GIZA++ alignment to spot similarities and differences in the alignments and identify parts of the original text that may not have been translated.

The authors were positive about the results of their approach, but it is unclear from the paper how they evaluated the effectiveness of their method and whether it would be useful for real-world translation users.

I was hopeful about this paper because I was searching for publications that used machine translation attention weights to help show the inner workings of the system. Unfortunately this paper predates transformers by a lot, and I didn't see much in the way of ideas to use.

#### User Evaluation of Interactive Machine Translation Systems.

Alabau, V., Leiva, L. A., Ortiz-Martínez, D., & Casacuberta, F. (2012). *User Evaluation of Interactive Machine Translation Systems*. Proceedings of the 16th Annual conference of the European Association for Machine Translation

This paper presents a study on the design of an effective user interface for interactive machine translation (IMT), comparing it against a phrase-based baseline. The authors found that their initial system was not an improvement, but after addressing feedback, the second system performed much better. The findings suggest that it is important to avoid jostling the predictions too much, to not undo any conversions that the user is making, to keep the user interface simple, and to pay attention to details like capitalization and number formatting. Overall, the study emphasizes the importance of UI design in evaluating an IMT system.

#### MT Quality Estimation for Computer-assisted Translation: Does it Really Help?

Turchi, M., Negri, M., Federico, M., & Kessler, F.-F. B. (2015). *MT Quality Estimation for Computer-assisted Translation: Does it Really Help?* Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)

Turchi et al. (2015) investigates the effectiveness of machine translation quality estimation (QE) for computer-assisted translation. The authors conducted a study with human translators using the Mate-Cat tool, comparing the performance of translators with and without QE indicators.

The study found that QE had a mild benefit for computer-assisted translation, with translators using QE indicators producing slightly better translations than those without.

Their QE model is using source-side complexity metrics and target-side language model probabilities to compute a score. I think it's unlikely that a target-side language model probability would be useful in a modern QE model because neural machine translation is so good at fluency.

It's also possible that the color indicators may have needed more time for users to get used to, and the randomization of the indicators may have dampened the potential benefits.

In my own work, I would be interested in using QE to inform authors about the quality of their text, rather than for translation tasks.

#### INMT: Interactive Neural Machine Translation Prediction

Santy, S., Dandapat, S., Choudhury, M., & Bali, K. (2019). INMT: Interactive Neural Machine Translation Prediction. *EMNLP-IJCNLP 2019-2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, Proceedings of System Demonstrations*, 103-108. doi:10.18653/V1/D19-3018

Santy et al. (2019) presents a system for interactive neural machine translation prediction (INMT), which uses a neural machine translation (NMT) model to suggest word and phrase completions in real-time as the user types. The authors demonstrate the system using a beam length of 2 to avoid diversity problems, but note that this can lead to challenges with partial words in the search.

The INMT system has a user interface that allows users to see which source words have been translated so far and provides BLEU scores for completion suggestions. However, the authors acknowledge that the completion user interface is not ideal and that the system only leads to a 30% reduction in keystrokes.

![INMT alignment visualization]({{ "/assets/img/posts/mt-chat-3-inmt-alignment.png" | relative_url }})

This study presents an interesting approach to using NMT for real-time translation, but the limitations of the system suggest that it may not be suitable for all contexts. In particular, the system may be useful for providing a "training wheels" approach to translation for doctors who have some knowledge of a second language, but it is unlikely to be effective for patients who have little or no knowledge of the second language. Additionally, the alignment visualization provided by the INMT system could be useful for some applications, but it is unclear how it could be incorporated into a healthcare chat interface.

------------------------------------------------------------------------

### Healthcare machine translation

#### Usability Issues in an Interactive Speech-to-Speech Translation System for Healthcare

Seligman, M., & Dillinger, M. (2006). *Usability Issues in an Interactive Speech-to-Speech Translation System for Healthcare*. Proceedings of the First International Workshop on Medical Speech Translation

Seligman & Dillinger (2006) examines usability issues in an interactive speech-to-speech translation system for healthcare. The authors provide a useful introduction to the challenges of translation in healthcare and discuss some of the proprietary technology used in their system, including techniques for ensuring accurate lexical senses in back-translation and the use of meaning cues to improve translation quality.

One of the key features of the system described in the paper is the ability to gradually tune word-sense preferences, which the authors argue can improve translation quality. Additionally, the system includes a "save as shortcut" feature that allows users to save commonly used phrases for later use, which could be useful in a healthcare chat interface.

However, the paper is somewhat dated and does not include any usability testing, so it is unclear how effective the system described would be in a modern healthcare context. Additionally, the use of voice commands and voice enrollment for automatic speech recognition may not be ideal for all users, particularly those who are not experts in the technology.

Their description of Meaning Cues sounds similar to what I'm doing with bilingual dictionaries.

#### Real-time Multi-media translation for healthcare: a usability study

Seligman, M., & Dillinger, M. (2011). *Real-time Multi-media translation for healthcare: a usability study*. Proceedings of Machine Translation Summit XIII: Papers

Seligman & Dillinger (2011) presents a usability study of a real-time multi-media translation system for healthcare, called Converser. The authors describe the challenges of deploying the system, including issues with literacy, font size and style, language switching, text-to-speech speed, and security. They also discuss the challenges of training users on the system and the difficulties of using the system in a hospital environment, where space and ambient noise can be limiting factors.

Overall, this paper provides a useful overview of the challenges of deploying a real-time translation system in a healthcare setting. This paper may be useful for identifying potential challenges and limitations of using translation technology in healthcare, but it does not provide definitive answers about the effectiveness of such systems.

#### Automatic Speech Translation for Healthcare: Some Internet and Interface Aspects

Seligman, M., & Dillinger, M. (2013). *Automatic Speech Translation for Healthcare: Some Internet and Interface Aspects*. Proceedings of the 10th International Conference on Terminology and Artificial Intelligence (TIA-13)

Seligman & Dillinger (2013) presents an update on the development of their real-time multi-media translation system for healthcare, Converser 4.0. The authors describe some of the challenges of deploying the system, including issues with internet connectivity and the use of cloud-based automatic speech recognition.

The authors also discuss the use of meaning cues and other techniques to improve the quality of the machine translation, and describe some updates to the user interface, including a "feeling lucky" feature for the machine translation. In this paper they mention that WordNet is one of the sources for meaning cues.

Overall, this paper provides a brief update on the development of the Converser system, but it does not include much new information.

#### Local Health Department Translation Processes: Potential of Machine Translation Technologies to Help Meet Needs

Turner, A. M., Mandel, H., & Capurro, D. (2013). Local Health Department Translation Processes: Potential of Machine Translation Technologies to Help Meet Needs. *AMIA Annual Symposium Proceedings*, *2013*, 1378.

Turner et al. (2013) survey the use of machine translation technologies in local health departments. The study, which was part of the TransPHorm project funded by the National Library of Medicine, aimed to identify potential ways that machine translation could help health departments better serve their communities.

Most health departments felt they were underserving their communities, regardless of the size or resources of the department. They also found that most departments used in-house bilingual staff for translation, and that there was a high level of awareness and interest in shared translation resources even though few departments contributed to shared translations.

Health professionals were optimistic about machine translation, especially if it were tailored to public health communication.

Overall, the paper felt more optimistic about machine translation compared to (Mandel and Turner, 2013), which I summarized in a prior post.

#### Evaluation and revision of a speech translation system for healthcare

Seligman, M., & Dillinger, M. (2015). *Evaluation and revision of a speech translation system for healthcare*. Proceedings of the 12th International Workshop on Spoken Language Translation: Papers

Seligman & Dillinger (2015) presents an evaluation and revision of the Converser for Healthcare speech translation system. The authors describe their use of off-the-shelf components for automatic speech recognition, machine translation, and text-to-speech, and discuss feedback from both patients and staff who used the system.

The authors found that the system was generally well-received by patients and staff, and that it was useful in a variety of medical scenarios. In particular, it was best received by technology-positive participants "in a pinch". They also identified challenges in verification of translations. In response to these challenges, the authors revised the user interface to adopt a "check before sending" and "edit after sending" paradigm.

This quote resonates with my experience:

> While numerous staff members (and, separately, their managers) praised the ability to verify translations, others also stressed that verification consumed limited time.

This could mean that staff who are very busy may skip verification at times, which could lead to miscommunications and medical risks.

This paper also included a picture of meaning cues, which could be relevant for my work:

![Meaning cues]({{ "/assets/img/posts/mt-chat-3-meaning-cues.png" | relative_url }})

There are some differences in how meaning cues work in this system compared to what I'm working on. In my use case, I'm integrating the dictionary to help teach the user the secondary language rather than focusing on the meaning cues for the user's primary language.

Overall, this paper provides valuable insights into the use of speech translation technology in a healthcare setting. The authors' findings suggest that the system was useful and well-received, which was sorely needed in their previous publications.

This was also the most recent paper I found by this group of authors. I tried searching for Converser or Spoken Translation, but I didn't find anything recent.

#### Using Google Translate in the hospital: A case report

Leite, F. O., Cochat, C., Salgado, H., Costa, M. P. D., Queirós, M., Campos, O., & Carvalho, P. (1 2016). Using Google Translate^© in the hospital: A case report. *Technology and Health Care*, *24*, 965-968. doi:10.3233/THC-161241

Leite et al. (2016) present a case study of using Google Translate for Ukrainian-Portuguese translation in a hospital setting. One complication was that a family member was available for translation, but the patient thought the family member was trying to keep him hospitalized. The authors report that the translation was successful in the case study even though it concerned very complex mental health challenges.

#### Workshop on Machine Translation (WMT) 2016, Biomedical Track

The biomedical track mainly concerns biomedical titles and abstracts from scientific publications, predominantly using training data from the Scielo corpus. They also included a parallel corpus of MEDLINE titles.

Only Spanish-English and English-Spanish attracted multiple submissions. I took notes on two high-scoring teams, IXA and TALP. They both used Moses for their MT system. The IXA team focused on the challenge of out-of-vocabulary words (OOVs). They used SNOMED-CT to augment translation vocabulary and further augmented vocabulary using morphology and transliteration.

The TALP team also worked on OOVs, but used a bilingual embedding to expand their vocabulary. They also worked to improve the fluency of translations using a neural character-based language model.

#### Babeldr vs Google Translate: A user study at Geneva university hospitals (HUG)

Bouillon, P., Gerlach, J., Spechbach, H., Tsourakis, N., & Mallem, H. (2017). *Babeldr vs Google Translate: A user study at Geneva university hospitals (HUG)*. 20th Annual Conference of the European Association for Machine Translation (EAMT)

Bouillon et al. (2017) study the effectiveness of BabelDr, their MT system, compared to Google Translate with hospital staff and patient actors.

BabelDr forces staff to search for predefined translations and structured questions such as yes-no questions. In contrast Google Translate will produce translations of any input.

Staff found BabelDr frustrating at times because they couldn't say exactly what they wanted. However, they were more accurate in diagnosis than they were with Google Translate, and it's wonderful to see researchers evaluate a critical healthcare task like diagnosis rather than just BLEU scores or subjective opinions on translation quality.

![BabelDr comparison with Google Translate]({{ "/assets/img/posts/mt-chat-3-babeldr.png" | relative_url }})

The evaluation didn't feel like an entirely fair comparison, because when doctors could not find a translation in BabelDr they would have to rephrase and try again. In contrast, Google Translate didn't reject any input. On the other hand, it's a conclusive test of the user interface. Like other papers I've seen, it's especially helpful to use closed-ended questions in a translation situation because it allows the system to rely on professional translations.

This is similar to what I would've done in telemedicine with chatbot translation.

#### Comparison of the quality of two speech translators in emergency settings : A case study with standardized Arabic speaking patients with abdominal pain

Spechbach, H., Mallem, I. S. H., Gerlach, J., Tsourakis, N., & Bouillon, P. (2017). *Comparison of the quality of two speech translators in emergency settings : A case study with standardized Arabic speaking patients with abdominal pain*. European Congress of Emergency Medicine, (EUSEM 2017)

This is a highly abbreviated version of the previous paper on BabelDr.

#### The MeSpEN Resource for English-Spanish Medical Machine Translation and Terminologies: Census of Parallel Corpora, Glossaries and Term Translations

Villegas, M., Intxaurrondo, A., Gonzalez-Agirre, A., Marimon, M., & Krallinger, M. (2018). *The MeSpEN Resource for English-Spanish Medical Machine Translation and Terminologies: Census of Parallel Corpora, Glossaries and Term Translations*. LREC MultilingualBIO: multilingual biomedical text processing

Villegas et al. (2018) presents the MeSpEN resource, a collection of parallel corpora, glossaries, and term translations for English-Spanish medical machine translation. The authors demonstrate the need for specialized medical data sets, citing previous work showing the inadequacy of general-purpose models for medical translation tasks. The MeSpEN resource includes data from a variety of sources, including academic publications and patient-facing resources like MedlinePlus. The authors also provide 46 bilingual glossaries and discuss the MDM-Portal, a database of translated questionnaires.

This paper provides a wealth of specialized data for English-Spanish medical machine translation. The MeSpEN resource, the EMEA corpus, and the MDM-Portal, in particular, may be potential sources of parallel data for medical chat translation systems.

#### A Speech-Enabled Fixed-Phrase Translator for Emergency Settings: Crossover Study

Spechbach, H., Gerlach, J., Karker, S. M., Tsourakis, N., Combescure, C., & Bouillon, P. (2019). A Speech-Enabled Fixed-Phrase Translator for Emergency Settings: Crossover Study. *JMIR Med Inform 2019*

Spechbach et al. (2019) presents a speech-enabled fixed-phrase translator called BabelDr, which is designed for use in emergency settings. The authors conducted a study with 12 French-speaking doctors and 2 Arabic-speaking patients, in which the doctors were asked to use BabelDr to diagnose the patients' simulated symptoms. The study found that all doctors were able to reach the correct diagnosis using BabelDr, indicating that the tool is effective for facilitating communication in emergency settings.

![BabelDr speech 2019 study]({{ "/assets/img/posts/mt-chat-3-babeldr-speech.png" | relative_url }})

However, the study also raises some questions about the efficiency of using a fixed-phrase translator in a healthcare setting. The time to diagnosis was relatively long compared to diagnosis of cystitis in telemedicine in my experience. Doctors also remained frustrated with being limited to a fixed bank of phrases.

I'm concerned that the authors needed to set the system category to "lower back pain" to allow the search to work. That suggests that the domain of medicine may be narrowed sufficiently even before the medical professional says their first sentence. I also had questions about the way they search for similar messages -- I expect that the findings would be highly sensitive to the quality of the similarity algorithm, which is not described.

I'd like to see subsequent research explore a combination between a fixed-phrase translator and open-domain translator like Google Translate to address the limitations of the phrase bank.

#### A Smart Chatbot Architecture based NLP and Machine Learning for Health Care Assistance

Ayanouz, S., Abdelhakim, B. A., & Benhmed, M. (2020). *A Smart Chatbot Architecture based NLP and Machine Learning for Health Care Assistance*. Proceedings of the 3rd International Conference on Networking, Information Systems & Security

This paper presents a brief review of research on the use of multilingual chatbots in healthcare settings. The authors suggest that user satisfaction should be the primary measure of the effectiveness of these chatbots, but this will be problematic. In my experience, patient satisfaction is most correlated with short-term things like whether the patient got antibiotics, not long-term health benefits.

#### Multilingual Healthcare Chatbot Using Machine Learning

Badlani, S., Aditya, T., Dave, M., & Chaudhari, S. (2021). *Multilingual Healthcare Chatbot Using Machine Learning*. 2021 2nd International Conference for Emerging Technology (INCET)

This paper surveys some ideas in multilingual chatbots, and it's interesting to see that it's similar in many ways to my experience in healthcare. However, it's mainly an idea survey rather than a system evaluation so I didn't take much away from it.

#### Findings of the WMT 2021 Biomedical Translation Shared Task: Summaries of Animal Experiments as New Test Set

Yeganova, L., Wiemann, D., Neves, M., Vezzani, F., Siu, A., Unanue, I. J., … Yepes, A. J. (2021). *Findings of the WMT 2021 Biomedical Translation Shared Task: Summaries of Animal Experiments as New Test Set*. Sixth Conference on Machine Translation

The authors note that the quality of machine translations has improved significantly in recent years, but also highlight some cases where translations were not entirely accurate. They provide some examples of recent challenges:

> There have been cases in which abbreviations were not translated correctly (e.g. HGS vs FPM for fuerza de prensión manual) and some times specific terms were not translated, e.g. receiver operating characteristic curve. Only in a few cases word gender was different to the article one. There are examples of words that are not translated properly for instance adnexal has been translated as adnexiales instead of anexas by one of the teams.

I saw the abbreviation problem with "UTI" in a previous post. Also, all systems were neural machine translation despite some preference for phrase translations in healthcare. It's plausible that evaluation has been too sensitive to fluency and not sensitive enough to adequacy, as a result of over-reliance on BLEU as the primary metric.

I was also disappointed that it's a unified biomedical track which combines many different kinds of biomedical communication. In particular, I feel that doctor-patient communication is quite different than doctor-doctor communication or scientist-scientist communication, and that those types of communications may need separate translation models or at least that the translation models should be aware of the recipient of the communication.

#### How well do real-time machine translation apps perform in practice? Insights from a literature review

Pluymaekers, M. (2022). *How well do real-time machine translation apps perform in practice? Insights from a literature review*. Proceedings of the 23rd Annual Conference of the European Association for Machine Translation

Pluymaekers (2022) is a literature review of the performance of real-time machine translation apps in practice. The review focuses on studies of the use of machine translation in communication apps, particularly in the healthcare domain. The author focuses on "fitness for purpose" as a key factor in evaluation -- Machine translation is being applied in the context of a large system, and should be evaluated by how well it allows users to achieve their goals. This is aligned with the frequent statement in healthcare that adequacy is more important than fluency for medicine. The review includes a number of studies that evaluate the ability of machine translation to facilitate accurate diagnosis, which is a good example of fitness for purpose.

However, many of the papers included in the review are relatively old, with the most recent study being from 2019. There is a need for more recent research on the performance of machine translation in healthcare contexts, as the field of neural machine translation has advanced significantly since many of the studies were published.

------------------------------------------------------------------------

### Course-correcting my project

I most recently read the "three directions" paper and I'll organize my thoughts in a similar way.

#### Directions that may help understand translations

- Showing multiple translations -- There's some evidence that this helps, and I'm sure it's best when the MT systems are unreliable and make different errors. That's not the case with the MT systems I have right now, but could become the case in the future if I train one especially for doctor-patient communication.
- Linking words to external knowledge sources -- There's some evidence that this can help, whether bilingual dictionaries or Wikipedia. In the healthcare space, linking to Mayo Clinic or another translated resource may be a good option too. One downside is that it places more burden on the reader, who may already be struggling.

I'm not optimistic about:

- Quality estimation for understanding -- There are mixed results of using this in systems, and it's very hard to have reliable QE models especially with good NMT models.

#### Directions that may help to write for MT

- Back-translation for review -- I'm optimistic about back-translation because it's so widely used even in healthcare. That said, it needs more work to ensure that it actually helps people assess translation quality rather than increasing trust without increasing quality.
- Flag "unstable" phrases -- This seems worth exploring. It might be hard to keep latency low if I'm using web APIs though.
- Redirect towards pre-translated databases -- I've read about multiple successes from pretranslated content. I'm not sure if I want to build such a database for this project, but I might consider using an already-existing database if one is available. In a company, this would be a great option -- It's simple and reliable. Moreover, there's already pressure to standardize physician content anyway so the database may exist depending on your company.
- Automatically ask for clarification on rare words -- The paper that did this in a speech system was quite effective. There might be a way to use click data on definitions to bootstrap data on word familiarity in secondary languages.

These directions may help for writing in a secondary language, once the writer knows enough:

- Word completion, possibly with the Google Docs interface -- Once the doctor is learning Spanish, I bet ideas from CAT like word completion would help a lot. The big questions I have are 1) What's the best way to use the other person's chat as context into the language model? 2) How can we make sure that the user double-checks the content, even when rushed?

I'm not optimistic about:

- Suggesting revision based on quality estimation
- Detecting misunderstandings with lexical chains

#### Other directions

The quality of message (QoM) paper was interesting, and the papers showing that ESL communication was often better than relying on MT. I wonder if the chat could start by helping the doctor and patient decide the best communication strategy based on their language proficiencies, MT quality, and any medical risk factors in the case? For instance something like this:

![Communication strategy diagram]({{ "/assets/img/posts/mt-chat-3-communication-strategy.webp" | relative_url }})

The one thing I missed was how to analyze the patient's case -- the medical severity and urgency of the case should be considered in deciding the best option.

I have a hunch that rapport is even more important in MT-mediated chat. The literature had hints that it may be critical to weathering all the communication challenges. I bet there's a way to give physicians more of an opportunity to establish rapport with one or two automated questions.

### Assorted other observations

BBN TransTalk would've been a good fit for hospitals, in contrast with Converser. The Converser papers often mentioned challenges like needing to cart around a laptop or users struggling with the interface. TransTalk was much simpler and more portable so I think it would've worked well.

I'm optimistic about some changes in research direction of the field:

- I'd love to see medical machine translation corpora split up more, for instance patient-doctor communication (chat, pamphlets, informational websites), doctor-doctor communication (clinical notes), scientist-scientist (academic papers).
- It's worth replicating some older experiments from before the advent of high quality neural machine translation.
- I'd love to see machine translation competitions emphasize adequacy or fitness for task. For instance in the medical field measuring diagnostic accuracy, triage accuracy, or treatment accuracy.
- I find myself pondering the differences between the fields of human-computer interaction (HCI) and user experience (UX). It's often hard to articulate the differences between the fields, but I found while reading so many HCI papers that there's often a lack of attention to detail in the user interface, ranging from the readability of fonts to layout to clutter. Papers often focus on one main change, but that change is being evaluated in the context of all the little details of the user interface.

### What's next? (Short term)

I'm headed on travel starting next week so I'll be quiet for a little while.

I'm most interested in these directions:

- Visualize NMT attention to enable users to explore definitions easier. I thought for sure I'd discover a research paper on this, but I haven't yet.
- Use multiple back-translations for translation instability and feedback to the writer
- Improve my user interface for definitions; it's too verbose
- Build a MT model that's more focused on adequacy for patient-doctor communications. That *might* make different kinds of mistakes as modern NMT systems and therefore it might be useful to include in a "two translations" type of interface

### What's next? (Long term)

- I've got a lot more papers to read but I want to find a better balance between reading and building. That's tough to do while also traveling!
- I've got a long list of things to follow up on from this review, such as potential corpora or CAT tools to check out.
- The papers on public health brochures had somewhat different needs than patient-doctor chat. I wonder how hard it would be to build a system for them? If I build a web system that people can use for chat as a demo, it might be worthwhile to include a page for pamphlet translation.
- I'd love to do a user study and actually publish if possible, but I'm not sure if I'll have the time or money for it when I get that far. I'd particularly like to develop an adequacy aka "is it good enough" metric for diagnosis and treatment, because my experience in healthcare is that diagnosis and treatment are often inexact.

### Appendix: Notes on using ChatGPT

I had taken notes on all the papers, but those aren't suitable for distribution. I thought it might be good to try using ChatGPT to convert those notes into narrative form; my experience is that it can't really generate true information aside from general knowledge, but it can generate content that's consistent with the input, so if the information is in the input it should be able to do it. (At least that's my interpretation of it)

I got a lot of value out of [learning more about prompt engineering](https://learnprompting.org/).

Things that worked:

- Setting expectations of the answer type by using a format like "Notes: … Narrative:"
- Giving examples of how I like to convert notes to narratives. This helped make sure it mostly sounded like me.

Things that didn't work:

- Just asking for a summary
- Trying to group the papers into sections -- I couldn't figure out how to do this, but some of the posts I've read suggest it should be possible with the right prompting

Challenges:

- Sometimes it didn't include information that's valuable either to the project or readers and I had to add that
- It often misrepresented my opinions from the notes as the opinions of the paper authors (very bad!)
- It often had lots of nice-sounding but meaningless sentences so I found myself deleting around 10% of the sentences
- It's nice to include quotes when possible but ChatGPT usually wouldn't do that
- ChatGPT's input length was a challenge at times. I'm not sure the best way to go about that

Successes:

- I find it's tough to start a narrative but much easier to edit once I have something started
- If my notes about a paper were very negative, ChatGPT found a much more polite way to say that

------------------------------------------------------------------------

If you made it to the end, I truly appreciate it! If you saw any issues, or would like to discuss further, feel free to reach out.

