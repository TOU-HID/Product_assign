# Steps 2–4: build the first product list

এই guide অনুসরণ করে নিজে code লিখব। লক্ষ্য: **API থেকে পণ্য এনে একটি নির্ভরযোগ্য FlatList দেখানো**। এই ধাপে search, filter বা navigation বানাব না।

This plan stays in `product_assignment/docs`. All application files below belong inside `ShopDiscover/`.

## First: decide Step 1 — আগে search পদ্ধতি বেছে নিই

| Choice | Easy explanation | Tradeoff |
| --- | --- | --- |
| **API-first** | প্রতিটি query-তে API call; পরিচিত phone query category endpoint-এ পাঠাব। | কম download; কিন্তু API-এর খারাপ matching এবং এক page filter করার সমস্যা সাবধানে সামলাতে হবে। |
| **Local catalog — recommended for this demo** | ছোট catalog API থেকে এনে cache করব। পরে app-এর TypeScript function দিয়ে search/filter করব। | নিয়ম বোঝা ও সম্পূর্ণ filter সহজ; শুরুতে download লাগে, stock পুরোনো হতে পারে, ৪০,০০০ পণ্যে একই পদ্ধতি ধরে নেওয়া যাবে না। |

**My recommendation:** local catalog for this assignment's small dataset. The investigation found 194 products. It lets you demonstrate clear search rules and avoids incomplete page filtering. API-first is more attractive for a large catalog when the API supports the search/filter behavior you need.

**সহজভাবে:** সব পণ্যের ছোট তালিকা এনে নিজের বোঝা নিয়মে search/filter করব। TanStack Query ওই তালিকা fetch/cache করবে; FlatList ফলাফল দেখাবে। প্রতি keystroke-এ নতুন API call লাগবে না।

This is still your decision. The steps below assume you choose local catalog. If you choose API-first, query keys, request parameters, and pagination need a different plan.

If you choose it, write your reason in your own words:

> I chose local search for the small demo catalog because I can apply clear relevance rules and filter the complete dataset. I accept initial download and stale-data costs. At 40,000 products, full-catalog loading needs reconsideration.

Do not claim it fixes every query or scales automatically. **Updated decision:** persist the TanStack product cache in AsyncStorage so saved catalog data survives app restarts. FlatList does not reduce catalog download size. Offline browsing requires a previously saved, compatible cache; images and live stock are not guaranteed offline.

## Files to create — কোন file কী করবে

From `ShopDiscover`, create folders:

```bash
mkdir -p src/lib src/features/products
```

| File | Responsibility / কাজ |
| --- | --- |
| `src/lib/queryClient.ts` | One shared QueryClient; cache/retry settings। |
| `src/lib/queryPersistence.ts` | AsyncStorage persister, cache key/version and restore policy; app বন্ধের পর data রাখবে। |
| `src/lib/queryLifecycle.ts` | NetInfo → onlineManager and AppState → focusManager, with cleanup; reconnect/focus refresh। |
| `src/features/products/types.ts` | Product type; কোন field কী ধরনের data। |
| `src/features/products/api.ts` | Fetch, validate, timeout/cancellation; API-এর কাজ। |
| `src/features/products/useProducts.ts` | Query key + `useQuery`; API ও screen-এর সংযোগ। |
| `src/features/products/ProductCard.tsx` | One product's thumbnail, title, price, stock label। |
| `src/features/products/ProductsScreen.tsx` | FlatList এবং loading/error/empty states। |
| Existing `App.tsx` | Provider + ProductsScreen; app-এর মূল সংযোগ। |

Create each file when its step begins; you do not need to write everything at once.

## Step 2 — connect TanStack Query with persistent storage

### Do this

```bash
cd /Users/md.touhidulislam/Projects/product_assignment/ShopDiscover
yarn add @tanstack/react-query@5 @tanstack/react-query-persist-client@5 @tanstack/query-async-storage-persister@5 @react-native-async-storage/async-storage @react-native-community/netinfo
cd ios
bundle exec pod install
cd ..
```

These are deliberate dependencies: Query handles API state; its two persistence packages save/restore the cache; AsyncStorage stores JSON on the device; NetInfo supplies native connection status. Rebuild Android/iOS after installing native packages; Metro reload alone is insufficient.

