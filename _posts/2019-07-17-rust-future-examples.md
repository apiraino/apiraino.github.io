---
layout: post
title: Writing Rust Futures in 2019
---

Some examples of Futures I wish I'd found before (or wasn't able to find). These examples are almost just copy and paste from various places, so the resources are there, I just needed to figure out the bigger picture.

All examples use the [Tokio runtime](https://tokio.rs).

Code is available on [Github](https://github.com/apiraino).

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

## <a id="hyper-basic"></a>Introducing Hyper 0.12

Hyper is a high-performance HTTP async server and client that sits on the Tokio runtime and Future crate.

The server listens for incoming connections and returns a string.

``` rust
// Notice we are using the future crate re-exported from hyper
// use futures::future;
use hyper::rt::Future;

use hyper::service::service_fn_ok;
use hyper::{Body, Request, Response, Server};

fn main() {
    println!("Start");

    let addr = ([127, 0, 0, 1], 3000).into();
    let server = Server::bind(&addr)
        .serve(|| {
            // This is the `Service` that will handle the connection.
            // `service_fn_ok` is a helper to convert a function that
            // returns a Response into a `Service`.
            service_fn_ok(move |_: Request<Body>| Response::new(Body::from("Hello World!\n")))
        })
        .map_err(|e| eprintln!("server error: {}", e));

    // runs on tokio runtime
    println!("Listening on http://{}", addr);
    hyper::rt::run(server);

    println!("Exiting");
}
```

## <a id="hyper-spawn"></a>Hyper spawns a Future

The server listens for incoming connections and spawns the "sleep" Future seen before.

Notice how che client connection is closed immediately and the Future is resolved at a later stage

Do *not* use `std::thread::sleep` to add a delay, you'll end up blocking the whole Tokio runtime thread!

``` rust
fn svc_wait(t: u64) -> impl Future<Item = (), Error = ()> {
    // code omitted for brevity
}

fn main() {
    let addr = ([127, 0, 0, 1], 3000).into();
    let server = Server::bind(&addr)
        .serve(|| {
            service_fn_ok(|req: Request<Body>| {
                // received the client connection
                eprintln!("Received client: {:?}", req.headers());
                // creating the future
                let f = svc_wait(2000);
                // the future is run NOW
                hyper::rt::spawn(f);
                // the client receives immediately a reply
                eprintln!("Sending back NOW a response to the client");
                Response::new(Body::from("Future triggered"))
            })
        })
        .map_err(|e| eprintln!("server error: {}", e));

    // runs on tokio runtime
    println!("Listening on http://{}", addr);
    hyper::rt::run(server);
}
```

Observe the server logging:

``` bash
# The request to the server will be immediately served, then the connection closed
$ curl localhost:3000
Future triggered

# this is the output you'll see on the server
$ cargo run
Listening on http://127.0.0.1:3000
Received client: {"host": "127.0.0.1:3000", "user-agent": "curl/7.64.0", "accept": "*/*"}
[start] waiting...
Sending back NOW a response to the client
... waiting ...
[end] waiting
```

A reply is being sent immediately to the client. The future is triggered, starts doing its "work" and finishes way after a reply is sent to the client.

## <a id="hyper-spawn"></a>Hyper with a simple endpoint router, spawns different Futures

The Hyper server has a router that recognize two endpoints:
- `GET /wait`: triggers the waiting Future seen before
- `GET /fetch`: triggers a request on a remote server

Basically the same as before but with a twist: the request router is itself a Future that resolves when the final Future is resolved.

Full code of this example is [here](#). Here we have the interesting bits:

``` rust
fn fetch_data() -> impl Future<Item = future::FutureResult<RespStruct, String>, Error = ()> {
    let uri: Uri = "http://httpbin.org/get".parse().expect("Cannot parse URL");
    Client::new()
        .get(uri)
        // Future is polled here
        .and_then(|res| {
            // extract the body from the Response
            res.into_body().concat2()
        })
        .map_err(|err| println!("error: {}", err))
        .map(|body| {
            // here parse the FutureResult, serialize into a validated Struct
            let decoded: RespStruct = serde_json::from_slice(&body).expect("Couldn't deserialize");
            future::ok(decoded)
        })
}

fn svc_wait(t: u64) -> impl Future<Item = (), Error = ()> {
    // code omitted for brevity
}

// Just an alias to make it more readable
type BoxFut = Box<dyn Future<Item = Response<Body>, Error = hyper::Error> + Send>;

fn service_router(req: Request<Body>) -> BoxFut {
    let mut response = Response::new(Body::empty());

    // routes the requesto to the appropriate worker
    match (req.method(), req.uri().path()) {

         // GET /wait
        (&Method::GET, "/wait") => {
            let r = svc_wait(1500);
            hyper::rt::spawn(r);
            *response.body_mut() = Body::from(format!("Triggered waiting {}ms", 1500));
        }

         // GET /fetch
        (&Method::GET, "/fetch") => {
            let r = fetch_data().map(|x| {
                println!("got data: {:?}", x);
            });
            hyper::rt::spawn(r);
            *response.body_mut() = Body::from("Sent request to external webservice");
        }

        // ... more routers

    }
    eprintln!("Returning a response");
    Box::new(future::ok(response))
}

fn main() {
    let addr = ([127, 0, 0, 1], 3000).into();
    let server = Server::bind(&addr)
        .serve(|| {
            // now we spawn a Future with our request router
            service_fn(service_router)
        })
        .map_err(|e| eprintln!("server error: {}", e));

    println!("Listening on http://{}", addr);
    hyper::rt::run(server);
}
```

## <a id="future-poll"></a>(TODO) Manually implementing a Future

Futures are cool because you "fire&forget" them. But what if we want to track their progress?

We need to manually implement the `.poll()` to be able to observe the various stages.

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

[https://github.com/chicagohaskell/async-futures-talk/blob/master/rustlb/examples/multi-http/src/main.rs](_posts/2019-07-17-rust-future-examples.md)

# Credits

Thanks to my friends of [Rust Rome](https://rustrome.github.io) for the incredbile support and for answering all my questions.

Thanks to [Bastian Gruber](https://github.com/gruberb) for his wonderful tutorials: namely [this](https://dev.to/gruberb/explained-rust-futures-for-web-development-a10) and [this](https://dev.to/gruberb/explained-rust-futures-for-web-development-a10).

And don't forget [the Hyper examples](https://github.com/hyperium/hyper/blob/master/examples).
