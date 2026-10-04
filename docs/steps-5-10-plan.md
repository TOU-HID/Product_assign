# Steps 5–10 — বাকি কাজের সহজ পরিকল্পনা

**Current progress:** see [session-status.md](./session-status.md). Search, stock/price filters, details/navigation and their automated tests are already implemented in the working tree. The fresh [search measurement](./search-measurement.md) and submission document drafts are available. Native verification and final human deliverables still need completion; do not restart Step 5 from scratch.

Based on [build-order.md](./build-order.md). Steps 1–4 are complete: catalog fetch, FlatList, persistence, loading/error/retry, and connection handling.

**এখন:** ছোট ছোট পরিবর্তন করব, নিজে বুঝব, দুই platform-এ দেখব, তারপর commit করব। নিচের সিদ্ধান্তগুলো প্রস্তাবিত; বাস্তব ফল দেখে প্রয়োজন হলে বদলাব।

## Keep the structure simple — সহজ structure

| Part | Decision / সিদ্ধান্ত |
| --- | --- |
| Server data | Existing TanStack Query + persistence owns the complete catalog। product data আবার React state-এ copy করব না। |
| Screen state | `useState` for search text, stock toggle, and applied price range; draft price inputs stay in the filter component। Redux/Zustand লাগবে না। |
| Visible products | Derive from catalog + search + filter। আলাদা results state রাখব না। |
| Rendering | Keep FlatList and stable product-ID keys। search বদলালে catalog query key বদলাব না। |
| Scope | Search, stock + price filters, details, recovery, evidence। cart/login/AI search এই কাজের অংশ নয়। |

Create files only when their step starts. App code stays inside `ShopDiscover/`; Markdown stays in the root `docs/` folder.

## Step 5 — local search

**Goal / লক্ষ্য:** relevant results using a few rules I can explain.

1. Create `src/features/products/searchProducts.ts`. Write a pure function: `searchProducts(products: Product[], text: string): Product[]`. It must not fetch, update React state, or change the original array.
2. Normalize input: lowercase, trim, and collapse repeated spaces. Empty input returns the catalog.
3. Apply the exact-query rules below **before** general matching. Do not replace `phone` inside every phrase.
4. For other queries, require every query word to match whole words in title, brand, category, or tags. Split punctuation/hyphens into word boundaries. Put products matching all words in the title first; break ties by ID. Leave description matching out of this first version because incidental mentions caused irrelevant results.
5. Add a labelled TextInput and Clear control in `ProductsScreen.tsx`. Keep `searchText` in `useState`; derive results with `useMemo` from catalog + text. Typing runs local search; no debounce or new API request is needed for this small dataset.
6. Show the filtered result count. An empty search result says “No matching products”; keep the input and Clear control available. It is different from an API error or an empty catalog.

| Query | Rule / প্রত্যাশিত আচরণ |
| --- | --- |
| `phone`, `phones`, `smartphone`, `smartphones` | Exact aliases → only category `smartphones`। পুরো phrase-এর জন্য নিয়ম। |
| `phone charger`, `phone chargers` | Only `mobile-accessories` whose title contains the whole word `charger`/`chargers`। ফোন বা `Charger SXT RWD` গাড়ি দেখাব না। |
| `red dress` | Require both words; return empty if the data cannot establish a match। রং বাদ দিয়ে অন্য dress দেখাব না। |
| `cheap phone` | No automatic price interpretation; search `phone` and choose a maximum price explicitly। “cheap” মানে কত দাম, user নিজে price filter-এ ঠিক করবে। |

**Why / কেন:** exact aliases improve the selected phone intent; whole-word rules avoid matching `phone` inside `headphones`. Accessory intent remains separate. These are limited rules, not general language understanding.

**Done when:** aliases return the same phone IDs; chargers remain accessories; no invented red-dress match; Clear restores browsing. Check typing and keyboard behavior on both platforms, including saved-catalog search offline.

## Step 6 — In stock + Price range + reset

