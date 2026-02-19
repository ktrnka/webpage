
---
layout: post
title: cv + latex/cs + phd = ???
date: 2011-05-23
---
So you're finishing up your PhD (or thinking about jobs) and you need to make a CV.  I remember this situation and I felt lost.  Here are some notes for beginners:

* read some of the articles on The Chronicle.  They have some excellent CV advice. Keep in mind that different fields are a little different though.
* find people in your field that you respect **and** want to be like, then try to get their CVs. This is probably easier in comp sci than other fields.

When I went through ~4-5 CVs, I checked which sections everyone had, the typical order of sections, and any formatting notes that I thought were good ideas.
Then I needed to decide on the format. Some people use a boring LaTeX document for their CV. *But wait!* LaTeX is about separating formatting and content! So I searched/browsed CTAN and found the [moderncv](http://www.ctan.org/tex-archive/macros/latex/contrib/moderncv) package. It's beautiful *and* LaTeX. That said, if you don't use LaTeX for publishing I wouldn't suggest starting just for the CV.
But if you *do* use LaTeX, here are my tips for creating a CV with moderncv.  I'll try to include tips for the content also.
One last, quick note: "curriculum vitae" and "vita" are proper but "curriculum vita" isn't. I don't personally care, but some people do so it's something to keep in mind. I think I saw this note in The Chronicle a while back.

design for multiple versions
----------------------------

If you aren't sure what you'll apply for, you may need roughly three CVs: a teaching CV, a research CV, and a research and development CV. What makes these versions different? The focus.

### the goal

The search committee for a teaching position wants to know about your teaching experience. How many classes have you taught? What were they about? Were they introductory or advanced? What's your teaching style? How does your teaching style affect your curriculum and/or delivery? Most of the sections are the same as a research CV, but the order is different. You may also want to include information such as review quotes, advising experience, whether your students switched to CS major, or any other positive experiences.

*Side note:*I don't suggest including teaching evaluation numbers because the reader will have no reference point for comparison. If you really want to include them, also include the numbers for other people teaching the same class, preferably in the same semester. Also, I tend to question the survey numbers. For example, see [this study](http://www.economics.harvard.edu/faculty/staiger/files/carrell%2Bwest%2Bprofessor%2Bqualty%2Bjpe.pdf).

The committee for a research faculty position wants to know about your publications and grants. If you have research advising experience, that's good too. Teaching and service are important but secondary. In contrast to a teaching school, a research school might want the following info:

* What is your thesis about? Not a whole page abstract, but the smallest, most boiled-down version.
* They see your conference proceedings - are they good conferences or not? So I included acceptance rates to help (when I could find them). It's mostly for situations where you're examined by many computer scientists but not all in your specific area.
* Are your publications really *your* research or your advisor's?
* Are you capable of working on projects other than your thesis?

If you're applying for industry positions, you want something more along the lines of research and development. They need to know about your software engineering experience and proficiencies. In contrast, faculty positions probably don't care too much about this. You might include examples of systems that you've developed, for instance.

### implementation

First and foremost, separate the sections into separate files.  If you've done that, you can simply include them in a different order. "But wait!", you say, "I need to include my thesis description in my research CV and not in my teaching CV!"
You can solve this problem with the *ifthen* package. There are several pseudo-guides online.  In my top-level documents I have this:

```
\usepackage{ifthen}

% conditional compilation flags
\newboolean{thesis-abstract}
\setboolean{thesis-abstract}{true}
```

Where I set the boolean differently in each top-level version.  In my education file I have this (the education file has my degree listings):

```
\ifthenelse{\boolean{thesis-abstract}}{\input{thesis-desc} \vspace{0.1in} \\ }{}
```

Now I don't have to worry about one version of my CV being out of date. Or a typo that I remember to correct in one but not the other. In this setup, I spend a fixed amount of time on formatting and maintenance focuses exclusively on content.
But note that I learned this *the hard way*. I had two different CV versions then realized how I could've done this when I went to make my third version.

color and style modifications
-----------------------------

I printed the CV in greyscale a few times and adjusted the greys/blues of my CV so that it didn't produce a hard-to-read dithering or anything. Tell yourself over and over: "How can I make it easier for my prospective employer?" If you can't answer that, ask faculty members you know about search committees, tenure evaluation, etc. The flip side is that you shouldn't overdo it. It'll never be perfect - you're just trying to streamline it 90%, not 100%.
Based on some of the CV advice articles, I also decided that I should add my name to the page number - for example, if someone doesn't happen to staple it, I want them to still know it's me. I had to edit the style file for both of these changes.

walkthrough
===========

I don't think I have the best vita, but I'm reasonably satisfied with the amount of information and the compactness. So I'll link my CV here and walk through the sections. The design goal is to expect some power law for the chance that they'll read a section as a function of how far into the CV it is. Another way of putting it: they'll probably read your name and education. Half as likely to read the next section. Half again to read the next section and so on. You really want to get to "the meat" of what they're looking for on the first page.

* [CV for research and development positions](http://kwtrnka.wordpress.com/wp-content/uploads/2011/05/trnka-rnd.pdf)
* [CV for teaching positions](http://kwtrnka.wordpress.com/wp-content/uploads/2011/05/trnka-teaching.pdf)
* [source latex files (and my tweaks to the class file)](http://www.cis.udel.edu/~trnka/trnka-cv-sources.zip)

header
------

I was glad that I included my Skype handle. My biggest regret is that I didn't include my lab phone number - my cell doesn't get acceptable reception in the office.
Also note, if there were two numbers listed, the icons really aren't enough unless you're looking closely.

education
---------

In my analysis of CVs I found that the education section was consistently first. In some sense, this is strange - do positions really get non-PhD applicants?
But on the other hand, pedigree is important. If they see you're from Stanford NLP, that greatly increases the chance that you're a good candidate. Another way of looking at it - did you get a mail-order PhD or a real one? You can argue about pedigree all you want, but people use it to build the short stack of applications.
The second thing to note is that I've included a thesis description for research and RnD CVs, but not for the teaching CV. Teaching applications want to get to the teaching experience right away, so you have to do all you can to get that on the first page. If you don't have much or any experience though, maybe you'd consider adding the thesis description.

research
--------

I treat my publications and research positions almost as a group, because it's the research part. If you're listed on any grants, that would also be in this group.

### research positions

I've seen this in some CVs - it's like the resume's employment history. But we have research assistantships or teaching assistantships instead. I have the RAs in my research section and the TAs in my teaching section.
The next thing to note is that I put effort into my descriptions. The reader probably doesn't give a huge amount of weight to the fact that you held a position. They want to know what you did and why you were better than someone else. How did your assets improve the project? It could be anything from coding expertise to research advice to publication.
I included this before publications because it gives a sense of the projects I've worked on. It's a sort of introduction to my publication list.
publications
Publications are the core of your application to research faculty positions. Also very important for research and development. Also important for teaching positions (but less than teaching experience there). Based on my survey of CVs, I found that people usually distinguish between 1) journal articles, 2) peer-reviewed conference publications, and 3) non-peer reviewed publications.
There are a few small points about my publication section:

* name bolded
  This allows them to see that I'm first author on most publications *at a glance*. It's like user interface design - you don't want them to work hard to get the information they want. I have to really give credit to a professor I met at ACL Ohio State for teaching me that search committees want to know whether you're riding your professor's or your lab's coattails.
* acceptance rates
  This depends on your tastes. Acceptance rates help people who don't know how prestigious each conference is. If the acceptance rate is very high or not listed, it's not shown. Though I think there was only one high acceptance rate on my CV that I didn't show, and I just couldn't find them for the others.
* awards
  If you win a best paper award, make a note of it under the paper. Use formatting to draw their attention to it.
* locations
  For popular conferences in my field (like ACL, NAACL, and ASSETS), I included the location because it's *much* easier to remember Tempe, AZ than 2007. I can't remember 2007 for the life of me, but I remember the style of the hotel in Tempe, the happy hour, the shape and size of the conference room, the pools, walking around town for ~10mi, chatting with Simon and his group, lending my miniDVI-VGA dongle to a woman from Jake's group, and so on. I remember that it was 95-105 but it wasn't humid so it didn't bother me so much.
* page numbers
  If someone wants to read your paper, they'll check Google Scholar or your webpage (probably). I included page numbers because I've been told that some automatic publication rating systems use "presence of page numbers" to rate the prestige of a publication. Go figure.

advising
--------

I advised an undergraduate and started a project with my advisor and him. That's a really important experience and I tried to play that up. There isn't too much to say about it though. In my research CV, I include it after publications. In my teaching CV, I include it after teaching.

teaching
--------

I have a lot of teaching experience, so it's broken into three sections: teaching, teaching assistantships, and guest lectures. I was debating about dropping this section from my RnD CV but decided to include it to show them what I've been up to.

### teaching

Especially for a teaching position, they want to know about your teaching style and how you strive to be a better educator. Therefore, I added a little blurb under each course explaining how I improved the previous curriculum or learned to improve my teaching in some way. I also included a short description of each course because the course title is often deceiving.
For my Applications of Natural Language Processing course, I felt that it was extremely relevant to my field so I included the course URL in addition to the other information.

### teaching assistantships

In contrast with teaching, I just listed my TA courses. Although maybe I could've explained that I redesigned and improved a procmail-based testing system for the 280 class, I couldn't say much for the other courses. TA work is mostly grading and dealing with boring work. If you lack teaching experience, you might be able to explain how you affected the class in your TA list.

### guest lectures

I included this section because it's a mixture of teaching and service. For teaching faculty positions, it shows that I'm capable of teaching on other subjects. I also think it shows that I'm pretty helpful.

software development
--------------------

You don't need this for teaching and research, but definitely for RnD work. Compared to my research and teaching sections, I'm the least satisfied with my development section.
I wish I had included my smaller projects, such as my Javascript mailto obfuscator, ParseTreeApplication, my Perl tool to compare stemmers/lemmatizers, and any other small projects that I released to others. Maybe I would've called it "hobbyist" or something along those lines.
It might've been nice to have a dedicated section showing how I have experience with databases, web applications, etc. But instead I tried to convey that in my descriptions.

### positions

I tried to describe my role and how my work affected others. In retrospect, I probably should've kept better tabs on my former systems and should've chatted more with my former boss (who's a cool guy anyway).

### proficiencies

For better or worse, you've gotta know the language you'll be working in to get the job (usually). Originally I listed the dreadful "years experience" next to each language, then decided that was complete BS on most resumes or CVs. So I changed it to something like advanced/intermediate/beginner. Then I realized that can mean anything, so I changed it back and decided that either way I'd clarify in the interview.
I tried to convey my experience by saying how I used each language. Though I don't think that worked out well in the end. I probably should've listed example systems/applications for each language.

other
-----

I needed a section for service and an award so I tossed them together at the end. Sadly I don't have more of this. But in general, tenure evaluations focus on research, teaching, and service. So those are your big three sections for faculty positions and you swap teaching and research depending on the position.

but what about me?
==================

Your vita is undoubtedly different. That's a decent analogy because *vita* means *life*. Of course you have different experiences! Maybe you have less teaching and more research or vice versa. Or maybe you've spent more time in software development. You'd want to include anything that makes you look like a desirable candidate.
In designing the order of sections, how to word things, the formatting, etc, here are some principles:

* view the CV from the reader's perspective.  Make it easy for them to see your good points.
* focus on your strengths.  Don't explain why you have weaknesses - that can be done on demand in interviews.
* differentiate yourself.  When they read your vita, they should get a sense that you're a real person, not a list of achievements.
* condense.  You need to include enough information, but they shouldn't have to flip through 4 pages very carefully to get to the important stuff.
* ask people to review your CV.  This can be hit or miss, but even a non-expert can give you excellent feedback.

the future
----------

LinkedIn is a great place for a professional profile. It's an excellent tool for finding jobs and networking. Unfortunately, it's much less common in academia - PDF CVs are more common. Also, LinkedIn's sections and processing don't work as well for academic work. Maybe that'll change in the future and then the traditional CV may be replaced with an automatically-generated CV from your LinkedIn profile.
