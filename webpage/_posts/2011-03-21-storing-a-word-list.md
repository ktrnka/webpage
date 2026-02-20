---
layout: post
title: storing a word list
date: 2011-03-21
---

It's been a while; my apologies. Teaching combined with job hunting and (attempted) research takes more than I expected. I suppose that makes me an optimist?

In any case, thinking about smartphone applications like [Swype](http://www.swypeinc.com) has me thinking about how certain practical applications need to pay attention to both memory and CPU usage. Normally we only focus on CPU usage though. It's also on my mind because I'm teaching a data structures/algorithms class.

For experimentation I'll simplify the problem and take a look at storing a word list, then checking whether a word is in the list or not. I'll predominantly focus on memory usage but I'll take notes on runtime also. For testing, I'll use Yet Another Word List (about 264k words) though in practice you'd want to prune the list for your application.

I'm running on Mac OS 10.6 and using rusage to measure memory usage before/after loading YAWL into each data structure in C++.

Implementation #1:  sorted vector<string>
-----------------------------------------

This takes 17.18 MB and O(log n) to check.  You could potentially use an interpolated search to speed up the runtime.

Implementation #2:  sorted string[]
-----------------------------------

This takes 13.17 MB to store the list. I'm surprised it's less space than the vector, but I guess the table could've just recently doubled in size for the vector.

Implementation #3:  hash table
-------------------------------

Assuming that we double the size of the list whenever we reach 75% load factor, it takes 21.52 MB. If I hard-code the initial size of the list to the perfect size for that load factor, then it's 17.96 MB.

Checking to see if something is in the list is probably plenty fast, though it depends on the hash function we choose. It should be possible to use a better hash function (like say perfect hashing) once we've finalized the contents and increase the load factor to shrink it more.

Implementation #4:  trie
------------------------

I never got to play with tries in undergrad/grad classes and I always felt like they were a cool data structure.

In a basic trie, each node branches according to the number of characters. In textbooks that means branching factor of 26, but realistically the number of characters depends on the application. Does uppercase/lowercase matter? Does punctuation count? And so on.

For the basic trie, I felt I could only assume that we're dealing with 7-bit ASCII, so a branching factor of 128. In this case, the memory usage is 862.5 MB! I thought it'd be wasteful but not *that* bad!

Implementation #5:  trie take 2
-------------------------------

Before even implementing the basic trie, I had been thinking about ways to improve. One way is to remap the characters by frequency (most frequent = lowest index) and dynamically allocate the child array. We expand the array something like a dynamic table in this case.

The implementation takes two passes over the file - one pass to compute character frequencies (and then compute the character map) then a second pass to build the actual trie.

This version reduces memory usage down to 34.89 MB. It's still quite a lot more than the array-based implementations, but it's a step. One of the nice things about this approach is that it should extend to Unicode really well.

I also tried reversing the strings, hoping to take advantage of the set of common suffixes. But this failed - memory usage increased to 54.41 MB.

Another problem I face is that I'm doubling the size of the child list each time, but this can jump past what we could potentially need. If I restrict it to (at worst) hold enough elements for the max nonzero, that helps a little, but only saves us 250k.

You could probably take one step further and use character bigram frequencies to build a bigram-based character map.

summary
-------

Tries suck up quite a lot of memory. I'll admit I didn't know that. I doubt they're much (if any) faster than a hashtable with a decent hashing function.

If you were really trying to save space, you'd trim the list based on word frequency. You'd also compress the strings somewhat (for instance, you could store only root forms and use some codes to indicate valid suffixes/prefixes). Then beyond that you might start using more traditional compression.
