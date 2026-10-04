# Search relevance measurement

Measured on 4 October 2026 using fresh DummyJSON responses and the app's actual `searchProducts` function.

For the query **`phone`**, the first five literal API results contain **0/5 smartphones**. Local search contains **5/5 smartphones**: precision at five rises from 0% to 100% for this selected intent.

| Method | First-five IDs | Smartphone count |
| --- | --- | --- |
| `/products/search?q=phone&limit=5` | 101, 104, 105, 107, 108 | 0/5 |
| Local search over the complete cached catalog | 121, 122, 123, 124, 125 | 5/5 |

The relevance rule is `category === 'smartphones'`. Stock filtering is off and no price range is applied in either comparison. Literal search returns 23 total matches; local search returns all 16 smartphone-category records from the complete 194-product catalog. The local first five are iPhone 5s, iPhone 6, iPhone 13 Pro, iPhone X, and Oppo A57.

The baseline response was captured at **2026-10-04 01:42:48 UTC**; the selected-field catalog at **01:43:27 UTC**, approximately 39 seconds later. These are separate requests, not an atomic snapshot. All five baseline products occur in the catalog, with matching values for the eight fields the app requests. Capture timestamps use the response files' modification times preserved when saving evidence.

The selected-field catalog, including thumbnail URLs, contains **79,235 bytes of response JSON**. This excludes image downloads, transport/compression overhead, JavaScript object memory, and persisted-query metadata. It does not measure startup performance or establish suitability for 40,000 products.

## Evidence and reproduction

- [Raw baseline response](./evidence/search/baseline.json)
- [Raw catalog response](./evidence/search/catalog.json)
- [Recorded result, timestamps, counts, and snapshot comparison](./evidence/search/result.json)
- [Measurement script](./evidence/search/measure.mjs)
- [DummyJSON product API documentation](https://dummyjson.com/docs/products)

From `product_assignment`, with Node 22.11 or newer:

```bash
node --experimental-strip-types docs/evidence/search/measure.mjs
```

This reruns the actual app validator and search function against the saved responses. It makes no network requests. Node may print a module-detection warning because the React Native package does not declare ESM; that warning does not affect the measurement. Keep the React Native package configuration unchanged.

To capture another measurement, fetch both documented URLs again, save the raw responses with their capture times, and rerun the script. The recorded `result.json` belongs to this capture; printing a new result does not overwrite it.

## Limits

This demonstrates one explicitly supported phone intent using category labels as relevance evidence. It does not prove improved relevance for arbitrary queries, conversion, or speed. `cheap phone` does not infer an invisible budget: search `phone` and apply a maximum price. `red dress` returns no match when both words cannot be established from title, brand, category, or tags. Category errors and stale prices/stock remain possible. Charger intent has separate rules and test coverage; it is not included in this metric.