1. Add `inStockOnly`, initially `false`, to `ProductsScreen.tsx`; use a labelled Switch.
2. Add optional minimum/maximum price inputs and **Apply price range**. Blank means no bound; zero is valid. Accept finite nonnegative decimal prices and require minimum ≤ maximum. Both bounds are inclusive; do not invent currency conversion.
3. Keep draft price text separate from the applied range. Invalid input shows an inline error and leaves the old range/results unchanged; show the active range explicitly. Provide **Clear price range**.
4. First search the **complete cached catalog**; then combine `stock > 0` and the applied price bounds. Do not filter only visible rows or slice before filtering. Put these pure rules in `filterProducts.ts` and price/stock controls in `ProductFilters.tsx`.
5. Derive FlatList data/count from the final array. Distinguish an empty catalog from “No matching products” and “No products match these filters”; keep controls available.
6. **Clear search** changes only search; **Clear price range** removes price bounds; **Reset all** clears search, stock, price drafts/range, and validation errors. Search/stock/applied-price/reset changes scroll to the top; details/back does not. A collapsible Filters section leaves more space for the list.

**বাংলা:** সব relevant পণ্যের ওপর stock filter করব। label মানে stock আছে; আজ delivery বা order নিশ্চিত নয়।

**Done when:** stock and inclusive price boundaries work independently/together with search; blank/one-sided ranges work; negative/non-numeric/reversed bounds show an error; Reset all restores browsing. Saved stock/price still use the existing update/offline information.

## Step 7 — details and return to the same list

