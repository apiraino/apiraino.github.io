---
layout: post
title: "In depth with Hyper: implementing a Service"
---

Follow-up to the previous [Hyper article](/2019/07/18/hyper.html).

Quick recap: Hyper is a high-performance HTTP async server + client that sits on the Tokio runtime and Future crate. These articles refer to Hyper `v0.12.33`. Despite the early release numbers, the framework seems to work well. Just expect the API to be unstable even between patch releases (!) (f.e. there was API breakage between `0.12.15` and `0.12.16`).

### <a id="part_1" href="#part_1" class="header-anchor">#</a> Implementing a `Service`

What is a Service? It's the basic router that handles all requests. You don't need to know a lot about it because in general you can use the [service_fn](https://docs.rs/hyper/0.12.33/hyper/service/fn.service_fn.html) and it will does all the job for you, see [previous article](/2019/07/18/hyper.html).

Here a succint overview (from the sources) of what a `Service` is:

``` rust
pub trait Service {
    /// The `Payload` body of the `http::Request`.
    type ReqBody: Payload;

    /// The `Payload` body of the `http::Response`.
    type ResBody: Payload;

    /// The error type that can occur within this `Service`.
    type Error: Into<Box<dyn StdError + Send + Sync>>;

    /// The `Future` returned by this `Service`.
    type Future: Future<Item=Response<Self::ResBody>, Error=Self::Error>;

    /// Returns `Ready` when the service is able to process requests.
    fn poll_ready(&mut self) -> Poll<(), Self::Error> {
        Ok(Async::Ready(()))
    }

    /// Calls this `Service` with a request, returning a `Future` of the response.
    fn call(&mut self, req: Request<Self::ReqBody>) -> Self::Future;
}
```

But what if we want to implement our own `Service`? And why would we want to do this?

I think (not 100% sure, though) the answer is if you want to factor in your router additional features.

For example, some endpoints need to do some work on a database. I need a connection to a database. One can simply open a connection on every request and close it once the job is done, but that would be extremely expensive.

How about we add a pool of database connections? Each request would pick one connection from the pool, do their job and return the connection to the pool once the job is done.

### <a id="part_2" href="#part_2" class="header-anchor">#</a> Getting a handle from a database

The only good crate I know for doing database connection pooling is [r2d2](https://crates.io/crates/r2d2). Let's see how we initialize the pool. Luckily this seems to be boilerplate I've everywhere so we'll just copy and paste and it'll just work.

I use Postgres so all the Diesel Traits are declined for this DB, but you can choose MySQL or SQLite3 and this code will change very little (I love Diesel). Not sure it makes sense to have a pool of Sqlite3 connections, though :-p

``` rust
use diesel::pg::PgConnection;
use diesel::r2d2::{ConnectionManager, Pool, PooledConnection};

// This is our pooled connection
struct Conn(pub PooledConnection<ConnectionManager<PgConnection>>);

// This is a shortcut for the Postgres pool
type PostgresPool = Pool<ConnectionManager<PgConnection>>;

// implementing Deref will ensure we retrieve the actual DB driver
// inside the Connection
// see: https://doc.rust-lang.org/std/ops/trait.Deref.html
impl Deref for Conn {
    type Target = PgConnection;

    // I don't understand if inlining give an actual advantage
    #[inline(always)]
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

pub struct MyBackendService {
    // our DB connections pool
    pub db_pool: PostgresPool,
}

impl MyBackendService {

    // This is a helper function to retrieve a connection from the pool
    pub fn get_conn(&self) -> Option<Conn> {
        match self.db_pool.get() {
            Ok(conn) => {
                Some(Conn(conn))
            }
            Err(err) => {
                None
            }
        }
    }
}
```

Now let's follow the [documentation](https://docs.rs/hyper/0.12.33/hyper/service/trait.Service.html) and implement our Service:

``` rust
// another shortcut to manage these long Rust type declaration...
// basically it says: a pointer to a Future which can return either a Response or an error
// oh, and this Future is thread safe (Send)
type BoxFut = Box<dyn Future<Item = hyper::Response<Body>, Error = hyper::Error> + Send>;

impl Service for MyBackendService {
    type ReqBody = Body;
    type ResBody = Body;
    type Error = hyper::Error;
    type Future = BoxFut;

    // Minimal request responder
    fn call(&mut self, request: hyper::Request<Self::ReqBody>) -> Self::Future {
        Box::new(
            future::ok(
                Response::builder()
                    .status(StatusCode::OK)
                    .body(Body::empty()
                ).unwrap(),
         ))
    }
}
```

Notice we need to use the `Send` Trait? Here are the [docs here](https://doc.rust-lang.org/nomicon/send-and-sync.html). I don't know how ot use it but the compiler told me so :-)

Well, now we have our service that always return a 200 to any request.

Now let's build everything and run it. We need to adapt the code seen in the previous article:
``` rust
    let addr = ([127, 0, 0, 1], 3000).into();

    // implement a service from a simple function
    // let server = Server::bind(&addr)
    //     .serve(|| service_fn(my_function_tralala))
    //     .map_err(|e| eprintln!("server error: {}", e));

    // reimplement using a Service
    let server = Server::bind(&addr)
        .serve(move || {
            let db_url = "postgres://usr:pwd@127.0.0.1/db_name";
            let manager = ConnectionManager::<PgConnection>::new(db_url);
            let pool = Pool::new(manager).expect("cannot create db pool");
            futures::future::ok::<MyBackendService, hyper::Error>(MyBackendservice { db_pool: pool })
        })
        .map_err(|e| eprintln!("server error: {}", e));

    // runs on tokio runtime
    hyper::rt::run(server);
```

Now let's see how an endpoint using a DB connection would look like. Again, refer to the previous article on how routing works:

``` rust
impl Service for MyBackendService {
    ...

    fn call(&mut self, request: hyper::Request<Self::ReqBody>) -> Self::Future {

        (&Method::GET, "/test") => {
            let db_conn = db_pool.get_conn().expect("Failed to get DB handle");
            let fut = future_that_does_a_query(&db_conn);
            Box::new(
                future::ok(
                    Response::builder()
                        .status(StatusCode::OK)
                        .body(Body::empty()
                    ).unwrap(),
             ))
        }

    }
}
```

Now when this endpoint is called the client will immediatly receive a 200 OK and our microserver has all the time to do its things. Which translates to: "ok, I got your task request and I'll do it eventually, now move along and don't stand in the queue. Next one, please!"

### <a id="part_3" href="#part_3" class="header-anchor">#</a> Level up: async DB connections

Ok, now we should have saved a lot of resources by using a connection pool.

Let's go to the next problem. `r2d2` provides a *synchronous* pool of connections but our microserver is *asynchronous*. What that means is that if we have to perform a "blocking" operation (HTTP request, DB query, read a file, anything that must stop the code waiting for something), the whole Future will be blocked until I didn't finish reading that 100mb file!

This is where things get hairy (and not everything is really clear to me).

I searched for an *asynchronous* DB pool, not much choice out there at this time. I tried using [bb8](https://crates.io/crates/bb8) but I wasn't even able to compile it on a new project. I've [opened an issue](https://github.com/khuey/bb8/issues/32) full of questions and parked the crate for the moment.

So how can we implement a non-blocking database handling?

Let's jump to the [next article to find out](/2019/08/29/hyper-threadpool.html)  (not ready yet, so you'll get a 404 ^_^)
