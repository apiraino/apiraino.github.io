+++
template = "post.html"
title = "Bye Bye, Google (almost)"
+++

Here I'll detail all the Google services I've replaced, for future reference.

I'll factor in the typical user, mostly wishing for things to "just work".

### <a name='part_i'></a>First and foremost

- :white_check_mark: Google search -> DuckDuckGo
- :white_check_mark: Google mail -> ProtonMail

This basically addresses 85% of privacy concerns.

### <a name='part_ii'></a>Chats / IM

Easier. Lot of fragmentation: to this day I wouldn't know which Google App to use.

- :white_check_mark: Threema (con: closed-source)
- :white_check_mark: Signal
- :warning:️ Telegram (con: some security / privacy concerns)
- :no_entry: all others (con: no significant userbase)
- A [riot.im](https://about.riot.im) coupled with a [Matrix](matrix.org) self-hosted instance on NextCloud. [See here](https://archive.fosdem.org/2018/schedule/event/matrix).

### <a name='part_iii'></a>NextCloud

- :white_check_mark: Feedly -> [NextCloud News](https://github.com/nextcloud/news) (+ [async python feed retriever](https://github.com/nextcloud/news-updater)) + [news-android](https://github.com/nextcloud/news-android)
  - NextCloud News unmantained
- :white_check_mark: Contacts -> [NextCloud Contacts](https://github.com/nextcloud/contacts/), Davx5 + any DAV application
- :white_check_mark: Google Calendar -> [NextCloud Calendar](https://github.com/nextcloud/calendar), [Davx5](https://www.davx5.com) + any DAV application
- :white_check_mark: Google Notes -> [NextCloud Notes](https://github.com/nextcloud/notes)
  - :white_check_mark: Can also be used as a PasteBin-like code snippets share tool
- :white_check_mark: Pocket / any "Read It Later" apps -> [NextCloud Bookmarks](https://github.com/nextcloud/bookmarks)
  - Performance problems when many bookmarks
- :white_check_mark: Google Drive -> NextCloud Files (out of the box)
  - :white_check_mark: file sharing, permissions, expire access
  - :white_check_mark: data encryption at rest
    - :warning: encryption key not safe if server is compromised
- :warning: Google Drive file edit -> [NextCloud Collabora](https://nextcloud.com/collaboraonline/)
- :white_check_mark: Google Photos -> NextCloud Gallery (out of the box)

### <a name='part_iv'></a>What keeps me in the Google bubble

- Collaboration, when required by third-parties (hardly solvable in most cases)
- Google Maps integration in Drive (might be solvable with a combo of OSM and other drawing tools)
