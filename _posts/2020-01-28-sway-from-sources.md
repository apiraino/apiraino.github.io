---
layout: post
title: "Build wlroots + Sway + accessories"
gist_id: 6657af11d059591410fb97ed5f39fddf
---

Like I mentioned [in my previous article](/2020/01/13/wayland.html#part_3) installing some Sway accessories can lead to frustration because package maintainers are behind the tarball releases. This is perfectly fine when these projects move fast, but it can lead to bogus issue reports and being told to "just update to the latest version", when the latest version is not yet available for your Linux distribution.

So I decided to build from scratch everything starting from `wlroots` (the compositor) up to Sway and friends in order to be free to update without having to wait for a packaged release.

### <a id="part_1" href="#part_1" class="header-anchor">#</a> Blurb about failed attempts blah blah my life sucks blah blah

First I tried the [build service from openSUSE](https://build.opensuse.org); after a signup process that smells like year 2003, I tried to find a project that targeted Debian packages so I could copy and paste stuff. I could not figure out the documentation to write a `.spec` file so I gave up out of frustration. But I'll be back.

Next I tried writing my [Docker container](https://gist.github.com/apiraino/262dc499ceeed7003bf83b6ecd9c9591) but I couldn't get from the tarballs to a .deb package.

Then I've found [this neat project](https://github.com/tsaarni/docker-deb-builder), a script that runs a Docker container that builds .deb packages without installing on the host all the tooling. There are other projects doing the same thing, example [this one](https://github.com/resnullius/deb-build-pkg) (didn't test it, though). But how the hell one build a Debian package? I'm too lazy to read the fine material and HOWTOs. I want to hack on something already done by someone else.

Finally, I saw the light, a friend of mine pointed me to [https://salsa.debian.org/swaywm-team](https://salsa.debian.org/swaywm-team), experimental repositories to build Sway packages for Debian unstable. Let's go!

The workflow now looks like:

- git checkout from github the \<application\> sources
- git checkout from salsa.debian.org the whole `/debian` directory for \<application\>, save it into the sources directory
- run the Docker container
- pray

### <a id="part_2" href="#part_2" class="header-anchor">#</a> Building the accessory packages

For every Sway accessory package run the container with:

```
$ ./build -i docker-deb-builder:19.10 -o <output-package-dir> <src-dir>
```

For Waybar need I needed to hack the `debian/control` file and force an older version of `libfmt-dev` for Ubuntu 19.10:

``` diff
-libfmt-dev (>=5.3.0),
+libfmt-dev (>=5.2.1),
```

### <a id="part_3" href="#part_3" class="header-anchor">#</a> Packaging sway and wlroots library

First make the packages for wlroots and ensure the final results is similar to this (assuming a tagged release for v0.10.0):

- libwlroots-dev_0.10.0-1_amd64.deb
- libwlroots-examples_0.10.0-1_amd64.deb
- libwlroots5_0.10.0-1_amd64.deb

Compiling Sway it's even more fun, we need to hack some files to get our package build to succeed. This can be probably fixed in some way.

- `debian/changelog`: add these lines to get a package name with the right version (in my case v1.4)

``` diff
sway (1.4-1) experimental; urgency=medium

  * Hacking my way to a 1.4 packaged version
```

- `meson_options.txt`: exclude `fish` and `zsh` completion files (for some reason they break the build)

``` diff
-option('zsh-completions', type: 'boolean', value: true, description: 'Install zsh shell completions.')
+option('zsh-completions', type: 'boolean', value: false, description: 'Install zsh shell completions.')
-option('fish-completions', type: 'boolean', value: true, description: 'Install fish shell completions.')
+option('fish-completions', type: 'boolean', value: false, description: 'Install fish shell completions.')
```

- `debian/sway.install`: remove the completions files

``` diff
$ diff debian/sway.install debian/sway.install.orig
3a4
> usr/share/fish/vendor_completions.d/sway*
8c9
<
---
> usr/share/zsh/vendor-completions/_sway*
```

Now start the Docker container and get inside it, we need to update the container with updated wlroots packages.

``` bash
docker run --rm -it \
    -v /home/$USER/sway-1.4.0/sway:/source-ro:ro \
    -v /home/$USER/docker-deb-builder/output:/output \
    -v /home/$USER/docker-deb-builder/build-helper.sh:/build-helper.sh:ro \
    -e USER=1000 -e GROUP=1000 \
    --rm docker-deb-builder:19.10
```

Now we will install the three previously created `wlroots` packages. They will need a lot of dependencies, yeah install them all, we're in a container, who cares:

``` bash
# this command will fail ...
root:~/# dpkg -i /output/libwlroots*

# ... but it will give us a list of needed packages
# that we install now
root:~/# apt install -f -y

# try again, it will work
root:~/# dpkg -i /output/libwlroots*

# now we have vandalized this Ubuntu instance.
# we can compile sway:
root:~/# ./build-helper.sh
```

and if it's your lucky day you will have something like this in your output directory:

``` bash
user@localhost:~/docker-deb-builder$ la output/
total 5556
-rw-r--r-- 1 user user  209676 Jan 28 23:33 libwlroots5_0.10.0-1_amd64.deb
-rw-r--r-- 1 user user   47568 Jan 28 23:33 libwlroots-dev_0.10.0-1_amd64.deb
-rw-r--r-- 1 user user   67700 Jan 28 23:33 libwlroots-examples_0.10.0-1_amd64.deb
-rw-r--r-- 1 user user  236800 Jan 29 14:20 sway_1.4-1_amd64.deb
-rw-r--r-- 1 user user 4820980 Jan 29 14:20 sway-backgrounds_1.4-1_all.deb
-rw-r--r-- 1 user user   13600 Jan 28 18:08 swaybg_1.0-2_amd64.deb
-rw-r--r-- 1 user user  278680 Jan 28 23:14 waybar_0.9.0-1_amd64.deb
```
You'll notice that I've have packaged:

- wlroots 0.1.0
- sway 1.4
- swaybg 1.0.2
- waybar 0.9.0

Install them all in your Ubuntu host and you're done.
