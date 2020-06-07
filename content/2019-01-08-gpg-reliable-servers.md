+++
template = "post.html"
title = "Finding a reliable OpenGPG server"
+++

Is it me, or the GPG directoy servers are either underesourced / unmanaged / slow?

An updated list:

- ❌  <a target="_blank" rel="noopener noreferrer nofollow" href="https://pgp.mit.edu">https://pgp.mit.edu</a>: returns a 500 error on queries
- ❌ <a target="_blank" rel="noopener noreferrer nofollow" href="https://keys.gnupg.net">https://keys.gnupg.net</a>: invalid SSL certificate
- ❌ <a target="_blank" rel="noopener noreferrer nofollow" href="http://keys.gnupg.net">http://keys.gnupg.net</a>: returns a 502 error on queries
- ✅ <a target="_blank" rel="noopener noreferrer nofollow" href="https://pgp.surfnet.nl">https://pgp.surfnet.nl</a>: seems to be working

I even tried sending an email to the suggested service at <a target="_blank" rel="noopener noreferrer nofollow" mailto="pgp-public-keys@pgp.mit.edu">pgp-public-keys@pgp.mit.edu</a>, received a not so nice error:

<figure>
    <img src="/images/lol-mail.png">
    <figcaption>hahaha email</figcaption>
</figure>
