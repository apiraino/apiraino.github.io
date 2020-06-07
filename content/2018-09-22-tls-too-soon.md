+++
template = "post.html"
title = "TLS: too soon to secure your email?"
+++


### <a name='part_i'></a>Part I: Disbelief

Some time ago I've read about the [STARTTLS Everywhere](http://starttls-everywhere.org) campaign by the EFF. I was immediately sold.

With the precious help of a friend (more knowledgeable than me on the matter), we configured my Postfix as follows:
``` postfix
smtp_enforce_tls = no
smtpd_tls_loglevel = 1
smtpd_tls_cert_file = /path/to/letsencrypt/fullchain.pem
smtpd_tls_key_file = /path/to/letsencrypt/privkey.pem
smtpd_tls_received_header = yes

smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtpd_tls_session_cache_timeout = 86400s
smtpd_tls_security_level = encrypt  # <--- THIS is the important part!
smtpd_tls_ciphers = high
smtpd_tls_mandatory_ciphers = high

smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
smtp_tls_session_cache_timeout = 86400s
smtp_tls_security_level = encrypt  # <--- THIS is the important part!
smtp_tls_ciphers = high
smtp_tls_mandatory_ciphers = high
```

After the changes everything works; so, let's start our experimentation period.

After a while (couple of weeks), as I sent emails from my various account, some mail server started spitting back my emails:

* tin.it
* tiscali.it
* \<another_italian_domain_pretty_important_to_me\>

The error message I receive is a nice:
<figure>
    <img src="/images/too_much_tls.png">
    <figcaption>Too much, too soon</figcaption>
</figure>

Two of these emails servers are *Italian national providers* - not amateurish Postfix installation from your know-it-all friend that plugs printer power cords.

Don't they, right?

### <a name='part_ii'></a>Part II: Technical support FTW ... or not?

This part will be really short. I've contacted the admin reference suggesting to improve their configuration and - of course - my request was ignored.

Well, not exactly ignored: I could actually hear their laughters thousands kms away.

So, all I could do was relax the configuration I was so proud of and allow a more tolerant communication among SMTP servers:
``` postfix
smtp_tls_security_level = may
# smtp_tls_security_level = encrypt
smtpd_tls_security_level = may
# smtpd_tls_security_level = encrypt
```

followed by the usual `postfix reload`.

### <a name='part_iii'></a>Part III: To add insult to injury

Fun fact! I have an old email account seldom used on one of the above-mentioned internet providers. I meant to use that account outside their country with the same SMTP settings because - well - what could possibly go wrong?

<figure>
    <img src="/images/smtp_outside.png">
    <figcaption>Ouch, *michael* doesn't like emails from evil countries</figcaption>
</figure>

Although this is described in a support page of that provider, it doesn't make this less awkward.
