---
layout: post
title: Where do you live?
---

Just noticed this funny thing from a DEFCON talk <a target="_blank" rel="noopener noreferrer nofollow" href="https://youtu.be/vJtmZZGcR54?t=77">of 9 years ago</a>.

``` bash
#!/bin/bash

MAC="<your-router-mac-address>"
TK="<a-free-google-api-token>"

curl -X POST -H "Content-Type: application/json" \
    "https://www.googleapis.com/geolocation/v1/geolocate?key=$TK" \
        -d \'{
            \"macAddress\": \""$MAC"\",
            \"signalStrength\": -43,
            \"age\": 0,
            \"channel\": 11,
            \"signalToNoiseRatio\": 0
        }\'
```
