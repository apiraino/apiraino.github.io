---
layout: post
title: Certbot für alles!
---

Those one-liners that:

    you've learned not to underrestimate

because:

    all the time it took to put them together

but:

    don't know where to keep

<hr />

How to generate a certbot certificate valid for a domain and multiple subdomains.

``` bash
certbot-auto certonly --expand --non-interactive --agree-tos \
    --keep-until-expiring --standalone \
    --domains \
        mydomain.com,sub1.mydomain.com,sub2.mydomain.com,sub3.mydomain.com
```
