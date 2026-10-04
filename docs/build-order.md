# Build in this order — এই ক্রমে বানাব

**Current resume point:** [session-status.md](./session-status.md). This table is the original build sequence; implemented steps and verified checks are recorded in the handoff.

Setup is complete. Use TypeScript, Yarn, TanStack Query, and FlatList. You write each step yourself; run it on both platforms and commit working changes.

| Step | What to do | সহজ বাংলা |
| --- | --- | --- |
| 1 | Choose API-first or local-catalog search. Recommendation for this small demo: local catalog; record its download/memory limits at 40,000 products. | search পদ্ধতি বেছে নেব। ছোট demo-তে local catalog সহজ; বড় catalog-এর সীমাবদ্ধতা লিখব। |
| 2 | Follow `steps-2-4-plan.md`: add TanStack Query, persistence packages, AsyncStorage, and NetInfo. Use PersistQueryClientProvider to restore saved products. | app বন্ধ করেও product cache রাখতে persistence যুক্ত করব। |
| 3 | Write a typed product-fetch function. Check HTTP status/data shape; add timeout and cancellation. Fetch only needed fields, including thumbnails. | পণ্য আনার function লিখব। ভুল response ও বেশি সময় লাগা সামলাব। |
| 4 | Fetch with `useQuery`; show products in FlatList using product-ID keys. Add loading, error + retry, and empty states. | আগে একটি কার্যকর product list বানাব, সঙ্গে loading/error/retry রাখব। |
| 5 | Add search with small, explained rules. Handle phone aliases; preserve `phone charger` intent. Do not invent matches for `red dress`. | বোঝা যায় এমন search নিয়ম লিখব; অপ্রাসঙ্গিক পণ্যকে সঠিক বলব না। |
| 6 | Add **In stock** (`stock > 0`) and **Price range** (optional minimum/maximum, inclusive), plus reset. Validate before applying; filter the complete relevant dataset. | stock ও minimum/maximum price filter দেব। valid range apply করব; সব relevant পণ্য filter করব। |
| 7 | Add product details and back navigation. Preserve search, filter, results, and scroll position. | details দেখে ফিরে এলে আগের অবস্থান ঠিক রাখব। |
| 8 | Demonstrate slow requests, failures, malformed data, offline restart, and recovery. Keep waiting/retries bounded. | খারাপ network, offline restart ও recovery দেখাব। |
| 9 | Write 2–4 meaningful tests. Include your design's most likely bug. Compare one metric with literal API search. | সম্ভাব্য ভুলের test লিখব এবং baseline-এর সঙ্গে improvement মাপব। |
| 10 | Finish README, DECISIONS, AI_USAGE, and a 2–4 minute recording of both platforms. Practice changing your code. | প্রয়োজনীয় documents ও video শেষ করব; নিজে code বদলানোর অনুশীলন করব। |

**Continue now:** [session-status.md](./session-status.md) records completed implementation and verification. Remaining work includes the iOS offline cold-restart check and final user deliverables.

Markdown files stay in `product_assignment/docs`. Application code belongs in `ShopDiscover/`.
