---
layout: post
title: My Git workflow
---

### <a id="part_i"></a>Git flow

- Install git flow, [AVH edition](https://github.com/petervanderdoes/gitflow-avh) because the original one is abandoned and the repo spammed. Also don't use any Ubuntu packages, the're old.
- Setup git flow, merges should default to a `develop` branch
- Feature branch workflow

``` bash
$ git flow feature start <branch_name>
$ git flow feature finish -k <branch_name>
```

### <a id="part_ii"></a>Git release

- Ensure you don't have unstaged diffs
- `git flow release start 0.3.0`
- Update the CHANGELOG
- Update the version number everywhere
- (opt.) `git flow release publish 0.3.0`
- `git flow release finish 0.3.0`

then, tag the release

``` bash
$ git tag -a 0.3.0 -m "release 0.3.0"
$ git push --tags
```
