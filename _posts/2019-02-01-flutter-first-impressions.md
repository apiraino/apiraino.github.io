---
layout: post
title: "Flutter: basically upselling Firebase services"
---

(the future is here and it's scary)


First impressions after trying Flutter (that is: a completely different thing I usually develop with).

In two or three days, I went from zero (i.e. install Android Studio and copy-paste the first tutorial) to a complete (albeit simple) app with multiple screens ("Activities", in Android parlance), routers and some advanced features like asyncronous network fetching (using `Future`) and background tasks (the `compute` keyword).

I'd say the worst obstacle was rewiring my brain to use Android Studio.

Having a look at the stacktrace of a simple "file not found" error, gives an idea of the layers upon which you're building your application (and I suspect that much more is hidden, I don't even see the Java underlying exception!) before getting to the actionable "levers":

<details><summary>Click to expand this blurb</summary>
<p>

```bash
Performing hot restart...
Syncing files to device Android SDK built for x86...
Restarted application in 1,546ms.
I/flutter (23143): got tap
I/flutter (23143): ══╡ EXCEPTION CAUGHT BY IMAGE RESOURCE SERVICE ╞════════════════════════════════════════════════════
I/flutter (23143): The following assertion was thrown resolving an image codec:
I/flutter (23143): Unable to load asset: assets/rooms/item4.jpg
I/flutter (23143):
I/flutter (23143): When the exception was thrown, this was the stack:
I/flutter (23143): #0      PlatformAssetBundle.load (package:flutter/src/services/asset_bundle.dart:221:7)
I/flutter (23143): <asynchronous suspension>
I/flutter (23143): #1      AssetBundleImageProvider._loadAsync (package:flutter/src/painting/image_provider.dart:429:44)
I/flutter (23143): <asynchronous suspension>
I/flutter (23143): #2      AssetBundleImageProvider.load (package:flutter/src/painting/image_provider.dart:414:14)
I/flutter (23143): #3      ImageProvider.resolve.<anonymous closure>.<anonymous closure> (package:flutter/src/painting/image_provider.dart:267:86)
I/flutter (23143): #4      ImageCache.putIfAbsent (package:flutter/src/painting/image_cache.dart:143:20)
I/flutter (23143): #5      ImageProvider.resolve.<anonymous closure> (package:flutter/src/painting/image_provider.dart:267:63)
I/flutter (23143): #6      SynchronousFuture.then (package:flutter/src/foundation/synchronous_future.dart:38:29)
I/flutter (23143): #7      ImageProvider.resolve (package:flutter/src/painting/image_provider.dart:265:30)
I/flutter (23143): #8      _ImageState._resolveImage (package:flutter/src/widgets/image.dart:630:20)
I/flutter (23143): #9      _ImageState.didChangeDependencies (package:flutter/src/widgets/image.dart:605:5)
I/flutter (23143): #10     StatefulElement._firstBuild (package:flutter/src/widgets/framework.dart:3846:12)
I/flutter (23143): #11     ComponentElement.mount (package:flutter/src/widgets/framework.dart:3696:5)
I/flutter (23143): #12     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #13     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #14     SingleChildRenderObjectElement.mount (package:flutter/src/widgets/framework.dart:4860:14)
I/flutter (23143): #15     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #16     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #17     SingleChildRenderObjectElement.mount (package:flutter/src/widgets/framework.dart:4860:14)
I/flutter (23143): #18     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #19     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #20     ComponentElement.performRebuild (package:flutter/src/widgets/framework.dart:3732:16)
I/flutter (23143): #21     Element.rebuild (package:flutter/src/widgets/framework.dart:3547:5)
I/flutter (23143): #22     ComponentElement._firstBuild (package:flutter/src/widgets/framework.dart:3701:5)
I/flutter (23143): #23     ComponentElement.mount (package:flutter/src/widgets/framework.dart:3696:5)
I/flutter (23143): #24     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #25     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #26     ComponentElement.performRebuild (package:flutter/src/widgets/framework.dart:3732:16)
I/flutter (23143): #27     Element.rebuild (package:flutter/src/widgets/framework.dart:3547:5)
I/flutter (23143): #28     ComponentElement._firstBuild (package:flutter/src/widgets/framework.dart:3701:5)
I/flutter (23143): #29     ComponentElement.mount (package:flutter/src/widgets/framework.dart:3696:5)
I/flutter (23143): #30     ParentDataElement.mount (package:flutter/src/widgets/framework.dart:4047:11)
I/flutter (23143): #31     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #32     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #33     ComponentElement.performRebuild (package:flutter/src/widgets/framework.dart:3732:16)
I/flutter (23143): #34     Element.rebuild (package:flutter/src/widgets/framework.dart:3547:5)
I/flutter (23143): #35     ComponentElement._firstBuild (package:flutter/src/widgets/framework.dart:3701:5)
I/flutter (23143): #36     StatefulElement._firstBuild (package:flutter/src/widgets/framework.dart:3848:11)
I/flutter (23143): #37     ComponentElement.mount (package:flutter/src/widgets/framework.dart:3696:5)
I/flutter (23143): #38     Element.inflateWidget (package:flutter/src/widgets/framework.dart:2950:14)
I/flutter (23143): #39     Element.updateChild (package:flutter/src/widgets/framework.dart:2753:12)
I/flutter (23143): #40     SliverMultiBoxAdaptorElement.updateChild (package:flutter/src/widgets/sliver.dart:1028:36)
I/flutter (23143): #41     SliverMultiBoxAdaptorElement.createChild.<anonymous closure> (package:flutter/src/widgets/sliver.dart:1013:20)
I/flutter (23143): #42     BuildOwner.buildScope (package:flutter/src/widgets/framework.dart:2266:19)
I/flutter (23143): #43     SliverMultiBoxAdaptorElement.createChild (package:flutter/src/widgets/sliver.dart:1006:11)
I/flutter (23143): #44     RenderSliverMultiBoxAdaptor._createOrObtainChild.<anonymous closure> (package:flutter/src/rendering/sliver_multi_box_adaptor.dart:274:23)
I/flutter (23143): #45     RenderObject.invokeLayoutCallback.<anonymous closure> (package:flutter/src/rendering/object.dart:1730:58)
I/flutter (23143): #46     PipelineOwner._enableMutationsToDirtySubtrees (package:flutter/src/rendering/object.dart:799:15)
I/flutter (23143): #47     RenderObject.invokeLayoutCallback (package:flutter/src/rendering/object.dart:1730:13)
I/flutter (23143): #48     RenderSliverMultiBoxAdaptor._createOrObtainChild (package:flutter/src/rendering/sliver_multi_box_adaptor.dart:263:5)
I/flutter (23143): #49     RenderSliverMultiBoxAdaptor.insertAndLayoutChild (package:flutter/src/rendering/sliver_multi_box_adaptor.dart:401:5)
I/flutter (23143): #50     RenderSliverGrid.performLayout (package:flutter/src/rendering/sliver_grid.dart:583:17)
I/flutter (23143): #51     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #52     RenderSliverPadding.performLayout (package:flutter/src/rendering/sliver_padding.dart:182:11)
I/flutter (23143): #53     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #54     RenderViewportBase.layoutChildSequence (package:flutter/src/rendering/viewport.dart:405:13)
I/flutter (23143): #55     RenderViewport._attemptLayout (package:flutter/src/rendering/viewport.dart:1316:12)
I/flutter (23143): #56     RenderViewport.performLayout (package:flutter/src/rendering/viewport.dart:1234:20)
I/flutter (23143): #57     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #58     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #59     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #60     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #61     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #62     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #63     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #64     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #65     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #66     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #67     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #68     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #69     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #70     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #71     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #72     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.performLayout (package:flutter/src/rendering/proxy_box.dart:104:13)
I/flutter (23143): #73     RenderObject.layout (package:flutter/src/rendering/object.dart:1634:7)
I/flutter (23143): #74     MultiChildLayoutDelegate.layoutChild (package:flutter/src/rendering/custom_layout.dart:142:11)
I/flutter (23143): #75     _ScaffoldLayout.performLayout (package:flutter/src/material/scaffold.dart:339:7)
I/flutter (23143): #76     MultiChildLayoutDelegate._callPerformLayout (package:flutter/src/rendering/custom_layout.dart:212:7)
I/flutter (23143): #77     RenderCustomMultiChildLayoutBox.performLayout (package:flutter/src/rendering/custom_layout.dart:356:14)
I/flutter (23143): #78     RenderObject._layoutWithoutResize (package:flutter/src/rendering/object.dart:1509:7)
I/flutter (23143): #79     PipelineOwner.flushLayout (package:flutter/src/rendering/object.dart:768:18)
I/flutter (23143): #80     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding&PaintingBinding&SemanticsBinding&RendererBinding.drawFrame (package:flutter/src/rendering/binding.dart:281:19)
I/flutter (23143): #81     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding&PaintingBinding&SemanticsBinding&RendererBinding&WidgetsBinding.drawFrame (package:flutter/src/widgets/binding.dart:677:13)
I/flutter (23143): #82     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding&PaintingBinding&SemanticsBinding&RendererBinding._handlePersistentFrameCallback (package:flutter/src/rendering/binding.dart:219:5)
I/flutter (23143): #83     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding._invokeFrameCallback (package:flutter/src/scheduler/binding.dart:990:15)
I/flutter (23143): #84     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding.handleDrawFrame (package:flutter/src/scheduler/binding.dart:930:9)
I/flutter (23143): #85     _WidgetsFlutterBinding&BindingBase&GestureBinding&ServicesBinding&SchedulerBinding._handleDrawFrame (package:flutter/src/scheduler/binding.dart:842:5)
I/flutter (23143): #86     _invoke (dart:ui/hooks.dart:154:13)
I/flutter (23143): #87     _drawFrame (dart:ui/hooks.dart:143:3)
I/flutter (23143):
I/flutter (23143): Image provider: AssetImage(bundle: null, name: "assets/rooms/item4.jpg")
I/flutter (23143): Image key: AssetBundleImageKey(bundle: PlatformAssetBundle#3e8f0(), name: "assets/rooms/item4.jpg",
I/flutter (23143): scale: 1.0)
I/flutter (23143): ════════════════════════════════════════════════════════════════════════════════════════════════════
```

