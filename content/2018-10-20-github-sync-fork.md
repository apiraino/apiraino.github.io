+++
template = "post.html"
title = "How to sync a GitHub fork"
+++

### <a name='part_i'></a>Part I: This is embarrassing

It's easy to rebase a branch, but when it comes to GitHub forks I <strong>always</strong> forget how to do it, so I keep on checking the same GitHub guide over and over. As with any other big humanity failure, history keeps repeating itself.

I'm not kidding when I say this is the most repeated DuckDuckGo search I've done in 2018: `github rebase branch fork from master`.

### <a name='part_ii'></a>Part II: HOWTO

Your forked project has by default one `upstream`: the one of your fork.

So, first add the original project as additional `upstream` (this needs to be done only once):

``` bash
$ cd coolproject_myfork
$ git remote add upstream git@github.com:original_owner/coolproject.git
```

Once the additional `upstream` is available, update you fork:
``` bash
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

push the updates to your master:
``` bash
$ git push origin master
```

Now you can update your feature too:
``` bash
$ git checkout <my_feature_branch>
$ git merge master
```

[source](https://help.github.com/articles/syncing-a-fork)

### <a name='part_iii'></a>Part III: Let's make things a bit better

When you're about to merge your feature branch in the main branch, it's *always* a good idea to do the opposite first: by merging the main branch into your feature branch you will ease your job in case of conflicts.

In the best scenario, there's nothing else you have to do.

In the worst case, if your feature branch is an unrecoverable mess or has a tormented history, you can "rebase" creating another feature branch from the current master and merge the messed up feature branch into the new, updated feature branch. But this is another topic. Something along this:

``` bash
$ git status
On myfork
...

$ git merge master
<a mess of conflicts>

$ git checkout master
$ git checkout -b myfork_take2
$ git merge --squash --no-commit myfork
$ git reset

# and now you have your patch out of the stage and can regroup in clean commits
# people working on the projects will thank you for keeping the git history clean
```
