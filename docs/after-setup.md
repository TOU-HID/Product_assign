# Next steps after setup

**Completed:** basic Android/iOS setup and Git, as you reported.
**Decided:** React Native CLI + TypeScript + Yarn + TanStack Query with AsyncStorage persistence + FlatList for product lists. NetInfo supports offline/reconnect behavior.
**Location:** all Markdown files stay in `product_assignment/docs`.

## 1. Investigate the API first

Run these yourself, or open the URLs in your browser:

```bash
curl 'https://dummyjson.com/products?limit=5'
curl 'https://dummyjson.com/products/search?q=phone'
curl 'https://dummyjson.com/products/search?q=phones'
curl 'https://dummyjson.com/products/search?q=smartphones'
```

Current findings are in `docs/api-note.md`, with saved responses in root `api-evidence.json`. Re-run the important checks yourself and add observations you can explain. Record **exact request → result count → example titles/categories → what you learned**.

## 2. Choose the behavior before coding

- Choose API search with small, proven improvements **or** local search over the small demo catalog. Decide after Step 1; explain the limits at 40,000 products.
- Start with one filter: **In stock**, if stock data supports it. It means available stock, not delivery today.
- Build two screens: **results → product details → back to the same results**.
- Defer login, cart, dark mode, and extra filters to keep the scope manageable.

## 3. Add TanStack Query

Inside the app folder:

```bash
cd /Users/md.touhidulislam/Projects/product_assignment/ShopDiscover
yarn add @tanstack/react-query@5 @tanstack/react-query-persist-client@5 @tanstack/query-async-storage-persister@5 @react-native-async-storage/async-storage @react-native-community/netinfo
```

Use one stable `QueryClient` and an AsyncStorage persister; wrap the app with `PersistQueryClientProvider`. Follow `steps-2-4-plan.md` for native installation, restoration, expiry, and connection handling.

| State | Where it belongs |
| --- | --- |
| API products, cached responses, request status | TanStack Query |
| Search input, selected filter, scroll position | React state/navigation state |

“Server state” means data received from the API; TanStack Query runs in your app. It does not require building a backend. Its memory cache alone does not survive app termination; the added persister saves/restores product data through AsyncStorage. Previously saved compatible data supports offline browsing; thumbnail files and live stock are not guaranteed offline.

## 4. Build one working piece at a time

1. **API function:** fetch products, check HTTP status and response shape, and enforce a request timeout.
2. **Query hook:** use `useQuery`; include every changing request input in its query key. Pass its cancellation signal to the request.
3. **Product list:** use `FlatList` with stable product-ID keys. It renders a limited window of rows to reduce memory use. Show loading, error + retry, and genuine empty states separately.
4. **Search + filter:** implement the behavior chosen in Step 2. Filtering one page must not claim to filter the entire catalog.
5. **Details + back:** preserve query, filter, and scroll position. Query caching alone does not preserve the screen's UI state.
6. **Network recovery:** choose bounded retries; demonstrate slow/failing/invalid responses. Label retained old results honestly. Integrate app focus with `AppState`; use NetInfo with `onlineManager` if adding automatic reconnect handling.

Run each piece on both platforms and commit each working increment. You write the code; I explain, review, and help debug.

## 5. Verify and prepare the submission

- Write **2–4 tests**, including your design's most likely bug; for example, wrong cache keys mixing search results or filters missing products on later pages.
- Pick **one metric** linked to your diagnosis. Compare the same queries against literal API search; explain what the improvement does not prove.
- Finish `README.md`, `DECISIONS.md`, and `AI_USAGE.md`; record actual decisions and AI assistance as you work.
- Record **2–4 minutes** showing Android, iOS, and network failure/recovery. Practice explaining and changing your code yourself.

**Do now:** read `api-note.md`, re-run the category/ignored-filter checks yourself, and choose the search strategy. Then build the first product list with TanStack Query and FlatList.

References: [installation](https://tanstack.com/query/latest/docs/framework/react/installation), [React Native integration](https://tanstack.com/query/latest/docs/framework/react/react-native).
