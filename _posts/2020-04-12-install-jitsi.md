---
layout: post
title: Installing a Jitsi.Meet server
---

With all the latest interest in videoconference tools, I decided to install [Jitsi.Meet](https://meet.jit.si/), on paper the best FOSS self-hosted alternative to the closed-source products we all know and use.

The installation is absolutely easy for everyone that has the basics of a Linux command line, it takes 5 minutes if an existing web server (either Apache or Nginx) is already in place. My respects to the team for having streamlined the installation of such a complex array of services talking to each other. I'll also detail some personal notes (as usual, as a reminder for my future self).

Example tutorial: [https://www.brring.com/2020/04/04/setting-up-a-jitsi-server-in-less-than-15-minutes](https://www.brring.com/2020/04/04/setting-up-a-jitsi-server-in-less-than-15-minutes) or a video (!): [https://www.youtube.com/watch?v=8KR0AhDZF2A](https://www.youtube.com/watch?v=8KR0AhDZF2A)

No need to repeat everything, here's just a summary:

- install a web server
- install the jitsi.Meet packages and automatically pull the (a lot of) dependencies
- install a Let's Encrypt certificate

At the end of the procedure the server is ready to be used on the domain name specified.

### <a id="part_1" href="#part_1" class="header-anchor">#</a> Now for some notes

Jitsi is [a hydra](https://github.com/jitsi/jitsi-meet/blob/master/doc/manual-install.md#network-description) and each head talk to each other through a TCP port. Your firewall must be configured to open the following ports:

```
iptables -A INPUT -p tcp --dport 5222 -j ACCEPT
iptables -A INPUT -p tcp --dport 5269 -j ACCEPT
iptables -A INPUT -p tcp --dport 5280 -j ACCEPT
iptables -A INPUT -p tcp --dport 5347 -j ACCEPT
iptables -A INPUT -p tcp --dport 4443 -j ACCEPT
iptables -A INPUT -p udp --dport 10000:20000 -j ACCEPT
# ... plus 80+443 for the webserver
```

After installing the packages, the installation asks if you want to install a SSL certiticate or "I want to use my own certificate". Since I have already Let's Encrypt `certbot` in place I can say no, because otherwise a lot of necessary packages will be installed. Also a lot of stuff that I don't want of a webserver (gcc, for example... 🤦‍♂️).

Jitsi pulls also a number of dependencies I don't understand, like the `x11-common` and a couple of X11 libraries, `libcups` and `libavahi-*`. Those cannot be removed.

Plus on Ubuntu 18.04.4 LTS the `openjdk-8-jre-headless` is installed. This can be replaced with the `openjdk-11-jre-headless`.

The installation files are in these directories:

```
/usr/share/jitsi-meet/
/usr/share/jitsi-meet-prosody/
/usr/share/jitsi-meet-web-config/
/usr/share/jitsi-videobridge/
```

Logs are here:

```
/var/log/jitsi/jvb.log
/var/log/jitsi/jicofo.log
/var/log/prosody/prosody.log
```

The service can be started and stopped with:

`systemctl restart jitsi-videobridge2.service`

The Java startup command visible from `top` or `ps` shows a whopping 112 java jars needed to run Jitsi. Let's have a look:

```
java -Xmx3072m
-XX +HeapDumpOnOutOfMemoryError
-XX HeapDumpPath=/tmp
-Dnet.java.sip.communicator.SC_HOME_DIR_LOCATION=/etc/jitsi
-Dnet.java.sip.communicator.SC_HOME_DIR_NAME=jicofo
-Dnet.java.sip.communicator.SC_LOG_DIR_LOCATION=/var/log/jitsi
-Djava.util.logging.config.file=/etc/jitsi/jicofo/logging.properties
```

Now all the jars:

<details><summary>Click to expand the list</summary>
<p>


```
-cp
/usr/share/jicofo/jicofo.jar
/usr/share/jicofo/lib/agafua-syslog-0.4.jar
/usr/share/jicofo/lib/annotations-15.0.jar
/usr/share/jicofo/lib/aopalliance-repackaged-2.6.1.jar
/usr/share/jicofo/lib/bccontrib-1.0.jar
/usr/share/jicofo/lib/bcpkix-jdk15on-1.54.jar
/usr/share/jicofo/lib/bcprov-jdk15on-1.54.jar
/usr/share/jicofo/lib/cglib-nodep-2.2.jar
/usr/share/jicofo/lib/commons-codec-1.6.jar
/usr/share/jicofo/lib/commons-lang3-3.1.jar
/usr/share/jicofo/lib/commons-logging-1.2.jar
/usr/share/jicofo/lib/concurrentlinkedhashmap-lru-1.0_jdk5.jar
/usr/share/jicofo/lib/core-2.0.1.jar
/usr/share/jicofo/lib/dnsjava-2.1.7.jar
/usr/share/jicofo/lib/dom4j-1.6.1.jar
/usr/share/jicofo/lib/fmj-1.0-SNAPSHOT.jar
/usr/share/jicofo/lib/guava-15.0.jar
/usr/share/jicofo/lib/hk2-api-2.6.1.jar
/usr/share/jicofo/lib/hk2-locator-2.6.1.jar
/usr/share/jicofo/lib/hk2-utils-2.6.1.jar
/usr/share/jicofo/lib/httpclient-4.4.1.jar
/usr/share/jicofo/lib/httpcore-4.4.1.jar
/usr/share/jicofo/lib/ice4j-3.0-10-g982e782.jar
/usr/share/jicofo/lib/jackson-annotations-2.10.1.jar
/usr/share/jicofo/lib/jackson-core-2.10.1.jar
/usr/share/jicofo/lib/jackson-databind-2.10.1.jar
/usr/share/jicofo/lib/jackson-module-jaxb-annotations-2.10.1.jar
/usr/share/jicofo/lib/jain-sip-ri-ossonly-1.2.279-jitsi-oss1.jar
/usr/share/jicofo/lib/jakarta.activation-api-1.2.1.jar
/usr/share/jicofo/lib/jakarta.annotation-api-1.3.5.jar
/usr/share/jicofo/lib/jakarta.inject-2.6.1.jar
/usr/share/jicofo/lib/jakarta.validation-api-2.0.2.jar
/usr/share/jicofo/lib/jakarta.ws.rs-api-2.1.6.jar
/usr/share/jicofo/lib/jakarta.xml.bind-api-2.3.2.jar
/usr/share/jicofo/lib/java-dogstatsd-client-2.5.jar
/usr/share/jicofo/lib/java-sdp-nist-bridge-1.2.jar
/usr/share/jicofo/lib/javassist-3.22.0-CR2.jar
/usr/share/jicofo/lib/javax.servlet-api-3.1.0.jar
/usr/share/jicofo/lib/jbosh-0.9.2.jar
/usr/share/jicofo/lib/jcip-annotations-1.0.jar
/usr/share/jicofo/lib/jcl-core-2.8.jar
/usr/share/jicofo/lib/jersey-client-2.30.1.jar
/usr/share/jicofo/lib/jersey-common-2.30.1.jar
/usr/share/jicofo/lib/jersey-container-jetty-http-2.30.1.jar
/usr/share/jicofo/lib/jersey-container-servlet-2.30.1.jar
/usr/share/jicofo/lib/jersey-container-servlet-core-2.30.1.jar
/usr/share/jicofo/lib/jersey-entity-filtering-2.30.1.jar
/usr/share/jicofo/lib/jersey-hk2-2.30.1.jar
/usr/share/jicofo/lib/jersey-media-jaxb-2.30.1.jar
/usr/share/jicofo/lib/jersey-media-json-jackson-2.30.1.jar
/usr/share/jicofo/lib/jersey-server-2.30.1.jar
/usr/share/jicofo/lib/jetty-client-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-continuation-9.4.17.v20190418.jar
/usr/share/jicofo/lib/jetty-http-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-io-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-proxy-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-security-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-server-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-servlet-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-util-9.4.15.v20190215.jar
/usr/share/jicofo/lib/jetty-webapp-7.0.1.v20091125.jar
/usr/share/jicofo/lib/jetty-xml-7.0.1.v20091125.jar
/usr/share/jicofo/lib/jicoco-1.1-22-gbec9167.jar
/usr/share/jicofo/lib/jitsi-android-osgi-1.0-SNAPSHOT.jar
/usr/share/jicofo/lib/jitsi-configuration-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-credentialsstorage-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-dnsservice-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-netaddr-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-protocol-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-protocol-jabber-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-protocol-media-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-util-2.13.cb5485e.jar
/usr/share/jicofo/lib/jitsi-utils-1.0-33-g2ed4090.jar
/usr/share/jicofo/lib/jitsi-xmpp-extensions-1.0-6-g009420d.jar
/usr/share/jicofo/lib/jna-4.1.0.jar
/usr/share/jicofo/lib/jnsapi-0.0.3-jitsi-smack4.2-3.jar
/usr/share/jicofo/lib/json-simple-1.1.1.jar
/usr/share/jicofo/lib/jxmpp-core-0.6.2.jar
/usr/share/jicofo/lib/jxmpp-jid-0.6.2.jar
/usr/share/jicofo/lib/jxmpp-util-cache-0.6.2.jar
/usr/share/jicofo/lib/libidn-1.15.jar
/usr/share/jicofo/lib/libjitsi-1.0-0-gb3296cf.jar
/usr/share/jicofo/lib/object-cloner-0.1.jar
/usr/share/jicofo/lib/objenesis-2.6.jar
/usr/share/jicofo/lib/orange-extensions-1.3.0.jar
/usr/share/jicofo/lib/org.apache.felix.framework-4.4.0.jar
/usr/share/jicofo/lib/org.apache.felix.main-4.4.0.jar
/usr/share/jicofo/lib/org.osgi.core-4.3.1.jar
/usr/share/jicofo/lib/osgi-resource-locator-1.0.3.jar
/usr/share/jicofo/lib/reflections-0.9.11.jar
/usr/share/jicofo/lib/sdes4j-1.1.3.jar
/usr/share/jicofo/lib/sdp-api-1.0.jar
/usr/share/jicofo/lib/slf4j-api-1.7.26.jar
/usr/share/jicofo/lib/slf4j-jdk14-1.7.26.jar
/usr/share/jicofo/lib/smack-bosh-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-core-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-debug-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-experimental-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-extensions-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-im-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-java7-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-legacy-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-resolver-javax-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-sasl-javax-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/smack-tcp-4.2.4-47d17fc.jar
/usr/share/jicofo/lib/tinder-1.3.0.jar
/usr/share/jicofo/lib/weupnp-0.1.4.jar
/usr/share/jicofo/lib/xml-apis-1.0.b2.jar
/usr/share/jicofo/lib/xmlpull-1.1.3.4a.jar
/usr/share/jicofo/lib/xpp3-1.1.4c.jar
/usr/share/jicofo/lib/zrtp4j-light-4.1.0-jitsi-1-SNAPSHOT.jar
```

</p>
</details>

And finally the configuration for the [Jitsi Conference Focus](https://github.com/jitsi/jicofo):

```
org.jitsi.jicofo.Main
--host=localhost
--domain=meet.yourdomain.com
--port=5347
--secret=xxxxx
--user_name=xxxxx
--user_domain=auth.meet.yourdomain.com
--user_password=xxxxx
```

### <a id="part_2" href="#part_2" class="header-anchor">#</a> Optimizations

```
net.core.rmem_max=10485760
net.core.netdev_max_backlog=100000
```

source: [here](https://github.com/jitsi/docker-jitsi-meet/pull/440#issue-402324914)

### <a id="part_2" href="#part_3" class="header-anchor">#</a> Ok, so how is it?

I've just briefly tested with a short call and it was not bad. The video quality is amazing (also your own video stream in local, when you see yourself) not a lot stable and often the quality indicator signaled a poor connection. But the quality never dropped to a freezing video stream, it just downgraded to standard quality from high quality. A first test with the mobile client didnt' work. I will do more tests in the following days.
