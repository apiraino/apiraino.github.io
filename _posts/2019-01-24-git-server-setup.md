---
layout: post
title: Setup a private Git server (quick and for dummies)
---

On your remote server, install the packages and create a `git` user:
```bash
$ sudo apt install git
$ sudo adduser git
```

optionally add your public key to access the repo for automatic SSH authentication:
``` bash
git@server.com:~$ mkdir ~/.ssh && touch ~/.ssh/authorized_keys
user@local-workstation:~$ cat ~/.ssh/id_rsa.pub | \
    ssh git@server.com "cat >> ~/.ssh/authorized_keys"
```

Create a `bare` new local repo:
``` bash
git@server.com:~$ mkdir my-repo
git@server.com:~$ cd my-repo
git@server.com:~$ git --bare init
```

The new repo is ready to be cloned:
``` bash
user@local-workstation:~$ git clone git@git.myserver.com:my-repo.git
```