**Choice:** React Navigation native stack with two screens: Products and ProductDetails. A stack keeps the previous screen mounted, which gives us a simple starting point for retaining its local state. Verify the actual list position on both platforms. [Navigation lifecycle](https://reactnavigation.org/docs/navigation-lifecycle/)

1. At this step, install from `ShopDiscover`:

   ```bash
   yarn add @react-navigation/native @react-navigation/native-stack react-native-screens
   cd ios
   rbenv exec bundle exec pod install
   cd ..
   ```

   Safe-area-context is already installed. Follow the installed screens version's Android activity/back configuration and rebuild both apps; Metro reload cannot link a new native dependency. [Official setup](https://reactnavigation.org/docs/getting-started/), [native stack](https://reactnavigation.org/docs/native-stack-navigator/)

2. Create `src/navigation/RootNavigator.tsx` with typed routes: Products has no parameters; ProductDetails receives `{ productId: number }`.
3. Keep the existing root Query/persistence/SafeArea providers and startup readiness gate. Mount the navigator in the ready branch. Keep navigator/screen definitions outside render; avoid doubled safe-area/header padding.
4. Make each ProductCard pressable with a labelled button action. Navigate using the product ID; dismiss the search keyboard before opening details.
5. Create `src/features/products/ProductDetailsScreen.tsx`. Read the product by ID from the existing catalog query. Show title, description, price, stock, optional brand, and thumbnail fallback. Reuse cached data offline; show a friendly unavailable state if the ID is absent. No separate detail API is needed for these fields.
6. Back should pop details, not navigate to a new Products instance. Keep search/filter state in the mounted Products screen, keep stable FlatList keys, and do not reset on focus. If the native check finds a scroll jump, add a small offset ref and restore it only on return; test again after refresh.

**বাংলা:** details-এ ID পাঠাব, cache থেকে পণ্য দেখাব। back করলে আগের screen-এই ফিরব—নতুন list খুলব না।

**Done when:** search → stock/price filters → scroll → details → back keeps text, toggle, price drafts/applied range, results, and position. Check Android hardware back, iOS header back/swipe, and offline details.

## Step 8 — demonstrate failures and recovery

Existing recovery code is already present. Verify it with the new search/navigation; add code only when a check finds a real gap.

| Scenario | Expected behavior / কী দেখব |
| --- | --- |
| Slow initial request | Loading stays visible; controls do not promise available catalog data yet। |
| Request exceeds 10 seconds | Request aborts; understandable timeout + explicit Retry। |
| HTTP/network error or malformed JSON/fields | Controlled error; no crash; retry can recover। |
| Refresh fails with previous data | Keep previous products, current search/filter, and error notice। |
| Saved-cache offline restart | Restore products; local search/filter/details work; offline/update notice remains। |
| First launch offline / unusable saved cache | “Connect to load products”; no endless spinner। |
| Connection returns | Stale catalog can refresh; failure still has Retry; successful refresh keeps UI choices। |

Use controlled fetch mocks for slow/error/malformed cases and actual native launches for offline/reconnect. If showing a mocked scenario on-device, keep it temporary and development-only, label it honestly, and restore the real API before final checks. Do not add a backend/proxy or a permanent demo framework.

**বাংলা:** test-এ simulation এবং device-এ বাস্তব offline—দুটির evidence আলাদা রাখব। save শেষ হওয়ার পর app বন্ধ করে খুলব; শুধু Metro reload offline restart নয়।

**Done when:** capture results on Android and iOS. Android release offline restart was checked earlier; **iOS release offline restart still needs verification**. Recheck both final builds after navigation changes. Restore normal networking and remove temporary demo changes.

## Step 9 — meaningful tests + one measurement

Keep the existing passing tests. Add missing feature coverage alongside implementation; do not postpone tests until the end. Explain 2–4 key acceptance cases for the assignment:

| Case | Bug it catches / কেন দরকার |
| --- | --- |
| Search aliases and charger intent | Alias handling must not turn an accessory request into phones or a car। |
| Complete-catalog stock/price filtering | An available match after the first five records must appear; test inclusive bounds, zero/blank/invalid ranges and reset। incomplete filtering এই design-এর সম্ভাব্য ভুল। |
| Details → back continuity | Search/filter and the mounted list remain intact; native checks prove actual scroll position। |
| Failure/offline recovery | Reuse existing API/cache/screen tests; extend only for a new gap। |

**Primary metric:** number of actual smartphones among the first five results for `phone` (0–5).

1. Near the same time, capture literal API search (`/products/search?q=phone&limit=5`) and the full catalog used by our implementation. Save response JSON, timestamps, first-five IDs, and the rule “category is smartphones.” Use stock filter **off** in both comparisons.
2. Run local search over that saved catalog. Count relevant products in each first-five list using the same rule. If the snapshots differ, disclose it rather than claiming identical data.
3. Write `docs/search-measurement.md`: baseline count, local count, query, IDs, conditions, and limitation. Historical baseline was 0/5; **remeasure and do not fill in an improvement before running it**.

**বাংলা:** একই query/নিয়মে প্রথম পাঁচটি ফল তুলনা করব। এটি শুধু phone intent-এর relevance; সব search ভালো, app দ্রুত, বা sales বাড়ে—এমন প্রমাণ নয়।

## Step 10 — submission and interview practice

| File / artifact | What to include / কী লিখব |
| --- | --- |
| `docs/README.md` | Replace the starter README with Discofy overview, Yarn setup for both platforms, verified devices/versions, architecture, test commands, and network-demo reproduction। |
| `docs/DECISIONS.md` | API evidence, local-search/filter rules, cuts/ignored requests, two rejected alternatives, 40,000-product limits, platform choices, measurement limits, one weak table query (`cheap phone`), and an actual reflection। |
| `docs/AI_USAGE.md` | Actual AI assistance, one real suggestion corrected/rejected and why, and decisions personally understood/chosen। rejected story বা নিজের কাজের দাবি বানাব না। |
| 2–4 minute recording | Show both platforms: browse → phone aliases → stock filter → details/back → offline/recovery. State limitations briefly। |

Practice changing one alias, the stock condition, and the timeout yourself. Explain: “API gets data; Query caches it; local functions search/filter it; FlatList shows it; navigation preserves browsing.”

**বাংলা:** ছোট পরিবর্তন নিজে করে দেখব এবং প্রতিটি সিদ্ধান্তের কারণ বলতে পারব।

Include the root `docs/`, evidence, and recording in the submission together with app source. Currently the Git repository is inside `ShopDiscover/`, so its link alone does not include root documentation.

## After each working step — প্রতিটি ধাপ শেষে

From `ShopDiscover`:

```bash
yarn tsc --noEmit
yarn lint
yarn test --runInBand --watch=false --watchman=false
```

Run the changed flow on both native platforms, then commit the actual working change with a simple message. Record measurement results only after running the comparison.

**Continue now:** see [session-status.md](./session-status.md). Search/filter/navigation, automated checks, release builds and the main native flow on both platforms are verified. Finish the iOS offline cold-restart check, personal reflection, recording and submission review.
