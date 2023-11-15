+++
template = "post.html"
title = "My wishlist for Rust '19"
+++

This isn't exactly a blog so this won't be exactly a "post", but I'd like to write down my thoughts on this notepad answering the call for [a wishlist for Rust 2019](https://blog.rust-lang.org/2018/12/06/call-for-rust-2019-roadmap-blogposts.html).

Opinions expressed are from the point of view of an enthusiast, Rust apprentice, that happened to be knee-deep involved in organizing the [RustFest in Rome](https://rome.rustfest.eu).

It's fun to pin today some thoughts and see in 12 months how things will have evolved!

### <a id="part_i"></a>First of all, the Community

There a lot of takeaways after helping organizing a conference with +200 attendees, [11 talks by 12 speakers](https://twitter.com/RustFest/status/1071720864134168577), plus workshops, [Impl Days](https://rome.rustfest.eu/about_impl_days) aaaand a beautiful city to walk by night.

Where would I like the conferencing story to go? It's a bit like in a startup, where there can be experimenting, a rollercoaster where *you* decide the next move. There are basically three things I'd like to see evolving:

* More crosstalk between conferences. Sharing know-how and resources will help organizers and new people willing to help organize an event but don't know how (hint: commitment is of the essence). This new people can then teach to others. And so on.

  This is why it is important to foster a network of conferences and _no-conf_ initiatives to keep the fire sparkling.

* More involvement of Rust companies. Sponsors are a great resource, but they are not faceless entities whom to ask for support and then "_thanks, see you next time_". They are made of very motivated people that may <strong>work with you in developing the Rust community</strong>.

  This is a call to involve them more. Conferences are just the tip of the iceberg of a partnership that can span the whole year: workshops, meetups, Rust companies can even host events. After all, it's in their best interest to have more Rust developers!

* A strong organization, the foundation for growth. Organizing activities for developers can quickly turn into a full-time job, it's no joke. It's called being a _community manager_. Many moons ago I've read an [interesting take on the topic](https://yakshav.es/sustainability/#professionalised-side-efforts). While not everyone can (or is willing to) afford this as a full-time commitment, also being part-time has its cost in terms of time and being responsive when the situation requires action.

  This is why it is important to build a core of people committed. The badge you earn (_look mom, I'm on the stage of a conference!_) is not free, but - hey - it's not like this is different from anything else: work needs to be done if you want the party to happen.

### <a id="part_ii"></a>More love to crates

So, I'm also a developer that is getting into the Rust world and wishes to have some of the bills deliciously covered by a Rust-flavoured fragrance. 2018 was a stepstone year for the ecosystem and a lot of praise has been given to the efforts to improve the language, the libraries, the _ergonomics_ of developing in Rust.

What I would like to see next:
- <strong>Less 0.1 bit-rot</strong>: some crates that are incredibly responding to a need, are often left in poor state (mostly lacking ancillary work, like documentation or examples) or as the language evolves, even broken.

  I also call for a "responsible" development when people start using your libraries; case in point the recent [breaking changes on the OpenSSL crate](https://github.com/sfackler/rust-openssl/issues/987), which caused some headaches.

- <strong>More "production" focused development</strong>: some developers are producing so much good stuff that they end up not having the mental bandwidth to juggle everything. The risk here is to put the ecosystem under a bad light. People coming from the "outside" judge the ecosystem by a library or the framework at hand; how can you use X and then explain to your CTO that a dependency of your project (deployed in production) has broken?

- <strong>Frameworks often are heroic one-man-bands efforts</strong>: from people that you even meet on IRC providing support (!) answering trivial questions to newbies like me: this is really heartwarming, but not sustainable. I wish for some heavier commitment of companies on Rust projects to let developers focus on the job (and this is already happening in some cases, see [Actix](https://actix.rs)). This is for the people asking on Stack Overflow: "what's the X equivalent for Rust?".

### <a id="part_iii"></a>Wishes expressed by others, that I share

Basically upvoting the following:

- The [async/await](https://github.com/rust-lang/rust/issues/50547) story, pretty please :^)
- Rust on the web: I strongly advocate for that, but frameworks are still in a "0.x" state (which doesn't necessarily means they're broken, see [Rocket](https://rocket.rs) or [Actix](https://actix.rs)). I would love to see a "1.0" at some point (that includes documentation, tutorials, ...).
- [The "boredom" of using Rust](https://www.ncameron.org/blog/rust-in-2022): a nice concept on how desirable is to be able to focus on the job at hand, without worrying about broken dependencies and nightly release of the compiler.
- The [tribal knowledge](https://cetra3.github.io/blog/rust-2019#documentation-churn) that is often lost on IRC logs - consequence of the "one-man-band" issue mentioned above.
- The half-life of Rust answers on Stack Overflow is short. Although updated as the compiler evolves (my infinite gratitude to those doing an amazing job there!), there are many deprecated answers, and that could be confusing. Agreed, that's a natural consequence of a rapid evolving language, but this forces me to deliberately ignore answers older than ~12 months.

### <a id="part_iv"></a>... ask what you can do for Rust

So far, my wishlist. But I want to add a little more to the proposition: what <strong>can I do</strong> for Rust?

In 2019 I will explore a bit how can I contribute to the Rust community environment; that's an area where I just moved the first steps, learned something, and I see a great potential for development.

My second goal would be to do some actual work in Rust: every developer that is being paid to do Rust development is a win for the ecosystem. Equally important are contributions to opensource projects: I mentioned some areas that would benefit from some polishing: well, that's a great place to start for helping! Lots of crates have "good first issues", need documentation, examples, even issue reporting or a simple star on the repository will help.

So, all in all, I'm sure that 2019 will build on the foundation laid by 2018. And unlike the stale joke of "the year of Linux on the desktop", I feel that 2019 will be "the year of Rust on our laptops" :-)
