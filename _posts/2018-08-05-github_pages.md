---
layout: post
title: "Locally testing a GitHub static website"
---

### Part I: The "hosted" solution

Github pages are nice, behind the scene there is a [jekyll](https://github.com/jekyll/jekyll) instance running your website/blog. Many plugins are available, you can compile HTML files out of a Markdown source you commit to the GitHub repository.

But what if you want to test locally the website before committing the changes?

You need to follow this tutorial [on GitHub](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll) and install:
- Ruby
- [Bundler](https://bundler.io)
- [jekyll](https://github.com/jekyll/jekyll)

Ok, what if you don't want any of this cruft installed (<sub>because as a pythonist *and* linux user, you already have your laptop messed up enough</sub>) just for your GitHub pages?

Docker to the rescue!

1) Checkout this repo: [https://github.com/BretFisher/jekyll-serve](https://github.com/BretFisher/jekyll-serve)

2) copy into your repo the file `docker-compose.yml`

3) From your website repo dir run: `$ docker-compose up`. It will download the docker image(s), build the container and run it on `localhost:80`; wow. This command (almost) equals to the following docker bash command:
``` bash
$ docker run --rm -p 80:4000 \
   -v $(pwd):/site \
   bretfisher/jekyll-serve
```

It's all good but ... that docker container defaults to using the [`minima` jekyll theme](https://jekyll.github.io/minima). As you can see, this site is pretty different and uses [the hacker theme](https://github.com/pages-themes/hacker), so how to load this theme?

### Part II: here be dragons

You can do that editing your `_config.yml` (create it if not present), adding (in my case) the following line:
``` yaml
theme: jekyll-hacker-theme

# other values you may already have
title: my blog
description: too much information
```

Run again the container, and ... watch it crash.
``` bash
$ docker run ....
...
      Generating...
jekyll 3.7.3 | Error:  No such file or directory - git
  Liquid Exception: No such file or directory - git in /_layouts/default.html
```

I could not generate anymore the static HTML, `jekyll serve` crashes for reasons not apparent to my ruby-newbie eyes.

So I tried what everyone does: trial-and-error, copy error on search engine, check stackoverflow, apply or discard patch, next error, rinse and repeat (gnawing your own teeth and mumbling 135 WTFs/minute).

First batch of fixes occurred when I've understood that the docker container downloaded a nice Ruby package called [`github-metadata`](https://github.com/jekyll/github-metadata). This package takes advantage of your remote repo to gather some info. But you need to tell it *what* your repo is. So let's fix that by adding to the `_config.yml`:
``` yaml
repository: apiraino/apiraino.github.io
```
and pass your GitHub token when you run the container:
``` bash
$ docker run --rm -p 80:4000 \
   -e JEKYLL_GITHUB_TOKEN=xxx \
   -v $(pwd):/site \
   bretfisher/jekyll-serve
```

this is explained [in their documentation](https://github.com/jekyll/github-metadata/blob/master/docs/configuration.md#configuration).

after a long back and forth I've finally nailed another issue: the ruby package `github-metadata` is not exporting a variable used by the `hacker` theme: `github.build_revision`, which is [required by this line of code](https://github.com/pages-themes/hacker/blob/master/_layouts/default.html#l7). I rolled back all the changes (yay) and verified that removing that single variable made everything work.

But why did it fail?

Like we said, the Ruby package takes advantage of the directive `repository` (and the GitHub token you pass to docker) to query your repo for some stuff; here's the Github documentation [about the metadata](https://help.github.com/articles/repository-metadata-on-github-pages). It's not clear where the fail happens: in the Ruby package or the Github API?

Ok, I can live without that variable, but I can't sleep until I really fix it. What is this variable, how can I retrieve it? Turns out that the metadata `build_revision` can be recovered from your local repo with a simple [`git rev-parse HEAD`](https://github.com/jekyll/github-metadata/blob/master/docs/configuration.md#overrides). Nice!

So, let's add another environment variable to our docker command:
``` bash
$ docker run --rm -p 80:4000 \
   -e JEKYLL_GITHUB_TOKEN=xxx \
   -e JEKYLL_BUILD_REVISION=$( git rev-parse HEAD ) \
   -v $(pwd):/site \
   bretfisher/jekyll-serve
```

and *FINALLY* the website appeared exactly like I see it on github.

The final touch? Oh, the `Docker compose` recipe we mentioned at the beginning so you don't have to remember that bash blurb. Let's amend the one provided by the [Dockerfile maintainer](https://github.com/BretFisher/jekyll-serve/blob/master/docker-compose.yml):

``` bash
$ cat docker-compose.yml
version: '3.7'

services:
  jekyll:
    image: bretfisher/jekyll-serve
    volumes:
      - .:/site
    ports:
      - '80:4000'
    environment:
      - JEKYLL_GITHUB_TOKEN=${JEKYLL_GITHUB_TOKEN}
      - JEKYLL_BUILD_REVISION=${JEKYLL_BUILD_REVISION}
```

Add those two env variables in your `.bashrc` file (or equivalent for other shells) or create a shell script to be loaded upon entering this directory:
``` bash
$ cat set_env.sh
#!/usr/bin/env bash
export JEKYLL_BUILD_REVISION=$( git rev-parse HEAD )
export JEKYLL_GITHUB_TOKEN=aaabbbcccddd
```

now simply run the Docker orchestrator:
``` bash
$ docker-compose up
```

### Part III: closing thoughts

Wow, that was some work to just switch a theme in a containerized Jekyll instance.

See, the funny thing of all this story is that the theme works out of the box when enabled on GitHub.

Now, the behaviour of the `github-metadata` package looks a bit odd, I'd like to understand where the problem is (the Ruby package? The GitHub API?). I opened an [issue on github](https://github.com/jekyll/github-metadata/issues/131) - let's see if we can get to the bottom of it.
