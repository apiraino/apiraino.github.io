---
layout: post
title: My Git workflow
---

### <a id="part_i"></a>Git flow

- Install git flow, [AVH edition](https://github.com/petervanderdoes/gitflow-avh) because the original one is abandoned and the repo spammed. Also don't use any Ubuntu packages, the're old.
- Setup git flow, merges should default to a `develop` branch
- Feature branch workflow

``` bash
$ git flow feature start name-of-the-feature
$ git flow feature finish -k <branch_name>
```

### <a id="part_ii"></a>Git release

- `git flow release start`
- Update the CHANGELOG file
- Update the version number everywhere

then, tagging the release (todo: check these commands)

``` bash
$ git tag -a 0.3.0 -m "release 0.3.0"
$ git push master --tags
```
