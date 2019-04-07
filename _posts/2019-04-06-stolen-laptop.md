---
layout: post
title: "Losing my laptop: lessons learned"
---

While I was at the [Rust LATAM conference](/2019/04/06/latam.html), bad luck struck me hard. As a side effect of being tired, I've lost my backpack with passport and laptop.

I could manage to exit Uruguay with some help from local friends and the local embassy of my country. On the other hand, unfortunately, the laptop should be considered <a target="_blank" rel="noopener noreferrer nofollow" href="https://en.wikipedia.org/wiki/Missing_in_action">M.I.A.</a> as was not promptly retrieved. At the end of this blurb of text I will detail a bit the terrible customer support of Uber handling this case.

A lost laptop, when it's your main interface to the digital world, is a precious lesson on how to secure your device and an interesting (albeit expensive!) test of my setup. So let's attempt a retrospective (note: I'm a Linux user).

### What went well

- Password keyring GPG-encrypted. I use <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.passwordstore.org">pass</a>; no password is saved in any browser or online third-party password storage (e.g. LastPass, Bitwarden, 1password, etc.)
- The master GPG key protecting the keyring is on a Yubikey, always kept separated from the laptop when not attended
- The GPG-encrypted keyring is syncronized on a private, self-hosted GIT repo
- Offline backup of the GPG private keys on a LUKS encrypted removable device. Password to decrypt the LUKS device kept offline on a piece of paper.

### What can be improved (and how)

- Some data lost because not committed/backed up (not deemed important). Suggestion: the content of the laptop should be considered a local cache.
- Laptop access only protected by a login password. Suggestion: use [yubico PAM module](https://developers.yubico.com/yubico-pam) to login using the Yubikey
- Disk not encrypted. Suggestion: encrypt the whole disk or at least a partition with the important things. Use [tomb](https://www.dyne.org/software/tomb). This partition should be decrypted on successful login and re-encrypted on logoff, hibernate, shutdown.
- Browser left with some open sessions. Suggestion: not much you can do. Sometimes it's impractical to always logout and login. Find a good compromise based on your workflow and threat model.
- Email client with local mail storage and local contact list (just the few I still contact through email). Suggestion: no good suggestion here. Maybe use a webmail interfaces?
- Need a new laptop. Suggestion: shit happens, get over with it.

### Countermeasures

Actions took to rebuild and secure my environment:

- Retrieved password keyring from the remote repo
- Retrieved `i3wm` configuration from my <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.gitlab.com/apiraino/dotfiles">dotfiles</a> repo
- Generated new SSH key to access remote servers and services. Deleted old pub keys from any `.ssh/authorized_keys`
- Changed a couple of passwords and invalidated a couple of active sessions
- Refreshed API keys for a couple of services

### About Uber

Ok, let's close with with a personal note about Uber.

What's the single essential thing that must happen when you leave an important item in a taxi? Being able to immediately contact the driver. With Uber this is not possible, because as the fare finishes, you lose the phone number of your driver.

So, after realizing that my laptop was in the Uber car, we used their App to file a "Lost Item" report. Second unnerving thing: they don't put you through a human being, you just push a button, end of the report.

After a radio silence of one day, we decided to pay a visit to the Uber headquarters in Montevideo. We have patiently explained the situation to a clerk (that verified and validated our story) and told us that the driver assured that no backpack was in their car.

We want to trust Uber and their drivers' word, so we ask if it's possible to contact the clients that took that car after us. Sure, it's possible but for privacy reasons these phone numbers can't be disclosed (makes sense). The clerk gives us a Post-It note with two emails to contact: `lert@uber.com` and `legal@uber.com`.

We write immediately and were disappointed to discover that `legal@uber.com` is not a valid recipient. Radio silence from `lert@uber.com`, not even a bot responding they've received our email.

We keep on sending emails every two days to `lert@uber.com` but now it's just plain stalking, we don't really expect to a) receive an answer and b) to retrieve my backpack after a week.

Uber support in managing my case was simply a joke.

This is one of the most clear examples of what's wrong in this new VC-funded economy: they provide a service without owning a single asset (e.g. cars or employees providing the service); they take no responsibility and their customer support is unwilling to help, when help is really needed.

If I needed one more reason to be skeptic towards some of these "disrupting" startups, well, here it is.
