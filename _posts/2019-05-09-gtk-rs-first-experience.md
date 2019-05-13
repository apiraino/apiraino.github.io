---
layout: post
title: "Half week .into() Gtk with Rust"
---

I've attended the [Rust+Gnome 2019 Hackfest](https://wiki.gnome.org/Hackfests/Rust2019).

<center>
    <figure>
        <img src="/assets/doge.png">
            <figcaption>Much fun, so spaß</figcaption>
    </figure>
</center>

I'll recap a bit the experience for future reference.

## Assess my Rust proficiency

Starting to get comfortable with Rust and its quirks, still uncomfortable with the Rust memory model. Never used GTK before, have a general idea of how a GUI application work.

## Day 1

### Where did I start

I tried my usual "brute force" approach when learning something new: skip tutorials and documentation, get a working codebase, try to figure out the basics by reading the code and have something working with a lot of copy and paste.

I used as a starting point a workshop that [Guillaume](https://github.com/GuillaumeGomez) and [Sebastian](https://github.com/sdroege) held at the [RustFest '18 in Rome](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop).

I liked how the application was structured: as a GUI application tends to have boiler-plate (to build the GUI itself, of course!), I want to keep this boiler-plate separated from the business logic, and even better split the GUI code in submodules, each with its own responsibility. This way, the application can grow without getting messy.

However, after writing a working sample application doing some wild copy-pasting, this tutorial didn't work very well for me, I got a bit lost in some details that I will explain below, so I've started from scratch with a clean slate.

### What was clear and helpful

Thanks to the [examples repo](https://github.com/gtk-rs/examples) I could hack together some simple examples, although perhaps not ideal in real-life applications, e.g. all the code in the `main` method does not tell you much about idiomatic GTK applications.

### What was confusing

In general the code from the workshop helped me figuring out the basics, but also raised some questions:
- The memory management with macro like [upgrade_weak()](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/macros.rs#L4) and [downgrade()](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/app.rs#L207) is (for me) an advanced topic that set me off.

  The [macro replacing it](https://github.com/gtk-rs/examples/blob/5b9c4b2d86a47ed3a5014ec723f3613ce3231827/src/bin/child-properties.rs#L19) helps but it has some downsides (that macro will be rewritten in the future), but anyway nothing a newbie should worry about.
- The `async` macro defined [here](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/macros.rs#L19) appears to be not needed anymore.
- For any button with multiple states (represented by an `Enum`), did I had to implement [all these methods](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/app.rs#L108)? Example:

    ``` rust
    #[derive(Debug, Copy, Clone, PartialEq, Eq)]
    pub enum ButtonState {
        Enabled,
        Disabled,
    }

    impl<'a> From<&'a glib::Variant> for ButtonState {
        fn from(v: &glib::Variant) -> ButtonState {}
    }

    impl From<bool> for ButtonState {
        fn from(v: bool) -> ButtonState {}
    }

    impl From<ButtonState> for glib::Variant {
        fn from(v: ButtonState) -> glib::Variant {}
    }
    ```

  This seems not to be needed anymore, but it is confusing.

- Why do I need to [wrap](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/app.rs#L34) my App struct with layers or `Rc` and dereferencing methods? Why don't I need to do all this when building a [simpler example application](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/blob/master/src/app.rs#L34)? Am I leaking memory if I don't?

  The general question for me is: do I need to wrap Structs to not leak memory? How do I know if my application is leaking memory?

All these questions found an answer in the following days.

### Accomplishments of today

After throwing away the first application stub, I've rewrote a second prototype, leveraging what I've learned but keeping things simpler. The second try went much better, I gained a basic understanding on how to structure a basic Gtk without stuffing everything into the `main.rs`.

## Day 2

During the night, while I was wearing off the Club Mate, I've decided that it was boring to just hack together a useless GTK app showcasing just random widgets without a purpose. Therefore I thought that it could be interesting to draft a basic simple "clone" of [Postman](https://www.getpostman.com/), the great tool to test APIs.

What I need is:
- An input widget to enter a URL
- A text widget with a listener to paste the HTTP response into (with some nice formatting, maybe)

I can leverage and get quickly out of the way the HTTP part using [reqwest](https://crates.io/crates/reqwest). And to add some spice to the receipt, why not making it asynchronous, so the main GUI thread is not blocked until the remote server answers.

A quick question lead to a simple answer: spawn a thread inside the event manager of the input widget. Here's a succint version of the implementation:

``` rust
// create a transmit/receive facility
let (tx, rx) = glib::MainContext::channel(glib::PRIORITY_DEFAULT);

// create the text widget and its text buffer
let response_container = gtk::TextView::new();
let buf = response_container.get_buffer().expect("dang!");
buf.set_text("Hey, placeholder text");

// spawn the thread when the user press <Return> on the input URL
// pass the transmitter
url_input.connect_activate(clone!(tx => move |_| {

    let client = reqwest::Client::new();

    thread::spawn(clone!(tx => move || {
        let mut resp = client
            .post(...)
            .send()
            .expect("Request failed");
        let resp_data : Value = resp.json().unwrap();

        // send result to channel
        tx.send(format!("{}", resp_data))
            .expect("Couldn't send data to channel");
    }));
}));

// attach the receiver, write the text into the buffer
rx.attach(None, move |response_data| {
    buf.set_text(&response_data);
});
```

### What was confusing

- I had to figure out a bit of Gtk "parlance", example:
  ``` rust
  Gtk::Button::set_sensitive(bool) = to enable/disable a button
  ```

### Accomplishments of today

- Removed all the code that yesterday I've found confusing, things seems to work either way: no idea if I broke anything :-)

- Understood a bit better how to read the GTK-rs APIs (example: the difference between `Entry` and `EntryExt`), where to look for methods implemented by widgets, where to look for events (`connect_*`).

- Added a thread "spawner" inside a widget event manager

## Day 3

Unfortunately I could not participate as I was offlined due to previous arrangements.

## Day 4

Today I tried experimenting with more new things. [@antoyo](https://github.com/antoyo) showed me his shiny new toy [relm](https://github.com/antoyo/relm) to create a GUI application using a declarative approach based on macros.

A really seducing way to create GUI applications, because - like we discussed - the GUI code shouldn't get in my way, I want to concentrate on the "business logic" of the application.

Unfortunately the first try didn't go too far as I got a bit lost in importing the right `relm_*` crates and macros. That looks like a stupid reason to be blocked :-) but at some point I've stashed the branch and got back the "classic" way. I'll definitively check `relm` at a later stage.

Today I've added a simple Http client (leveraging the `reqwest` crate), and a couple more widgets and started testing this simple application.

Things got slower because I tried decoupling the business logic of the application, doing weird things like trying to move and handle gtk objects far from their context. I couldn't make sense of what I was doing, so I gave up.

As the last day went on, I felt more and more tired so as I produced less and less code I was trolling more and more the gtk-rs team :-) I've forked the gtk-rs repo and stashed some small PR that I hope to push real soon, in time for the next major release.

It is absolutely great to have maintainers behind your back giving explainations and encouraging you to submit PRs even for trivial things. This is the best part of the open-source development.

But in the end I've accomplished less that I wanted, that's price to pay for experimenting :-)

### What was confusing

- I didn't not manage to *quickly* hack together a new version of the application using relm
- Rust quirks got again in the way

But that was basically all I can complain for this day.

### Accomplishments of today

- Got a bit more comfortable with the GUI code and how it's meant to be written
- Added a (yet unfinished) Http client to manage the connections
- Prepared a small PR for the `gtk-rs` main repository (that likely will be merged before the next main release)
- Learned a bit more on how to correctly stack widgets horizontally and vertically and how to lay down things like you imagine them

## General acknowledgements

The **amazing** gtk-rs people doing an **amazing** job on the Gtk tookit.

The **amazing** gtk-rs people patiently explaining me a lot of basic stuff :-)

[kinvolk.io](kinvolk.io) for hosting the whole band and fueling us with an endless stream of caffeine.

Once again the Rust developer community proved to be incredibly competent and helpful.

It was great meeting again the gtk-rs and some really good friends.

I couldn't have asked more from a workhop.

As an unexpected bonus, experienced Gtk-rs developers and maintainers were really interested in my questions and feedback to understand where the pain points were to a complete newbie with no prior experience of the toolkit. This report is also for them!

<center><h3>Thank you folks, you are great!</h3></center>

## References

[RustFest 18 waorkshop on GTK-rs](https://github.com/sdroege/rustfest-rome18-gtk-gst-workshop/tree/master/src)

Misc [GTK applications in Rust](https://gitlab.gnome.org/World/Rust)

[GTK-rs examples](https://github.com/gtk-rs/examples)

[Documentation](https://gtk-rs.org/docs-src/)

Other projects to inspect for good first issues:
- https://gitlab.gnome.org/GNOME/fractal
- https://gitlab.gnome.org/BrainBlasted/Social
- https://gitlab.gnome.org/World/podcasts
- https://gitlab.gnome.org/World/Shortwave
- https://gitlab.gnome.org/users/haecker-felix/projects
- https://gitlab.gnome.org/haecker-felix/Authenticator

[Relm](https://github.com/antoyo/relm): inspired by [Elm](https://github.com/gdotdesign/elm-ui), a library that abstracts the details when building a GUI.
