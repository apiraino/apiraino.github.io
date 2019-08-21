---
layout: post
title: Link Cleaner +
---

Here it is, published: [Link Cleaner +](https://addons.mozilla.org/en-US/firefox/addon/link-cleaner-plus)

This is a funny (and I hope useful) project I had forked and, with the help of another friend, moved a bit forward.

### <a id="part_i" href="#part_i" class="paragraph_link">&#182;</a> What is "Link Cleaner +"?

A Firefox extension that "cleans URLs before opening a link, removes trackers, rewrites redirects pages such as of Amazon, Facebook, Steam, Reddit and AMP URLs". As part of keeping a healthy internet browsing habit, I had discovered months ago this interesting extension (the original [Link Cleaner](https://addons.mozilla.org/en-US/firefox/addon/link-cleaner)). The GitHub page of the project, unfortunately, is riddled with issues, features requests and pull requests left unattended. So after a while we decided to fork the project and try to pick where the project left.

It's a work in progress, but it was important to get out a first version and then iterate.

Anyway, let's a look at it works (and how I'd like to see it improved).

The workflow of a browser extension is pretty much the same for Chrome and Firefox (luckily, since Firefox 57+ and WebExtensions came to the world) both APIs are pretty much the same, therefore much of the code can be shared and easily compile for both platforms.

### <a id="part_ii" href="#part_ii" class="header-anchor">#</a> Step 1: clean query params

We first intercept the action of opening a URL:

``` javascript
// Filter out utm_* query parameters
var clean_utm_req = build_query_param_remover(f_match_utm);
browser.webRequest.onBeforeRequest.addListener(
    clean_utm_req,
    {
        urls: ["<all_urls>"],
        types:["main_frame"]
    },
    ["blocking"]
);
```

This function (shortened for clarity) cleans query params from a URL and return a clean new URL.

``` javascript
// Clean URL query params
function link_cleaner(orig_url, shouldRemove) {
    var url = new URL(orig_url);
    var ret_val = {'redirectUrl': ''};

    if (url.search.length > 0) {
        var params = url.searchParams;
        var new_params = new URLSearchParams(params);
        var needs_redirect = false;
        for (let p of params.keys()) {
            if (shouldRemove(p)) {
                needs_redirect = true;
                new_params.delete(p);
            }
        }

        // Original URL has been cleaned of nefarious query params
        // A redirect URL has been created
        if (needs_redirect) {
            url.search = new_params.toString();
            ret_val = {redirectUrl: url.href};
        }

        // Clean AMP url (if enabled)
        if (settings['clean_amp_links'] === true) {
            var cleaned_url = clean_amp(url);
            if (cleaned_url.href !== url.href) {
                ret_val = {redirectUrl: cleaned_url.href};
            }
        }
    }
    return ret_val;
};
```

This function is generic enough to be applied to all URLs, example: clean all `utm_*` query params:

``` bash
https://www.domain.com/page?utm_source=mytracker
```

First we create an anonymous function with a regexp to match, then we invoke a generic query param cleaner (`build_query_param_remover`)

``` javascript
var f_match_utm = p => p.startsWith("utm_");

// a generic entrypoint to invoke the real link cleaner
function build_query_param_remover(shouldRemove) {
    return function(requestDetails) {
        return link_cleaner(requestDetails.url, shouldRemove);
    };
}

var clean_utm_req = build_query_param_remover(f_match_utm);

// This is the browser listener we sniff everytime a HTTP request is about to be performed
browser.webRequest.onBeforeRequest.addListener(
    clean_utm_req,
    {
        // apply this rule to any URL
        urls: ["<all_urls>"],
        types:["main_frame"]
    },
    ["blocking"]
);
```

### <a id="part_iii" href="#part_iii" class="header-anchor">#</a> Step 2: clean URLs

When we want to sanitize the URL itself, we need custom rules for any URL we want to manage. Example:

``` bash
# from this
https://www.amazon.co.uk/Crazepony-UK-Camera-Vacuum-Plastic-Crazepony/dp/B06XPCXCSH?SubscriptionId=AKIAILSHYYTFIVPWUY6Q&...

# into this:
https://www.amazon.co.uk/dp/B06XPCXCSH
```

(code shortened for clarity)


``` javascript
function clean_amazon(url) {
    var new_url = document.createElement('a');
    let slash_d_index = url.indexOf("/d");
    let slash_ref_index = url.indexOf("/ref=", slash_d_index + 2);
    if (slash_ref_index > 0 && url.length > slash_ref_index + 1) {
        new_url.href = url.substring(0, slash_ref_index + 1);
    } else {
        url = new URL(url);
        if (url.search.length > 0) {
            url.search = "";
            new_url.href = url.href;
        }
    }

    // scrap SEO friendly text
    var dp_idx = new_url.pathname.indexOf('/dp');
    if (dp_idx > 0) {
        new_url.pathname = new_url.pathname.substring(dp_idx, new_url.pathname.length);
    }
    return { redirectUrl: new_url.href };
}
```

### <a id="part_iv" href="#part_iv" class="header-anchor">#</a> Further thoughts and a wishlist

- If you squint enough at the code, you'll see that for <strong>every HTTP request the browser does, we run a lot of regexps work</strong>. If you're worried about the performance hit, then you are in good company: I'm worried, too.

- Regexps are bad. I'd like to run some benchmarks to see if and how much they affect the browser performances. As a side thought, many privacy focusing extensions basically run a lot of regexps against blacklists.

  Some of these extensions are noticeably slowing the browsing experience. A possible solution to explore could be using some WASM code to optimize hot code paths. [uBlock](https://github.com/gorhill/uBlock/tree/master/src/lib/lz4) and [HTTPS Everywhere](https://github.com/EFForg/https-everywhere) already do that (I didn't check the code, therefore I cannot comment on the results).

- Manually adding rules is a time-consuming effort known to be problematic and frustrating (both for users and developers). Without trying to build a complicated tool (such as: a backoffice for end-users to add regexps to the ruleset), one can think of something to (at least) submit their wishes in form of Gihub issues or pull requests. Example: describing a workflow that would lead to an effective pull requests.
  - Step 1: Identify the URL you would like to see cleaned
  - Step 2: go to [Regex 101](https://regex101.com) and write your rule
  - Step 3: open a PR submitting your suggestion and a test case
  - Step 4: the CI automatic build would tell if that breaks anything

  Such solution would not cover 100% of users, but hopefully we can drive the more technically-inclined to a faster path to merging their suggestion.
- Tests are also essential to keep performances under scrutiny.
