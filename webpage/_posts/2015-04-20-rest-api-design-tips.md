---
layout: post
title: REST API design tips
date: 2015-04-20
---

For the server side of [Pollable](http://pollable.me/) we iterated on the REST API several times and learned a lot the hard way. And [this excellent article](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api) is great for design tips.

We're using RESTful calls of Json only and https only; much of this deals with the design of the Json objects.

Know your API user
==================

Of course you should understand the client's use case. But more than that: You should **understand what libraries they're using**.

For example, [GSON](https://code.google.com/p/google-gson/) is commonly used on Android but doesn't cope well with optional fields: does 0 mean the value is missing or is set to 0? (A developer using GSON would need to use Integer rather than int to tell.)

Other client-side factors to consider, in no particular order:

* Will your Json field names bleed over into model objects in Java or Objective-C? Will that lead to awkward conflicts with variable names in those languages? GSON has field renaming policies but you have to consider whether a typical API user knows about that or wants to write the code.
* Will the returned Json objects be dumped into a SQL database like an Android ContentProvider? If so you may want to avoid hierarchical objects to work easier with a flat table.
* Optional fields/values cause tons of trouble.
  + One of our pain points was a field for your vote on a poll. At first we didn't include it for unvoted polls or related polls but it led to excess client code to update client data values rather than overwrite.

Consistency is king
===================

The more consistent your API, the less code the client has to write (and probably fewer bugs).

One issue is error handling. It's nice and clean if you can use HTTP error codes. Suppose an endpoint like PUT /poll returns a 400 error for invalid data.

But what about a version of the endpoint to add 100 polls as a batch? Do you return HTTP 400 if one poll is bad? In that case do you accept all the others or reject them all? Or do you return 200 and failed status codes/messages for each individual poll? We do the latter and have an inconsistent API. :(

Possible options, none ideal:

* Eliminate singleton endpoints, forcing clients to wrap data in a singleton array. This forces code reuse but it's not user-friendly.
* 400 status return for any bad data at all, reject the entirety of array input. For some apps this is exactly what's necessary - maybe the objects in your import don't make sense without each other.
* Wrap responses in an envelope to convey success/failure, use the same envelope for singleton and array data. This can lead to confusion because you're returning HTTP 200 OK but it seems best in the long run.

Fail early
==========

When you're prototyping a Python/[Tornado](http://www.tornadoweb.org/en/stable/) server with MongoDB backend, it's tempting to interpret the Json from clients, process a little bit, and insert straight to MongoDB. But Json in Python is decoded to a dict and MongoDB doesn't have a schema.

You might be inserting bad data to MongoDB. A completely separate endpoint may fail the next day. Debugging gets harder the further the error propagates from the root cause.

In the case of Python with MongoDB it's very helpful to use basic Json validation. If you need to process any fields they'll generate errors if missing or incorrect.

But when you're starting out you really can't afford 500 lines of code spent on validation that you update twice a day. We went with [jsonvalidator](https://code.google.com/p/jsonvalidator/) due to simplicity: provide an example Json object and it'll check that all the fields are present and the right types. We also tried [jsonschema](https://pypi.python.org/pypi/jsonschema) in conjunction with [orderly](http://orderly-json.org/) but it was verbose and didn't deal as well with required fields.

Documentation helps even in a team of three but save yourself some pain and catch errors from typos early on.

General consideration: Should the client do more work or the server?
====================================================================

We started off with one client implementation so at the time I felt that it didn't matter. We'd only have internal clients anyway. It seemed like a debate about who'd spend their time on the work really.

Since then I've changed my tune: Eliminate as much client code as you can. This is partly due to iOS: even bug fix releases can take two weeks to make it through app approval.  But you can update the server much faster.