</p>
</details>

So, how did we get there?


### <a name='part_i'></a>The Past

- First "generation" of SDKs and languages (Objective-C and Java)
- Specialized skills, although developers cheered a "lower level" entry barrier (compared to what was available at the time)
- Marketplace! Woohoo!!11!
- Attract developers to sell apps: more users => more apps => platform dominates the market (caveat: Google has always had in mind to sell ads since acquiring Android)

### <a name='part_ii'></a>The Present

- Second "generation" of SDKs and laguages (Swift and Dart a.k.a. Javascript on steroids)
- Convergence of skills, even lower entry barrier
- Marketplace: overflowing of low quality ads-riddled apps
- Moving features on the cloud, smartphones becoming again dumb terminals
- SDKs sell cloud services

### <a name='part_iii'></a>The Future

- Big players offering training and tools for nothing
- Less and less work to build an app (tipically involving backend and frontend work)
- An army of devs willing to make a quick buck and selling users' data using their apps. This is <a target="_blank" rel="noopener noreferrer nofollow" href="https://media.ccc.de/v/35c3-9941-how_facebook_tracks_you_on_android">already happening</a>.


So, Flutter documentation is great, the tutorial on dedicated websites are clear. The language logo is not dumb. What could possibly go wrong?

Google is basically upselling Firebase services.

Half joking here, but it wouldn't surprise me <strong>at all</strong> if Facebook would make its SDK more and more pervasive to the point of releasing its own operating system.
