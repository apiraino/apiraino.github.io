<< [go back](/)

## On enabling power suspend with an external monitor attached on Ubuntu

### Part I: setting the basic suspend

You can access the power management from the Gnome settings and set the computer to suspend after a delay (both on battery and on AC).

<figure>
    <img src="/images/gnome_suspend.png">
    <figcaption>Gnome settings for the suspend behaviour</figcaption>
</figure>

Set them to your preference and now the laptop should always suspend after the delay you've set.

One more thing: there's a separate setting to configure the "close lid" action.

Once, it was right with the Power settings, but at some point it has been removed.

<figure>
    <img src="/images/gpm-prefs.png">
    <figcaption>OLD and NEW Gnome power settings</figcaption>
</figure>

Oh wait, it was not removed. Just moved to a place that only the [Tweak companion utility](https://wiki.gnome.org/Apps/Tweaks) can reach:

<figure>
    <img src="/images/gnome-tweaks-power.png">
    <figcaption>What. The. Actual. Fuck.</figcaption>
</figure>

As a side note, I've discovered in the [ArchLinux wiki](https://wiki.archlinux.org/index.php/GNOME#Configure_behaviour_on_lid_switch_close) that this setting, when set to _false_, creates this file:

`~/.config/autostart/ignore-lid-switch-tweak.desktop`

a "drop-in" configuration file that will trigger the Gnome Tweaks _inhibitor_. Just wow.

### Part II: the external monitor

I soon realize that this is just partially what I need: I have an external monitor attached and this seems to be a completely different can of worms.

The external monitor is blocking the suspend feature. Well, one can argue that it makes sense: you might want to attach an external keyboard+monitor to a laptop, close the lid, put it away in a corner and keep on working.

On the other hand, I'd like the laptop to always suspend immediately when I close the lid, with or without an external monitor attached.

After some research, I discover a hidden Gnome setting: `lid-close-suspend-with-external-monitor`.

Why is it hidden? There's no explicit flag for this on Gnome settings (or Gnome Tweaks).

This setting can be changed using `dconf-editor` (`apt install dconf-editor`):
``` bash
$ dconf-editor org.gnome.settings-daemon.plugins.power
```
Then look up `lid-close-suspend-with-external-monitor`, its default is *false*. Set it to *true*.

So, not only this setting if not actionable in a "user-friendly" way, not even using Gnome Tweaks, but also it looks to be undocumented. I've found a reference on a [Ubuntu Mate forum](https://ubuntu-mate.community/t/not-sleep-laptop-when-external-display-is-connected/16921) after throwing some random keywords at DuckDuckGo. And only after - now I knew what to look for - I've found it referenced in other places too. I was not able to find a reference in any Gnome documentation. And, in my opinion, this is not good.

While the majority of people were complaining that their laptop suspended when they closed the lid, this is exactly the behaviour I was looking for, se let's set `lid-close-suspend-with-external-monitor` to _false_.

It doesn't work.

If I unplug the monitor or explicity request to suspend, it suspend-on-lid-closing works. With the external monitor attached, no way. \*sigh\*.

Let's apply some more DDG-fu. Uhm ... more people complaining about this. I also see floating keywords such as _systemd_, _nvidia_, _bugs_ ... \*groan\*, I should have seen this coming.

[This answer on askubuntu.com](https://askubuntu.com/questions/613693/15-04-15-10-16-04-closing-lid-does-not-suspend-laptop-if-connected-to-extern/613773#613773) suggests a problem with the nVidia chipset (ah-ah, so [Linus was right?](https://www.youtube.com/watch?v=JbovJbKALzA)). That was in 2015, will they have fixed by now? I disable the nVidia chipset altogether with `nvidia-settings` and switch to the FOSS _nouveau_ driver from Ubuntu "Software & Update".

No luck.

### Part III: following _systemd_ bloody trail

[Here](https://github.com/systemd/systemd/issues/7137) there's a thorough bug report that teaches me how to edit the `logind` configuration, followed by a convoluted explaination by Poettering on why systemd's behaviour is correct and passes the buck to the Gnome folks. At least I see that in my laptop something's blocking the `handle-lid-switch` action. I only need to get rid of those "block"s.

Following [this](https://bugs.freedesktop.org/show_bug.cgi?id=76267) and [this]() systemd issues, I decide to bite the bullet and dive into the _systemd_ configuration and `logind.conf` documentation (`man 5 logind.conf`), changing the following:
``` bash
HandleLidSwitch=suspend
HandleLidSwitchDocked=suspend
LidSwitchIgnoreInhibited=no
```
Restart systemd _logind_ service with `sudo systemctl restart systemd-logind`.

Nope.

What's the problem with systemd not honouring the `LidSwitchIgnoreInhibited` setting?

According to this [ArchLinux forum thread](https://bbs.archlinux.org/viewtopic.php?pid=1735292#p1735292) there's a Gnome bug that inhibits the suspend on lid closing. I'm not commenting further that thread.

Next hint retrieved from another [issue](https://bugzilla.redhat.com/show_bug.cgi?id=1517967#c4), this time on Fedora: apparently there's a patch for this! I'm getting closer, I can feel it.

Unfortunately that thread says that the patch didn't make it to Bionic Beaver, *BUT* a [workaround](https://bugzilla.gnome.org/show_bug.cgi?id=788915#c10) disables all lid management done by Gnome:
``` bash
Edit /etc/UPower/UPower.conf
Change the setting
IgnoreLid=false to IgnoreLid=true
```

YES, it worked!

### Part IV: final thoughts

I can only be thankful to the generosity of the collective mind, a whole lot of people, whom each bit of hint allowed to move me an inch forward to the solution, allowing me to understand and (possibly fix) the issue at hand.

Complex projects not talking to each other, bad design decisions, then reverted, half-assed documentation. Volunteers doing what they can to help, sometimes doing what they want. This year will _never_ be the year of Linux, until stuff like that persists.


<< [go back](/)