1. In `queryClient.ts`, import `QueryClient`, create it **outside a React component**, and export it. Otherwise renders could recreate your cache.
2. In `queryPersistence.ts`, create one storage instance and one `createAsyncStoragePersister`. Use a dedicated key such as `shopdiscover-product-cache`, `throttleTime: 1000`, and the settings below. Do not separately save every product in React state or write the same catalog to another storage key.
3. AsyncStorage's current upstream API uses `createAsyncStorage('shopdiscover')`. Check the installed version's exports: older versions use a default `AsyncStorage` object. Pass the resulting storage object to `createAsyncStoragePersister({ storage, key, throttleTime })`; it needs `getItem`, `setItem`, and `removeItem`.
4. In `App.tsx`, use **PersistQueryClientProvider** from `@tanstack/react-query-persist-client` with `client` and `persistOptions`. It replaces ordinary QueryClientProvider and coordinates cache restoration before fetching. Keep `SafeAreaProvider`.
5. In `queryLifecycle.ts`, connect NetInfo to `onlineManager` using its initial state and subscription. Explicitly disconnected/unreachable means offline; unknown reachability is not proof of offline. Connect `AppState` active/background changes to `focusManager`. Register once, remove listeners on cleanup, and avoid fetching before the initial connection check completes. If that check fails, let the bounded request/error path handle uncertainty.
6. Initially show a simple “Products” heading; fetching starts in Step 3/4. Remove unused starter imports. Show “Restoring saved products…” while `useIsRestoring()` is true.

**বাংলা:** QueryClient memory-তে data রাখে। persister সেটি AsyncStorage-এ save করে; app আবার খুললে provider data ফিরিয়ে আনে। NetInfo internet-এর অবস্থা জানায়। app restart করেও saved catalog ব্যবহার করতে পারব।

### Starting settings — এগুলো প্রস্তাব, নিজের কারণ বুঝে ব্যবহার করব

| Setting | Value | Reason / কারণ |
| --- | --- | --- |
| `retry` | `false` | First version uses explicit Retry; repeated hidden attempts will not prolong waiting। |
| `staleTime` | `60_000` | Data stays fresh for one minute; avoid needless immediate requests। এটি stock সঠিক থাকার নিশ্চয়তা নয়। |
| `gcTime` | `24 * 60 * 60_000` | Keep unused queries for 24 hours; must be at least persistence `maxAge`। |
| `networkMode` | `'online'` | Network requests pause when known offline; restored data can still render। |
| `refetchOnReconnect` | `true` | Recheck stale data after connection returns। |
| `refetchOnWindowFocus` | `true` | With the AppState bridge, recheck stale data on app activation। |
| Persistence `maxAge` | `24 * 60 * 60_000` | Discard saved snapshots older than 24 hours on restore; this is a chosen policy, not guaranteed availability। |
| Persistence `buster` | `'products-v1'` | Change when cached product shape becomes incompatible। |

Put query settings under `defaultOptions.queries`. Put `persister`, `maxAge`, `buster`, and dehydration rules under the provider's `persistOptions`. This **replaces the previous ten-minute gcTime**.

Persist only the `['products', 'catalog']` query when it contains validated data. Use a `shouldDehydrateQuery` predicate checking its exact key and `query.state.data !== undefined`; keep the last good data eligible even if a later refresh failed. Set `shouldDehydrateMutation` to return false. Validate restored catalog data with the same product validator before rendering; reject incompatible/corrupt cached data and recover with an online fetch or a clear offline message. Storage failures must not crash the online app or promise that saving succeeded.

**বাংলা:** staleTime মানে কখন data আবার যাচাই করা দরকার। gcTime মানে unused memory cache কতক্ষণ থাকবে। maxAge মানে পুরোনো saved snapshot restore করার সীমা। এগুলো আলাদা। ২৪ ঘণ্টা একটি demo policy; data এক মিনিট পর stale হলেও offline-এ দেখানো যাবে, সঙ্গে last-updated তথ্য।

**Done when:** both platforms show the heading with no provider/native-module errors; type/lint checks pass. Full persistence verification needs real product data in Step 4. Commit this wiring step.

## Step 3 — write the product API function

