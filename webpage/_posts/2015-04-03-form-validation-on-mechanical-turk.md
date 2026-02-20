---
layout: post
title: Form validation on Mechanical Turk
date: 2015-04-03
---
[Amazon's Mechanical Turk](https://www.mturk.com/mturk/welcome) is a great system for surveys, writing short snippets, tagging images, and other small tasks. But you spend your time on the littlest things.

Problem: Workers submitting the form without all the fields filled out
======================================================================

Most of my tasks have requested short snippets. For example, I asked workers to provide example searches for an ad:
![Search for more info]({{ "/assets/img/posts/wp/macbook_air_ad_search.png" | relative_url }})
I had workers provide three example searches. But I'd get emails like this:
"I was doing your survey and hit the return key by accident before the last question."
"I hit enter and it submitted the Hit before I typed in a third question."
"While attempting to complete this survey, I hit enter after filling in the first box, and it submitted the HIT without my intending it.  Can I please finish it?"
Generally I respond and say sure, send me what you would've written. But it's very cost-ineffective. I might spend a couple minutes wording it to be polite and then look up their ID, approve the results, and once the batch is done I'd have to remember to copy the emailed results into the downloaded spreadsheet.
**This isn't a people problem. This is a user interface problem.** Why would they even be able to submit the form when it's blank?

Form validation in Javascript
=============================

Fortunately this is a common problem in web forms: certain values are invalid and it's easier to notify the user before they hit enter by using Javascript libraries. I picked [Parsley](http://parsleyjs.org/) because it was the first search result and it's simple.
You need to be comfortable editing the HTML of your HIT. Add these two lines near the top:

```
<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script src="http://parsleyjs.org/dist/parsley.min.js"></script>
```

Add this bit near the end. I have it after the "End Survey Body" comment.

```
<script type="text/javascript">
 $('#mturk_form').parsley();
</script>
```

Now add "required" to any input tags you want to require, such as:

```
<input class="form-control" name="poll_2" required size="120" type="text" />
```

Now you're all done! Here's what it'll look like if you hit enter or click Submit with a blank field.
![If you hit enter it'll show a little popup below the field.]({{ "/assets/img/posts/wp/mturk_validation.png" | relative_url }})

Other notes
===========

This method is convenient if you're creating HITs form the web UI but if you're creating via the API you might not be controlling the HTML.
I used a CDN version of jQuery so that it loads faster but Parsley isn't in Google's CDN. It looks like [cdnjs has one](http://cdnjs.com/libraries/parsley.js/) so I'll switch to that.
There's another way if you create via API and [QuestionForm](http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QuestionFormDataStructureArticle.html) - you can provide an AnswerSpecification that rejects empty fields. I tried it briefly but learned that it's checking on the server side and attempts to submit the form but then shows an error at the top of the screen. It's much more clear with an inline error message.
I've only done very minimal form validation but you could reject content over or under a certain length, match a regular expression, or enforce any number of requirements. See [Parsley's validators](http://parsleyjs.org/doc/#validators).
