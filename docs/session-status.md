# Resume point — 4 October 2026

This is the current handoff. Older step plans describe the intended sequence rather than completed verification.

## Existing implementation

Steps 5–7 are implemented in `ShopDiscover/`: local search, stock and inclusive price filters, reset, native-stack details and cached product lookup. Do not recreate them. These edits were already present when this continuation began and are now saved in the application repository.

## Verified in this session

- TypeScript and lint passed.
- Jest: 18 tests in seven suites passed. Includes search/accessory intent, full-catalog filtering, invalid drafts/reset, details/back state and list-instance continuity, API errors/timeouts/cancellation, persistence and connection lifecycle.
- Fresh search comparison: `phone` has 0/5 smartphone-category results in literal API search and 5/5 in local search. Raw snapshots and reproducible script are in [search measurement](./search-measurement.md).
- Starter README replaced with the actual setup/architecture/checks. [Decisions](./DECISIONS.md) and [AI usage](./AI_USAGE.md) drafted from observable evidence; user reflection/recording remain outstanding.

## Native verification

The initial concurrent native builds caused heavy memory pressure on this 8 GB Mac. They were interrupted and verification changed to sequential builds with fewer workers. Do not count interrupted builds as passing.

**Android passed:** release build for Pixel 6 Pro API 33 (Android 13), ARM64, with `assembleRelease -PreactNativeArchitectures=arm64-v8a --max-workers=2`. Real UI checks passed: 194-product browse; `phone` → 16 results; stock → 15; maximum 500 → 12; scroll → details → hardware back with identical product-card bounds; retained price draft; Reset → 194; force-stop/relaunch offline with saved catalog; offline search/details/back; reconnect while retaining search. The emulator's original Wi-Fi/mobile-data settings were restored. [Check log](./evidence/native/android-checks.log), [capture timestamps](./evidence/native/android-checks.json), and PNG/XML evidence are in `docs/evidence/native/`.

**iOS passed:** Xcode 27.0, simulator SDK 27.0, ARM64 release, using `-jobs 2 ARCHS=arm64 ONLY_ACTIVE_ARCH=YES`. Installed on iPhone 17 Pro, iOS 26.5. XCTest verified search → stock → maximum 500 → scroll → details → header back, retaining search/applied range/draft/results and card position within three points, then Reset. A separate passing test verified edge-swipe back preserves browsing position. Initial automation attempts failed at focus and rapid batched typing; the passing test taps explicitly and waits for each controlled input update before the next synthesized key. Failed-attempt logs are retained rather than treating them as passing. [Native evidence index](./evidence/native/README.md). **Real iOS offline cold restart/reconnect remains unverified.**

Temporary verification scripts are under `/private/tmp/shopdiscover-native-checks/`. They exercise real native UI without introducing a permanent app demo mode. Build logs are under `/private/tmp/shopdiscover-*-build.log`. Keep any completed evidence under `docs/evidence/native/` before ending a session.

## Remaining work

1. Verify iOS saved-cache offline cold restart and recovery using a real test device or appropriate network control. iOS Simulator shares host networking; this session did not change host networking. Android's real cold-restart/reconnect check passed. Distinguish native evidence from controlled Jest mocks.
2. Review the docs and add the user's actual reflection and any earlier AI interactions they remember.
3. Record the final 2–4 minute narrated demonstration of both platforms and practice modifying the rules/timeout.
4. Include both the application repository and parent documentation/evidence in the submission. The parent repository records the updated application commit.

Application changes are saved in `ShopDiscover/`; documentation, measurement, native evidence and the updated application reference are saved in the parent repository. Both commits use the configured user identity. Both emulators started for verification were stopped after capturing evidence; Android's connection settings were restored first.
