
---
layout: post
title: computational complexity + ??? = reality
date: 2011-08-20
---
This is an opinion piece on computational complexity or Big-O notation. There are two sides that I've experienced - teaching and software development. To some extent they're tied - teaching should prepare students for real-world use of complexity analysis. I'll start with software development then transition to teaching. I've adapted my data structures curriculum with good success, but it could probably use a few more years' trial-and-error.
Sometimes you're in a situation where you have two algorithms with the same functionality and you need to pick one. In these cases, we have complexity analysis to guide us. But it's only a guide. It's the equivalent of saying "restaurant A is more crowded than B, therefore it must be better". Sure that will work sometimes, but there are many other factors involved.

maps
----

Complexity fails to adequately describe the problematic situation of picking a good map implementation. There's considerable disagreement over whether we should teach hashtables as O(n) access or O(1) average access, and how to place prominence on the average case compared to the worst-case. Students of different teachers will similarly disagree about binary search trees - if they even know to specify unbalanced, we have the O(n) vs O(log n) misunderstanding.
Ultimately when we're developing a product, we care about whether it runs *fast enough*. So how much is fast enough?
\*crickets\*
Here is a list of things I feel are inadequately taught in data structures classes:

* the memory overhead of binary search trees may be significant for your application
* the memory overhead of hashtables may be significant  for your application
* in the real world, hashtable performance is a factor of not just collisions but also how long your hash function takes to compute
* performance of various hashtable collision resolution interacts with memory hierarchy architecture
* hashtables, binary search trees, and binary search of arrays are all extensively used in real software

sorting
-------

Sorting is a great example of the adage "there's no such thing as free lunch", but students don't usually take that away.  People want a simple story like "n^2 bad, n log n good". Reality has something more to say:

* if you're sorting small arrays, you can have it all with insertion sort - top-notch speed, in-place, and stable
* a decent shell sort actually performs pretty well, even though we maybe are unclear about the tightest upper bound possible
* heapsort typically performs poorly even though it's better worst-case than quicksort and in-place unlike mergesort
* if you know your data is partially sorted, the rules of the game change
* if you're sorting large classes in C++, the rules of the game change
