---
layout: post
title: hiding emails from web bots
date: 2010-10-31
---

Inevitably your email address will be somewhere on the web and a web bot will scan that webpage, extract the emails, and add them to a big list for spammers.  In response, some people spell out their email address like "trnka at udel dot com".

I imagine people view it as a deterrent - bots can grab the majority of email addresses even without processing for spelled-out ones, so there's little benefit to adding processing.  At the same time, it only takes a few minutes of fiddling with regular expressions to parse most of the spelled-out ones, and I'm sure it would have a very low false-positive rate.

Instead, I use Javascript to dynamically generate the email address.  My reasoning is that the normal way of writing a web bot forces you to parse the html yourself (or run it through a parser), so you don't have Javascript execution.  Of course it'd still be a problem if my email address were in plain text, but instead I hex-escape the email.  Not being content with that, I then semi-randomly split up the hex string into a concatenation.  Here's what the Javascript can look like:

```html
<script type="text/javascript">
    addr = decodeURIComponent("%74%" + "72%" + "6E%6B%61%" + "4" + "0%75%64" + "%" + "6" + "5" + "%" + "6" + "C" + "%" + "2" + "E" + "%" + "6" + "5" + "%" + "6" + "4" + "%" + "7" + "5");
    document.write(`<a href="mailto:${addr}">${addr}</a>`);
</script>
```

I generate my Javascript mailtos with a Perl script, and although the random splitting isn't perfect or anything, it's good enough.  However, I'm not so naïve as to think that it can't be parsed, but it's probably safer than spelling out the email address and the end-user doesn't have to know about it (aside from some NoScript users).  If bots learn to parse that, you could of course move the code into an external Javascript file or do all sorts of other sneaky things.

In some sense, the practice of trying to hide your email from scanners is moot - if bots grab emails from PDFs, there's nothing I can do about my published papers.  Similarly, I can't do much about hyperlinks on departmental webpages or other types of lists.  At the same time, it's plausible that maybe someday in the distant future, Apache might change any mailto link into a random code generation (more random even than what I've shown).
