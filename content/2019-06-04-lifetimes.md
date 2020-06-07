+++
template = "post.html"
title = "Lifetimes and strings in Rust"
+++

Today I've finally cleared a couple of basic concepts about `&str` (string slice) and `String` (string) in Rust. Let's very briefly recap.

Let's see the following code snippet:

``` rust
fn get_str<'a>() -> &'a str {
    let s = String::from("ok");
    &s.to_owned()
}

fn main() {
    println!("{}", get_str());
}
```

This won't compile:
```bash
error[E0515]: cannot return reference to temporary value
 --> src/main.rs:3:5
  |
3 |     &s.to_owned()
  |     ^------------
  |     ||
  |     |temporary value created here
  |     returns a reference to data owned by the current function
```

and here is why. When we run the application we need to consider how the stack memory works:

1. we are in the `main` body
2. we invoke `get_str()`
3. The function `get_str()` is allocated on the stack
4. When we return from `get_str()` the stack will be freed and everything allocated inside will be destroyed

Rust will block you and here's why it won't even compile! It's warning you ("a reference to data owned by the current function") that it won't allow you to return a pointer (`&str`) to a deallocated memory location.

Inside `get_str()` we are allocating a new chunk of memory on the stack. This memory location cannot be referenced outside of `get_str()`, once we return.

The only solution to this is to fix as follows:

``` rust
fn get_str() -> String {
    let s = String::from("ok");
    s
}

fn main() {
    println!("{}", get_str());
}
```

So, as a rule of thumb it's always better to use `&str` when passing strings around, if the content is meant to be read-only, it's equivalent to doing:

``` c
char *ptr = malloc(10);
ptr[0] = '\0';
```

But be careful when you're returning a `&str` allocated inside a function. That won't be allowed.

Unless you bind that `&str` to a parameter lifetime: you explicit the fact that the `&str` the function receives, will outlive the function:
``` rust
fn get_str<'a>(mut s: &'a str) -> &'a str {
    println!("{}", s);
    s = "new value";
    &s
}

fn main() {
    println!("{}", get_str("old value"));
}
```

This will print:
```
$ ./target/debug/test
old value
new value
```

The `&str` is allocated outside the function and even though it's modified inside it, we're allowed to return the pointer; or simply use the `String` object (like said before).
