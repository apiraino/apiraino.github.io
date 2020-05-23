---
layout: post
title: Refactored Emacs config
---

I've completely reworked my Emacs config. I've been using the excellent uber-package [Prelude](https://github.com/bbatsov/prelude) for years, but like many big monolithic installations you don't know if you really need everything. Also, although very customizable, I had found two 'core' packages I could not disable without touching the core files, which I didn't want to.

So, I've started from scratch, read one by one all the packages I had installed before and one by one installed and configured each package I wanted to keep. I've learned a lot about a packages and how to tailor your own Emacs. I'm tired and I hate emacs eLisp and probably I did not yet finish, but I still [even more](/2019/01/24/software-appreciation.html) amazed by this surprising piece of software and the incredible community behind.

Just for the record a clean Prelude installation is ~25Mb, now my whole Emacs installation (included compiled packages) floats around 8.5mb. My entire Emacs configuration file is under 11kb, 6kb (!) without comments. The Emacs binary is around 38mb stripped.

```
$ du -sk .emacs.d
8656   .emacs.d
$ du -sk .emacs.d.prelude/
25760  .emacs.d.prelude/
```

I challenge anyone to show me an entire IDE, organizer, TODO list, email client, IRC client, [psycotherapist](https://www.emacswiki.org/emacs/EmacsDoctor) and much more in such a small bundle. 

If the world ended, it can be rebuild using Emacs, the basic building block of anything.
