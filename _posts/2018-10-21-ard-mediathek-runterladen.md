---
layout: post
title: ARD Mediathek Filme runterladen
---

### <a name='part_i'></a>Part I: Filme

ARD uses a video streaming player that streams H.264+AAC content from an akamaihd CDN. Subtitles are in [TimedText](https://en.wikipedia.org/wiki/Timed_Text_Markup_Language) format.

#### Example URL for episode download

To see which streams are available, inspect network traffic with your browser and download the `master.m3u8` file, you will find something like that:

```
https://dasersteuni-vh.akamaihd.net/i/de/YYYY/MM/DD/<UUID>/,512-1,640-1,320-1,480-1,1280-1,960-1,.mp4.csmil/index_2_av.m3u8?null=0
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=316000,RESOLUTION=480x270,CODECS="avc1.66.30, mp4a.40.2",CLOSED-CAPTIONS=NONE
https://dasersteuni-vh.akamaihd.net/i/de/YYYY/MM/DD/<UUID>/,512-1,640-1,320-1,480-1,1280-1,960-1,.mp4.csmil/index_3_av.m3u8?null=0
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3771000,RESOLUTION=1280x720,CODECS="avc1.64001f, mp4a.40.2",CLOSED-CAPTIONS=NONE
https://dasersteuni-vh.akamaihd.net/i/de/YYYY/MM/DD/<UUID>/,512-1,640-1,320-1,480-1,1280-1,960-1,.mp4.csmil/index_4_av.m3u8?null=0
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1988000,RESOLUTION=960x540,CODECS="avc1.77.30, mp4a.40.2",CLOSED-CAPTIONS=NONE
https://dasersteuni-vh.akamaihd.net/i/de/YYYY/MM/DD/<UUID>/,512-1,640-1,320-1,480-1,1280-1,960-1,.mp4.csmil/index_5_av.m3u8?null=0
```

`<UUID>` is a unique directory with the transmission content

choose the desired resolution (streams won't go beyond 1280x720 anyways), f.e.:

`https://dasersteuni-vh.akamaihd.net/i/de/YYYY/MM/DD/<UUID>/,512-1,640-1,320-1,480-1,1280-1,960-1,.mp4.csmil/index_1_av.m3u8?null=0`

build the download URL with:

`https://pdvideosdaserste-a.akamaihd.net/de` + `/YYYY/MM/DD/<UUID>/` + `1280-1.mp4`

n.b. sometimes "1280x720" resolution is not explicited but the file is there as well most of the time.

### <a name='part_ii'></a>Part II: Untertitel

Example URL for subtitles:

get the `documentId` from URL, f.e.:

`http://mediathek.daserste.de/Filme-im-Ersten/<Film_name>/Video?bcastId=1933898&documentId=57028028`

get the player configuration from:

`http://mediathek.daserste.de/play/media/57028028?devicetype=pc`

then search for `_subtitleUrl` and download the XML.

or:

`https://www.daserste.de/unterhaltung/serie/<fernsehserie>/videos-folgen-verpasst/<fernsehserie_folge_1>-ut100.xml`

Then convert the XML to .srt (more common in video players):

- [works fine!](https://gotranscript.com/subtitle-converter)
  ```
  cat orig.srt | sed 's/10:/00:/g' | dos2unix > tmp.srt
  mv -f tmp.srt orig.srt
  ```

- [not tested](https://github.com/rg3/youtube-dl/issues/12303#issuecomment-315519815)

thanks ARD for putting all this wealth of stuff free for everyone.
