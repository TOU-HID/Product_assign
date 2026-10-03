# Step 4 — First FlatList / সহজ ব্যাখ্যা

**Now built:** API products → TanStack cache → FlatList, with loading, retry, refresh, and offline browsing.

**বাংলা:** API থেকে products এনে Query cache-এ রাখি; FlatList দেখায়। loading/error/offline অবস্থাগুলো আলাদাভাবে সামলাই।

## 1. Read these files in order

| File | Purpose | বাংলা |
| --- | --- | --- |
| `src/features/products/useProducts.ts` | Connect `fetchProducts(signal)` to `useQuery` with `['products', 'catalog']`. | একই catalog-এর query/cache ব্যবহার করে। |
| `src/lib/useOnlineStatus.ts` | Subscribe to the existing `onlineManager` using `useSyncExternalStore`. | network বদলালে screen update হয়; নতুন NetInfo listener লাগে না। |
| `src/features/products/ProductCard.tsx` | Show title, API price, stock, and an 88×88 thumbnail or placeholder. | পণ্যের card; image না থাকলে/ব্যর্থ হলে/offline হলে placeholder। |
| `src/features/products/ProductsScreen.tsx` | Choose the right state and render a typed `FlatList<Product>`. | পরিস্থিতি বুঝে list/message/Retry দেখায়। |
| `src/lib/queryPersistence.ts` | Validate saved products before hydration; discard unusable cache and handle storage failures. | saved data দেখানোর আগে যাচাই করে; খারাপ cache বাদ দেয়। storage ব্যর্থ হলেও app চলে। |
| `App.tsx` | Mount the screen after restoration and initial connection readiness; apply safe-area padding once. | cache/network check শেষ হলে screen দেখায়; notch/system bar-এর জায়গা রাখে। |

## 2. Screen decisions

| Situation | What happens / কী হবে |
| --- | --- |
| Restoring storage | “Restoring saved products…”; queries wait। আগে saved cache ফেরত আসে। |
| Offline, no catalog | “Connect to load products”; no endless spinner। paused request চলমান request নয়। |
| First active request | Spinner + “Loading products…”। শুধু সত্যিই fetch হলে spinner। |
| First request fails | Error + Retry। আবার চেষ্টা করা যায়। |
| Data exists, refresh fails | Keep the list + notice + Retry। আগের ভালো products সরাই না। |
| Offline, data exists | Keep list + offline notice + last-updated time; disable refresh। পুরোনো data দেখি, নতুন stock নিশ্চিত নয়। |
| Refreshing existing data | Keep list; show refresh indicator। পুরোনো list রেখেই নতুন data আনি। |
| Empty successful response | “No products available”; pull-to-refresh still works। খালি ফলাফল error নয়। |
| Storage fails | Show a storage notice; online browsing still works। restart-এর পরে data পাওয়া নিশ্চিত বলি না। |

`hasData` means `data !== undefined`, so a valid empty array still counts as a successful catalog. `isLoading` means first active fetch; `isFetching` also includes refresh. A paused query can be pending without fetching.

**বাংলা:** `[]` একটি valid ফলাফল। `isPending` দেখেই spinner দিলে offline-এ চিরকাল spinner থাকতে পারে। তাই fetch চলছে কি না দেখি।

## 3. Why these choices?

- **Static query key:** local search will reuse the same catalog. / পরে local search-এর text বদলালে আবার API call লাগবে না।
- **Stable ID keys:** `String(item.id)` identifies rows across refreshes. / index দিয়ে পণ্যের পরিচয় রাখি না।
- **One vertical FlatList:** renders a window of rows; no surrounding vertical ScrollView. / সব card একসঙ্গে render করতে হয় না; তবে সব catalog download এখনও লাগে।
- **No duplicated request state:** Query owns data/loading/error; card state only remembers a failed image URL. / loading/error আলাদা `useState`-এ রাখিনি।
- **Price as supplied:** display the API number to two decimals; currency/conversion is not invented. / নিজের মতো BDT বা discount হিসাব যোগ করিনি।
- **Safe cached recovery:** reuse `validateProducts()`, preserve last successful update time, and let the provider enforce 24-hour expiry + `products-v1`. / পুরোনো/ভুল cache যাচাই করে সামলাই।

## 4. Run and verify yourself

From `ShopDiscover`:

```bash
yarn android --device emulator-5552
yarn ios --udid 20425173-4F93-4645-908F-B47F27028F4F
yarn tsc --noEmit
yarn lint
yarn test --runInBand --watch=false
```

Device IDs above are the devices used in this session. Choose your actual device if they change.

**Offline restart:** use a release build (`yarn android --mode release` / `yarn ios --mode Release`), load online, allow the storage write to finish and verify the saved copy, fully close the app, disconnect the device, and reopen it. Expect products + offline notice + image placeholders. Reconnect after one minute; stale data refreshes. Test an empty cache offline separately: expect “Connect to load products.”

**বাংলা:** release build-এ JavaScript app-এর ভেতর থাকে। তাই Metro ছাড়াই সত্যিকারের offline restart দেখানো যায়। শুধু thumbnail URL save হয়, image file নয়।

**iOS build fix:** this Xcode rejected AsyncStorage's resource bundle's iOS 13 target. `ios/Podfile` now sets that bundle to React Native's minimum (15.1) after pod installation. Generated Pods files are not manually edited. This session used `rbenv exec bundle exec pod install` because the plain command selected system Ruby instead of the project's Ruby 3.1.6.

**বাংলা:** একটি dependency-র resource target পুরোনো ছিল। Podfile-এ app-এর minimum version মিলিয়েছি, যাতে আবার Pods install করলেও fix থাকে।

## 5. Verification — কী যাচাই হয়েছে

AI-assisted checks on 3 October 2026:

- **Code:** TypeScript, lint, and all **four tests passed**. Tests cover startup, native listeners/fallback, list/retry/paused/refresh behavior, and valid/expired/incompatible/corrupt cache plus storage failure.
- **Android 13 phone emulator:** debug + ARM64 release builds passed; 194 products rendered. The actual SQLite cache held 194 products. Fully stopping and reopening the release app with Wi-Fi/mobile data disabled restored all products, offline notice, last-updated time, and image placeholders; scrolling worked. Clearing only the demo app's data offline showed “Connect to load products” without a spinner. Reconnecting loaded 194 products again. A native pull-to-refresh gesture updated the last-successful timestamp. The debug app was reinstalled afterward for continued development.
- **iPhone 15 Pro / iOS 17.5:** debug build and the 194-product list passed. A temporary HTTP-404 endpoint kept the list visible with the refresh-error notice and Retry. The normal endpoint was restored, and the list recovered with a newer update time.

**Still verify manually:** an iOS release-build offline restart before recording the final assignment demo. Automated cache/network checks do not replace that native demonstration.

**বাংলা:** Android-এ আসল offline restart ও empty-cache পরীক্ষা করেছি। iOS-এ list এবং failed refresh-এর পরে আগের data রাখা যাচাই হয়েছে। iOS release offline restart নিজে চালিয়ে final video-তে দেখাতে হবে।

Screenshots: [Android online](./screenshots/step4-android-online.png), [Android offline](./screenshots/step4-android-offline.png), [empty cache offline](./screenshots/step4-android-empty-offline.png), [iOS online](./screenshots/step4-ios-online.png), [iOS refresh failure](./screenshots/step4-ios-refresh-error.png).

References: [FlatList](https://reactnative.dev/docs/flatlist), [persistent query cache](https://tanstack.com/query/latest/docs/framework/react/plugins/persistQueryClient).