**Progress:** A/B implemented in `types.ts` and `api.ts`; TypeScript/lint and local request/validation checks passed. Read [the short bilingual explanation](./product-api-explained.md). Step 4 screen integration remains next.

### A. Define the data you actually need

In `types.ts`, define `Product`:

- Required: `id`, `title`, `description`, `category`, `price`, `stock`, `tags`.
- Optional display data: `thumbnail`, `brand`.
- ID: positive integer; price: finite nonnegative number; stock: nonnegative integer; title/category: nonempty strings.
- Validate description as a string and tags as an array of strings. Normalize missing optional thumbnail/brand to an absent value.

**বাংলা:** TypeScript type লিখলেই API data নিরাপদ হয়ে যায় না। response আসার পর বাস্তবে field-এর type/value পরীক্ষা করতে হবে।

### B. Request the small catalog

Use this URL in `api.ts`:

```text
https://dummyjson.com/products?limit=0&select=title,description,category,price,stock,tags,thumbnail,brand
```

`limit=0` requests all products. `select` requests only these fields; the investigated API also includes IDs. Verify that remains true before trusting the response.

Write a function with this contract:

```ts
fetchProducts(signal: AbortSignal): Promise<Product[]>
```

Follow this order:

1. Use built-in `fetch`; another HTTP library is unnecessary for this step.
2. If TanStack's signal is already aborted, stop. Otherwise forward its cancellation to a request `AbortController`.
3. Start a **10-second timeout** that aborts the request. This is a starting UX choice above the supplied 3.8-second p90, not a guarantee that every valid request finishes in time.
4. Fetch with the request controller's signal. Check `response.ok` before trusting JSON.
5. Read JSON as `unknown`; validate the response object, `products` array, each record, and unique IDs. For this full-catalog strategy, check that the valid returned count matches the response's valid `total`.
6. Reject malformed required data with an understandable error. Do not silently return an incomplete catalog and call its filters complete. Optional missing images get a fallback later.
7. Return the validated `Product[]`. In `finally`, clear the timer and remove the external abort listener, whether the request succeeded or failed.

**বাংলা:** fetch সফল হলেও data ভুল হতে পারে। timeout আর TanStack cancellation দুটোই রাখতে হবে। শুধু timer দিয়ে error দেখিয়ে background-এ request চালু রাখা ঠিক নয়। timeout error ও সাধারণ cancellation আলাদা রাখব।

**Done when:** you can explain the function from request to validation/error. The successful response includes all products and IDs; type/lint checks pass. A small temporary manual call is fine if needed; remove temporary debugging afterward. Commit the step.

## Step 4 — render the first FlatList

**Progress:** hook, cards, screen states, pull-to-refresh, and restored-cache validation are implemented. TypeScript/lint/four tests pass. Both native debug builds render the catalog; Android release offline/empty-cache restart and iOS controlled refresh failure were checked. iOS release offline restart remains a manual verification before the final demo. See [the short bilingual explanation](./products-list-explained.md) for file responsibilities, screenshots, and verification.

### A. Add the hook

In `useProducts.ts`, connect your function:

```ts
useQuery({
  queryKey: ['products', 'catalog'],
  queryFn: ({ signal }) => fetchProducts(signal),
})
```

Return the query result from `useProducts()`. The static key is correct because this request loads the same catalog. Later local search text/filter values belong in React state, not this query key. A changed API request needs an appropriate changed key.

**বাংলা:** একই catalog-এর cache ব্যবহার করব। পরে local search-এর text বদলালেই আবার API request করব না।

### B. Render these states in ProductsScreen

| Situation | Screen behavior / কী দেখাব |
| --- | --- |
| Saved cache being restored | “Restoring saved products…”; use `useIsRestoring()`। |
| Offline with no saved catalog | “Connect to load products”; a paused query is not a running request। |
| Offline with restored catalog | Keep FlatList; “Offline — showing saved products” + last-updated time। |
| No data yet, request running | “Loading products…” + ActivityIndicator। |
| No data, request failed | Short error + Retry button calling `refetch()`; disable it while fetching। |
| Successful response with zero products | “No products available”; network error বলব না। |
| Products available | FlatList + product count। |
| Existing products being refreshed | Keep list visible; show a small refreshing indicator। |
| Refresh fails with cached products | Keep list; show “Could not refresh; showing previous data” + Retry। |

