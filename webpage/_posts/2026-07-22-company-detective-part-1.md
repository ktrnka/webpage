---
layout: post
title: "Trust, Bias, and the Sources Behind Deep Research"
date: 2026-07-22
description: "An honest company read from biased web sources: diversifying, debiasing, and balancing what reaches the LLM. Lessons from building Company Detective in 2024."
ai_disclosure: "TODO (Keith, KT-176): write the AI-usage disclosure for this post"
---

Every source you'd use to evaluate a company is biased in its own way. The company's own site is selling you. Glassdoor highlights the most furious employees. Reddit runs hot or cold depending on the subreddit. The question that got me started: how much of the real story can you infer from unreliable sources?

In the summer of 2024, after a layoff at Singularity 6, I made a list of ideas that might be fun to work on. I ranked them on whether I thought they could do some good in the world, whether I'd learn from them, and whether I was excited to build them - excited to build something that pushed the envelope in terms of quality of product experience. The first idea was [Future Crap]({% post_url 2024-06-24-future-crap-part-1 %}), which I've written about. 

The second idea became Company Detective. This post will focus on the product and motivation side of the project, and the next post will dive into the engineering. I also included many references at the end.

One note on timing: I built this back in 2024, before "deep research" was a product category or even a common phrase.

I've seen a lot of people go through layoffs. It's a bummer to see friends and coworkers affected. It's also a downer to see the overall industry trend and how many people are struggling. At the same time, there are a lot of jobs out there, but people go through these long processes, and it takes a while to find a fit. So I was thinking: can I automate some of the process that I follow when finding jobs? If so, maybe it could help others a little.

