---
layout: post
title: Integration tests in Rust and CI
---

I'm writing a small service in Rust, let's summarize how it works:

1. A client calls my server on `https://www.rustserver.com/endpoint`
2. The client receives immediately a `200 OK` to acknowledge the request
3. The server calls external services on `https://ext1.domain.com`, `https://ext2.domain.com`, `https://ext3.domain.com`, etc.
4. The server retrieves all the responses, do some parsing and store them somewhere

While it's important to have unit tests for step (4), I'd also like to have integration tests and trigger the whole workflow from start to finish.

### <a id="part_i"></a>The tool I need

In Python I was used to have a mocking library that allows me to define such as:

``` python
import mock

@mock.patch('mybackend.application.api.call_external_server')
def test_1(self, server_mock):

    # the test client calls my endpoint
    resp = self.call_my_server(email=self.email, token=self.tk)
    self.assertEqual(resp.status, 200)

    # verify that the external server call has been really happened
    self.assertEqual(1, len(server_mock.mock_calls))

    # other tests to check what happened after the external call was completed
```

So, how do we put this workflow under integration tests on Rust? I looked for a mocking library but couldn't find one to be easy enough to use. The crate [mockito](https://github.com/lipanski/mockito) gets close to what I'd like a mocking library to but it can only mick an HTTP request that it's directly called from the test.

The alternate approach is to roll up your sleeve and find a creative solution: for example start a proxy server that intercepts all outbound HTTP request and returns a static JSON.

### <a id="part_ii"></a> Adding the man in the middle

[mitm](https://github.com/mitmproxy/mitmproxy) is my proxy of choice when I need to inspect traffic, easy enough to get things done quickly.

`mitm` can be quickly scripted to have all sorts of funny things happening! In my casew I just want the request to be intercepted and a static JSON response returned. This can be accomplished with 10 lines of python:

``` python
from mitmproxy import http
from mitmproxy import ctx

def response(flow: http.HTTPFlow) -> None:

    if '/oauth2/v1/access_token' in flow.request.pretty_url:
        ctk.log.info('Gotcha!')
        with open('static_response.json', 'r') as fp:
            flow.response = http.HTTPResponse.make(
                201,
                fp.read().encode('UTF-8'),
                headers={"Content-Type": "application/json"}
            )
        return

```

Run it with and then try to call the remote endpoint:

``` bash
$ mitmproxy --scripts my_script.py
```

<figure>
    <img src="/assets/mitm.png">
</figure>


### <a id="part_iii"></a>Adding a proxy in a Rust http client

Ok we have the proxy. How do we tell the Rust client to use the proxy? And since this is only needed in tests we need a flag to enable the proxied call.

My solution, while not the cleanest, is to have a compilation flag to compile the client with or without the proxy (I use [hyper](https://hyper.rs) as http client and [hyper_proxy](https://github.com/tafia/hyper-proxy) to add a proxy).

Let's a feature flag

``` toml
# Cargo.toml
...
[features]
proxy_requests = []
default = []
...
```

Add the proxied connection flag to the client:

``` rust
use hyper::{client::HttpConnector, Body, Client};
use hyper_proxy::ProxyConnector;
use hyper_tls::HttpsConnector;

pub struct MyClient {
    #[cfg(feature = "proxy_requests")]
    pub client: Client<ProxyConnector<HttpConnector>, Body>,
    #[cfg(not(feature = "proxy_requests"))]
    pub client: Client<HttpsConnector<HttpConnector>, Body>,
}

impl MyClient {
    pub fn new() -> Self {
        let http_connector = HttpConnector::new(4);
        let https_connector = HttpsConnector::new(4).expect("TLS initialization failed");
        let proxy = {
            let proxy_uri =
                format!("{}:{}",
                    get_env!("PROXY_HOST"),
                    get_env!("PROXY_PORT")
                ).parse().unwrap();
            let proxy = Proxy::new(Intercept::All, proxy_uri);

            // My proxy is on plain HTTP
            let proxy_connector = ProxyConnector::from_proxy_unsecured(http_connector, proxy);
            proxy_connector
        };

        // When running tests and CI builds, run with "cargo run --features=proxy_requests"
        #[cfg(feature = "proxy_requests")]
        let client = Client::builder().build::<_, hyper::Body>(proxy);

        // In real life, server is run with "cargo run"
        #[cfg(not(feature = "proxy_requests"))]
        let client = Client::builder().build::<_, hyper::Body>(https_connector);

        MyClient { client }
    }
}
```

Let's write an integration test. This integration test is completely unaware of what's happening behind, it will always succeed. But it's useful to trigger the internal workflow.

``` rust
#[cfg(feature = "proxy_requests")]
#[test]
fn test_workflow() {
    let c = utils::TestClient::new();
    let url = c.add_to_url("/test").expect("Could not generate Url");
    let mut response = c.client.get(url).send().expect("Could not GET /test");
    let resp = response.text().unwrap();
    assert!(response.status().is_success(), format!("{} - {:?}", response.status(), resp));
}
```

Like mentioned in the code comments, I run tests with:

``` bash
$ cargo run --features=proxy_requests
$ cargo test --features=proxy_requests
```

Now all connections all intercepted by our man in the middle. In production I run:

``` bash
$ cargo run
```

### <a id="part_iv"></a>Setup the CI

Now the last part: let's automate this and update our CI builds!

I use CircleCI for this project, so I've updated the configuration file with the following items (see the comments):

``` yaml
jobs:
  rust-tests:
    docker:
      - image: circleci/rust:latest
    steps:
      - ... some steps ...
      - download-and-install-mitm
      - run:
          name: Run mitm
          background: true
          command: |
            # I'm running the headless version of "mitmproxy"
            mitmdump --scripts my_script.py
      - run:
          name: Run server
          environment:
            DEPLOY_MODE: test
            RUST_BACKTRACE: 1
          background: true
          command: |
            # Run the backend with maximum debug logging
            # Enable proxied requests
            # use "nohup" to log the output to a file
            RUST_LOG=my_backend=debug nohup cargo run --features=proxy_requests
      - run:
          name: Run tests
          environment:
            DEPLOY_MODE: test
            RUST_BACKTRACE: 1
            RUST_TEST_THREADS: 1
            RUST_TEST_NOCAPTURE: 1
          command: |
            # enable the integration tests under feature flag
            cargo test --features=proxy_requests --all
      - run:
          name: Post-mortem checks
          command: |
            sh ./scripts/post-mortem.sh
```

One more problem to solve. Like mentioned before the integration test has no way to know to report a failure, it will always succeed.

The only trace I have if something breaks is inspecting the server logging (notice the `nohup` when running the Rust server). In future I'd like to integrate a serious logging facility in Rust that allows me to write a proper log file and log to syslog.

In the meanwhile I'll just ... well ... grep through the logged stdout for a "BACKTRACE" or other markers :-)

Here is what the `post-mortem.sh` does:

``` bash
RES=$( grep -c BACKTRACE $LOGFILE )
if [ "$RES" -ne "0" ] ; then
    echo "test(s) failed"
    cat $LOGFILE
    exit 1
fi
```

Like I said, nothing here is implemented the way I'd like, but it's a start.

Things I'd like to improve in the future:
- Ideally find a serious HTTP mocking library and remove the whole proxy crutch
- Add a logging facility, I will investigate [log4rs](https://github.com/sfackler/log4rs)
- Improve the post-mortem reporting