Handle restoration first, then cached data/offline/paused states, then an actual initial request. `isPending` alone must not control the spinner: a query can be pending with `fetchStatus === 'paused'`. Use `isLoading` for initial active fetching and `isFetching` for active requests. Display `dataUpdatedAt` as the last successful update time. Disable Retry/pull-to-refresh while known offline or fetching; stale queries can refetch on reconnect. Reconnection may be detected before the API is reachable, so keep the timeout/error/manual Retry path.

Check whether `data` exists before replacing the whole screen with an error; a failed refresh can still have cached data. Derive request status from the query result; do not keep a second loading/error state in `useState`.

### C. Build the list and cards

1. Render a typed `FlatList<Product>` with `data`, `renderItem`, and `keyExtractor={(item) => String(item.id)}`.
2. Start with a single-column list. Keep the screen at `flex: 1`, apply safe-area padding, and avoid nesting it inside another vertical ScrollView.
3. Each card shows thumbnail, title, API price, and stock label. Use fixed thumbnail dimensions; missing/failed images show a placeholder. Do not invent BDT conversion or discount calculations.
4. Keep these stock labels separate: positive stock → “In stock”; zero → “Out of stock”. This is not the filter yet.
5. Add pull-to-refresh using `onRefresh` and a boolean `refreshing` that represents a refresh with existing data.

**বাংলা:** আগে একটি সহজ, scroll করা যায় এমন list বানাব। stable ID key ব্যবহার করব। data থাকা অবস্থায় refresh ব্যর্থ হলে পুরো list সরাব না।

### D. Check your work

```bash
yarn tsc --noEmit
yarn lint
```

Run on Android and iOS. Confirm cards, safe areas, scrolling, image fallback, and refresh work. A known offline query pauses; to test an actual failed request, stay connected and inject a controlled error or unreachable endpoint, then restore it before committing.

**Offline restart demo:** load products online, allow the throttled storage write to finish, verify it completed, and fully terminate the app. Disconnect the simulator/device's network and relaunch the installed app. It should restore saved products with an offline label. Reconnect after data becomes stale; refresh should succeed. Also verify a fresh install/empty cache offline shows “Connect to load products,” not an endless spinner. Test an expired/incompatible/corrupt cache and a failed refresh that leaves saved products usable.

For a true no-network restart demo, use a release build that bundles JavaScript locally; a development app may still require Metro even though product data is saved. Explain this difference in the recording/setup instructions.

**Offline limits:** JSON stores thumbnail URLs, not image files. Use image placeholders offline. Current price/stock is not guaranteed, cache expires under the chosen restore policy, and search/filter selection is not automatically persisted by Query. Once local search/filter is added, it can operate on the restored catalog.

**Done when:** first load, failure/retry, empty handling, cached refresh, and offline restart all work as intended on both platforms. Include one meaningful test for restore/paused-state behavior within the assignment's total 2–4 tests. Commit your own working code.

## Stop here and review — এই পর্যন্ত করে বুঝে নিই

Explain these in your own words: Where are memory cache and disk storage? How do staleTime/gcTime/maxAge differ? Why wait for restoration? Why is the key static? How does timeout differ from cancellation? Why can a paused query need no spinner? Why does FlatList need stable keys?

After review, continue with **Step 5: local search rules**. Search/filter logic must be separate from fetching so you can change it live.

References: [QueryClient/provider](https://tanstack.com/query/latest/docs/framework/react/quick-start), [cache defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults), [cancellation](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation), [FlatList](https://reactnative.dev/docs/flatlist), [API field selection](https://dummyjson.com/docs/products).

Persistence references: [PersistQueryClientProvider, maxAge and gcTime](https://tanstack.com/query/latest/docs/framework/react/plugins/persistQueryClient), [async storage persister](https://tanstack.com/query/latest/docs/framework/react/plugins/createAsyncStoragePersister), [native focus/connectivity integration](https://tanstack.com/query/latest/docs/framework/react/react-native), [AsyncStorage API and native installation](https://github.com/react-native-async-storage/async-storage).
