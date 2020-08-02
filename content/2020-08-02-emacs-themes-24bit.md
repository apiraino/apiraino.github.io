+++
template = "post.html"
title = "Enabling Emacs 24bit themes"
[extra]
gist_id = 95d7c232d96a43e38ee996935b44d37d
+++

This weekend I've spent some time on [`/r/unixporn`](https://old.reddit.com/r/unixporn/) and enjoyed their beautiful desktop customizations. The next things I know is that I've ended up into another hell-hole to enable one theme on my Emacs. Let's see how deep the rabbit hole goes and summarize the keypoints learned.

### Preface: Linux shells suck

Mr. Obvious, I suppose?

There is a crowd of lost souls out there trying to figure out and explain in which order the linux shell loads configuration files, because the most common answer is: "it depends". It's one of the classic UNIX stratified crust dating back to (I guess) ~20 (30?) years ago and always kept back compatible. Anyway, done with the complaints, let's move on.

Looking back, these were the steps I went through to reach the goal:

1) Why Emacs screws up theme colors
2) Because it's a 24bit colors theme: how do I have Emacs support such themes?
3) It depends on the shell: what shell do I have and why it doesn't behave the way I want
4) The shell doesn't know how to manage more than 256 colors: how do I fix this?
5) I have the fix: how to apply it in a consistent way?

In one sentence: on a Linux shell, you need to customize `terminfo` to have Emacs display more than 256 colors.

Each damn step took its own good deal of research, trial and error, let's go through each one.

### 1) Why Emacs screws up theme colors

Many Emacs themes (especially the most beautiful) have more than 256 colors. In my narrow-minded view, never could I imagine that so many colors could be needed.

Installed the theme, run Emacs, I get *slightly* disappointed, the product does not match the label on the tin.

<figure>
    <img src="/images/emacs-theme-00.png">
    <figcaption>Comparing what I see to what I am *supposed* to see</figcaption>
</figure>


### 2) How do I have Emacs display more colors?

Emacs support 24bit colors since 26.x. I notice that "graphical" Emacs (`emacs-gtk` and `emacs-lucid`, compiled against X11 and more libraries) behave differently. They bring a set of dependencies and eLisp functions to check for graphical capabilities. Now I understand why I don't have any of those. I've always used `emacs-nox`, the version without dependencies, [without even realizing the limitations](https://emacs.stackexchange.com/a/45564).

Running `emacs -nw` (no window) shows the same behaviour as using `emacs-nox`, so I can test capabilities both on the "enhanced" emacs version and the barebone one.

All good, then? Nope. It's not a problem of emacs, rather of the shell I'm sitting on.

### 3) What shell do I have and why it doesn't behave the way I want

Let's first check the terminal capabilities:

```
$ echo $TERM
xterm-256color
```

but

```
$ echo $COLORTERM
truecolor
```

[This Github gist details 24bit support](https://gist.github.com/XVilka/8346728) in many shells: it's very likely that a modern shell supports 24bit colors.

So how do I do that?

### 4) Have more color on the Linux shell

In order to have 24bit colors, you need to first instruct the shell to use such a palette, being the standard 256 colors (or worse, if you're out of luck). This is done by generating a new `terminfo` file (a database describing terminals).

You can verify this with one of the many scripts around, example [this](https://askubuntu.com/questions/821157/print-a-256-color-test-pattern-in-the-terminal).

This procedure is detailed on [GNU's emacs faq](https://www.gnu.org/software/emacs/manual/html_node/efaq/Colors-on-a-TTY.html) and it takes 10 seconds.

Let's generate the 24bit `terminfo` file:

```
$ tic -x -o ~/.terminfo terminfo-24bit.src

# or better, a XDG basedir compliant path:
$ export TERMINFO=$XDG_CONFIG_HOME/terminfo
$ tic -x -o $TERMINFO terminfo-24bit.src
```

and tell our shell to use more colors:

```
$ export TERM=xterm-24bit
```

Now let's run emacs and compare the colors available with `M-x list-colors-display` with the new env var enabled.

<figure>
    <img src="/images/emacs-theme-03.png">
    <figcaption>The number of colors is doubled!</figcaption>
</figure>

Interesting fact: even on a 24bit enabled shell, Emacs only has ~550 colors instead of ~256: this is something curious I didn't figure out.

As always, the funny thing is that once you identify exactly the problem, there is always a place where you could find the correct solution, [this blog post](http://www.skybert.net/emacs/colourful-tty-emacs) for example - provided you could formulate the right question.

### 5) Persist this configuration

I throw the new env vars in `~/.profile` so after the next login I will have everything set.

Nope.

When I open a new terminal (I use Gnome Terminal) from X11 or Wayland I don't see my $TERM applied and I am back to 256 colors. Terminal (non graphical) shells are fine.

More digging. And here I've learned the exact [differences between shells](https://unix.stackexchange.com/questions/170493/login-non-login-and-interactive-non-interactive-shells): login, non-login, interactive and non-interactive.

Turns out that Gnome Terminal is the "culprit". By default it doesn't open a login shell (which makes sense) but that means that it **overwrites** your `~/.profile` with something else (which is not ok).

I can say "overwrite" by placing `echo` statements all along the login process and save a log file:

```
-- Loading /etc/profile [start]: $TERM=dumb
-- Loading /etc/profile [end]: $TERM=dumb
-- Loading ~/.profile [start]: $TERM=dumb
-- Loading ~/.profile [end]: $TERM=xterm-24bit
-- Loading ~/.bashrc: $TERM=xterm-256color          # <-- WHAT THE HELL?!
user@localhost:~$
```

`printf` debugging never disappoints.

You have two choices: create `~/.bash_profile` or tell Gnome Terminal to behave like a login shell which will force reading the `./profile` file. I choose the second option because I don't want another confusing file lingering around.

Now all settings will survive a reboot.
