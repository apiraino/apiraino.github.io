---
layout: post
title: First steps in async Rust
---

### <a id="part_i"></a>The target

Learning how to write a simple web service in Rust that performs HTTP requests.

These requests should be asynchronous because we don't know when the external service will answer. Take into account also service timeouts.

### <a id="part_ii"></a>Tooling

Still not sure what to use, let's try to quickly from the bottom up:

The operating system kernel has threads. When you launch a thread, then you must poll it and when it finishes you get the results.

On top of the OS I need a "runtime", a layer that manages the `.poll()` method. The `poll` returns either an "OK" or "NOT YET DONE" kind of response. The runtime puts to sleep this "thing" that polls the thread for some time, than asks again.

Tipically I have a pool of these threads.

An async function in Rust is abstracted as a `Future`, i.e. something that is launched and will eventually resolve to a result. A Future is polled until is resolves and returns some result (or an error). Future have been recently [stabilized in Rust stable](https://blog.rust-lang.org/2019/07/04/Rust-1.36.0.html#the-future-is-here).

I'd like to use the soon-to-be (as of July 2019) stabilized async/await syntax. Draft of the syntax [is been published here](https://github.com/rust-lang/rust/issues/62149).

#### The runtime

I ought to choose a runtime. There are two possibilities:

- [tokio](tokio.rs): tried to use it before we had Future and await/async available and it was impossible to grasp. Looking at the versioning, the project seems to have stalled [until recently](https://www.reddit.com/r/rust/comments/c5eqj1/tokio_master_branch_switching_to_stdfuture).

- [Runtime](https://github.com/rustasync/runtime): the name of the project is confusing, the aim seems to add a thin layer to abstract the runtime and let the user choose between two runtimes: tokio and the "native" (Romio+Juliex) one. [Reading this comment](https://github.com/SergioBenitez/Rocket/pull/1008#issuecomment-507158310) on the future async dor Rocket, "Runtime" does not looks like a sensible choice. Runtime build on two components:
  - [Romio](https://github.com/withoutboats/romio), the reactor
  - [Juliex](https://github.com/withoutboats/juliex), the executor

don't understand the current state of Runtime and if I should use it.

[Q] **Why do I, as the developer, should be concerned about choosing a runtime?** : only if I'm not using a web framework that abstracts the choice for me.

[Q] **Do I really have to manually `impl Future` for my async methods and manage the states?**: Maybe not. I can probably add a placeholder crate (https://github.com/alexcrichton/futures-await) to use today the syntax that will be stabilized tomorrow (hopefully available in Rust stable 1.38/9). But the syntax differs from that of the Runtime crate. And the crate seems to be abandoned.

[Q] **How does this crate fits into the picture: https://github.com/rust-lang-nursery/futures-rs**

[Q] **reqwest/hyper async clients: how do they fit into the picture?**: An async client is needed to emit thread-unblocking http requests, that don't block the thread. If I run an async server (ex. Hyper), then I *must* use also an async client, too.

### <a id="part_iii"></a>Frameworks

A nice to have, but I think I need something more basic, just something listening and allow some administration of the tasks. Not a user facing component.

[Tide](https://github.com/rustasync/tide): this is Flask-like light framework that uses Runtime. Develope by the async WG.

[warp](https://seanmonstar.com/post/176530511587/warp), which relies on hyper and tokio. Developed by Sean McArthur.

[tower-web](https://github.com/tower-rs/tower), a (seemingly) very early work-in-progress framework. Relies on futures 0.1 and tokio 0.1. Developed by Carl Leche.

### Special mentions

[actix-web](https://actix.rs): a full-fledged web framework. Looks to be very fast not easy to grasp (especially the middleware part is confusing).

[rocket](https://rocket.rs), I already use it, it's synchronous but I believe works to make it async has started, [see this PR](https://github.com/SergioBenitez/Rocket/pull/1008#issuecomment-507049080) (porting to hyper 0.12).

### <a id="part_iv"></a>References

- [Future Trait stabilized in 1.36](https://blog.rust-lang.org/2019/07/04/Rust-1.36.0.html)
- [Explained: How does async work in Rust?](https://dev.to/gruberb/explained-how-does-async-work-in-rust-46f8)
- [Futures in Rust for Web Development](https://dev.to/gruberb/explained-rust-futures-for-web-development-a10)
- [https://areweasyncyet.rs](https://areweasyncyet.rs)

- [Async-await status report #2](ttps://www.reddit.com/r/rust/comments/cawahp/asyncawait_status_report_2)
- [Discussion on Discord](https://discordapp.com/channels/442252698964721669/474974025454452766/598878779695300609) (spoiler: no useful info gathered)
- [How to run a set of Futures in any order](https://github.com/chicagohaskell/async-futures-talk/blob/master/rustlb/examples/multi-http/src/main.rs) and [caveats on polling](https://docs.rs/futures/0.1.28/futures/stream/futures_unordered/struct.FuturesUnordered.html).
