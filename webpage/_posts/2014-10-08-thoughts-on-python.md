
---
layout: post
title: Thoughts on Python
date: 2014-10-08
---
Python is a great language: It's simple and popular enough to have excellent APIs. A couple years ago I switched over from mostly Perl-based scientific code to Python. Since then I've been mostly in Python with some digressions in Java/Hadoop and C. Although Python is popular for web frameworks, my usage is entirely experimental in nature: building/evaluating language models, prototyping ideas, data analysis, and a variety of natural language processing.
At some point you get used to a language and you can't see the ugly aspects of it as much. My motivation here is to write up the confusing and unpleasant aspects of Python before I fully internalize them and forget.
For better or worse, I'm judging Python through the lens of my past experiences. In other words, in some ways I'll be comparing to the bits of Perl, Java, C, and C++ that I like.
Python 2.x vs 3.x
Python 3 handles Unicode much better but we're stuck in 2.x land due mostly to our existing code base. Python 3 advocates may say that it's not so bad to switch and I agree that it's a small pain for a single person. But in a team you'll have much more legacy code and even if the conversion scripts worked correctly it's still disruptive to have everyone relearn some of the little things for a few weeks.
Too many options
Optparse was the new argument handling module in 2.6 but deprecated in 2.7. Some of our systems were on 2.6 only for a long time so as a result much of our code uses optparse. But most new code uses argparse which is frankly better for us due to support for unicode literals and just a more friendly interface. I'm glad we're phasing optparse but it'll linger forever.
Python's quote style was particularly foreign to me coming from Perl, where single quotes and double quotes behave differently (variables interpolated in double). But if they do the same thing, what to use? If you're adding code to an existing module, of course you should remain consistent with existing code. But for new code I toyed with using single for dict keys and similar constant-like data and double for format strings. Ultimately I went with double only because it was more consistent with the team and it's easier for a new Pythonista to adjust to. In the end my issue is that we're burdened with choices that are mostly the same.
API consistency
Code style is important in subtle ways: If the code is written in the style you're used to, it's suddenly easier to read. Variables, classes, functions, constants are all named the way you're used to and so you can benefit from shared assumptions. When I first moved to industry I felt oppressed by rigid style but I've seen code bases with and without a formal style and I prefer the ones with consistent style.
When talking about style in Python you have to start with PEP-8, the official style guide. PEP-8 is great but gives the user too many options and wisely suggests consistency above all. That said, new Pythonistas rarely read PEP-8 and learn conventions by example from the design of the Python language and API.
In Java learning style by example is fine. But in Python that will lead you astray. To be fair, PEP-8 explicitly warns that the Python API is inconsistent.
How should you name classes? Camel case? Initial caps? Full words with underscores? PEP-8 clearly says camelcase but the Python API undermines it. Look to the collections module for instance: namedtuple, deque, Counter, OrderedDict, and defaultdict. Some of this comes from consistency with another rule: lowercase for built-in types. In a way it makes sense to have named tuple match the casing of tuple or defaultdict match the casing of dict. But it's weird to have a different naming rule for built-in classes vs imported classes.
 
A related issue is consistency of method names. When there's consistency you don't think about it. For example, take str.find and re.search. They do basically the same thing but are named differently. There's a similar issue with the collections classes: Is it .update or .extend? Is it .add or .append? (In this case perhaps it's easier to tell cause append implies order)
