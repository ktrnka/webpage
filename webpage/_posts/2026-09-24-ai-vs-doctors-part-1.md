---
layout: post
title: "Diagnostic Accuracy Is a Poor Proxy for Quality of Care"
date: 2026-09-24
series: ai-vs-doctors
description: "Lessons from years leading applied ML at a text-based primary care company: why diagnosis headlines are misleading, for ML and healthcare folks."
ai_disclosure: "I used AI to organize many old notes, comments, and documents. And to help me remember old topics by interviewing me. Then again in the reviewing and editing phase. I wrote the words myself. -Keith"
---

You've all seen a headline like "AI is better than doctors at diagnosis". I've come across that headline so many times that I rarely even roll my eyes anymore. In the past I used to take the time to nudge people away from misunderstandings and towards a more experienced view of healthcare. My goal with this article is to encourage more realistic conversations about the future of AI/ML in healthcare.

This is part of a bigger issue in which medicine is often oversimplified by people from other fields. In software engineering and machine learning research, we're often drawn to narratives of whether we could bring computer science approaches into other fields. Could we lead the next wave of medical progress? Ok now I'm rolling my eyes.

I was guilty of having some thoughts along those lines when I was first starting out in healthcare technology. Maybe I'd read too many ML chapters or papers that started with medical diagnosis as a clear-cut machine learning problem. Or maybe I'd bought into narratives about the bad user experience of electronic health record systems (EHRs). It's been so many years now that I no longer have a clear view of why I was so off base back then.

This affects much of healthcare technology, but I'll focus on diagnosis and adjacent problems in applying AI/ML to healthcare. And unless otherwise stated this is US-centric.

My credibility comes from leading the applied machine learning team at 98point6 for years until leaving in 2022. We deployed many pre-LLM ML models in real clinical practice for text-based primary care. We didn't do the things the ML literature focused on, because in early collaboration with doctors we found those things were not that useful, or had an unacceptable risk profile for patients. In our early work, our ML projects came to focus on saving time for our doctors, with secondary benefits for medical quality.

## Accuracy doesn't make sense when you really think about it

Most headlines or quotes focus on accuracy in the machine learning sense: What percentage of diagnoses are exactly correct? Machine learning textbooks do the same. The better textbook examples may even include [ICD](https://en.wikipedia.org/wiki/International_Classification_of_Diseases), [Snomed](https://en.wikipedia.org/wiki/SNOMED_CT), or other standardized diagnosis codes.[^billing_codes]

[^billing_codes]: ICD is the International Classification of Diseases, and is revised periodically. In plain terms, it's the list of diagnosis options in the drop-down when someone's setting your diagnosis in the system. It has some grouping of codes, and it's commonly described as designed for billing (payments from insurance companies to healthcare systems). SNOMED CT is a competing standard, and in my own experience I've seen it much less in clinical practice than in research publications.

I'm here to say that diagnostic accuracy isn't as well formed as it might seem.

First off, the diagnostic coding systems are rarely how doctors describe their diagnosis. We did an early experiment where we asked doctors to write their diagnosis in a few words, no formal codes, and what they wrote looked vaguely similar to formal ICD codes, but not as close as you'd expect. That's somewhat understandable. After all, ICD codes were made for the purpose of billing aka insurance. They weren't made for the purpose of standardized communication between medical professionals. That said, even though ICD is not ideal, most doctors are familiar with it so replacing it would not be easy.

The classic example of an ICD code would be J06.9 "acute upper respiratory infection, site not specified".[^acute] In plainer language at 98point6 that meant "common cold, probably viral". That part about it being viral is important: Antibiotics kill bacteria, not viruses, so they wouldn't help if it's actually viral. There's more to it as well: There's uncertainty in what's causing it. Maybe the patient has felt awful for 4 days and it *could* be bacterial, but we don't know. So there's a lot of missing detail in that ICD code.

[^acute]: For readers outside of medicine, "acute" in this context means short-duration, like a few days to a few weeks. "Chronic" is the term for long-duration medical conditions.

Second, ICD codes are hierarchical. So given the same case, one clinician may be more specific about the location than another, say J01.9 "acute sinusitis, unspecified" vs J01.0 "acute maxillary sinusitis". The second code just explains the location within the sinuses. If you're building machine learning against this data and you get the precise location wrong (or the absence of location), many evaluations give you zero credit. That might not sound so bad, but to put it in perspective, many evaluations consider it equally bad to omit the precise location within the sinuses as it is to confuse a common cold with cancer. An ML model that's focused on getting diagnosis codes exactly correct will focus on what happens to be documented, over what's medically important.

Some evaluations do better by giving partial credit for matches along the ICD hierarchy but the hierarchy isn't as useful as it seems to be. Clinics adopt conventions about what the various codes mean and when to use them (and sadly, if you're getting reimbursed by insurance, code selection is guided by revenue optimization).

