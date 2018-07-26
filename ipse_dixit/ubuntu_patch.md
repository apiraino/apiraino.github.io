<< [go back](https://apiraino.github.io)

# On submitting a patch for an Ubuntu package

I had the chance to peep into how an Ubuntu package is cooked and submitted: the procedure is clearly described in clear, detailed steps on the Ubuntu wiki, so this is just a summary for my own reference: I'll give a lot of details for granted.

First of all you need a Launchpad account, with your SSH public and GPG key:

[http://packaging.ubuntu.com/html/getting-set-up.html](http://packaging.ubuntu.com/html/getting-set-up.html)

Then you need to setup your workstation for building packages and various tooling for patching package sources:

[http://packaging.ubuntu.com/html/fixing-a-bug.html](http://packaging.ubuntu.com/html/fixing-a-bug.html)

I don't like to add a lot of random packages to my workstation, so I wrote down all the packages I had to install in order to replicate the environment in a virtual machine or (as Ubuntu suggests) an [LXD container](https://help.ubuntu.com/lts/serverguide/lxd.html) - although I'll have to investigate if it can run GUI applications.

Now, I discovered there are two ways to patch the sources of a package. One involves using [edit-patch (1)](https://manpages.debian.org/stretch/devscripts/edit-patch.1.en.html), as described in the previous link, the other revolves around [quilt (1)](https://manpages.debian.org/stretch/quilt/quilt.1.en.html), a nice tool that Andrew Morton wrote for his own purpose of maintaining patches to the Linux kernel (the _-mm_ branch). Usage is detailed here:

[https://raphaelhertzog.com/2012/08/08/how-to-use-quilt-to-manage-patches-in-debian-packages](https://raphaelhertzog.com/2012/08/08/how-to-use-quilt-to-manage-patches-in-debian-packages)

`edit-patch` is easier to use, but if you feel like playing with `quilt` it'll only take 5 minutes to get acquainted. So, basically the procedure consists in:

1. ensure to have `deb-src` packages activated in your `sources.list`, then run `apt update`
2. create a patch containing all the changes that you want applied to the package (e.g. `git diff > patch.diff`)
3. create a work directory somewhere and `cd` into it
4. get the sources for the package you want to update: `pull-lp-sources <ubuntu_release> <package_name>`
5. descent into the source directory and either use `edit-patch` or `quilt` to create and apply the patch you create before
6. sign-off the patch and fill up some paperwork (changelog and other stuff)
7. locally build the package, install it and test if it works
8. submit your patch on Launchpad, attaching it to a bug. Await comments from the mantainers.

For any question or doubt, support is available on irc.freenode.net on `#ubuntu-motu` or `ubuntu-motu@lists.ubuntu.com`.

<< [go back](https://apiraino.github.io)
