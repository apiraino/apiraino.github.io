---
layout: post
title: Bye Bye, Google (almost)
---

Here I'll detail all the Google services I've replaced, for future reference.

I'll factor in the typical user, mostly wishing for things to "just work".

### <a name='part_i'></a>First and foremost

- :white_check_mark: Google search -> DuckDuckGo
- :white_check_mark: Google mail -> ProtonMail

This basically addresses 85% of privacy concerns.

### <a name='part_ii'></a>Chats / IM

Easier. Lot of fragmentation: to this day I wouldn't know which Google App to use.

- :white_check_mark: Threema (closed-source)
- :white_check_mark: Signal
- :warning:️ Telegram (some security concerns)
- :no_entry: all others (no significant userbase)
- A [riot.im](https://about.riot.im) coupled with a [Matrix](matrix.org) self-hosted instance on NextCloud. See here: https://archive.fosdem.org/2018/schedule/event/matrix

### <a name='part_iii'></a>NextCloud

- :white_check_mark: Feedly -> NextCloud News (+ async python retriever)
- :white_check_mark: Contacts -> NextCloud Kontakte, Davx5 + any DAV application
- :white_check_mark: Google Calendar -> NextCloud Kalender, Davx5 + any DAV application
- :white_check_mark: Google Notes -> NextCloud Notizen
- :white_check_mark: Pocket / any "Read It Later" apps -> NextCloud Bookmarks
- :white_check_mark: Google Drive -> NextCloud Files
  - :white_check_mark: file sharing, permissions, expire access
  -:white_check_mark: data encryption at rest
    - :warning: encryption key not safe if server is compromised
- :warning: Google Drive file edit -> NextCloud Collabora
- :white_check_mark: Google Photos -> NextCloud Galerie

### <a name='part_iv'></a>What keeps in the Google bubble

- Collaboration, when required by third-parties (hardly solvable in most cases)
- Google Maps integration in Drive (might be solvable with third-party tools)
