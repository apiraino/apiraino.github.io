---
layout: post
title: Configuring Postfix and Dovecot
---

### <a id="part_i"></a>The itch that needed to be scratched

I had to move my own server on another machine because the old VPS was aging and due to be turned off soon-ish by the provider.

So I took the chance to re-learn for the n-th time some <i>madz sysamin skillz</i> and configure to the maximum security extend possible the mail server.

First of all, the struggle. Being something that I don't usually do, I always start almost from scratch and have to educate me over terms and protocols like POP3, IMAP, STARTTLS and so on.

Then, the utter hostility of these services towards the poor soul that needs to implement the services. Really a lot of time was spent looking for resources and trying a myriad of different settings until finding the right combo that make everything play along the way I wanted.

Here are some lessons learned.

### <a id="part_ii"></a>You can't simply live under a SSL rock

I've tried since quite some time to implement the industry best practices and [tried to lock myself in an ideal world](/2018/09/22/tls-too-soon.html) where everything has the green sigil of Let's Encrypt.

Well, I've realized that this is simply not possible because there's always a non-negligible percentage of servers that simply don't care as much and if you want to talk with them, you have to be more tolerant.

So you dutifully implement STARTTLS, hoping this will be a hint to move the conversation to a more secure place. Often it won't be the case and you'll still see server from important provider sending in plain text!

I'm appalled by how a lot is discussed about privacy and security but still - in the business world - a lot of sensible documents are exchanged via email in plain text.

### <a id="part_iii"></a>Mail protocols are insecure by design, and it shows

At the 35C3 I could attend a very interesting talk about the (in)famous <a target="_blank" rel="noopener noreferrer nofollow" href="https://media.ccc.de/v/35c3-9463-attacking_end-to-end_email_encryption">Efail S/MIME vulnerability</a> (still not completely resolved!). The speaker showed how the root evil of everything is an inordinate amount of patching over protocols (POP3/SMTP) that are not supposed to be secure, because born in a more trustful world than today. Or, like the Postfix manual aptly says: "In a distant past, the Internet was a friendly environment".

### <a id="part_iii"></a>You are a hamster running in a wheel

The moment you start a task like this, you realize you have a long way ahead. Then you patiently make your way in that jungle that is Postfix and Dovecot. Then you succeed and you are - oh - so proud of your server. You'll probably say to yourself: this time I will document everything.

But then I gave up because in the end it doesn't make sense to put all the knowledge of a sysadmin on a Markdown file. I won't simply remember that *that* setting solved that problem, I cannot write a book with all the steps. Can you write down all the steps and possible pitfalls when compiling a C source code?

And finally you realize that in a month you will have forgotten everything and the next time you'll start from scratch, exactly like this time and time before: you basically live in the <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.imdb.com/title/tt0107048/">Groundhog Day movie</a>.
