---
layout: post
title: "Appreciation for software #5: i3 window manager"
---

If there a piece of software that screams **NEEERRRRRD** is definitively the [i3 window manager](https://i3wm.org).

Months ago I was using a vanilla Ubuntu with Gnome. Nothing to really complain about that, but I wanted something more snappy and that could solve the problem of having layers of overlapping windows, sometimes forcing me to some "long sessions" of alt-tabbing to find the lost shell, which is very distracting when you're deeply concentrated.

A friend of mine was proudly showing me his i3 setup, telling me all the advantages of a tiling window manager. Then I saw this weird window manager consistently  in hackerspaces, hackatons and all things starting with "hack-" so I had to try it because there could be a serious boost in productivity.

After many months of test, I can finally say that I find myself at home with `i3`. It's *fast*, stable, well documented, flexible to an exent I couldn't believe possible, features are added very carefully. The reason is: if `i3` doesn't do it, write a script and a keybinding. Moreover there is a big community of aficionados that wrote scripts for everything, therefore you have a good start on how to solve the most common needs (ex. volume up and down).

It has a very cool logo.

It loads in a snap, the config file makes sense and it's very simple yet dense of information; I can apply configuration changes in the blink of an eye, I can have for all practical purposes an infinite amount of keyboard shortcuts and recently I've finally learned how to restore windows in their workspaces. So at startup I always load automatically my setup without manually placing windows.

With `i3` you can effectively detach the mouse and disable the touchpad, they're really not needed :-) although I'm not that hardcore (so I still use it, but it's my choice).

A concession that `i3` graciously grant to the user is the possibility to have floating windows (ahh evil!) when it makes sense: example for applications that simply start and stay minimized in the tray-icon (for example I have the NextCloud sync agent, it would be a waste of desktop real estate).

Using `i3` also means giving up to some comforts, which I am not yet ready, therefore I still have half-Gnome under the seat for some utilities that are not easily replaced by a non-Gnome one, example:

- I like Gnome Shell
- The bluetooth agent (`blueman-applet`), limited but does the job
- The network manager applet (`nm-applet`), small, complete and it simply works
- Sometimes I use `gnome-text-editor` :^)

The second disadvantage of using a tiling window manager is that applications born to be used with floating windows a little uncomfortable (es. Gimp) or sometimes I see weird things when stupid websites open a popup for PayPal payment.

The natural complement of `i3` is [py3status](https://github.com/ultrabug/py3status), a python tool to manage the status bar (because `i3` itself has a little too barebone management of that). Like `i3` itself it's completely programmable through plugins, it's well documented, has a great API and comes with a ton of scripts from the community. Using `i3` with `py3status` is like heaven for those that want to customize things to the detail. And it's incredibly fun, it's like playing with Lego!

Another tool that I find very useful is [dmenu](https://tools.suckless.org/dmenu/), a tool to directly start applications (think of using Spotlight on OSX). It replaces the application start menu of a usual window manager.

Mandatory screenshot of my boring desktop: minimal, clean and with a touch of gory, desperate sadness.

<figure>
    <img src="/assets/desktop.png">
    <figcaption>That gradient</figcaption>
</figure>

You'll find around much nicer dekstops that are really beautiful. And they're so different one from the another that you wonder if you are looking at the same window manager. That's the power of `i3`!
