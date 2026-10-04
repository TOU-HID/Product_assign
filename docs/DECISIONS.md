# Decisions

## Scope and API evidence

The assignment's complaints support a focused discovery flow: relevant search, explicit stock/price controls, network recovery and details/back continuity. They do not establish a causal improvement in sales. Cart, login, AI chat, extra brand/rating/discount filters and promotional clutter are deferred. [Requirements](./plan.md).

Initial investigation and the fresh comparison found 194 products. Literal `phone` search ranks accessories before smartphones and aliases behave inconsistently. Unsupported API filters and pagination require investigation; filtering a single page cannot establish complete availability. [Investigation](./api-note.md), [original responses](../api-evidence.json), [fresh measurement](./search-measurement.md).

## Local search and filters

The app fetches the complete selected-field catalog and validates completeness before caching. The fresh JSON response, including thumbnail URLs, is 79,235 bytes; images, object memory and cache metadata cost more. Local search/filtering then works over the complete cached dataset and can operate offline after a successful save.

Exact phone aliases select the smartphone category. Exact charger phrases select mobile accessories with a whole-word charger title. General queries require every word across title, brand, category or tags; all-title matches rank first, then ID. Description matching is excluded because incidental mentions gave irrelevant results.

`red dress` stays empty when both requested words cannot be established. The weak query **`cheap phone`** does not invent a budget: search `phone` and set an explicit maximum price. Category labels can be wrong; these rules are limited rather than natural-language search.

Stock means `stock > 0`, without a delivery/order promise. Both price bounds are inclusive; blank is unbounded and zero is accepted. Invalid decimal/reversed ranges show an error while preserving the applied range. Price drafts stay separate from applied filters.

## State, navigation and recovery

TanStack Query owns the catalog; React state owns UI choices. Visible results are derived. Native stack navigation retains the Products screen and passes only a product ID to details, which reuse the catalog. Search/filter/reset changes scroll to the top; details/back and refresh do not intentionally reset it. Native scroll evidence is separate from JavaScript state tests.

React Native CLI, TypeScript and Yarn continue the existing setup. Navigation/screens introduce native code requiring rebuilds on both platforms. Safe-area handling uses the existing provider and the native details header.

Requests time out after 10 seconds; automatic retries are disabled and Retry is explicit. Connection startup is bounded at five seconds. Refresh failure keeps previous data; saved-cache validation and a 24-hour age limit prevent blindly restoring unusable data. Offline browsing requires a prior successful save. Prices/stock may be stale and thumbnail URLs are not offline image storage.

## Alternatives not selected

| Alternative | Reason and tradeoff |
| --- | --- |
| API-first category routing and pagination | Avoids a full download and is a better direction for larger catalogs. For this small demo, the whole validated catalog makes complete stock/price filtering and intent rules easier. Existing API limitations still constrain broad behavior. |
| Curated fixtures or a new search backend | Fixtures control demonstrations but do not demonstrate real API quirks. A new backend violates the assignment constraint. Clearly labelled fixtures remain useful for tests. |

## Scale and evidence limits

At 40,000 products, full download, validation, serialization, storage, memory and synchronous matching/sorting need reassessment. FlatList limits rendering work only. Prefer existing API pagination and server-supported search/filtering where available; a few filtered pages cannot be called complete. Backend search is a future discussion rather than an implemented assignment feature.

The `phone` comparison improved smartphone precision at five from 0/5 to 5/5. Separate responses were captured approximately 39 seconds apart; overlapping records matched the app's requested fields. This does not measure all queries, latency, conversion or large-catalog performance. [Reproduction and raw evidence](./search-measurement.md).

## Personal reflection to complete

The user should add their own reflection after reviewing the implementation and native checks: which tradeoff they would change, what they can modify live, and what they learned. No personal experience or authorship claim has been filled in on their behalf.
