---
layout: post
title: "The Gap Between Medical AI Research and Clinical Practice"
date: 2026-11-01
series: ai-vs-doctors
description: "Measuring AI in a real clinic vs the AI-vs-doctors studies: what to measure, and why assistance comes before automation. For ML and healthcare builders."
ai_disclosure: "This is mostly handwritten, with AI support in planning, searching, and reviewing. -Keith"
---

This series started with [my criticism of diagnostic accuracy as a proxy for medical quality]({% post_url 2026-09-24-ai-vs-doctors-part-1 %}), focusing on the way researchers use it to compare AI against doctors. Then I directed AI to survey medical research in [Part 2]({% post_url 2026-10-10-ai-vs-doctors-part-2 %}), both the history of ML and modern AI in healthcare, finding that promising research results often fail to produce meaningful outcomes.

This piece is about the contrast between my experience in applied work and the research, diving much deeper into experiences from 98point6 and also looking more closely at the research.

## Task design

Part 2 notes that the most common study design involves radiologists reading images with no history and no prior scans, and "systematically underestimates human diagnostic capability and artificially inflates the relative value of narrow AI." Doctors are skilled at real clinical workflows, not artificial tests. Adapting to a new task takes time, and studies often drop them into a new task without the time or incentive to adapt. The triage story mentioned in Part 1 initially started this way. We were fortunate to find a different task that, while still artificial, was good enough to be useful in our product.

Since Part 2 commented on the triage project, I'll add one brief detail: The similarity to preference judgments in search engines isn't a coincidence; I was directly inspired by that work.[^prefjudge]

