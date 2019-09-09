---
layout: post
title: "Appreciation for software #2: photorec and srm"
---

How many times did I delete by mistake some photos I had dumped from the camera SD card? Too many.

However I've always got my back covered by [photorec](https://www.cgsecurity.org/wiki/PhotoRec), a little and very simple tool to use. You just launch it on your SD card and while it does the job you can go grab a coffee.

Photorec works with virtually any filesystem, because it has no notion of filesystem. When a file is deleted, most of the times the actual data is still there, only the entry in the index table is deleted so the filesystem knows that that cluster is reusable.

Photorec first figures out the block size and then "blindly" proceeds scanning the surface in steps, looking for known file headers (jpg, png, zip, etc.).

If some adjacent clusters belonging to a file have been (partially) overwritten, nothing can help. This is why it's important to attempt a file recover as soon as possible before using the device again.

<center>
    <figure>
        <img src="/assets/popart.jpg">
        <figcaption>Pop Art by chance</figcaption>
    </figure>
</center>

This raises the question about how to securely delete files.

There are many options, but the tool I find myself using is [srm](https://en.wikipedia.org/wiki/Srm_(Unix)) as it's a drop-in replacement for `rm`. Uses `/dev/urandom` to overwrite clustes:
``` bash
$ srm -r ~/Projects/private_stuff
```

And finally, remember these two golden rules:
- Never sell or give away your old SD cards, destroy them.
- For some fun, buy used SD cards off of eBay ;-)