I had other motivations too. Of course, there was the motivation to learn - I wanted to really practice more with large language models and get a feel for that. There were also several interrelated systemic issues in the back of my mind, like [Zebras vs unicorns](https://medium.com/zebras-unite/zebrasfix-c467e55f9d96), [enshittification](https://pluralistic.net/2023/01/21/potemkin-ai/), and the craft of software development. I'm still searching for a better term than "craft". I think of building niche, high-quality software back in the day, and people often building it out of passion, seeing what's the best that we can make. So I was feeling a mixture of all these different things.

And the thing that I found particularly interesting with Company Detective is that I was trying to use it, in an old-school YC sense, to say: let me push the envelope in terms of company research as hard as I possibly can, and that will force me to solve a lot of problems in applied LLMs. So the efforts in research or engineering are really downstream from trying to push the envelope in terms of a particular user experience or product idea.

## What I was trying to build
Think of the no-BS scoop a friend who works there gives you in two minutes (is it a good place to work, and why), or the kind of candid, long-form account a journalist writes when they really dig into a company, the way the Theranos and WeWork deep-dives did. I was drawn to the question of how much might be possible from the public web.

The core of the challenge was credibility of information. This ties back to old motivations for the internet: if you think about PageRank and Google Search, it was really about how to use citation graphs to estimate the credibility of a web page. It's become less reliable since then though, as financial incentives pushed people to abuse the link graph. How could we get back to a reliable view of credibility?

When I think about my own research during a job search, I'm not just thinking about credibility in general but the credibility of any particular source. When I read a company's webpage, of course they're going to say they have wonderful core values, or that they're a leader in AI, or an innovator in this, that, or the other thing.

Back when I applied to Swype in 2011, I wanted a candid view of the product's strengths and weaknesses. I didn't rely on the company webpage; instead I read the beta user forums to develop a more honest review of the product, which gave me hints about the corporate priorities.

It's one thing to do that as a person, but it's another thing to consider building software to do that. In AI/ML solutions, I often consider: what's the best a human could do at this? Could that serve as an approximate upper bound for software? Some of the information a journalist digs up for those deep-dives was out there online before they published, just in places that are hard to find, or that people don't know about. When I think about my lived experiences from 98point6 and Singularity 6, how much of the candid insider info could we reconstruct from public sources?

## Credibility engineering: which source to trust for what

When I was trying to solve this, I felt that the upper bound is really limited by the context - and when I say context there, I mean the context to the large language model. It's very limited by what data sources we're pulling, how we're organizing those data sources, and how we make them digestible for an LLM. Also for the reader, keep in mind that this was 2024 when we didn't yet have deep research tools, didn't have reasoning models, and LLMs were just generally weaker.

This section is a survey of high-level directions in building a credible company research report.

Here's roughly how that shakes out for Singularity 6 (the studio behind the game Palia):

| Source | Company events | Product/update record | Employee experience | Player experience |
|---|---|---|---|---|
| Company websites | ~ mostly good news | ✓ authoritative | ✗ hype | ✗ cherry-picked |
| News | ✓ verified | ~ major launches only | ~ if newsworthy | - |
| Glassdoor | ~ anecdotal, undated | - | ✓ but neg-biased | - |
| Formal reviews | - | ~ | - | ~ covers the game, not the community; goes stale |
| Steam reviews | - | ~ | - | ✓ some neg. bias |
| Reddit | ~ early rumors | ~ reactive, not authoritative | ~ unverified leaks | ✓ polarized, leans neg |

✓ = real signal (bias noted) · ~ = partial, unverified, or stale · - = not covered · ✗ = no real signal, just spin

### Diversify the sources (aspect-based summarization)
One was inspired by aspect-based summarization, Columbia Newsblaster, and Google News - how do we deliberately seek out company or product information in specific categories, and then stitch it all together. So I thought of the various aspects of a company I research and what's discoverable online, then worked on sub-summaries of each.

One aspect was the user experience of the company's products. This is what I did at Swype, where I tried to find the real stories, the real experiences with the product, to understand what the company had been prioritizing, what the company's good at, what it's bad at, what the current weaknesses are from the user base. I could extrapolate from that to figure out a bit about company priorities.

Another aspect was the employee experience, which points to employee reviews on Glassdoor. There were some other smaller sources too, like Reddit or Blind. Indeed had added something similar to Glassdoor reviews before they acquired Glassdoor, but even so, Glassdoor had something like ten times as many employee reviews. So that's the company-insider perspective - what's it like for them.

Another aspect was the financial history. For startups, this would include things like fundraising, customer growth, partnerships, headcount growth, that sort of thing. 

And then, of course, there's some general information too, like news coverage or the company webpage.

So that was one major effort - deliberately seeking out information on different aspects of a company to provide contrasting views.


### Debias by source category
Another piece of this was debiasing by category. I'd take my own knowledge and experience and put it into the prompt, to instruct the model on when to trust sources in a particular category.

A company website is trustworthy for certain information but not all. The stuff that hypes up the company and drives sales or marketing isn't going to be as trustworthy as things that are more simply, factually verifiable - who's on the leadership team, who their customers are, what their products are, what their jobs are, or whether they've passed a SOC 2 audit.

Employee reviews have different biases, and tend toward polarized reviews, and especially toward negative reviews. I'd seen this firsthand managing at 98point6: people who are extremely frustrated or extremely angry are more likely to post a review, people who are moderately happy usually don't, and people who are extremely happy only sometimes feel motivated enough. So there's a sampling bias in who has enough motivation to go through the hurdle of writing a review, and that skews your view of a company. You also have to keep in mind that some people take their individual experience and aggrandize it as a trend.

Crunchbase is trustworthy for fundraising, but I found their headcount numbers tended to be outdated and old, so that wasn't as trustworthy and it's helpful to tune the summarization prompts to consider that.

So with each different source, I'd consider: based on my own observations, when can we actually trust this information? And then I'd bake that into the prompt, so that when the model was extracting text or summarizing abstractively, it would focus on the areas where each source was more trustworthy. This interacted with diversification too: If I composed the general review from the company webpage plus news, the prompt guidance could point the LLM to pick certain info from each.

### Make the context digestible
Even with 2026 LLMs, when you mix a little relevant context with a lot of distracting context, the quality degrades.

The most concrete challenge happened with mobile app reviews. Due to differences in scraping Apple and Google reviews, I might get 90,000 Apple reviews and 10,000 Google reviews. If I just injected all of that into a single prompt, even if it could handle that many tokens, the summary would be biased toward the Apple reviews. It may be that those two platforms are equally important, but we're going to lose that. The fix there was pretty simple: downsample the Apple reviews so that both have ten thousand.

Another example of this was in searching for company news. Excluding unreliable sources helped because it's one less thing the LLM needs to reason about. Another thing that helped was using a distribution of publication dates in the search operator so that we deliberately diversified across time - trying to get some stuff published in the last year, some stuff from a couple years ago, so we're getting the story over time. So then it'd be possible to tell the story of the company - how it grew, how it fell, or whatever.

There are many ways to make better use of the context window, but I want to emphasize that some of these are efforts to make diversity of sources work as a strategy. Injecting different views can help but you need to balance the sources in the context to make the most use of it.

### Why not RAG?

Initially I'd considered retrieval-augmented generation (RAG) but decided to go a different direction, or rather, I felt that web search was already enough RAG for me.

Say we're trying to look over all the Glassdoor reviews for a company. We're considering: could we throw everything into a single LLM call? Or would we rather do RAG, and then load up the context window with the results? Or maybe something in between: multiple RAG searches, then load up the context window with those.

The challenge with RAG is that you have to know what you're searching for. And that's just not how I approach Glassdoor reviews as a human, as a potential candidate. I want to read a good sample of the positive reviews and a good sample of the negative reviews, and see if there are themes to dig into. And then I might go searching once I know what to look for.

For example, I might not search for signs of sexism at every single company. And even if I did, the telling review might never use the word. Say a review mentions that the female doctors tend to get called by their first names while the male doctors get their titles. It doesn't say "sexism", but if I see a review like that I'm going to take a little extra time to search for the full story.

If I think about that as RAG versus a summarization approach: with RAG, I'd have to know to search for that in the first place. I could anticipate a list of perhaps five or ten things to check at all companies, but I'm not convinced I could really anticipate everything or that RAG would always find those things. In contrast, a summarization approach is less susceptible to biased sampling of the data. The main obstacle was to avoid imparting bias from how much of the context came from each source.

Maybe there's a way to accomplish the same goal with RAG. I didn't see any promising options so I built the best I could with a summarization approach.

## How would I know it worked?

Initially I considered writing a gold standard reference document using all of my insider knowledge of former employers, and using that in evaluations. I tried that for 98point6 but realized that I could only do it for two companies, which wouldn't be enough for a formal eval. And it was time consuming, not something I could ask friends to write for their employers. So for the companies I knew well, I evaluated against a list of key topics I knew and relied on manual review for others.

Then once the reports were reasonable, I asked friends for feedback, whether former employers or to help in job searches. Sometimes that was as informal as texting and other times we had a call to discuss. That helped with a lot more high-level quality assessment, not just basic things like hallucination but more fundamental topics like resolving ambiguous company names.

## The coverage ceiling

One thing I found was this coverage ceiling: what's discoverable on the open web, and what's not. Company Detective usually had great context for mid-size startups, essentially the ones I'd dogfooded, like 98point6, Singularity 6, and companies of that size.

So, to quickly walk through [98point6](https://ktrnka.github.io/company-detective/companies/98point6.html), the approach found a lot of great context on the company, even if the summarization struggled with a complex timeline. It covered things like fundraising, the early days when we were both building the technology and operating the clinic, partnerships, awards, the sale of the physician group to Transcarent, then later the sale of the technology to Transcarent too, and layoffs. It also surfaced what employees liked or disliked. The product's story is in the context too: patients liked the affordability, ease of use, and a lot of great doctors, but also that they had a worsening experience over the years. Much of the candid story of 98point6 is there in the context, even if the organization and summarization of that context could be improved.

It didn't work well for large companies. If you look at a company like Microsoft (it's huge), even when you talk to people in person, you hear that it's a very different company depending on what part of it you're working in. But Glassdoor isn't segmented by subdivision of Microsoft. So there's a real challenge in trying to identify the relevant data. Maybe it's possible somehow, but it was a pretty big level of challenge that I didn't tackle at the time.

The other side of the challenge was small companies. A friend of mine was interviewing at a local Seattle startup called Synthesize Bio so I ran them through Company Detective. But at the time, they had zero information on their web page. The only information I could even find myself online was on LinkedIn which is very locked down. If I could access LinkedIn programmatically, maybe I could've shifted to a deep dive on the founders which would've been helpful.

And there are other coverage limitations too. A lot of information just isn't online. Or you may discover a Blind post that tells the inside story but it looks awfully similar to a Blind post that's complete fiction. It's also possible to read between the lines a bit - supposing a startup's last round of funding was 14 months ago and they have no jobs posted on their careers page - that's probably a bad sign even though it's the absence of typical signs. But that's a lot of speculation to ask an LLM to do reliably.

## Why it wound down

In the fall of 2024, I had it working pretty well. People could submit companies to add, and I'd rebuild it weekly, so it would pull in new news and other changes to the code that tried to improve the credibility of the reports we generated.

I was trying to grow the user base, and what I said to myself was: my first level of traction, my first bar to cross, is whether, if I show this to friends, they're actually saying, "can you run this for me, for this situation?" Am I getting actual evidence that there's a need there, that they're pulling on it? There were cases of that, but I'd set a pretty clear number, and I did not hit it. That was really part of what made me think: okay, maybe this isn't quite working out.

When I did user interviews, I got people to talk a lot about their challenges and workflow. From those interviews I came to feel that it needs to be this big, real-time system. For someone who's job-seeking (Sunday night, when they happen to have an hour away from the kids), it needs to be a system where they type a few things, click a few things, and get a deep report that gives them the full story on a company they're about to interview with. It needs to meet people where they are. Doing something asynchronous was great for rapid iteration and earlier feedback, but it wasn't really enough to help job seekers in the moment.

I was also running into engineering challenges: The data sources were becoming more locked down, so I had to put more time into that.

And then the real story is that Layr came along. My cofounder had approached me that Fall. He'd been working on related challenges in context engineering, dealing with the problem that the quality of the output is really sensitive to the coverage of the context, whereas the LLMs themselves are fairly commoditized: you can just swap them out as better/cheaper ones come out. So the innovation is happening in the context. It turned out we'd both been circling this same problem from different angles, so it was a natural transition.

## My view from 2026

Now in 2026 I don't maintain Company Detective anymore. That's really just because the data integrations require ongoing maintenance to keep up with upstream changes. These days I tend to start company research either with a search-based LLM or deep research tool. I find that modern deep research tools are useful enough to get my bearings, even if they often lack a detailed history of the company, never integrate Glassdoor, and only some providers hook into Reddit.

I don't regret it, though, because the approach of trying to push as far as I could on the user experience pushed me down this interesting angle of credibility - trying to understand the limits of what software can do for information credibility. And that's still a worthy question to answer today. I still feel strongly that it's possible to go much further than I did, and help people find and focus on the most trustworthy information - especially if you think back to what made the original Google search so magical.

Another thing still on my mind is that a product-first mindset is underapplied in large language models. There's a lot of opportunity for people to innovate if they're driven by trying to build a delightful, wonderful user experience - not delightful in the sense of words appearing in nice fonts, but in the product design, meeting people's actual needs. 

So instead of keeping the code alive, I'd rather pass on what I learned. This article is my first attempt at that: the earned lessons, plus a map of references below, for whoever wants to carry them further. If this kind of craft is your jam, I'd love to hear from you, whether to trade ideas or just connect! Feel free to reach out on [Linkedin](https://www.linkedin.com/in/keith-trnka/).

<!--reading-time-stop-->

## References & Inspirations

> **On the ✅:** it marks work **peer-reviewed at an established venue** - the venue is named in each citation (e.g. ACL). Entries without it are preprints, essays, books, or standards documents - often excellent and worth your time, just held to a different bar.

### Bucket 1 - What shaped the build
*Papers and essays I read during or for the project. I tried to find as many of the influences from old notes and bookmarks as I could but I'm sure I missed a few.*

**Summarization method (extract-then-abstract, aspect-based → the multi-lens design):**
- **Suhara et al., 2020.** [OpinionDigest: A Simple Framework for Opinion Summarization](https://aclanthology.org/2020.acl-main.513/). *ACL.* ✅ - Aspect-based abstractive summarization over many reviews (e.g. Yelp): extract opinion phrases, cluster, synthesize. This was an inspiration for how I did review summarization, though it works at a finer aspect granularity.
- **Tan et al., 2020.** [Summarizing Text on Any Aspects](https://aclanthology.org/2020.emnlp-main.510/). *EMNLP.* ✅ - Aspect-conditioned summarization that deliberately covers a *diverse* set of aspects so the summary is comprehensive. The closest inspiration for my product / employee / financial aspects.
- **Stiennon et al., 2020.** [Learning to Summarize from Human Feedback](https://proceedings.neurips.cc/paper/2020/hash/1f89885d556929e98d3ef9b86448f951-Abstract.html). *NeurIPS.* ✅ - The RLHF-for-summarization landmark. It planted one unused idea: use reader-preference data to spend more compute refining summaries for the most-viewed companies, and early ideas in how to use feedback at scale.
- **Wang et al., 2023.** [Element-aware Summarization with LLMs (Chain-of-Thought)](https://aclanthology.org/2023.acl-long.482/). *ACL.* ✅ - A slot-filling flavor of summarization: fill an event's prototypical elements, then summarize around them for a dense, specific result; chain-of-thought helps. I considered this for doing the Company Detective pipeline as one long CoT chain, but it would've needed far too many context tokens.
- **Adams et al., 2023.** [From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting](https://arxiv.org/abs/2309.04269). *New Frontiers in Summarization Workshop (arXiv:2309.04269).* - Iteratively densifies a summary with an LLM. Interesting technique; I didn't use it because the outputs were already dense, and the step count parameter felt like it would make things much harder to debug.
- **Khosravani, 2023.** [Recent Trends in Unsupervised Summarization](https://arxiv.org/abs/2305.11231). *arXiv:2305.11231.* - A great survey of the space; the kind of read that pushes you toward an extract-then-abstract *hybrid* rather than purely extractive or purely abstractive.
- **Zeng et al., 2023.** [Meta-review Generation with Checklist-guided Iterative Introspection](https://arxiv.org/abs/2305.14647). *IJCAI 2024 AI4Research Workshop (arXiv:2305.14647).* - Checklist-guided iterative self-critique to synthesize a meta-review from many paper reviews. Loosely adjacent to component-level quality checks (and a reminder that meta-reviews come with training data, which CD didn't have).

**Context efficiency:**
- **Li, 2023.** [Unlocking Context Constraints of LLMs: Enhancing Context Efficiency of LLMs with Self-Information-Based Content Filtering](https://arxiv.org/abs/2304.12102). *arXiv:2304.12102.* - Drops low-self-information (predictable / redundant) spans so a fixed context window carries more signal per token. This is the clearest academic version of CD's "make the context digestible" move, though CD filtered coarsely (downsample the over-represented source, exclude unreliable ones, diversify by publication date) rather than at the token level.
- **Liu et al., 2024.** [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/). *TACL (arXiv:2307.03172).* ✅ - Models under-use information in the middle of long contexts (U-shaped position bias); §5 argues "more context" isn't always better. **Caveat: a 2023 finding - may be weaker in 2026 models.**

**Evaluation:**
- **Liu et al., 2023.** [G-Eval: NLG Evaluation using GPT-4](https://aclanthology.org/2023.emnlp-main.153/). *EMNLP (arXiv:2303.16634).* ✅ - LLM-as-judge with chain-of-thought + form-filling; a step past BLEU/ROUGE for summarization. Good orientation if you're weighing whether to trust an automated judge.
- **Zhang et al., 2024.** [Benchmarking LLMs for News Summarization](https://aclanthology.org/2024.tacl-1.3/). *TACL (arXiv:2301.13848).* ✅ - Two takeaways: LLMs are strong at this, and the *reference* summaries in standard benchmarks are low quality, so reference-based eval can be risky if you don't verify them.
- **Husain, 2024.** [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/). *Blog (hamel.dev).* - The practitioner case for evals; nudged CD toward low-level component tests + LangSmith tracing.
- **Yan et al., 2024.** [What We Learned from a Year of Building with LLMs](https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/). *Essay (O'Reilly), in three parts.* - Practitioner lessons: get the most from fundamentals, prefer small single-purpose prompts, break work into debuggable stages, craft your context, don't assume long-context fixes everything, LLM-as-judge isn't a silver bullet. This was a major influence that helped me refine my approach.

**Other technique (mostly background / adjacent):**
- **Zhou et al., 2023.** [Least-to-Most Prompting](https://arxiv.org/abs/2205.10625). *ICLR.* ✅ - Decompose a hard problem into ordered sub-problems and solve in sequence. Tangential to CD's core, but part of the "break it into stages" instinct.
- **Hu et al., 2024.** [SLM Meets LLM: … Hallucination Detection](https://arxiv.org/abs/2408.12748). *arXiv:2408.12748.* - Small-model + big-model hallucination detection (detect-then-revise). I preferred detect-then-*revise-the-prompt*; considered this, didn't implement it.
- **Cohen-Wang et al., 2024.** [ContextCite: Attributing Model Generation to Context](https://proceedings.neurips.cc/paper_files/paper/2024/hash/adbea136219b64db96a9941e4249a857-Abstract-Conference.html). *NeurIPS.* ✅ - Attributes each part of an output to specific context via delete-and-rerun sensitivity (LIME/SHAP-like). Compelling for verifying attribution, but too many runs to afford on an API.
- **Zhong et al., 2025.** [Mix-of-Granularity: Optimizing Chunking Granularity for RAG](https://aclanthology.org/2025.coling-main.384/). *COLING 2025 (arXiv:2406.00456).* ✅ - Optimizing chunk granularity for retrieval. Adjacent to CD's multi-granularity summary problem (high level details founding date vs. low level details like free-parking), though it didn't answer it.


### Bucket 2 - The credibility lineage (assembled mostly in hindsight)

This category of references were mostly assembled in hindsight while writing the post. The credibility theme itself came into focus more as I *wrote* this than while I built it. Only in hindsight did I see that much of what I was reaching for is the same problem Google originally set out to solve and that it has a long history under many names. So I did a second, partial lit review and collected it here: credibility is a genuinely under-built and impactful area, and this is a head start for anyone who wants to get into credibility.

**Web-credibility, exogenous (link/graph-based):**
- **Page et al., 1999.** [The PageRank Citation Ranking: Bringing Order to the Web](http://ilpubs.stanford.edu:8090/422/). *Stanford InfoLab.* - *Known beforehand.* Links as credibility votes - the original web-credibility mechanism. *CD relation: I reached for its decayed descendant, backlinks-as-credibility, as a heuristic, while also relying on Google's internal credibility in searching.*
- **Kleinberg, 1999.** [Authoritative Sources in a Hyperlinked Environment (HITS)](https://dl.acm.org/doi/10.1145/324133.324140). *JACM.* ✅ - Companion hubs-and-authorities link model.
- **Gyöngyi et al., 2004.** [Combating Web Spam with TrustRank](https://www.vldb.org/conf/2004/RS15P3.PDF). *VLDB.* ✅ - Propagates trust from a hand-picked good-seed set, because PageRank rewards skilled spammers. *CD relation: my backlink filter is similar to TrustRank's intuition.*
- **Wu et al., 2006.** [Topical TrustRank](https://dl.acm.org/doi/10.1145/1135777.1135792). *WWW.* ✅ - the link-world version of "reliability depends on what you're asking."

**Web-credibility, endogenous (fact/content-based):**
- **Dong et al., 2015.** [Knowledge-Based Trust: Estimating the Trustworthiness of Web Sources](http://www.vldb.org/pvldb/vol8/p938-dong.pdf). *VLDB.* ✅ - Introduces **exogenous** (link structure) vs. **endogenous** (correctness of stated facts) signals, and jointly estimates page trustworthiness and per-fact truth at web scale.

**Truth discovery / corroboration (closest to "de-correlated sources / evidence over claims"):**
- **Yin et al., 2007.** [Truth Discovery with Multiple Conflicting Information Providers (TruthFinder)](https://dl.acm.org/doi/10.1145/1281192.1281309). *IEEE TKDE.* ✅ - A source is trustworthy if it states many true facts; a fact is true if stated by trustworthy sources - iterated jointly.
- **Lin et al., 2018.** [Domain-Aware Multi-Truth Discovery](http://www.vldb.org/pvldb/vol11/p635-lin.pdf). *VLDB.* ✅ - Source reliability varies by domain; infer per-domain expertise.
- **Ma et al., 2015.** [FaitCrowd: Fine-Grained Truth Discovery](https://dl.acm.org/doi/10.1145/2783258.2783314). *KDD.* ✅ - Models a source as multiple sources by topic, because reliability varies by topic. **The closest work to "trust which source for which claim."**
- **Wojcik et al., 2022.** [Birdwatch: Crowd Wisdom and Bridging Algorithms (Community Notes)](https://arxiv.org/abs/2210.15723). *arXiv:2210.15723 (Twitter).* - *Known beforehand.* Bridging-based ranking via matrix factorization: trust a note rated helpful **across normally-disagreeing groups** (it assumes the main axis of disagreement is political), de-biasing via the community itself rather than an external source of truth.

**Modern credibility-aware RAG:**
- **Pan et al., 2024.** [Not All Contexts Are Equal: Teaching LLMs Credibility-aware Generation](https://aclanthology.org/2024.emnlp-main.1109/). *EMNLP 2024 (arXiv:2404.06809).* ✅ - Classifies retrieved sources by credibility and exposes that signal to generation. The closest single paper to CD's problem. *CD relation: CD treats credibility as per-source-*type* (a company site is trustworthy for some claims, not others), not one score per source.*
- **Deng et al., 2025.** [CrAM: Credibility-Aware Attention Modification](https://ojs.aaai.org/index.php/AAAI/article/view/34547). *AAAI 2025 (arXiv:2406.11497).* ✅ - Down-weights low-credibility documents at the attention level. Elegant, but needs access to attention weights - not possible through a hosted API like OpenAI's.
- **F. Wang et al., 2025.** [Astute RAG](https://aclanthology.org/2025.acl-long.1476/). *ACL 2025 (arXiv:2410.07176).* ✅ - Reconciles retrieved vs. the model's *internal* knowledge by reliability and cross-source confirmation ("source awareness").
- **H. Wang et al., 2025.** [RAG with Conflicting Evidence (MADAM-RAG / RAMDocs)](https://arxiv.org/abs/2504.13079). *COLM 2025 (arXiv:2504.13079).* ✅ - A dataset plus multi-agent debate that separates ambiguity / misinformation / noise. Good vocabulary for telling an entity-resolution problem (ambiguity) apart from a reliability problem (misinformation).
- **Ge et al., 2025.** [Resolving Conflicting Evidence in Automated Fact-Checking (CONFACT)](https://arxiv.org/abs/2505.17762). *arXiv:2505.17762.* - Injects **media-source credibility** (via a database like Media Bias/Fact Check) at retrieval and generation. Works well for news factuality; real-world cousins include Ground News.

**Summarization structure (for the multi-lens design):**
- **McKeown et al., 2002.** [Columbia Newsblaster](https://doi.org/10.3115/1289189.1289212). *HLT.* ✅ - *Known beforehand.* Multi-document news summarization: crawl → cluster by event → summarize per cluster. The structural cousin of CD's multi-lens design, and it's a project I've found inspiring since grad school.

**Non-ML - the human-side lineage for "trust which source for which claim":**
*I didn't read these for the build, and I haven't worked through them closely - they're the terms and sources I'd start searching if I picked this thread up. Information science and journalism named "which source to trust, and for what" long before the ML papers did.*
- **"Primary vs. self-interested source."** Information literacy / journalism; Wikipedia's [WP:ABOUTSELF](https://en.wikipedia.org/wiki/Wikipedia:Verifiability#Self-published_or_questionable_sources_as_sources_on_themselves) is the concrete version. The pre-ML name for debias-by-category.
- **Wilson, 1983. Second-Hand Knowledge: An Inquiry into Cognitive Authority.** *(Book; free on the [Internet Archive](https://archive.org/details/secondhandknowle00wils).)* "Cognitive authority" as domain-specific rather than global.
- **ACRL, 2015. [Framework for Information Literacy](https://www.ala.org/acrl/standards/ilframework)** - the "Authority Is Constructed and Contextual" frame.
- **Lateral reading ([Wineburg & McGrew, 2019](https://stacks.stanford.edu/file/druid:yk133ht8603/Wineburg%20McGrew_Lateral%20Reading%20and%20the%20Nature%20of%20Expertise.pdf)) · SIFT ([Caulfield, 2019](https://hapgood.us/2019/06/19/sift-the-four-moves/)).** Judge a source by what the rest of the web says about it, not by reading it alone.

**Tools & products in the space (for orientation - not papers):**
- **[Perplexity](https://www.perplexity.ai/)** - the mainstream AI "deep research" answer engine (LLM + web search + citations); the natural comparison point for CD's reports.
- **[open_deep_research](https://github.com/langchain-ai/open_deep_research)** (LangChain) - an open-source deep-research / report-generation agent; a hackable example of the pattern.
- **[GigaBrain](https://join.thegigabrain.com/)**, **[Reddit Scout](https://www.redditscout.com/)** - aggregate Reddit/forum opinions to answer "is X any good?" - single-source cousins of CD's de-correlated blend.

**On the funding-model theme:**
- **Zebras Unite, 2017.** [Zebras Fix What Unicorns Break](https://medium.com/zebras-unite/zebrasfix-c467e55f9d96). *Medium.* - The essay behind "zebras vs. unicorns": profitable, sustainable, purpose-driven companies the VC unicorn model overlooks. Ties to §1 and the coda's small-viable-business critique.


## Acknowledgments

I want to thank many people that gave it a shot and provided useful feedback along the way: Tiffany, Chris, Adam, David, Jeff, Christy, Mike, Andy, and I hope I'm not forgetting too many people! 
