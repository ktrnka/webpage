---
layout: post
title: Localization in Swype
date: 2018-09-01
---

I stumbled into a conversation about localization the other day and thought back to my time at Swype and Nuance, wishing I had an article about the challenges we faced. For some context, Swype was a keyboard app for Android that was acquired by Nuance in 2011 and continued to grow for a few years at Nuance, including an iOS version. Depending on the year, Swype was available¹ in: Google store, Apple store, or preloaded on your phone via the manufacturer.

### Key challenges

The first key challenge is that the Swype keyboard supports many languages: In the last version of the app, there were 103 languages available². The linguistics team did a great job developing word lists and other resources for new languages, but couldn't do localization of the app strings. And for a long time we localized the entirety of the app into all supported languages.

The second key challenge is manufacturer-specific customization. That often involved changing the strings in the app, for instance removing the Swype branding from all strings. Customers often wanted localization in all languages so we often had to re-translate. These are companies like Samsung, LG, HTC, and so on.

### Issue 1: Company names and made-up words

We had to include the name *Swype* in many strings. In a language like Russian we'd [transliterate](https://en.wikipedia.org/wiki/Transliteration): keep the pronunciation similar but use a different alphabet. But that doesn't work in Chinese so we had to make up a different name. Then the translators needed access to a translation guide to ensure that we consistently translated the English brand name to the Chinese brand name.

It gets worse though: We used the term "swyping" to describe the act of dragging your finger through the letters. And we used that term in the help menus! So now we need to ask the Russian translator to come up with the verb form of the transliterated version of the brand name. And likewise for many languages. Eventually we cut this word out of all strings because it wasn't worth the effort.

### Issue 2: Working with translators

At that time, there wasn't a single website where you could just have the Android strings translated for you. We used an agency that had a wide pool of translators, but this had additional challenges:

- Some translators were hard to reach. For example, translation of Spanish was complete in a day but translation of Mongolian might take a week or two. That led to difficult decisions around releasing the updated app with partial updates to localization vs delaying the whole release.
- Each translator had a different way of working. For a long time it involved sending Word documents back and forth (ugh!). This caused two other problems: 1) ' would be converted to smart quotes and we needed to un-convert 2) Translators felt more free to edit and would often mangle variable placeholders such as "%s". Eventually we required XLIFF format but it took a while to get there.

### Issue 3: Consistency

One problem in translation is that the ambiguity of each language is different. In Spanish, to ask if someone wants a beer I might say "Quieres una cerveza?" or "Se quiere una cerveza?" They're both asking if you want a beer but the former is *tu* form that you'd use with friends and family while the latter is *usted* form and is more formal.

This affects localization because there are TONS of verbs. Take a string like "Show helpful tips". There's a different form of "show" for formal vs informal commands and you have to decide which to use.

Why is this a problem? Because we didn't instruct our translators on whether to use *tu* or *usted* form. Each translator decided for themselves. So some of our strings were in *tu* form and others *usted* form. As a result, our app felt inconsistent to Spanish speakers.

Eventually we solved this with a style guide, but the real problem is that the person setting it all up originally wasn't even aware that Spanish had a language feature that English doesn't. I'm not even sure how we caught this issue — probably we have a native tester or maybe a translator asked for clarification eventually.

### Issue 4: Dealing with branches of Swype

In the end, we maintained branches of our code base for several customers. This led to considerable problems because we couldn't afford to separately translate and update the 2–3 branches of the app that were under active development.

We had a loose collection of data and scripts to attempt to share translations between branches without overwriting de-branded content or re-branded content. Eventually this was centrally managed in a database with a web frontend.

Branching caused other problems so I'm going to say that the branching was the real culprit though it may have been unavoidable.

### Issue 5: Unsolved mysteries

It's reasonable to focus on what Android and iOS support — some combination of language and location such as en-US for US English. This paradigm works relatively well but breaks down as you start to support more languages than the operating systems:

- Hinglish: This is a mixture of Hindi and English written with English letters. In Swype it was more commonly used than Hindi. But the spellings aren't standardized and there's no ISO code for Hinglish. So when a user selects the Hinglish keyboard, should the app switch strings to Hinglish or should its strings match the operating system, which doesn't have Hinglish available?
- Serbian: This language can be written in Latin script or Cyrillic — [wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Serbian) says 47% favor Latin and 36% prefer Cyrillic. But again we have the same problem because there's no ISO code to distinguish.

### Quick tips

- Make a conscious decision about whether you need to translate ALL strings into ALL languages. Some of our help pages had been opened less than 100 times per year and those were definitely not worth it.
- Use standard tools and standard interchange formats whenever possible.
- Test your app with native speakers.
- Think about a style guide for each language.

### See also

- [Challenges of App Localisation](https://blog.prototypr.io/challenges-of-app-localisation-618add749450)
- [The Only App Localization Tutorial You Will Ever Need](https://phraseapp.com/blog/posts/the-only-app-localization-tutorial-you-will-ever-need/)

### Notes

1. There were also versions for Windows Mobile and a couple other small operating systems.
2. There were also several languages supported by our core code and shipped as a part of our SDK to manufacturers that weren't available in Swype itself, because we didn't have the resources to develop the keyboard layout and strings for those languages.
