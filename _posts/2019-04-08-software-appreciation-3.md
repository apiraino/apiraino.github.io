---
layout: post
title: "Appreciation for software #3: pass"
---

After a couple of iterations to increasingly secure my accounts, I think I've finally found the sweet spot between ease of use and features.

The path to `pass` was more or less this:

- In the beginning, it was "saving passwords in the browser". Works fine until you realize that an attacker can access the decrypted passwords from the browser's memory because (as far as I know), passwords are decrypted until the browser stays open.
- Then I had a quite long relationship with [KeepassXC](https://keepassxc.org) and its great [browser extension](https://github.com/keepassxreboot/keepassxc-browser); the tiny team working on it is amazing, but in the end I've found KeepassXC GUI cumbersome, the CLI features lagging behind and the browser extension pattern matching (to fill login fields) sometimes lackluster.
- Finally I've looked for an offline solution, because it was the only way I could have full control.

I've completely skipped the step of "online password keyrings" because I don't have enough info to assess their security. Some of them have Javascript frontends that have been exploited, then patched, then exploited again. Others seems more secure, but only because there were no public disclosure about security incidents. Besides, I can reach syncronization on different devices using another workflow (detailed later).

[pass](https://www.passwordstore.org), on the other hand, is an incredibly powerful and simple tool to manage passwords. Its strength lies in being a simple tool that does *one* thing well: storing passwords. The secret of its success is the long list of ancillary tools the community have grown around it and the possibility to chain it with other tools.

So, the points in favor of **pass** are:

- Store password offline, easily management (generate new entries, rename and edit)
- The keyring is encrypted with a GPG key you choose
- Password entries stays encrypted at all times: you only decrypt the entry that you need (each password entry is a separate GPG file) and will briefly stay in the clipboard (45 seconds by default)
- Git integration: syncronize the encrypted keyring on a private, hosted repo
- `i3wm` integration with [passmenu](https://git.zx2c4.com/password-store/tree/contrib/dmenu): a useful script to access the keyring from `dmenu`
- Easy OTP generation [using a plugin](https://github.com/tadfisher/pass-otp)

The last point, although admittedly very useful, should not be evangelized as it defeats the purpose of OTP token generation (i.e. keep the OTP seeds separated from the device that stores the passwords).

The topic has also been discussed by the team providing the [browser extension](https://github.com/browserpass/browserpass-extension/issues/76) and finally decided to externalize this feature, leaving the decision to the user.

Lately I've equipped myself with a Yubikey, and discovered that I can further enhance this scenario using a seemingly convoluted workflow, but it should balance ease of use and security. More on that in a separate article.
