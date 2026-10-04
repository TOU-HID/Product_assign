# Discofy / ShopDiscover

A React Native shopping discovery demo with real DummyJSON products, local search, stock and price filters, product details, preserved browsing state, and a saved catalog for offline use.

Application code lives in `ShopDiscover/`; Markdown lives in the parent `docs/`. Include both and the evidence when submitting.

## Setup and run

Use Node 22.11+, the project's Yarn 3.6.4, JDK 17 and Android SDK for Android, and Xcode plus Bundler/CocoaPods for iOS. The project uses React Native 0.87.1 and React 19.2.3. [Detailed environment setup](./setup.md).

```bash
cd ShopDiscover
yarn install --immutable
rbenv exec bundle install
cd ios
rbenv exec bundle exec pod install
cd ..
yarn start
```

Keep Metro running. In separate terminals, from `ShopDiscover/`:

```bash
yarn android
yarn ios --simulator="YOUR INSTALLED IPHONE SIMULATOR"
```

Use `bundle` without `rbenv exec` if your selected Ruby already matches the project's setup. Rebuild both native apps after native dependency changes; Metro reload cannot link navigation/screens.

## Behavior and architecture

- `api.ts` fetches and validates the complete selected-field catalog, with a 10-second timeout and query cancellation.
- TanStack Query owns server data. AsyncStorage saves the catalog and validates restoration. Data becomes stale after one minute; saved cache expires after 24 hours. Reconnect/focus can refresh stale data. Automatic retries are disabled; errors offer explicit Retry.
- Pure search/filter functions derive results over the whole cached catalog. React state owns search and applied filters; `ProductFilters` owns price drafts and validation feedback. Invalid ranges leave applied results intact; Reset clears all choices and errors.
- FlatList uses product-ID keys. Native-stack navigation keeps Products mounted; details receive an ID and reuse the catalog. Details/back and refresh do not intentionally reset scrolling.

Exact `phone`, `phones`, `smartphone` and `smartphones` queries select smartphones. Exact `phone charger`/`phone chargers` queries select charger-titled mobile accessories. Other queries match every whole word across title, brand, category and tags; title matches rank first. Search typing makes no new API request.

Stock means `stock > 0`. Optional price bounds are inclusive; blank means no bound and zero is valid. `cheap phone` does not infer a budget: search `phone` and set a maximum. `red dress` stays empty if both words cannot be established. Cached prices/stock can be stale. Thumbnail URLs do not guarantee offline images; there is a fallback. Cart, login and delivery promises are outside scope.

## Verification

From `ShopDiscover/`:

```bash
yarn tsc --noEmit
yarn lint
yarn test --runInBand --watch=false --watchman=false
```

On 4 October 2026, type checking, lint and all **18 tests in 7 suites** passed. Coverage includes alias/accessory intent, complete-catalog inclusive filtering, invalid drafts/reset, cached details/back, failures, timeout/cancellation, persistence validation and offline/reconnect behavior.

Both ARM64 release builds passed. Native checks on Pixel 6 Pro API 33 (Android 13) and iPhone 17 Pro (iOS 26.5) verified search, stock/price, details/back, preserved position and reset. Android also passed real offline cold restart/details/reconnect; iOS passed header back and edge-swipe position checks. iOS XCTest input updates were allowed to settle between synthesized keys. [Native logs and screenshots](./evidence/native/README.md). Real iOS offline cold restart remains unverified; see [session status](./session-status.md).

[Fresh search measurement](./search-measurement.md): smartphone precision in the first five for `phone` is **0/5** for literal API search and **5/5** for local search. Raw responses, timestamps and a reproducible script are included. This measures one intent, not conversion, speed, general language understanding or scale.

## Network demonstration

1. Load online; wait for products and at least two seconds for the one-second persistence throttle.
2. Search/filter, scroll, open details and return. Compare text, filters, results and position.
3. Disable test-device connectivity. Terminate and relaunch a **release** build without Metro. Saved products should restore; local search/filter/details should work with an offline notice.
4. Restore connectivity. Stale data may refresh while UI choices remain. A failed refresh should retain cached products and offer Retry.
5. Check first launch offline with no usable saved cache: “Connect to load products,” without an endless spinner.

API tests simulate slow responses, HTTP/network errors, malformed data and cancellation. These are distinct from real device connectivity checks. Metro reload is not a cold restart. iOS Simulator shares host networking; use a real test device or a network control that does not disrupt unrelated host traffic.

## Submission

Read [decisions](./DECISIONS.md), [AI usage](./AI_USAGE.md), and [session status](./session-status.md). The final 2–4 minute narrated recording of both platforms and personal reflection/interview practice remain user deliverables. Do not claim unrecorded native checks as complete.
