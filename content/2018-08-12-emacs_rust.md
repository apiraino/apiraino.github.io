+++
template = "post.html"
title = "EMACS Rust linter suddenly chocking"
+++

### <a name="part_i"></a>Part I: a little surprise

I'd spend a fair amount of time to [setup EMACS for Rust development](https://github.com/apiraino/emacs_reference/blob/master/guide.md#rust-specific-setup).

All of a sudden, I've recently realized I could not run `cargo build` easily anymore, I often had this message:
``` bash
$ cargo build
    Blocking waiting for file lock on build directory
```
and there I had to wait for long (like, a full minute!).

Ooook, let's spend some quality-time debugging **\*groan***

So, where do we start? The message, of course. [Here](https://github.com/rust-lang/rust-mode/issues/181#issuecomment-319161568) I see someone is experiencing the same symptoms with another setup. The message _lingo_ basically says there are concurrent tasks attempting to compile sources. Uhm ... and who is the other ghost compiling process?

I'll start doing some tests randomly saving a buffer in EMACS after or before a fresh build. After a while I see that simply opening a file in a buffer is triggering a chain reaction of `cargo test` processes:
``` bash
/home/me/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/bin/cargo test --no-run --bin my_rust_project --message-format=json
/home/me/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/bin/cargo test --no-run --lib --message-format=json
```

What in the world is triggering a **tests** run!?

### <a name="part_ii"></a>Part II: the facepalm

I comment out all my [customization to EMACS](https://github.com/apiraino/emacs_reference/blob/master/.emacs.d/personal/jman.el) and run on bare [Prelude](https://github.com/bbatsov/prelude).

Still tests running when I open a file.

Damn, ok let's patiently comment all the Prelude modules and see which one is triggering this. Turns out that *any* modules I have enabled triggers this behaviour, so there must be a common module above all.

Fast-forward: the culprit is the `prelude-programming` module, namely this piece of code:
``` elisp
(if (fboundp 'global-flycheck-mode)
    (global-flycheck-mode +1)
  (add-hook 'prog-mode-hook 'flycheck-mode))
```
What does Flycheck know about Rust? A syntax checker that triggers tests? **\*sigh***

So after some more research, I see that Flycheck *does* know Jack [about Rust](http://www.flycheck.org/en/latest/languages.html#rust) and in a way I didn't expect: a `flycheck-rust-check-tests` config parameter.

This parameter has been added [many moons ago](https://github.com/flycheck/flycheck/blob/7a7a358b6232cff6a2f0f80f8c8b314e505b8c56/CHANGES.old#L376) (in 2014) when the project was not even on GitHub so I don't have a diff or an issue to refer to. Let's have a look at the [`flycheck.el`](https://github.com/flycheck/flycheck/blob/master/flycheck.el#L9477) elisp code:
``` elisp
(flycheck-def-option-var flycheck-rust-check-tests t (rust-cargo rust)
  "Whether to check test code in Rust.

For the `rust' checker: When non-nil, `rustc' is passed the
`--test' flag, which will check any code marked with the
`#[cfg(test)]' attribute and any functions marked with
`#[test]'. Otherwise, `rustc' is not passed `--test' and test
code will not be checked.  Skipping `--test' is necessary when
using `#![no_std]', because compiling the test runner requires
`std'.

For the `rust-cargo' checker: When non-nil, calls `cargo test
--no-run' instead of `cargo check'."
  :type 'boolean
  :safe #'booleanp
  :package-version '("flycheck" . "0.19"))
```

If `flycheck-rust-check-tests` is set to `nil` *and* `cargo` is installed, flycheck will execute `cargo test --no-run` instead of `cargo check`. Let's do this and add a line to the Rust prelude module (`prelude-rust.el`) trying to mute that parameter:
``` elisp
(setq flycheck-rust-check-tests nil)
```
and ... the `cargo test` little devils are not spawned anymore.

### <a name="part_iii"></a>Part III: the unanswered questions

The saying goes that if you reproduce a bug, you're halfway to its resolution. I'll add that fixing the bug takes you to a 90%; but only understanding the cause of a behaviour unlocks the real 100% achievement.

So what triggered such a `cargo test` frenzy? Has it ever always been there, just unnoticed?

The most likely answer is that Flycheck run `cargo test` and I manually run `cargo build` from the command line. Each of these two commands invalidates the compiled cache, so what happened is something like this:
- Open file in buffer (`cargo test` triggered, slow run unnoticed)
- code-code-code
- Save buffer (`cargo test` triggered: fast run)
- from CLI run `cargo build` to run my application (slow run)
- _/me wtf?!_

and then:
- code-code-code
- Save buffer (`cargo test` triggered: slow run unnoticed)
- from CLI run `cargo build` (message warning about concurrent build)
- _/me wtf?!_ again

Running several times in a row only *one* of these two commands doesn't invalidate the build cache, so the issue doesn't happen.

Setting to `nil` that variable made Flycheck switch from `cargo test` to `cargo check` to get errors produced the following benefits:
* `cargo check` is the recommended way to get [compilation warning/errors](https://github.com/flycheck/flycheck/pull/1289) and in some scenario should [speed things up](https://blog.rust-lang.org/2017/03/16/Rust-1.16.html)
* informed me to not run `cargo build` unless I really need to
* does not run `cargo test` to get syntax/lint errors, which was awkard and confusing in the first place
* *BUG*: there's an old outstanding bug, due to `cargo check` metadata caching: on _--lib_ cargo projects (not _--bin_) it only shows compiler warnings _once_ after a rebuild, see [issue](https://github.com/rust-lang/cargo/issues/3624)

Flycheck command before:

    cargo test --no-run --lib --message-format=json

and after:

    cargo check --lib --message-format=json

Finally, let's ensure this won't happen again - let's save this in my custom EMACS config:

    M-x flycheck-rust-check-tests

set the value to `nil`, then save to `~/.emacs.d/personal/custom.el`. This improve upon the previous solution as now I don't need to customize `prelude-rust.el` anymore.

Second step, disable `rust` from the list of checkers:

    M-x flycheck-disabled-checkers

Now, my `custom.el` has two new configs:
``` elisp
 '(flycheck-disabled-checkers (quote (rust)))
 '(flycheck-rust-check-tests nil)
```

Closing thoughts: an outstanding issue in the Rust world is how to speed compiling times up, but that's nothing we can do here, eventually we will get there.

Oh, one last comment: I hate elisp so much that I find a perverse pleasure in understanding how it works.
