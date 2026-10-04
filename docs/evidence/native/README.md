# Native verification — 4 October 2026

Both release builds passed. These checks used emulators/simulators, not physical devices. [Build summary](./build-results.txt), [platform/result metadata](./results.json).

## Android

Pixel 6 Pro API 33, Android 13, 1440 × 3120, ARM64 release. [Passing check log](./android-checks.log), [timestamps](./android-checks.json), [verification script](./android_flow.py).

Verified live catalog counts: browse 194; `phone` 16; stock 15; maximum price 500 gives 12. Scroll → details → hardware back retained the product card's exact bounds, search, filters and price draft. Reset restored 194. After connectivity was disabled, force-stop/relaunch restored saved products; search/details/back worked offline. Reconnect cleared the offline notice and retained search. Original Wi-Fi and mobile-data settings were restored in `finally`.

Screenshots and matching accessibility XML:

- [Online browse](./android-online.png)
- [Phone search](./android-phone-search.png)
- [Filtered, scrolled list](./android-filtered-scrolled.png)
- [Details](./android-details.png)
- [Back with preserved position](./android-back-preserved.png)
- [Reset](./android-reset.png)
- [Offline cold restart](./android-offline-restart.png)
- [Offline details](./android-offline-details.png)
- [Offline back](./android-offline-back.png)
- [Reconnected](./android-reconnected.png)

Earlier host memory pressure produced an emulator System UI wait dialog. The passing run followed an emulator reboot; it did not encounter the dialog. Do not attribute that earlier system failure to the app.

## iOS

iPhone 17 Pro, iOS 26.5; ARM64 release built using Xcode 27.0 and simulator SDK 27.0. [Passing discovery check](./ios-checks.log), [passing swipe check](./ios-swipe-check.log), [XCTest source](./NativeFlowTests.swift), [temporary project generator](./create_project.rb).

Discovery check verified search → stock → maximum 500 → scroll → details → header back, retained query/range/draft/results, and the same card position within three points, followed by Reset. A separate edge-swipe check preserved browsing position. These are two individually passing native XCTest cases, separate from the 18 Jest tests.

- [Online browse](./ios/9800B9ED-FC26-436E-B91F-881A97968335.png)
- [Phone search](./ios/BD9651B6-D2A6-4462-99CD-30B3700E0805.png)
- [Filtered, scrolled list](./ios/162A03E5-3568-4CED-8847-92B8D67C7E79.png)
- [Details](./ios/C65107E6-6EE4-486E-8F49-1762104FF257.png)
- [Header back with preserved position](./ios/DDA421B9-AEE5-4254-9401-C8094B834F2F.png)
- [Reset](./ios/AA06D077-EA0C-41F8-92B2-C309D6073D89.png)
- [Edge-swipe back with preserved position](./ios-swipe/ECF6D288-F8E6-47EA-A9A6-81140A2DFA8C.png)

Exported XCTest manifests preserve attachment identity/device/timestamps: [discovery](./ios/manifest.json), [swipe](./ios-swipe/manifest.json).

Initial automation attempts failed at keyboard focus and then rapid batch typing, which left only `p` in search. [Initial attempt](./ios-initial-attempt.log), [second attempt](./ios-second-attempt.log). The passing harness uses an explicit input coordinate and waits for each controlled field update before synthesizing the next character. This proves the recorded flow under that timing; it does not establish arbitrary rapid-input behavior.

**Real iOS offline cold restart and reconnect were not verified.** Simulator networking shares the host; no host network settings were changed. Jest offline/cache simulations do not replace that native check.

## Reproduction notes

The scripts are evidence helpers for this Mac/project and recorded device configuration, rather than a portable app test framework. They use the recorded 194-product live dataset, local project paths and simulator IDs. Update those assumptions if the environment/API changes.

Android: install a release APK on `emulator-5554`, then run the saved Python script with host/device access. It temporarily changes emulator connectivity and restores the previous settings. It requires the recorded screen resolution for gestures.

iOS: copy `NativeFlowTests.swift` and `create_project.rb` to `/private/tmp/shopdiscover-native-checks/`; from `ShopDiscover/`, run `rbenv exec bundle exec ruby /private/tmp/shopdiscover-native-checks/create_project.rb`. Install the release app with `simctl`, then run `xcodebuild test` for the generated `NativeChecks` scheme and your simulator destination. Use distinct result-bundle paths. No permanent app demo mode or application source modification was introduced by these helpers.
