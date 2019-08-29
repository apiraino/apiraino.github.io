---
layout: post
title: Writing Rust Futures in 2019
---

Some examples of Futures I wish I'd found before (or wasn't able to find). These examples are almost just copy and paste from various places, so the resources are there, I just needed to figure out the bigger picture.

All examples use the [Tokio runtime](https://tokio.rs).

All examples use the [futures crate](https://crates.io/crates/futures) v0.1.2x.

Code is available on [Github](https://github.com/apiraino/rust-future-explorations).

Update: the part about Hyper has been moved [to its own article](/2019/07/18/hyper.html).

## <a id="part_i"></a>Brief prologue: what is a Future

A Future is simply a plain Rust function which return type is a `Future`. I won't go in detail of what a Future is, others can explain that better than me. The standard return type is as follows:

``` rust
fn something() -> impl Future<Item = (), Error = ()>
    // do something...
}
```

That reads as: return a `Future` which contains an `Item` or an `Error`.

`Item` can also be an integer:

``` rust
fn something() -> impl Future<Item = i32, Error = ()>
    // do something...
}
```

Or the `Error` can be something more useful:

``` rust
fn something() -> impl Future<Item = i32, Error = String>
    // do something...
}
```

or a custom type:

``` rust
struct MyStruct {
    name: String,
    age: i32
}

fn something() -> impl Future<Item = MyStruct, Error = ()> {
    // do something...
}
```

Now let's see some basic examples. We'll be just scratching the surface of what can be accomplished with Futures.

## <a id="first-future"></a> Your first Future

``` rust
fn my_fut() -> impl Future<Item = (), Error = ()> {
    println!("running my_fut");
    future::ok(())
}

fn main() {
    // the Future returns a unit
    tokio::run(my_fut());
}
```

Console output is:
``` bash
$ cargo run
running my_fut
```

## <a id="simple-future"></a>A Future that returns an integer

``` rust
fn my_fut() -> impl Future<Item = i32, Error = ()> {
    println!("running my_fut");
    future::ok(42)
}

fn main() {

    // run the Future, forget about it
    tokio::run(my_fut());

    // run the future, inspect the return value
    let f = my_fut().map(|x| {
        println!("future resolved: {}", x);
        ()
    });
    tokio::run(f);
}
```

Console output is:
``` bash
$ cargo run
running my_fut
future resolved: 42
```

## <a id="sleeping-future"></a>A Future that sleeps for 1 second

``` rust
fn svc_wait(t: u64) -> impl Future<Item = (), Error = ()> {
    println!("[start] waiting...");
    let when = Instant::now() + Duration::from_millis(t);
    Delay::new(when)
        .map_err(|e| panic!("timer failed; err={:?}", e))
        .and_then(|_| {
            println!("[end] waiting");
            Ok(())
        })
}

fn main() {
    // Future returns a ()
    let f = svc_wait(1000).map(|_| {
        println!("future finished");
        ()
    });
    tokio::run(f);
}
```

The console output will be:
``` bash
[start] waiting...
... 1 sec ...
[end] waiting
future finished
```

It's important to note that if you want to simulate a long-lasting async task you should *not* use `std::thread::sleep`, you'll end up blocking the whole Tokio runtime thread!

## <a id="future-poll"></a>(TODO) Manually implementing a Future

Futures are cool because you "fire&forget" them. But what if we want to track their progress?

We need to manually implement the `.poll()` to be able to observe the various stages.

I still have to figure out how this stuff work.

Here's some code pasted from elsewhere.

``` rust
impl Future for Magazine {
    // here we return a single byte
    type Item = u8;
    type Error = io::Error;

    // this method is getting called from the runtime. Everytime we can read
    // a byte into the buffer, we return `Async::Ready`
    fn poll(&mut self) -> Poll<Self::Item, Self::Error> {
        let mut buffer = [0;1];
        match self.0.poll_read(&mut buf) {
            Ok(Async::Ready(_num_bytes_read)) => Ok(Async::Ready(buffer[0])),
            Ok(Async::NotReady) => Ok(Async::NotReady),
            Err(e) => Err(e)
        }
    }
}
```


``` rust
struct AwakeFuture {
    name: String,
    count: i32,
}

impl AwakeFuture {
    fn new(name: String) -> AwakeFuture {
        AwakeFuture { name, count: 0 }
    }
}

impl Future for AwakeFuture {
    type Item = i32;
    type Error = ();

    fn poll(&mut self) -> Poll<Self::Item, Self::Error> {
        match self.count {
            3 => {
                eprintln!(
                    "[{}] Future {} has finished counting",
                    self.count, self.name
                );
                Ok(Async::Ready(self.count))
            }
            _ => {
                eprintln!("[{}] Future {} is not yet ready ...", self.count, self.name);
                // FIXME: I'm afraid this won't ever work
                self.count += 1;
                Ok(Async::NotReady)
            }
        }
    }
}

fn main() {
    let awake_future = AwakeFuture::new(String::from("awake-future"));
    tokio::run(awake_future.map(|x| {
        eprint!("x={:?}", x);
        ()
    }));
}
```

## <a id="future-poll"></a>One more thing: running more Futures together

[https://github.com/chicagohaskell/async-futures-talk/blob/master/rustlb/examples/multi-http/src/main.rs](https://github.com/chicagohaskell/async-futures-talk/blob/master/rustlb/examples/multi-http/src/main.rs)

# Credits

Thanks to my friends of [Rust Rome](https://rustrome.github.io) for the incredbile support and for answering all my questions.

Thanks to [Bastian Gruber](https://github.com/gruberb) for his wonderful tutorials: namely [this](https://dev.to/gruberb/explained-rust-futures-for-web-development-a10) and [this](https://dev.to/gruberb/explained-rust-futures-for-web-development-a10).

And don't forget [the Hyper examples](https://github.com/hyperium/hyper/blob/master/examples).
