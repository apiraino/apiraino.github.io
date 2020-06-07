+++
template = "post.html"
title = "Enabling any website as a Firefox custom search engine"
+++

I am an avid user of the Firefox [Custom Search Engine](https://support.mozilla.org/en-US/kb/use-search-bar-firefox) feature, so I'd like to add any site I use frequently that allows a search through a `GET` request, example:
``` curl
https://www.thewebsite.com/search?keyword=%s
```
The Mozilla documentation details how to add new search custom engines. Basically we have two options:

1) From the Firefox search widget, when a plus `+` icon appears as you land on your website

<figure>
    <img src="/images/ff_cse.png">
</figure>

2) For websites not supporting the custom search engine feature (more on that later), you can bookmark the search URL provided by the website. Example:

<figure>
    <img src="/images/bing_cse_lol.png">
    <figcaption>Bing being good at ignoring OpenSearch support</figcaption>
</figure>

The procedure is explained, for example, [here](https://www-archive.mozilla.org/docs/end-user/keywords.html) and [here](http://kb.mozillazine.org/Using_keyword_searches): you basically bookmark the search page and assign it a keyword:

<figure>
    <img src="/images/bing_cse_bookmark.png">
    <figcaption>Add a bookmark with quick keyword access</figcaption>
</figure>

From now on you can perform in the URL bar searches writing the custom search engine keyword and the search terms, example: "\<keyword> funny cats", example "bing funny cats".

This is ok-ish, it works; if you have many sites to bookmark for fast access, it kind of clutters my bookmarks and ... it just doesn't _feel right_. I wanted to dig this thing to the core and understand what makes a website have that `+` icon appear on Firefox.

Enter the [OpenSearch Description](https://github.com/dewitt/opensearch/blob/master/opensearch-1-1-draft-6.md#version) specification!

Well, turns out that (of course) I just didn't discover anything special.

Firefox will show your site as a potential custom search engine if the page you're visiting contains in the `<HEAD>` tag a reference to a properly crafted XML file, describing how to access the search function:
```html
<link rel="search" type="application/opensearchdescription+xml" href="/osd.xml" title="MyWebsite search!"/>
```

The XML file specification is long but the bare minimum to make it work could be:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
    <ShortName>MyWebsite search</ShortName>
    <Url type="text/html" template="https://www.thewebsite.com/search?keyword={searchTerms}"/>
    <Url type="application/opensearchdescription+xml" rel="self" template="/mywebsite_osd.xml"/>
    <InputEncoding>UTF-8</InputEncoding>
    <OutputEncoding>UTF-8</OutputEncoding>
</OpenSearchDescription>
```

And the custom search engine is now enabled for your site.

<figure>
    <img src="/images/roll_your_own_cse.png">
</figure>

Finally, these two files cannot be simply accessed from the filesystem, it must be an HTTP request. So, if you want your favorite site to support this feature, send them an email (I did) and see how they ignore your request! XD

Second option is to host these two files somehere, just anywhere: Firefox won't check if the search URL you provide comes from the same hosting of your files. This means that `localhost:80` can add a custom search engine for `https://www.thewebsite.com/search?keyword={searchTerms}`.

Not the safest thing if you ask me: this could be used for some subtle phishing, if you don't pay close attention to the URL that pops up (or find a way to disable the popup via CSS).

If you don't have any hosting available, you can use one of the many ways to serve a simple HTML.

Repeat for every site you want to map in custom searches, the final result for me
looks like this:

<figure>
    <img src="/images/ff_cse_shortcuts.png">
</figure>
