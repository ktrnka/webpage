---
layout: post
title: basics of bibtex
date: 2010-10-23
---

Like most authors in my area, I use LaTeX for writing papers and BibTeX for citations in those papers.  I remember how daunting it felt when I had just started though. At someone's suggestion, I started by looking at others' LaTeX and BibTeX, which helped, but I also needed structured information.  Hopefully this post helps people who are in the situation I was in.

The first problem I had was understanding the types of entries and the fields I needed.  It wasn't around back then, but now [the BibTeX Wikipedia page](https://en.wikipedia.org/wiki/BibTeX) provides the information:  a list of entry types and the required/optional fields for each.  In addition to the other information, the list shows that you can use the *note* field to include whatever additional information you'd like (e.g., url, access date).

Beyond the basic understanding, I figured my .bib file was just a list of independent entries. That's not quite true; the two notable features I wish I'd learned sooner were macros and crossref fields.

Generally, you'd define macros at the top of your bibtex file and then you can use them in the entries.  They're expansion rules, similar to C-style macros.  Macros are one way to have a consistent way of displaying conference/journal names.  They're also a way to quickly change all cited conference/journal names to a short form if you need to cut a few lines to fit space requirements (e.g., EMNLP vs Empirical Methods in Natural Language Processing).  Here's an example:
```bibtex
@string{iui = {International Conference on Intelligent User Interfaces (IUI)}}
```

Crossrefs allow you to have a hierarchical entry structure.  When you specify a cite key in the crossref field, it looks up that entry and fills in any blank fields.  You can use them to specify the conference information only once and crossref to it from each publication, or you can use them to make aliases of citations.

The main downside of macros and crossrefs is that it makes it more difficult to send people a simple, single BibTeX entry (like on your webpage). In any case, I wish I'd known about them when I was starting.

Probably the biggest improvement in bibliographies came from using [BibDesk](https://bibdesk.sourceforge.net/) to manage my bibtex file instead of editing it manually. There are certainly some things about it I don't like, but generally it's an excellent solution for OS X. If you're new to BibTeX, the required fields for the publication type are bolded and at the top. You can drag-and-drop the a pdf to the side to keep track of your pdf copies. If you like to take digital notes, you can put them in the Annote tab if you view an individual entry. It's also nice and easy to add to it; you can copy/paste bibtex entries from ACM/ACL/Google Scholar and paste them right into BibDesk. One thing I suggest is to setup your preferred citation key format, and then you can setup a keybind to auto-generate the citation key in your preferred format.

Before I finish, here are a couple other random notes that I didn't realize at first:

* You can setup a keybind in TeXShop to auto-complete a citation key.  For me, if I don't remember the citation key but I remember the author, I type the author name, select what I've typed, and press apple-shift-k to provide all the completions form BibDesk (note that BibDesk has to be open).  The option is in system preferences, in keyboard, under keyboard shortcuts: "Complete Cite Key". There's also a way to use Apple's completion (ESC) to give a drop-down list, but I don't like that at all.
* Individual conference styles will have different LaTeX citation commands.  ACL style, for example, provides \shortcite{key}, which you use for more natural text. For example, "Trnka \shortcite{trnka08blah}" generates "Trnka (2008)" in contrast to "\cite{trnka08blah}" which generates "(Trnka, 2008)".
* Be sure to include all relevant information in your bibtex; it's easier to remove it from a given publication than dig up something you forgot about years ago.  Page numbers were the one I forgot.  Naively I figured this was the digital age, but I was told to include them for automated tools that evaluate department/faculty quality across fields.
* Some venues used to require everything to be in the LaTeX file, and I didn't realize at first that I could just copy and paste out of the .bbl file.
* Similarly, if you're in the process of shortening your paper, you can just edit the .bbl file instead of modifying your bibtex database.  (credit to Emily Hill for this one)
