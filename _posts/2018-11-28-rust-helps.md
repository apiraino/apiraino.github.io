---
layout: post
title: Rust compiler friendliness #1
---

``` bash
$ cargo_check
    Checking open-taffeta v0.1.0 (/home/.../open-taffeta)
error: can't qualify macro_rules invocation with `pub`
 --> src/config.rs:8:1
  |
8 | pub macro_rules! get_token_duration {
  | ^^^ help: try exporting the macro: `#[macro_export]`

```

```
/me wonders how to make this macro public
RC: Look buddy, I know you're too lazy to check the documentation ...
me: Oh ... thanks XD
```
