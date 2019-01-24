---
layout: post
title: "Appreciation for software (I): Emacs"
---

I was reading this [blog post](https://bastibe.de/2018-10-14-appreciation-for-open-source-and-commercial-software.html) on how we often forget to thank and recognize the effort to the "unsung heroes" of the software world. I find those words truly inspiring, I also had an interaction with the author through GitHub (a very nice person, by the way).

Let's don't forget that many people write software for any reason but money: therefore a sincere "thank you" can often be the best reward. Because, of course, we are humans made of flesh and purposes and need recognition for the things we do.

Therefore I've decided to join him and have my periodical appreciation post on a tool or an application that greatly helped me or simply made chuckle :-)

---

The honour of the first post on the theme can't be dedicated to none other than the software I use the whole day for so many things.

Some people joke that Emacs is more of an operating system lacking a decent text editor rather a ... wait ... I see a trap, here: is Emacs an IDE or advanced text editor? It's simply Emacs. Funny how people discuss what Emacs really is: it's a software in its own category.

Learning Emacs teaches you about more than Emacs itself: it teaches you about the quality that software can reach, the complexity and unfriendlyness :-) Also a lot about how a truly open system is uspposed to be.

When you've been using Emacs for enough time, when you need a specific tool for a job, you'll stop looking for a new tool to install: as a first thing, you'll search for an Emacs package to do that.

You also learn how much of the stuff you write can be in bare text, without binary files. You start thinking if the increasing complexity of some software is justified by actual improvements.

Emacs' history is [worth reading](https://en.wikipedia.org/wiki/Emacs) and despite an ugly icon and an [irritating language](https://xkcd.com/297/) it became one of the most long-lived software ever written; and this alone, more than 40 years later, is a remarkable achievement in itself.

I am by no means an experienced Emacs user, nor I dwelved into `elisp` unless forced by [overarching annoyances](https://github.com/rust-lang/rust-mode/pull/269), but I spent a lot of time documenting my Emacs experience and writing my own guides; to me it's simply impossible to remember all the keycombo for all the Emacs packages I use.

Here's my [Emacs setup](https://github.com/apiraino/emacs_reference). I'll copy-paste the [list of the tool](https://github.com/apiraino/emacs_reference/blob/master/guide.md#whats-in-my-personal-lisp-file) that I use:

* <a href="https://geoff.greer.fm/ag" target="_new">ag</a>: super fast grep replacement
* <a href="https://github.com/davidhalter/jedi" target="_new">jedi</a>: Python autocompletion
* <a href="http://www.flycheck.org" target="_new">flycheck</a>: Python syntax-checking
* <a href="https://github.com/jorgenschaefer/elpy" target="_new">elpy</a>: Emacs Lisp Python Environment
* <a href="https://github.com/flycheck/flycheck-rust" target="_new">flycheck-rust</a>: Rust syntax-checking
* <a href="https://github.com/racer-rust/emacs-racer" target="_new">emacs-racer</a>: Rust code-completion, goto-definition and docs browsing
* <a href="https://github.com/yoshiki/yaml-mode" target="_new">yaml-mode</a>: Major mode fpor YAML files
* <a href="https://github.com/paetzke/py-autopep8.el" target="_new">py-autopep8</a>: Python PEP8 linter
* <a href="https://github.com/syohex/emacs-git-gutter" target="_new">git-gutter</a>: git diff on the fly
* <a href="https://github.com/bastibe/org-journal" target="_new">org-journal</a>: great tool to write a developer's diary
* <a href="https://elpa.gnu.org/packages/xclip.html" target="_new">xclip</a>: (linux only) yanked text in emacs is available in X11 (overwrites X11 clipboard)
* <a href="https://github.com/w-vi/ox-wk.el" target="_new">ox-wk</a>: module to export from ORG mode to Dokuwiki

Not to mention the tools available out of the box:

* <a href="https://orgmode.org" target="_new">org-mode</a>: "your file in plain text". Documents, TODOs, notes. And export to whatever format you want.
* <a href="https://www.emacswiki.org/emacs/InternetRelayChat" target="_new">IRC client</a>

Each developer of each of these packages should deserve a personalized praise.

There are downsides in using Emacs, of course:
* Once you get into "Emacs-mode", it's hard to switch back: this also means that if you are guest on another workstation, you feel so clumsy. And your pair-programming buddy might find awkward seeing you constantly inserting random text
* The documentation, although exhaustive, is not an easy read. I gave up on reading it, I can easily find answers on Stack Overflow anyways.
* Although extensible, I honestly hate Lisp (and it's my fault, no problems admitting that); nonetheless that's a major road-block for me to write my own tools

Emacs should be approached little by little: for example, first try it as TODO or note taking tool, see if that improves your workflow. If yes, then try adding another tool. And so on.
