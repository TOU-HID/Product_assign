# Product API — সহজ ব্যাখ্যা

File: [api.ts](../ShopDiscover/src/features/products/api.ts)

**One job:** fetch the complete catalog and return checked `Product[]`.
**বাংলা:** সব পণ্য এনে data যাচাই করে একটি পরিষ্কার list ফেরত দেয়।

## Read it in this order

| Part | English | বাংলা |
| --- | --- | --- |
| `fetchProducts(signal)` | Fetch → check HTTP → read JSON → validate → return products. | request → HTTP check → JSON পড়া → যাচাই → list ফেরত। |
| `controller` | Stops the actual request when TanStack cancels it. | TanStack cancel করলে আসল request বন্ধ করে। |
| `timedOut` | Records whether the ten-second timer stopped the request first. | ১০ সেকেন্ডের timer আগে request বন্ধ করেছে কি না মনে রাখে। |
| `catch` | Reports timeout, cancellation, or the original error. | timeout, cancel বা আসল error ফেরত দেয়। |
| `finally` | Removes the timer and cancellation listener in every case. | সফল বা ব্যর্থ—সব ক্ষেত্রেই timer/listener সরায়। |
| `validateCatalog()` | Checks the response and requires product count to match `total`. | response যাচাই করে; list-এর সংখ্যা `total`-এর সমান হতে হবে। |
| `validateProducts()` | Checks the list and rejects duplicate IDs. Also used for saved data. | list ও duplicate ID যাচাই করে; saved data-তেও একই নিয়ম। |
| `validateProduct()` | Checks one product and keeps only the fields we need. | একটি পণ্য যাচাই করে দরকারি field রাখে। |

## Why keep the checks?

TypeScript types do not check API JSON at runtime. Required fields must be valid: positive unique ID, nonempty title/category, text description/tags, nonnegative price, and integer stock. Missing or unusable brand/thumbnail is allowed; usable strings are trimmed.

**বাংলা:** TypeScript লিখলেই API data ঠিক হয়ে যায় না। প্রয়োজনীয় field ভুল হলে error দিই। brand/thumbnail না থাকলে পণ্য বাদ দিই না।

A partial or invalid catalog is rejected instead of silently hiding products. A request cancelled first stays `AbortError`; a timeout first stays `TimeoutError`, even if cancellation follows. Late responses are rejected.

**বাংলা:** অসম্পূর্ণ/ভুল catalog গ্রহণ করি না। cancel আগে হলে cancel error, সময় শেষ আগে হলে timeout error। পরে response এলেও গ্রহণ করি না।

## What can I change?

- Endpoint/selected fields: `PRODUCTS_URL`.
- Timeout: `REQUEST_TIMEOUT_MS`.
- Product fields: `types.ts` and `validateProduct()` together.

**বাংলা:** URL, সময়সীমা বা field বদলাতে এই জায়গাগুলো পরিবর্তন করব। Type ও বাস্তব validation একসঙ্গে বদলাব।

**Interview:** “I fetch the complete small catalog, validate it before use, and clean up slow or cancelled requests.”
**বাংলা:** “ছোট catalog-এর সব পণ্য আনি, ব্যবহারের আগে যাচাই করি, slow/cancelled request বন্ধ করে cleanup করি।”