At 98point6, a common cold that's probably viral would be J06 (acute URI) or perhaps J00 (acute nasopharyngitis aka inflammation of the nose/throat). A cold that's bacterial would be J01 (acute sinusitis). Though keep in mind these are conventions from 98point6, not universal across all clinics. We could consider grouping the J0 codes for partial credit, but any ML model should be penalized more for mixing up a bacterial vs viral infection because it changes the choice of prescription or treatment.

There's yet another kind of partial credit hidden in ICD codes: cause-based diagnosis codes vs symptom codes. In some cases it can seem subtle, like "rhinitis" (runny nose) vs "allergic rhinitis" (runny nose, caused by allergies). In other cases it's not as clear to the patient: urinary tract infection (UTI) vs dysuria (burns when peeing). The latter diagnosis implies that the physician isn't confident enough that it's caused by an infection, and usually means that they want to order a test to be sure and won't commit to a UTI diagnosis until they have test results.

This is hinting at a third topic: Disagreement by medical professionals on diagnosis codes. I'm not talking about the kind of disagreement you see on TV with dramatic debates; it's not usually like that. I'm talking about two professionals largely agreeing on the facts of the case, but documenting it differently or helping the patient in different ways. Perhaps one doctor wants to go the extra mile and be more specific than the other. Or one doctor has a higher threshold for ordering antibiotics, and therefore they're being more cautious about picking diagnosis codes that indicate a bacterial infection.

We ran into this sort of "disagreement" heavily in a triage project. The context was that our clinic was often overwhelmed in 2020 due to suspected COVID cases, and the clinic needed help with a long line of patients. Ideally, the system should identify cases where it was medically unsafe to let a patient wait in line. Initially we had clinicians triage the waiting room but that was often taking time away from working directly with patients.

We asked doctors to label cases for a basic triage decision: Should this patient skip the line? We found very low agreement scores despite several rounds of improvement to the annotation manual.[^kappa] For example, we found clear disagreement in cases where a patient just said "allergies" and nothing more. A doctor from an emergency department may say "they could be going into anaphylactic shock and I've gotta talk to them now" while a family doctor might say "they'd say so if it were life-threatening allergies". The two agreed on the presented facts and even both agreed that they wanted more information from the patient, but given only the choice to triage or not, they disagreed. Instead, we changed the annotation to a choice they could agree on: comparing two cases and picking the one that was more urgent, also called preference judgements. For example, "Which of these two cases needs attention first: 'allergies' or 'it's been a rough day and now my left arm is going numb'". Given that choice, different doctors would agree more readily and we could build an ML-based triage system from it. The takeaway here is that disagreement in ML approaches to healthcare can be an artifact of the labeling scheme rather than the professionals.

[^kappa]: I can't remember if we used [Kappa](https://en.wikipedia.org/wiki/Cohen%27s_kappa) or [Alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha) for this project. Both measure how much the people labeling agree beyond chance: 0 means chance agreement, 1 means perfect agreement. Alpha is compatible with more types of annotation, though Kappa might be more common in the literature. The annotation manual provides written guidance on how to label, and better guidelines tend to improve agreement scores.