[^prefjudge]: The real coincidence is *how* I learned about it: [Ben Carterette](https://scholar.google.com/citations?user=zgHZ-KMAAAAJ) gave a talk at the University of Delaware when he was interviewing for a faculty position around 2010. His thesis work showed that preference judgments were a faster and better way to annotate relevance, despite the challenges they introduce. It's one of the inspirations I've used for years in how you can solve certain ML problems by reframing a task.

Part 2 described adjudication as a better way to build reference data, in which disagreements are debated until consensus is reached. We tried this for triage labeling, and the main benefit was that it helped us spot our labeling task as the problem. Adjudication alone doesn't save you from a poor choice of labeling task.

Once the triage model was live, we compared the cases it flagged and the ones doctors referred to the emergency room or urgent care. That looked good, but the two decisions aren't the same. Triage would happen after the patient's first couple of sentences; the referral decision happens after the doctor has talked to the patient and knows more. And some ER referrals were actually about the capabilities of the ER: The patient wasn't in danger, but they needed equipment that only the emergency department has.

## Product evaluation in practice

Randomized controlled trials (RCTs) are the gold standard in medicine, though the quality varies from study to study.[^rct-quality] AI in medicine is often criticized for its lack of RCTs, and I get it. I also can't really criticize companies for that, because we didn't run RCTs at 98point6. We got close at times, and took extra effort in the data analysis.

[^rct-quality]: As a concrete example, the zolpidem (Ambien) clinical trials were designed assuming that the effect on men and women was the same and didn't check for different dose-effects. 20 years after the approval, the FDA halved the recommended dose for women after finding that women metabolize it more slowly. Effectively, the trial's design led to overdosing in women, and as far as I can tell, clinical trials still sometimes struggle to test for different outcomes on different people. The underlying questions to ask about any study: Is the result trustworthy for the people studied? And does it apply to your patients? Researchers call these internal and external validity, and medical research has them described well, with structured assessment tools for each study design: for example, Cochrane's RoB 2 for randomized trials, and QUADAS-2 for diagnostic accuracy studies, which scores applicability separately from bias.

The common approach in tech is an A/B test: the same idea as an RCT. Ideally we'd randomize across sessions or users and compare the effect. That wasn't appropriate in most of our work though. We focused on projects that saved time for physicians, and it's not ok to flip it on and off randomly throughout the day. Randomizing by physician would be less disruptive while also helping to control for learning effects. However, in the early years the clinic had fewer than 10 doctors. We also had some features that needed to run *before* a doctor was assigned to the case, so we *couldn't* randomize by doctor for those.

I'll describe evaluation in one early project (2017) and one late project (2022), then I'll come back to the topics of what to measure and what to control for.

When mentioning 98point6 projects, I want to be clear that these projects were team efforts across many people and often many teams. In some cases, my thinking may be influenced by echoes of long-forgotten project plans. I don't intend to take credit for the ingenuity and hard work of others, only share the lessons we learned so that future healthtech work does better.

### Automated intake: Question Bot

Question Bot was the automated intake interview, and we never A/B tested it. We launched it in 2017 when the clinic had only a couple of visits per day, and improved the model and user interface over the years. The automated questions were determined after the patient entered a couple sentences describing the reason for their visit (aka chief complaint). At that point in time, the doctor wasn't yet assigned; usually they'd pick up a case at the end of the automated questions. 

The lack of scale was a major obstacle in our effort to be data-informed. At the start of 2018, our daily visits were still in the single digits. At the start of 2019, we had tens of visits per day. Then at the start of 2020 we had a little over a hundred per day, which scaled rapidly in the March 2020 COVID surge. The evaluation effort in the early period (2017-2018) was frankly a desperate effort to find any sort of statistical power we could. We tried a wide range of things:
- Measuring time per visit before/after launch: Not enough statistical power to overcome the confounding factors on efficiency, and properly controlling confounders in randomization was impractical.
- Correlating efficiency with the number of questions asked: It was invalid because the ML models would ask more questions in easier cases (common cold, UTI, etc).
- Developing "active time" metrics: This helped to reduce variance and focus on the parts we cared about, but still wasn't enough statistical power.
- Annotation of visits: We had doctors annotate visits (including bot turns) to get a rough estimate of savings when compared to pre-bot visits. It was a mixture of peer-review and self-review depending on availability. There were some clear outcomes: We had many common cases in which doctors had no additional questions of patients, or only one. So there were signs that it was helping, even if we didn't have the evidence of a formal study. When a slide deck required a number, we said 20-40% of clinician time was saved based on a conservative estimation from this annotation.

The annotation process also helped us learn more about clinical workflows, for instance highlighting questions about medication history that weren't directly related to the patient's chief complaint.

By the time we had *maybe* enough patients to run a proper statistical test, the clinic had come to depend on the bot so we couldn't turn it off just to run a proper A/B test.

One surprise over the years was that the workload itself changed: As Question Bot did a more complete interview, doctors extended the medical care. With a little extra time, they'd ask about flu shots, take time to elicit and update the patient's history, or otherwise check on the patient's overall health. So it seemed like we hit an efficiency wall, but our clinic was also providing much more thorough medical care. That's a wonderful thing even if it wasn't easy for us to quantify, and I call it out to highlight a risk of being overly fixated on what's easy to measure.

One day, perhaps around 2019, Question Bot stopped asking questions. The doctors on shift demanded that any change be reverted, feeling that they wouldn't be able to catch up with incoming patients. Slack messages flew in all directions while we figured out what the issue was.[^outage] That reduced some of my doubts about whether the clinic wanted Question Bot, though I'll also concede that a busy clinic really has no time to deal with any unannounced changes.

[^outage]: For the engineers in the audience: An announced change had been made earlier that day but that wasn't the actual cause. A service-to-service auth token was rotated in one service but not another, so all services were running but two of them couldn't talk to each other anymore. For the deeper engineering lesson: The token rotation was done intentionally for a minor security concern, but nobody had tested secret rotation before.

If I could go back and redesign the metrics with what I know now, I would've tried a dose-effect test once we had enough scale, perhaps in late 2018. That might look like 50% of visits dropping a random 25% of the bot-added questions: perhaps large enough to measure impact without being too disruptive. We would've had to do that before adding features building upon Question Bot, like when we enabled doctors to edit the question queue if they had time.

### Chat suggestions

Chat suggestions, quick replies for the doctor's side of the conversation, launched in 2022 and came the closest to a proper test. We started with an opt-in beta group of physicians, initially only had the feature enabled while we were monitoring, and improved both the model and the user interface over the course of a month or so. That improvement loop along with a willingness to turn it off is what enabled us to safely and quickly build a good system. Once we'd made enough improvements, we brought in another wave of physicians to do a more controlled evaluation. I can't remember exactly how we randomized except that we controlled for common confounders in the randomization.

On the analysis side, we used a generalized linear model (GLM) or a similar regression to analyze the effect of the feature on time per visit while controlling for common confounders as much as we could.

As with Question Bot, we had metrics to show it was helpful to the clinic but the data didn't tell the full story. This must've happened during the evaluation test: one of the doctors said more or less, this is great, please can you release this to the clinic ASAP because we're swamped over here? This was coming from someone that I'd considered a late adopter of technology. It's more common for clinicians to push back against software changes; they rarely have the time to learn something new for only a chance of a marginal benefit. So the ask to launch sooner was a sign that it was perceived as worthwhile, either because it wasn't a disruptive change, the benefit was worth it, or both. The subjective and the objective evidence pointing in the same direction quieted my private worries about the full launch.

The biggest underlying differences from the Question Bot launch were that our clinic was much larger, and our team was larger as well.

### High level metrics

When I started in 2016, I had a limited understanding of healthcare frameworks. Our efforts in machine learning were focused on assisting doctors, and we focused on measures of clinician efficiency. We used several internal metrics of efficiency, each with different strengths and weaknesses, and I'll mention two: 

- Active clinician time was good at filtering out idle time, but it was also a major effort to decide and track which seconds count as "active". 
- Visits per physician-hour captured multitasking well, but was sensitive to supply/demand balance and plummeted overnight when most patients were sleeping. 

We also measured patient satisfaction in post-visit surveys, though it was much harder to attribute any changes in aggregate satisfaction to specific product changes.

I like the quad aim as a framework for progress in healthcare, though I didn't learn about it until later in my time at 98point6. And the practical side of progress differs a bit from the theory, even for successful efficiency projects: In the short term after launching a feature to save time, it buys the clinicians some relief and I saw them repurpose that time in a range of ways, from more care to more collaboration. I got the impression that it unlocked more individual agency, which was a part of why it was appreciated. But then over time as we onboarded more patients and the clinic scaled with demand, the new schedules were built around updated efficiency numbers so the contribution of efficiency work shifted from clinician satisfaction to cost reduction for patients.[^eff2cost]

[^eff2cost]: Even that statement is oversimplified: Faster visits led to tighter schedules which certainly improved the unit economics of running our clinic. However, patients didn't notice because we were providing our service at cost. In the early years, visits were heavily subsidized and it wasn't until my last year that we started to hit break-even. So those efficiency gains in practice were more about the financial sustainability of the company at already-low prices to patients. If the business model had been different, improvements to clinical efficiency could have led to cost reduction for patients, though that assumes that the initial price is much higher.

### Common confounders

Confounders were a major challenge for us. I'll list out the big ones.

For clinician efficiency:
- The specific clinician had a huge effect.
- The type of case had a big effect, like common colds were quick and mental health cases were often very involved
- Clinicians tended to speed up if the clinic was very busy or slow down if it wasn't. Or in other words, the amount of medical care was changing in response to clinic load, as well as niceties like bedside manner.
- Text-based primary care[^primary-care] improves access, but starting a visit from home or work also means that a visit may get interrupted, which can affect efficiency metrics.

[^primary-care]: I should clarify that 98point6 mainly did urgent care rather than primary care. As I understand it, urgent care is mainly one-off cases, while primary care is more focused on a long-term provider-patient relationship. I'm still learning to correct some of my old habits and caught this late in the editing process.

For patient experience:
- Often the biggest effect was whether they got a prescription, even in cases where it was not needed.
- If the clinic was busy, waiting times would increase and clinicians would reduce some of the niceties. But also patients were very understanding when they understood the reason, such as during COVID surges.
- The specific clinician, again

In later years, we used simple approaches like GLM to help separate the confounder-driven effects from the intervention effects.

The biggest successes will tend to show improvement across multiple metrics. They'll also tend to yield strongly positive feedback. Although that usually isn't called "data", it's meaningful evidence and corroboration that shouldn't be discounted.

### Reaching for outcomes

I started writing this article intending to audit our projects by the rung of [Fryback and Thornbury's ladder](https://doi.org/10.1177/0272989X9101100203), but came to see that many projects don't cleanly map to a diagnosis-centered ladder. We could look at the Question Bot story and claim that any efficiency improvement was leading to increased medical care, then claim it's rung 4 (changing treatment). But that feels like an overreach. On the other hand, if we view efficiency as business-internal cost reduction, it doesn't really map to the ladder at all. 

Instead, as I think about our range of projects, we hoped to make progress at rungs 4-6 even if the pathway to get there wasn't through diagnosis. For example, with triage we could see a reduction in waiting times for urgent needs, and perhaps at scale we could measure in terms of patient outcomes. So I'd say there are many pathways to progress in patient management, outcomes, and societal benefits, not only through diagnostic accuracy.

It's good to strive to measure outcomes that matter to patients, doctors, and society. In practice, you may not have the scale or data necessary to observe a change in the outcomes you value. But we can still do better than accuracy metrics alone:
- Although we couldn't measure outcomes with triage, we could measure a significant reduction in waiting times for ER referrals compared to other cases. We heard concordant feedback from our quality team, and did not observe harm to patient satisfaction or clinical efficiency.
- We couldn't measure improvements to care from diagnosis predictions, but we could do better than accuracy by measuring the effect on efficiency, we noted concordant feedback from clinicians, and investigated any potential of biasing diagnosis to reduce the risk of harm.
- We couldn't measure population-level antibiotics resistance at our scale, but we could measure indicators of unnecessary antibiotic prescription, showing better processes than external references in [McCune et al, 2021](https://doi.org/10.30953/tmt.v6.272). This relies on existing publications to connect our process metric to metrics around our actual goal of society-level health. And keep in mind, we also needed to monitor patient satisfaction to ensure that they feel good about it too.

Reaching for higher-level metrics reduces the risk of bad decisions, but doesn't completely mitigate those risks. There's the risk of choosing a high-level metric that correlates with the desired outcome but does not cause it, as in the [CAST trial](https://doi.org/10.1056/NEJM198908103210629). There's the risk of worsening one metric in the effort to improve another, which is especially common in efficiency projects.

It's important to build the habit of reaching for outcome metrics at small scale. That will ensure that you're developing software and operating a clinic more safely once you hit a scale where it's both more impactful and more clear. It's also good to get in the habit of seeking out research that establishes the known causes of each outcome so that you're choosing surrogate metrics that are more reliable.

Even at a much greater scale, I wonder what we could've measured for Question Bot. Perhaps a dose-effect response on the percentage of cases flagged for safety in peer review? That's still a surrogate metric, but it's higher up the ladder towards patient health when compared to speed or accuracy of the model itself.

I'd expect to see broad outcomes improvements from more wide-ranging interventions: More reliable medication history (whether AI or not), or coaching in areas like sleep, exercise, nutrition, and social connection.

In practice, over 2017-2022 we progressed from opening the clinic to optimizing efficiency and had just started using narrow metrics like PHQ-9.

## The stronger studies of "AI vs doctors"

It was great to see progress towards more realistic evaluation of AI/ML in medicine in Part 2. I read some of the stronger studies and I'll comment below.

First up is the AMIE work from Google, posted as a preprint in 2024 then published in Nature as [Tu et al in 2025](https://doi.org/10.1038/s41586-025-08866-7). It's quite similar to 98point6: They're asking AI to interview a patient as well as generate a differential diagnosis and management plan, and it's primary care. They compare AMIE to doctors on text-based primary care with patient actors, judged by blinded specialist reviewers and also judged by the patient actors themselves. They find that AMIE fared better than doctors across a range of metrics from diagnostic accuracy (judged by people reviewing the differential diagnosis) to patient satisfaction metrics. The approach to building AMIE was interesting to read as well: They created a patient agent to act from a given clinical vignette, and used that to refine their doctor agent.

They note that the doctors were unfamiliar with text-based medical care and received no formal training, and so they hedge their conclusions appropriately.

This is a great step towards a more realistic evaluation, but I wish they had gone beyond diagnosis into treatment; medicine doesn't stop when you've got a good differential diagnosis. [Liévin et al, 2026](https://www.nature.com/articles/s41586-026-10764-5) follows up to test AMIE for treatment.

I'll quote from Tu et al's conclusion:

> Translating from this limited scope of experimental simulated history-taking and diagnostic dialogue towards real-world tools for people and those who provide care for them requires a substantial amount of additional research and development to ensure the safety, reliability, fairness, efficacy and privacy of the technology.

I agree that steps towards real-world tools would be helpful. I also like that their conclusions emphasize humility and caution in interpreting the results, though I wish they'd highlighted the large gap between a decent differential diagnosis and interventions that actually improve health.

We built a decent diagnosis ML model at 98point6, and the actual value we saw was 1) helping doctors to remember ICD-10 codes 2) use as a trigger for rule-based systems 3) use as pre-training for other models. Perhaps if we'd made it much better, we could've stepped into clinical decision support (CDS), but that wasn't something our doctors often needed help with. And how would you even monitor the safety of a production CDS, unless you're monitoring outcomes that are downstream of diagnosis?

The next work is ([Brodeur et al, 2024](https://arxiv.org/abs/2412.10849)), which is a widely-cited preprint that was [published in *Science* in 2026](https://doi.org/10.1126/science.adz4433). The authors mostly come from the medical field.

> Overall, our findings show that LLMs now demonstrate superhuman performance in differential diagnosis, diagnostic clinical reasoning, and management reasoning, and are superior in multiple domains compared to prior model generations and even expert human physicians. ... We must now focus on human-computer interaction studies and prospective clinical trials to rigorously assess the potential of artificial intelligence systems to improve clinical practice and patient outcomes.

This is similar to the quote from Tu et al, but I prefer that they're calling out human-computer interaction and patient outcomes so clearly.

They survey a wide range of medical tasks, largely using NEJM clinicopathological conference (CPC) vignettes and some real ER cases. In diagnosis evaluations, they're asking a second group of clinicians to judge the responses against the reference, which is a good way to give partial credit on diagnosis. It's great to see that they're including tasks a bit beyond diagnosis: They include a triage task, a task involving test ordering, and one involving patient management.

I would've liked more detail on the prompts used in each task and how they were developed. Prompting often has a significant effect on the quality of the output. It also wasn't entirely clear to me what the standards were for the expert judges, but at least they measure expert judge agreement with Kappa scores.

My read is that LLMs with specific prompts are capable of high quality in specific situations, and *may* generalize to other medical tasks and clinics. They characterize this as a proof of concept, not a system that could be deployed, and I agree wholeheartedly that we should take steps towards measuring patient outcomes in prospective, real clinical settings. Though as an aside, I'll admit that I'm internally wincing at the thought of doing a full clinical trial for an automated physician, but there are less risky ways to evaluate core technologies.

For the programmers in the audience, I'd say this is the equivalent of LLMs demonstrating superhuman performance on Leetcode and other work-adjacent tasks. You know as well as I do that it's just a proxy for what we actually do, and it was a useful proxy when AI coding was pretty bad. But it's not a very useful proxy anymore. With that perspective in mind, their conclusion reads more as a critique of the benchmarks rather than the broad claim of LLM superiority you might see in headlines:

> Our study suggests that LLMs have eclipsed most benchmarks of clinical reasoning, motivating the urgent need for prospective trials.

The third paper is the Microsoft AI's DxO preprint by [Nori et al, 2025](https://arxiv.org/abs/2506.22405), which was recently published as [Nori et al, 2026](https://doi.org/10.1126/science.aeh7930) in Science. This work focuses on the AI side of things, and it builds on the prior works: Their agent requests patient information in a chat and simulates test ordering. Then when it has enough information, it concludes with a diagnosis. At first glance it sounded like an agent simulating the patient, but it's actually a gatekeeper agent that reveals clinical information in response to requests. Those requests for information can be a list of questions or test orders. The original source of information comes from NEJM CPC teaching cases and MIMIC ED cases, though most of the information in the session is synthetically generated by the gatekeeper agent to be consistent with the original case.

Their claims of much higher diagnostic accuracy than humans need to be unpacked a bit. They're comparing diagnostic accuracy by having both the AI agents and doctors do tests from the same cases in SDBench[^same-cases-caveat], and use LLM-as-judge with a physician-authored rubric and physician validation of the judge. They compute accuracy from the rubric by judging whether the assessment is likely to lead to the same patient management. I'd prefer that they use a different model provider to mitigate any question of self-preference bias though.[^self-preference]

[^same-cases-caveat]: The 2026 abstract cites numbers from different groups of cases. The matched case comparison supports the same conclusion but the gap is smaller, mostly on ED cases, and it can be found on Page 45 of the supplemental material in Table S13.

[^self-preference]: [Pombal, Rei & Martins 2026](https://arxiv.org/abs/2604.06996) shows that models still have meaningful self-preference biases, even with a rubric. That said, the papers do a good job of comparing LLM-as-judge against in-house physicians and the 2026 supplement compares GPT and Claude as judges of AI diagnosis under "judge sensitivity analysis". They tested on DxO and the AI baseline but I would've also liked to see the physician judgments included as well.

I have mixed feelings on this work. When I look over the messages from the gatekeeper agent, they look like something elicited by a nurse, not something that a patient would say directly. To use their example:

> Initial case information: A 29-year-old woman was admitted to the hospital because of sore throat and peritonsillar swelling and bleeding. Symptoms did not abate with antimicrobial therapy

Did the patient report the swelling and bleeding? Would the patient be able to reliably report that it's in the region of the tonsils? I can believe that they'd self-report using a throat spray at least. Also, most patients tend to include extraneous information when asked, because patients don't have a complete understanding of what medical experts need.

In contrast, at 98point6 a typical patient-reported chief complaint for this case might be "I have a really bad sore throat that's not going away. My spit is sometimes pinkish which is weird... I don't think I've been eating dragonfruit today". I'm even being a little generous by giving a hint of bleeding; we usually needed to elicit that afterwards. Question Bot would pick it up from there, until handing off to a doctor. The reason I'm highlighting the example is that in consumer tech (which the authors suggest considering), the initial information tends to be much slimmer. That makes the initial differential diagnosis problem more exploratory, rather than a process of ruling out diagnostic candidates.

Patient-reported information also needs confirmation or additional questions to translate into medically-useful information. For example, if a patient reported a fever we couldn't take that at face value because many patients report that for feeling hot or tired. It didn't have the same clinical meaning as a sustained, measured temperature of over 100.4 F. In teaching cases, the information is presented as already-resolved facts which simplifies the task.

The gatekeeper agent in this work can be a bit artificial: When the AI asked "Can you estimate your daily urine volume ...?" the gatekeeper agent synthesized the response "approximately 8–10 voids per day, with volumes of about 300–400 ml per void, resulting in an estimated total daily urine output of 2.5–3 L." There's a bit of a gap between the gatekeeper response and a real patient's response.

The paper acknowledges that monetary costs leave out time-to-result and logistical availability, and an actual clinical example would help. Consider a case that looks like a repeat urinary tract infection (much lower severity than the cases in SDBench). In theory the doctor orders a urine culture and waits for the results before diagnosing and treating. In practice the culture takes a couple of days while the patient is in pain, so it's more common to order the prescription and the lab test together, and the lab test results can lead to a change of treatment if the culture results are abnormal. And a significant percentage of patients just don't get the urine test done. I learned this the hard way when trying to integrate lab test result data for clinical decision support: In theory the doctor could wait for the lab results, but in practice clinicians consider many tradeoffs to provide the best care they can.

Though I'm critical here, my intention is to emphasize: You can't just take a proof of concept like this, duct-tape it to a clinic, and expect higher quality or lower cost medical care. The paper alludes to this in the limitations and future work, but doesn't seem fully aware of just how much further the work has to go. The MAI group recently added a forward-looking position piece in [Liu et al, 2026](https://bmjdigitalhealth.bmj.com/content/2/1/e000395), though I felt while reading that it's underinvested in human-computer interaction and overfocused on ideas around autonomous AI, with little commentary on what's legal or safe.

Back to some things I liked about the DxO work:
- I really liked the graph of diagnostic accuracy vs cost-of-tests and the Pareto curves. That's a great way to visualize the tradeoffs, even if the diagnosis axis isn't one of the quad aims
- They're open about many of the limitations of the work
- I like that they included basic prompts as baselines to compare to their multi-agent system
- Great to hear: "In these cases, MAI-DxO often sought disconfirming evidence and switched its diagnostic path"

Google's AMIE group teamed up with Beth Israel Deaconess, including Brodeur from the previous paper in [Brodeur et al, Oct 2026](https://doi.org/10.1016/S0140-6736(26)01535-7) ([preprint](https://arxiv.org/abs/2603.08448)) to run a prospective test of AMIE in urgent care. They had 100 patients complete an AMIE chat session under human supervision until concluding with a differential diagnosis (after excluding some cases and intervening a few times), and handed off that chat session and a summary to the doctor. Privately, AMIE logged the management plan, and they had clinical evaluators do a blinded comparison of the differential diagnosis and management plan from both the clinician and AMIE. They found that the two were roughly similar, though human doctors were more practical and cost-effective. I should note that doctors could see the AMIE differential, and it may have changed their behavior in about half of cases reviewed, so the evidence behind "roughly similar" is a bit weakened.

This reminded me a lot of our work on Question Bot, because much of the bot chat was asking questions which led into a handoff to the doctor. It's tough to get that handoff right, and they found that as well. Our doctors found it pretty time-consuming to read a full chat transcript, which motivated us to organize our medical findings in a compact UI.

This work felt like a cautious step towards clinical care: It's a relatively small scale study with lots of oversight. Because the size is small, it's understandable that they did a single-arm study without attempting to measure patient outcomes.

They propose future work to identify cases that are safe to consider automating. At 98point6 we reviewed cases for increased clinical assistance, prioritizing those that had clear clinical practice standards, were relatively low-risk, and were common enough to merit the effort. We settled on common colds and urinary tract infections. Though keep in mind that the system didn't know right away whether something is a common cold, and so the increased assistance needed to cover a whole cluster of closely related conditions. And also keep in mind that we provided more extensive assistance to doctors, not automated care.

When I think further into the future about any possible AMIE deployment... even if it could legally diagnose bacterial sinusitis and prescribe an appropriate antibiotic, what would it do when the symptoms suggest a more serious diagnosis? It would need to hand off to a clinician, and so the integration and clinical UX needs to be improved. I'm hopeful that Google's [partnership with Included Health](https://research.google/blog/collaborating-on-a-nationwide-randomized-study-of-ai-in-real-world-virtual-care/) will focus more on the clinical handoff.

Across all of these papers, I've seen significant progress despite any criticism I may have. There's acknowledgment that these are proof of concept experiments done "in the lab", and we need to be doing more realistic testing to have any confidence that they could actually contribute to healthcare. It's also great to see acknowledgments that we're using proxies for outcomes when we focus so much on diagnostic accuracy, and that it's sometimes done because that's the only data we have at hand.

If I'd had AMIE or DxO back at 98point6, I'd apply them in these ways:
- Use them to prioritize cases for peer review that look like they have diagnostic errors. If that's effective in supporting the medical quality improvement process, I'd anticipate requests to pull that into the clinic for in-visit error-checking. But it's also possible it wouldn't work on many cases and it'd be better to learn that in a low-risk application.
- Use them for simulated patients in pre-prod environments. This would be useful for training new members of the medical team that are learning how to use our software. It'd be particularly useful if we could not just pick the type of case but also ramp up the difficulty, like an inaccurate medication history or more vague description of symptoms. It would also be highly useful for anyone testing the software. As before, this is a low-risk application that could be rolled out quickly.
- Experiment with them as alternatives to the core machine learning in our existing features.

As a researcher, I like assistive applications of AI because it's much safer and quicker to deploy, and therefore I'm able to learn from any mistakes much more quickly and safely. That doesn't just help me improve the immediate research, but helps me identify gaps in which my simulations are unrealistic of real clinical practice. It also helps me build close relationships with clinical experts, which further improves my learning process. That may explain why I felt a bit disappointed to see so many publications that keep the medical and AI/ML work separate: Our best work at 98point6 came from close collaboration between the medical and technology groups.

## Is AI/ML assistance helpful? The literature and the practice

Part 2 presented mixed findings about whether AI/ML assistance is helpful, and it's an area I have a lot of lived experience with, even if I'm new to this literature. I'll start by commenting on the studies, then discuss my own experiences afterwards.

### Literature

[Goh et al 2024](https://doi.org/10.1001/jamanetworkopen.2024.40969): This is a small-ish RCT, asking if AI deployments in typical healthcare conditions are helpful despite minimal software support and no training. They found that giving participants access to ChatGPT didn't improve differential diagnosis, diagnostic reasoning, or planned test orders on clinical vignettes. Note that it didn't find that the combination was worse; they just weren't statistically different. They did see a hint that participants with more LLM experience might've been faster, but that was only p=0.07.

The study doesn't tell us much about what's possible with a LLM + doctor combination, only what to expect in organizations that just pay for HIPAA-compliant ChatGPT and provide no training or system integration. So it's more an assessment of what I'd deem a low-effort (and probably common) LLM integration. And also keep in mind that this was 2024: Everyone had less baseline experience with LLMs, and models are much stronger than GPT-4 now.

They also tested a "LLM only" condition that had a lightly optimized prompt, and it showed much stronger results than humans. I was initially surprised and suspicious, but after seeing actual examples in the Supplemental materials, it's much less surprising that an LLM would be more thorough at generating highly detailed output from highly detailed input.

[Goh et al 2025](https://doi.org/10.1038/s41591-024-03456-y) wasn't covered in Part 2, but it shares many similarities and was even run at the same time. The main difference is a focus on patient management, which includes test orders as well as treatment decisions. In this case they provided a little more training and tech support, and found that the doctors did better with GPT-4 than without: about a 6.5% improvement on a complex scoring rubric of patient management. It's tough to say exactly why, but one interesting factor is that the LLM use slowed the doctors down and they saw correlation between the judges' ratings and how much time was spent in the case. In their words:

> The group using the LLM spent more time solving cases, a finding that aligns with historical studies of diagnostic support systems, but contrasts with recent findings of LLM use within diagnostic reasoning. While this increased time may be due to the combined effects of case problem-solving and LLM interaction, engaging with the LLM may have served as a beneficial "time out" to better consider the patient context. ... Of note, the persistent advantage of the LLM group after adjusting for time spent and response length suggests that the improved performance cannot be attributed solely to these factors.

The [Mingyang Chen et al 2026](https://doi.org/10.1038/s41746-026-02409-8) paper was a meta-review of many studies comparing AI and healthcare providers (HCPs), as well as studies of HCPs with/without LLMs. It's a nice addition to Brodeur, AMIE, and DxO (in fact, AMIE is included). Although I like their coverage of LLM vs HCPs, I'll focus on the takeaways for LLMs as assistive tools for HCPs:
- 72% of studies focused on diagnosis, 18% on triage, and 10% on both. None focused on patient management, treatment, outcomes, or physician satisfaction.
- The quality of the LLM has a big effect, which explains how some older studies may see little benefit while newer ones show more.
- LLMs were less helpful on more realistic cases.
- They noted that LLMs tended to be less helpful for text+image input, though I expect that to vary greatly with the model used and the type of image.

Among other things, they implore study authors to include more details around the interaction workflows of HCPs using AI, as well as the user interface design.

This quote is a good place to land on:

> Current evidence suggests potential value as assistive tools, yet the predominance of retrospective designs and curated cases creates substantial uncertainty about real-world performance.

[Vaccaro et al 2024](https://doi.org/10.1038/s41562-024-02024-1) is a meta-review of human-AI combination, but across fields rather than limited to healthcare. They were seeking evidence of synergy: When the human-AI combination is better than either alone. I'll list the relevant findings:
- If the AI alone was better than the human alone, the combination was somewhere in the middle (no synergy).
- If the human alone was better than the AI alone, the combination was better than both.
- Newer studies show more human-AI synergy, possibly due to stronger models or better designed interactions.
- The type of input and type of output had an effect.
- The presence or absence of AI explanations or confidence scores didn't have an effect.

When they say "better" they're using the metrics from the studies they surveyed which included task accuracy, error, and quality.

My takeaway is that there's good evidence that AI features can help improve results over humans alone, but that it doesn't always achieve the "best of both worlds" goal. Though even an assistive system that isn't synergistic can still be a valuable improvement.

Keep in mind that these are often studies "in the lab", and we've seen in mammography screening that sometimes the real-world clinical impact of humans with CAD tools is actually worse than the human alone. ([Lehman et al 2015](https://doi.org/10.1001/jamainternmed.2015.5231))

There were a few studies briefly mentioned in Part 2 that were the kind of evidence I wanted, plus one newer study. Because this section is running long I'll keep it short:
- [Zhou et al 2021](https://doi.org/10.1038/s41746-021-00524-2) is a meta-review of RCTs including ML in clinical practice, and focuses on tools to assist clinicians. The core finding is that even strong results often fail to translate to improved clinical outcomes. They saw that newer studies tended to demonstrate improved outcomes, possibly due to the rise of better models and possibly due to focusing on tasks or specialties that are more likely to benefit.
- [Agweyu et al 2026](https://doi.org/10.1038/s41591-026-04503-6) is a randomized controlled trial of `gpt-4o` in primary care in Kenya. They did not find evidence of improved patient outcomes as a result of LLM use, though they did see more complete clinical documentation. [A companion article](https://doi.org/10.1038/s44360-026-00082-5) reviewed many cases for safety, noting the potential for improved care but also observing that harmful LLM advice was adopted more than expected.
- Part 2's ambient scribes paragraph covers a range of papers, and my view is that they show signs of promise in saving time and reducing burnout. I'm confident that it's *possible* to help clinicians in a meaningful way, though it may depend on the specific implementation, specialty, or other factors.

### Practice

In my experience, whether a clinical product feature is helpful has less to do with it being LLM-based, ML-based, or rule-based and much more to do with the design of the user interface. It's helpful to think about the human-computer pair as a single system. Good systems are designed around the strengths and weaknesses of both, while also acknowledging that people are not robotic and have diverse relationships with technology.

These are some more specific factors that affect the overall outcomes of help or harm:
- Is the user interface easy to learn and use?
- Is the feature interrupting the physician, or does it operate at just the right moment in the clinical workflow?
- Does the feature reduce the physician's agency or autonomy?
- For AI/ML models, how good is the quality? Is the UX designed to minimize the harm of errors?

This isn't the first time I've seen study results be highly moderated by the quality of the user interface: I first saw this in my PhD research in word prediction around 2004. Back then, the sentiment in the assistive technology field was that word prediction didn't help for typing speed at all. But when I scrutinized the studies behind that sentiment, I found terrible user interfaces with low-quality language models behind them. That led to [our group's user study]({{ "/assets/pdf/trnka09taccess.pdf" | relative_url }}) in which we optimized the user interface for usability, and we showed that word prediction can help typing speed significantly if the user interface was decent, the predictions were good enough, and the user's baseline typing speed was already low. Looking back at it now, I wish I'd also compared a good user interface versus a bad user interface to emphasize that the results are not simply the result of the underlying algorithm.

Google researchers found the same with ML work for pathologists. In Dr. Lily Peng's telling [at ML4H 2019](https://slideslive.com/38921881/machine-learning-for-health-ml4h-what-makes-machine-learning-in-medicine-different-4): they had a sensitive model, specific pathologists, and expected the combination to work well. "When we tried to hack a system together, it didn't work. In fact, the pathologists were slower and they weren't more accurate... It turns out we had the crappiest UI in the world." After a designer pass that outlined the regions of interest, "the pathologist and the model together were better than either alone, especially for smaller cases or smaller metastases."[^quotes]

[^quotes]: Quotes from conference talks edited lightly for length and clarity.

I'll describe a few example projects at 98point6 focused on AI/ML assistance and whether they helped.

One 98point6 project that didn't work out was automated differential diagnosis with explanations. We could easily generate a differential diagnosis, and could use tools like LIME or SHAP to highlight key phrases supporting or refuting a diagnosis. In demos, doctors liked the explanations a lot, but ICD-10 codes didn't have the right granularity. We would've needed to remap ICD-10 codes into a more clinically-meaningful hierarchy to build something with even a real chance of being clinically useful. Explanations were not the dealbreaker.

A more successful example was connected to Question Bot: Initially the automated interview with the patient was presented as a chat log of questions and answers. But it was a bit wasteful for doctors to spend so much time re-reading the same questions over and over. So a much-loved project took that automated medical interview, organized it by body system, abbreviated the questions where possible, and highlighted any abnormal answers to yes/no questions. Even though it was much loved by the clinic, it didn't show up in our efficiency metrics. And in the later years when the bot interviews were longer, the card could be quite verbose so clinicians could sometimes miss things. So even with a project I consider more successful than most, we faced many challenges and the evidence was not that strong.

An example of a project we walked back was auto-complete for messages. Early on, it was clear that a lot of clinical time was going just into typing. One of the many attempts to improve typing speed was autocomplete against a bank of perhaps a thousand common messages. The biggest problem was the cognitive cost of reviewing the autocomplete and the distraction of the UI updates. In the end, we didn't find a user interface that sufficiently minimized the cost of reviewing so we removed the feature. (Later, the chat suggestion project was another effort aiming at the same challenge, but it didn't require nearly as much overhead from clinicians and the recommendations were much more contextually relevant.)

We tried to filter out bad ideas early and stress test all prototypes, but whether those were retrospective or prospective evaluation, they could never be fully realistic of clinical practice. In real clinical practice, doctors are juggling competing demands for time, managing health consequences for real people, and their licensure is always at some risk, however small. So we did our best to evaluate ideas in the lab, but also needed to roll out features carefully, monitor aggressively, and be willing to turn features off if anything looked bad. And beyond that, any surprises in production were signals that we needed to make our prototype testing more realistic.

Let me wrap up this section with advice for integrating AI/ML features into clinical workflows, based off of what I've seen work or fail:
- Consider the cost of attention: Are you asking doctors to constantly review something, or do they just memorize ".tsym" to type "Thank you so much"
- The doctors are the ones liable, so keep the control with them. Allow them to direct or interrupt any automation. (This has some parallels to [recent job satisfaction studies in coding](https://rdel.substack.com/p/rdel-153-how-does-adopting-ai-tools), and [Doctorow's centaurs vs reverse-centaurs writing](https://pluralistic.net/2022/04/17/revenge-of-the-chickenized-reverse-centaurs/))
- Minimize hand-offs between automation and humans: It's awful to be sitting around "on call" for an AI to complete something, especially if you're responsible for being timely.
- Trust is key: You've got to deliver value with little risk and little overhead. Explainability can help, and it doesn't always need to be in the product - even offline work like reviewing cases with both your AI/ML team and clinic can help clinicians decide when to rely on your work, and when not to
- Pick tasks that are relatively safe by default (like asking questions, or suggesting a diagnosis only in the documentation view)
- Design AI/ML features to fail gracefully. That can mean restricting it to a curated bank of actions/messages.

To modernize this discussion, I'll imagine how I'd approach a project we hadn't solved in my time at 98point6: Saving time in clinical notes. Clinical notes were the second most time-consuming task, behind the medical interview. When asked, clinicians stated that notes are for subsequent visits, but also they rarely read notes from prior visits. Because they could be used in malpractice lawsuits, there were understandable concerns about the content of each note. And we also heard goals around professionalism and teamwork. Take this as just an example because I haven't gone back to interview our clinicians in depth to fully understand their needs and concerns.

The majority of a typical note is already in the chat log, it's just slow to find and read. The biggest value-add from the practicing clinician is their internal thought process in diagnosis and treatment.

I'd want to reduce the level of effort into each note, not increase liability risk, and provide equal or better value to the few doctors that read the case in the future.

I think it's best to start with example output:

**What we did and why** (written during the visit):

> Viral URI, no ABx: 3 days in, no measured fever. Fluids, rest, OTC decongestant; f/u by day 10.
>
> Written by Dr. A, edited by Claude Opus 8
> {: .quote-source}

**Automated summary** (an addendum outside of the visit):

<div class="ai" markdown="1">

> Clinically-relevant findings:
> - "Stuffy nose, sore throat, really run down since Sunday" (chat)
> - Felt "a little feverish" Monday night; no measured temperature (chat)
> - Nasal drainage clear (chat)
> - No cough, chest pain, or trouble breathing (intake)
> - No chronic conditions, no current medications (profile)
>
> Assessment:
> - Viral upper respiratory infection
>
> Plan:
> - Rest, fluids, OTC decongestant as directed
> - Return visit if not improving by day 10, or if measured fever over 100.4 F
>
> Written by Claude Opus 8 from chat, medical history, ...
> {: .quote-source}

</div>

The practicing doctor would focus on the short and important part: the natural, informal one-liner they'd naturally give to a colleague, since the reasoning is the main part that can't come from chat. They'd write it shorthand, with the AI/ML component translating for other clinicians, and we can improve the system over time using data from edit logs. The automated summary would be generated after the visit closes and take a more prominent role in peer-review, where reviewers can edit or remove it as appropriate.

Although incomplete, this example touches on some of the lessons I've learned the hard way:
- Doctors stay in control
- We're minimizing the cost of reviewing, both in reviewing the edited reasoning (because it's short), and reading it later
- The attribution notes help with trust, and if the auto-summary has a mistake, the attribution means they won't be judged as much by peers
- When available, quotations are easy to verify and easy to trust
- The role of AI/ML in the more critical part (clinical reasoning) is limited to a lower-intelligence task of spelling, abbreviations, formatting, and expanding shorthand with specifics already in the record
- We have a plan to improve the AI/ML based on usage data

## Who's responsible for the whole health system?

Google's diabetic retinopathy work was the subject of a great session at the 2019 ML4H workshop [by Dale Webster and Lily Peng from Google](https://slideslive.com/38921881/machine-learning-for-health-ml4h-what-makes-machine-learning-in-medicine-different-4) on the Thailand deployment. For safety, the DR tool punts on blurry images and poor lighting, and in the Thailand deployment that was about 21% of the images ([Beede et al, 2020](https://doi.org/10.1145/3313831.3376718)). So when there's a fuzzy photo at a remote clinic, the patient is referred to an eye doctor, the nearest one is hours away and many people don't have the means to even get there. That's all because the screening tool wasn't sure what it saw. And although 21% doesn't *sound* bad, that's enough to make up half to two-thirds of all referrals. That's a lot of burden on patients that didn't pay off.[^dr_extras] Part 2 quotes [Coiera](https://doi.org/10.2196/16323) on "the last mile," where technically high-performing systems perform poorly, and his recommendation to develop and test within the context where the thing will finally be used. This is a sad example of what it means in practice. It's not just a system that fails to work - it's a system that also incurs meaningful costs to people, whether in money, time, or quality of life.

[^dr_extras]: [Ruamviboonsuk et al, 2022](https://doi.org/10.1016/S2589-7500(22)00017-6) is the prospective followup with more details if you'd prefer peer-reviewed work rather than my reconstructed estimate from the papers. They include precision/PPV stats but exclude the "punt on low-quality images" category from PPV. If you count non-DR vision problems as worth the trip, that would mean about half of the referrals are worth it, up from a third.

Lauren Oakden-Rayner's talk ["Preventing Disasters"](https://slideslive.com/38923243/preventing-disasters-why-safety-is-the-foundation-of-medical-machine-learning) is also worth highlighting for the many ways in which ML work can fail to improve outcomes (or even harm them). I'll mention a couple of her points:
- The human+computer mammography system worked great in the lab, but doctors in real practice changed their behavior to the point that it was more harmful than the doctor alone.
- Babylon's work in the UK took the easy cases out of general practitioner clinics, causing some to go bankrupt
- IDx can help identify more diabetic eye disease, but it could double the amount of referrals and it takes 15-20 years to train more ophthalmologists

I'll quote one of the takeaways made throughout the day:

> If you're producing a system that's going to see widespread use in the healthcare system, talk to a health economist.

The sepsis alert in Part 2 is a related pattern. It wasn't the screening alone that caused problems, but the design of the alert and notification system around it. The cost of an alert or notification is not zero, and I always think of a [chapter from Robert Wachter's *The Digital Doctor*](https://medium.com/backchannel/beware-of-the-robot-pharmacist-4015ebf13f6f): a hospital's alert system firing so often that the important alert got ignored along with the rest, and a child received something like a 39-fold overdose of a drug and very nearly died. And I find it deeply frustrating that the practicing clinician can lose their license, while the people involved in making the software risk little or nothing.

Did we do better at 98point6? Frankly we were too small to have an observable effect on the overall health system or population health. If we'd continued exponentially growing, I could see the risk of a quick shift from the regime of desperate-survival to big enough to affect the whole system. I mention it because it's a common risk of quickly scaling startups in critical industries.

Speaking of hypergrowth, 230 million people use ChatGPT for health questions every week, as of January 2026 ([OpenAI, 2026](https://openai.com/index/introducing-chatgpt-health/)). The health answers aren't currently subject to the same testing and quality controls as software meant for clinical practice. In fairness, patients have been relying on "Dr Google" for a long time now. But on the other hand, a web search is only surfacing medical information while AI is "action-directing" to use the FDA term. Although this isn't currently regulated by the FDA as far as I know, their [August 2026 GenAI whitepaper](https://www.fda.gov/medical-devices/digital-health-center-excellence/considerations-regulation-generative-ai-enabled-medical-devices-discussion-paper-and-request) treats these very differently. While we wait on regulation, we've already seen examples of harm related to AI medical advice ([Eichenberger et al, 2025](https://doi.org/10.7326/aimcc.2024.1260), [NYT, 2026](https://www.nytimes.com/2026/10/27/well/ai-chatgpt-medication-epilepsy-death.html)).

Even if we don't have a system of responsibility for health outcomes in these cases, I wish we at least had the kind of transparency that would enable patients to make informed choices about the risks and benefits of reliance on AI for medical advice.

## Misc comments and pushback on Part 2

- Part 2 found no AI-versus-clinician study that weights diagnostic errors by their clinical cost. Given that the review covered a couple of hundred papers and that it's a common topic in ML textbooks since at least 2005, that's concerning.
- The pulmonary embolism coding example, where "rule out PE" got coded as PE: Although I trust that many deployed systems have had this problem, it's not a reflection on the state of the art in AI/ML, and hasn't been for some time.
- Specialty erasure. Studies are done in one niche but headlines sometimes over-generalize. A radiology model is for radiology. A sepsis model is for sepsis. The lessons may generalize; the models don't.
- Hinton's "stop training radiologists": He later walked this back, saying "a combination of A.I. and a radiologist, and it will make radiologists a whole lot more efficient in addition to improving accuracy" ([NYT, 2025](https://www.nytimes.com/2025/05/14/technology/ai-jobs-radiologists-mayo-clinic.html)). It's a reasonable correction from replacing doctors to assisting them, with a better focus on efficiency as a measure of assistance. That's roughly the starting line we had at 98point6 in 2016.
- Readmissions: Part 2 mentions a good criticism that readmissions can be gamed once you attach Medicare-sized financial incentives to it. Absent those, readmissions seem like a decent aggregate measure, with the caveat that not every readmission is avoidable. 
- The generic-drug default going from 75% to 98%: unlikely to be the result of only a UI change. That usually comes with an organization-wide directive to shift to generics, and the software default, policy, and practice all change at once. And a UI-only change would only work where clinicians expect the same outcome from either drug.

## Conclusion

Part 2's literature review surfaced interesting and new work for me:
- The clinical trial where optimizing a surrogate measure led to killing people. I knew all too well about the risk of reward hacking in ML/RL systems, but it's another thing entirely when people die as the result of a bad surrogate measure.
- It's great to see research in automation for the medical interview, especially when it extends into differential diagnosis, treatment plans, lab orders, and considers cost. Though there's a lot more work to be done!

Initially I was enamored by Fryback and Thornbury's ladder, showing how diagnostic accuracy could lead to changes in patient management, which could lead to improved outcomes. Now I see that it's just an example of how we can build a ladder of subgoals along the path to improving our top-level outcomes like the quad aim.

Thinking back to my stances from Part 1, I feel more strongly that diagnostic accuracy has to be viewed in context with all the details of how it's evaluated to have any useful meaning. I've softened from calling diagnosis simply an intermediate output, realizing that there are specialties more focused on diagnosis than primary care.

We've seen some glimmers of hope: Features or products that are designed to assist clinicians in actual practice. These efforts can yield progress along the quad aims, in contrast to work that exaggerates a non-existent competition between AI and doctors.

What makes some efforts deliver results while other efforts don't is not always clear, and the evidence backing the progress on outcomes is less strong than evidence towards surrogate measures. Despite all the challenges though, I'm convinced it's possible to produce software that's meaningfully better for clinicians and patients, and it takes a real commitment to optimizing human-computer systems in medicine.

And it's not enough to demonstrate progress on proxy metrics like diagnostic accuracy. We've got to be moving up our metrics ladders towards the quad aim.

Show me progress on outcomes that patients actually care about.[^poem]

[^poem]: Paraphrased from patient-oriented evidence that matters (POEM), a test for evaluating medical publications [(Slawson and Shaughnessy, 1997)](https://doi.org/10.1136/bmj.314.7085.947). Thanks Mandy for recommending this paper!

Show me more work that saves doctors a meaningful amount of time in a real clinic. 

Show me work that gets them home in time for dinner. 

Show me the work that makes it easier for them to take a sick day.

Show me the work that shifts time from mind-numbing paperwork to meaningful relationships.

People already use Google and ChatGPT for medical advice - show me studies of net-positive health outcomes from their use, and then make the tools better for both individuals and society.

This series started as a reaction to headlines of AI superiority over doctors at diagnosis. But most of the strong studies are still comparing the two at test-taking and narrow tasks, not in real clinical work. The prospective study of AMIE in clinic is mainly testing for non-harm at this stage.

Instead of pitting AI/ML and doctors against one another, the most promising work is seeking opportunities to help improve clinical practice today as a pathway to explore bigger contributions in the future. That's much quicker and safer than prospective studies of an automated doctor. If we're able to show improved outcomes from AI assistance in research studies, and those improvements hold up in real practice, and we do this enough times to earn genuine trust from our clinical partners, then after all that we can have a serious conversation about automation.

---
<!--reading-time-stop-->
