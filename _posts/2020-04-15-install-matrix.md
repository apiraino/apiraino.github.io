---
layout: post
title: "Installing a Matrix server"
gist_id: 892fa8003a241a1d70d7642b63a0a5e6
---

In my (impossible) mission to manage my digital life without relying on third-party SaaS, another important step is a chat system. Can my usecase be accomodated with something else than Slack? Let's quickly overview the options for self-hosting, then what I've installed and how does it look like.

Briefly, the options and how I feel about them as of March 2020:
- [matrix.org](https://matrix.org): I saw a [CCC talk](https://media.ccc.de/v/35c3-9400-matrix_the_current_status_and_year_to_date) and made a note to try it. I was attracted by the global federation idea behind it. Connect your instance with other instances and bridge with third-party systems.
- [Rocket.chat](https://github.com/RocketChat): a server written in JS using Meteor, a framework my frontend friends say it's past its times. Will keep an eye on it.
- [Mattermost](https://mattermost.com): another promising alternative, but also heard a couple of lukewarm comments about usability. I might try it, though.
- I'm probably forgetting others worth a mention ...

As usual, this is my subjective experience (right or wrong), these are my unfiltered thoughts (right or wrong) and this is not a blog post trending on twitter :-P this is just me taking down notes.

As the title suggests, I decided to try matrix, the name was cool (lol) and it seems to have the most buzz across Nerdlands.

The reference implementation of the Matrix protocol is a Python3 server called [Synapse](https://github.com/matrix-org/synapse). Installing Synapse is very easy. There's a handy Docker container for a quick install. Although I usually prefer installing non-dockerized services, now I just want the convenience to throw that and play with it, so I'll go for the fastest path with a SQLite database.

I had to figure out a little bit the proxy pass-through configuration, the Synapse server needs two open ports. I think the 8448 is for the login and for federation (that is, users from other Matrix instances willing to join your instance).
```
<VirtualHost *:443>
    SSLEngine on
    ProxyPass / http://127.0.0.1:8008/ nocanon
    ProxyPassReverse / http://127.0.0.1:8008/
</VirtualHost>

<VirtualHost *:8448>
    SSLEngine on
    ProxyPass /_matrix http://127.0.0.1:8008/_matrix nocanon
    ProxyPassReverse /_matrix http://127.0.0.1:8008/_matrix
</VirtualHost>
```

Other small details to take care of, like manually enable the possibility for users to signup (which I find awkward because how else do I create the admin user?) and it's basically done. I spin up the docker image and we're online. I must say Synapse made a very good first impression, my first evaluation is always a sort of "grandma's test" and see in how much time I can walk the happy path provided by the documentation.
As usual, after starting the service, first check the open ports: Synapse opens to the world the TCP/8008, the python3 server (Twisted). Let's close it immediately:

`iptables -I DOCKER-USER -p tcp --dport 8008 -j DROP`

### <a id="part_1" href="#part_1" class="header-anchor">#</a> The Matrix clients

A brief overview of the clients available (as of March 2020). Easy: [Riot.im](https://riot.im), the rest looks like a lot of work in progress stuff.

Your can either use it from the [browser or download an Electron App](https://github.com/vector-im/riot-web). The Android client to be used is [RiotX](https://github.com/vector-im/riotX-android). I'd say that both clients work fine. Sometimes I receive complaints that the client is not receiving updates, maybe a push notifications issue? No idea, I'm not going to dive into the code and investigate.

The user interface is pretty basic but it's ok. I find interesting that I can edit the previous message simply by pressing arrow up.

<figure>
    <figcaption>Edit an old message</figcaption>
    <img data-gifffer="/assets/riot-edit-msgs.gif" />
</figure>

I like end-to-end encrypted rooms, just be careful: losing the client key will cut you out from reading the messages and that's by design.

<figure>
    <caption>The localization could use a bit of love, though</caption>
    <img src="/assets/riotim-e2e.png">
</figure>

I then invited some friends of mine (already resigned to be my guinea pigs).

There are a lot of fine settings, which is interesting. For example you can notify the server when you're writing, if you're reading a message, for mentions, for messages from bots and so on and so forth. The customization is at least on par (if not more customizable) with other platforms like Zulip or Slack. I have disabled the typing notification because each keystroke sends 4 requests (!) to the server. Seriously, wtf?!

Would a WebSocket work for this?
```
2020-04-16 10:38:41,258 - synapse.access.http.8008 - 302 - INFO - OPTIONS-37149 - 11.22.33.44 - 8008 - {None} Processed request: 0.001sec/0.001sec (0.000sec, 0.000sec) (0.000sec/0.000sec/0) 2B 200 "OPTIONS /_matrix/client/r0/rooms/!xxx/typing/%40user%3Achat.domain.com HTTP/1.1"
2020-04-16 10:38:41,309 - synapse.access.http.8008 - 302 - INFO - GET-37148 - 11.22.33.44 - 8008 - {@user:chat.domain.com} Processed request: 16.861sec/0.002sec (0.007sec, 0.000sec) (0.000sec/0.000sec/0) 694B 200 "GET /_matrix/client/r0/sync?filter=0&timeout=30000&since=s1234_56789_0123_4567_890_1_2_34_5 HTTP/1.1"
2020-04-16 10:38:41,310 - synapse.access.http.8008 - 302 - INFO - PUT-37150 - 11.22.33.44 - 8008 - {@user:chat.domain.com} Processed request: 0.013sec/0.001sec (0.002sec, 0.004sec) (0.000sec/0.000sec/0) 2B 200 "PUT /_matrix/client/r0/rooms/!xxx%3Achat.domain.com/typing/%40user%3Achat.domain.com HTTP/1.1"
2020-04-16 10:38:41,377 - synapse.access.http.8008 - 302 - INFO - OPTIONS-37151 - 11.22.33.44 - 8008 - {None} Processed request: 0.000sec/0.001sec (0.000sec, 0.000sec) (0.000sec/0.000sec/0) 2B 200 "OPTIONS /_matrix/client/r0/sync?filter=0&timeout=30000&since=s1234_56789_0123_4567_890_1_2_34_5 HTTP/1.1"
```

Using the client is ok, after some time one get used to minimalistic style and the sometimes confusing interface. I am no UX expert at all but:

- Why would I want in the first level of a popup menu (i.e. where space is at a premium!) an item to show the message source json?
- Why the "react" and the "stickers" icons are the same?

<figure>
    <img src="/assets/riotim-web-ux-0.png">
</figure>

- Why the "reply to message" UI covers my messages?

<figure>
    <img src="/assets/riotim-web-ux-1.png">
</figure>

- Why the "forward message" cancel icon ("X") is up there?

<figure>
    <img src="/assets/riotim-web-ux-2.png">
</figure>

It's really hard getting it right when it comes to UX.

Some features, from and external point of view, look hacked rather baked into the client. Example: here is how I can add and use a Giphy bot to a room.

<figcaption>(You have just downloaded a 4mb GIF)</figcaption>
<img data-gifffer="/assets/riot-add-giphy-synapse.gif" data-gifffer-alt="Can't even troll my friends" />

Yes, it works (kind of) but the implementation is not refined. Notice how much time it takes to have a feedback from the bot. The experience could be disappointing for a user.

Respect for the people working on this project and trying to make it a sustainable business, I'm really rooting for them. But I also have to be honest and say that as of today I cannot suggest this platform to my non technical friends/clients, unless the constraints are clear from the start (no custom emojis, no gifs, no fun). I don't see that friend of mine that has TikTok installed using this.

The great added value I want to explore in the following weeks is the integration with other (non) proprietary platforms. I can have a relay on IRC, Slack, Telegram, Discord etc. because unfortunately I have to have a user account on each of these platforms to stay in touch even for two only two people. A single centralized client for many proprietary platforms all orchestrated by a decentralized platform. The irony is not lost on this.

I tried quickly setting up a bridge towards a Slack account and I failed the grandma's test. Apparently I need to install a Docker container (another one?). So I'll have a look at that later.

### <a id="part_2" href="#part_2" class="header-anchor">#</a> On decentralized platforms

I noticed that *no* matrix client except those from riot.im implement end-to-end (e2e) message encryption. Same story for the servers that implement the Matrix protocol. Same [for the SDK](https://matrix.org/sdks/): only the matrix team did accomplish this.

At the CCC, Moxie Marlinspike from Signal gave a "controversial" talk about how a decentralized messaging system cannot work. Like it or not, he has a point: implementing e2e on a decentralized protocol is a huge pain in the ass *if* you don't want to sacrifice usability for your users. If you don't want to share your contacts with the server, fine, but then good luck porting your data to another device. You can backup on the messaging platform implicitely (like on Signal) or explicitely (like on Threema). Threema even gives you the option to backup on an offline device, which is a very good approach.

But. My Threema contacts never backup their data when they change device and regularly lose their ThreemaID and cannot recover their account data. They have to pay for another Threema licence (!) or I need to kindly ask the support for help (!!). Because they're non-tech people used to have "magically" their contacts and important chats and important nude pics automatically synchronized. You can't even have them do a simple thing like clicking a goddman button and backup their stuff before throwing away the old smartphone.

I hate giving my contacts to Signal, but I see the usecase. My contacts on Signal were mostly phone numbers. You can't tell one from the other when they're all numbers. At some point I enabled sharing my contact list (which Signal promises to be stored encrypted on their servers) and - bam! - my contacts suddenly became real people with name and surname. Cool, right? The side effect is that when a contact in my list creates an account on Signal we both receive a notification - a *completely unsolicited and that I cannot opt-out* - stupid notification saying "hey, your friend John Doe in on Signal!". Well, thanks but I don't want this crap.

Centralized platforms have spoiled users and now it is hard to decentralize people's *minds*.
