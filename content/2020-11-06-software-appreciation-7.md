+++
template = "post.html"
title = "Appreciation for software #7: NoScript"
+++

[NoScript](https://noscript.net) is a Firefox extension that I've been using for so many years (I think +5 years is not far from the truth) and it deserves much more visibility and recognition than it has.

At its core [NoScript](https://noscript.net) blocks JavaScript from executing on your browser. As simple as it seems, this has profound ramifications and consequences on your browsing experience and the "internet user" you become.

During the years JavaScript became more and more widespread, ubiquitous but also more annoying and ... dangerous. A lot of tricks and malicious scripts started pestering and tricking users.

With NoScript this all will disappear. Together with half of the websites becoming broken or unusuable :-)

NoScript has a very fine-grained blocking mask that allows to singularly block scripts, objects, media files, iframes, `fetch` requests and so on ... but the single most useful one is the ability to allow scripts either permanently or temporarily for that session (and reset the permission grant when the browser is restarted). Some scripts might be needed on some websites but not on other. If I see that a scripts is used almost everywhere I just add it the permanent whitelist.

I have a policy of whitelisting JavaScript. Instead of choosing what to block, I choose what to allow. It takes a bit of patience, because websites need to be loaded twice when they do not work without scripts.

But it's really a formative experience. Here are some key takeaways I could think of right now:
- You realize that often the "full enhanced" experience that JavaScript provides is just bullshit. I put the blame on who has developed the website, not on JavaScript.
- The amout of trackers that pile up on some websites is perplexing (load any news website and have a look at the network traffic). You realize there's something deeply broken in their business model when they feel the need to profile their users so passionately. The "free content" on Internet spoiled us and we're not paying anymore for a lot of things. This has consequences.
- It goes without saying that the same website without JavaScript runs faster on my computer. As a user, most of the time I accept a visually broken website until it's usable for this reason only. I don't care if it looks like shit: if it works I'm ok with that.
- By intentionally breaking websites, you learn how they work. By allowing scripts one by one from a domain you realize what it's really needed and what is dubious stuff that apparently has no functional purpose.

I admit I have a Firefox profile without NoScript in case I want to visit one of those websites (such as facebook, instagram, youtube, ...). In the latest months Facebook-owned products became more hostile and basically blocked the content for non-logged users. Somewhere in 2020 Instagram because unusable for me as a non-logged user. If you didn't notice this change, then you see why it's important to raise questions such as: why can't I use a website like I perfectly did weeks ago? Why do they force me to use scripts for *the very same* website and no additional feature? Why do they *force* me to be logged in?

On the other hand there are also funny surprises. twitter.com is 90% perfectly usable without javascript (only videos do not work) and you also have access to the list of followers and following of a profile, which are blocked behind a login in the JavaScript version. Again, a clear sign of hiding features for no good reason.

NoScript is basically what makes browsing bearable for me since quite a bit of time. To make a parallel for the casual reader, Firefox without NoScript is similar to what a lot of people experienced in May 2019 during the infamous Firefox incident of the [accidental expiry of the Addons certificates](https://hacks.mozilla.org/2019/05/technical-details-on-the-recent-firefox-add-on-outage) that caused all addons to stop working and people suddenly experienced the "internet" without adblockers and various other added functionalities. My friends and I stayed without using a browser for a couple of days, only opening it on a selected list of websites. It was a surreal travel back in time to those "funny websites" of the 2000s, with websites assaulting the visitor with colors, stuff moving and confusing content, your laptop fans spinning like they were compiling a "hello world" in Rust.

That day of May 2019 I fully realized the junkyard that the Internet of websites and webapplications had become while I innocently enjoyed my happy years of browsing, ignoring what was really happening outside there. It was an uncomfortable but necessary wake-up call.

One more note: using privacy-focused extensions such as Adblock Origin or Privacy Badger is different, as they are focused on the "privacy" part of the browsing experience, they just block trackers and such. NoScript is a declaration of war to the bloated Internet that we are seeing today.

But history repeats itself and will once again. Just as the wave of abusing GIFs and banners came and went away, then the wave of Flash applications, now this. This wave of insane SPA and steaming pile of JavaScript poo will be abandoned and turned into something else when people's patience will be depleted. Whatever will come will perhaps make NoScript useless (for example browser fingerprinting), whatever will come will be again abused, will trigger a new generation of counter-tools to fight them back. And so on and on.