What I'd like from a diagnosis coding system is a short, structured assessment that both the doctor and patient could agree on: What symptoms are most bothering the patient, and a partial root cause assessment. Something like a codified version of: "Difficulty concentrating, caused by sinus pressure, caused by a viral infection."  In theory this can be achieved using SNOMED CT's [post-coordination](https://en.wikipedia.org/wiki/SNOMED_CT#Precoordination_and_postcoordination) (aka "due to") but I haven't heard of this in practice, even though I suspect it's viable.

This section is running long, but I want to briefly mention a couple other gotchas before moving on:
- If you have an autocomplete system for picking diagnosis codes, it will have some effect on the distribution of codes selected. We saw this at 98point6, and it actually helped to standardize the non-clinical aspects of coding
- If you're trying to predict diagnosis from clinical notes, the diagnosis is often right there in the note, though it may not be ICD coded yet. If you're building a system to output ICD codes for clinical notes, that's unlikely to help much in diagnosis itself but may help in filling out the diagnosis paperwork.

## Primary care physicians rarely need help with diagnosis

It's easy to claim that diagnosis is the core of a medical visit, but that's an oversimplification.

Our doctors rarely needed help in choosing the diagnosis. Sometimes they might need help remembering the right [ICD-10](https://en.wikipedia.org/wiki/ICD-10) code if it's something rare. They definitely need help reducing the burden of notes and documentation. They might need some help in adhering to relevant clinical guidelines if they're new to the practice. And occasionally they may need help with a difficult case.

The most common challenge they faced was getting the relevant clinical context from the patient. That's what took so much time. **It might take 5-10 minutes to elicit the patient's story and ask questions, then 1 second to decide the diagnosis, then 10-15 seconds to find the right ICD code.** That's not to suggest that diagnosis is trivial, just that it's very fast for doctors with years of training and experience when compared to interviewing a patient. That's why we put our effort into eliciting and summarizing the patient's story at 98point6. There's a secondary benefit there that the bot didn't get tired, and so it helped with consistency and quality of practice in some cases.

Beyond this, many visits don't even center on a diagnosis:
- **Medication refills**: The patient's condition is already known. Sure you gotta pick a diagnosis code but it doesn't mean the same thing as a fresh diagnosis. These visits looked very different than a classic acute care visit.
- **Mental health**: Patients with depression and anxiety typically have different needs than a simple prescription - these visits were often lengthy, personal conversations in which much of the care is the conversation itself.
- **Referrals**: Many insurers require that you speak to a primary care physician before being allowed to speak to a specialist. 
- **Prescription oopsies**: Sometimes there were issues with the pharmacy, ranging from the patient saying the wrong one, to a healthcare provider picking the wrong one, to getting off work late and finding that the pharmacy is closed, to the pharmacy being out of a particular drug.
- **Doctor's note**: During COVID, some companies required that their workers have a signed doctor's note to call out from work, and that took a surprising amount of time, to the point that we prioritized dedicated software to help with doctor's notes.

So what does it mean to be accurate at diagnosis if the patient tells you upfront they need a refill for their ADHD meds? What does diagnostic accuracy even mean when editing the pharmacy on a prescription? Realistically, you'd only want to measure diagnostic accuracy for visits where diagnosis is non-trivial, but that's rarely done.

Articles in AI/ML in primary care typically focus on overly simplified patient data, omit the hard part of elicitation, and often omit the wide range of visit types seen in practice. The data may be simplified to a vignette (a short paragraph) or multiple-choice questions. The doctor's job also extends far beyond interviewing the patient: They need to decide whether to trust self-reported facts like temperature, or decide to order tests and put the diagnostic process on hold until the results come in. 

In many cases, even if the task involves open-ended data, it's reconstructed from clinical notes, and those are pre-filtered by doctors. Doctors often write just the essential details needed to support their conclusion, especially when faced with limited time. That's not just for clinical reasons but also to minimize legal liability in the US, because clinical notes are a key piece of evidence in malpractice lawsuits and doctors are very aware of it.

## In primary care, diagnosis is only a debugging output anyway
 
When we fixate on diagnosis, we're focused on an intermediate step. The patient wants to get better, or at least not get worse. I hinted at this with antibiotics: The patient wants to get better fast, and the doctor is deciding what treatments to consider. For a common cold, the big fork in the road is to use antibiotics or not, and the decider is whether the cold seems to be caused by bacteria or not.

At one point I thought it might be better to have a model predict treatment rather than diagnosis. But even that is oversimplified! The doctor is considering counterfactuals: Will this prescription help at all? Is it worth the risk of side-effects? Will they use it properly if they get it? Can they afford it? Can they get to a pharmacy?

To give a practical example, urinary tract infections were one of the most common conditions we treated. They're often treated with antibiotics and we had clinical guidelines about which antibiotic to prefer, when to order a lab test, etc. When trying to understand the data better, I noticed that one doctor would order antibiotics a little differently than others so I asked about it. They were concerned that the patient wouldn't take all the doses of our guideline-preferred antibiotic. That increases the risk of developing antibiotic-resistant infections both in themselves and in the population at large. So in those cases they'd order fosfomycin, which required only a single dose. It's really not as simple as always treating a particular diagnosis with a particular medicine, and even then none of the deciding factors were clear in our data.

So treatment can be affected by many reasons, some of which aren't visible. That makes treatment a challenging machine learning task as well.

And even treatment isn't quite what we want to optimize: We want to make our patients better. We want to decide on an intervention that is much better than sleeping more. So we really want to be optimizing health outcomes, but that's much less of a focus than I'd like in healthcare technology.

We had a few measures of outcomes at 98point6, but none were ideal:
- **Post-visit surveys**: This gave us data on whether patients improved, but <10% of patients filled it out and it was a biased sample of patients.
- **Return visits**: In some cases we asked them to come back if they didn't feel better in a few days. In other cases, they'd come back if anything went poorly. In other cases though, they'd just vanish out of the system and go to a different medical provider.
- **[PHQ-9](https://en.wikipedia.org/wiki/PHQ-9)/[GAD-7](https://en.wikipedia.org/wiki/Generalized_Anxiety_Disorder_7)**: There are standardized outcomes surveys for depression and anxiety, but it's easiest to get patients to fill them out when coming for a visit not as a followup. And typically patients are not going to come to us if they're feeling great.
- **Peer review**: We had a clinical QA team that did peer review of cases for safety, and that gave some visibility on outcomes like risky deviations from guidelines. Although it was time-consuming, I like that the effort was focused on quality improvement rather than just grading and assessment.

If I were approaching this today with AI/ML in mind, I'd explore a few options:
- Proactive patient health checks with the [Healthy Days](https://doi.org/10.1186/1477-7525-1-37) survey: This is a very simple 4-question survey that does a good job of capturing a wide range of health issues. It's non-trivial to design a system in which it's valuable enough for patients to fill out consistently, but I believe it's possible.
- One-button post-visit follow-up for acute care visits: Something very simple like checking if they're feeling better 3 days later would go a long way in providing feedback on our treatment, and if they aren't feeling better, proactive outreach might be useful.
- Peer review has to be a part of the system, regardless of whether it produces data for AI/ML. Medicine is simply too complex to try to automate all of quality review, and we really depend on people to spot emerging issues.

## Conclusion

Headlines comparing AI diagnosis against doctors are measuring something that seems easy to measure, but often it's a distraction from more impactful efforts. The headlines themselves also nudge patients to trust AI over the medical professionals actually caring for them.

Diagnostic accuracy is useful debugging, just not that interesting as a top-line outcome. Here are some examples of more meaningful outcomes for text-based primary care that I have some awareness of, even if I don't have great citations at hand:
- Saved doctors time per visit: We found this with several of our projects, though measuring it is much harder than it sounds.
- Improved medical job satisfaction: Multicare CMIO Dr. Michael Han [described this with ambient AI for clinical notes.](https://www.commure.com/blog/how-health-systems-are-unlocking-value-with-ambient-ai)
- Reduced patient out-of-pocket costs: Mail-order pharmacies like Cost Plus Drugs are a good example. 
- Reduced avoidable return visits: This is one of the quality metrics for hospitals.

In each case, we're looking for progress in one area without worsening in others. The quad aim is a useful breakdown of goals:
- Improving patient experience
- Improving population health
- Reducing costs
- Improving the work-life of clinicians and staff

## Looking ahead to Part 2

I don't want to rely on only my memory for all of this, and my best information is from years ago. So I kicked off an AI literature review. I pushed the agent to check the credibility of each source, expressing preferences for peer-reviewed work and meta-reviews when possible, as well as verification of claims in the full texts. I also directed the survey to explore research areas that I'm not experienced with: My usual reading areas are ML, NLP, and HCI, so I asked it to survey into medical literature as well. And I was directing the review to focus on the tasks being assessed, as well as overgeneralization of claims (which is sadly very common in headlines and even some ML research).

But then when I read the initial lit review, I felt both that it was an interesting piece on its own and that it would be impractical for me to fact-check and edit the whole thing. So I acted as reviewer for the AI literature review, and I'll share that in Part 2. Then I'll be back in Part 3 to add commentary and connect the literature back to my lived experiences from 98point6.

## Thanks

Big thanks to Alex, David, and Mandy for reviewing!

---