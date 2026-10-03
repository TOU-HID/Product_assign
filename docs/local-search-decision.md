# Why I chose local search — কেন local search বেছে নিলাম

> I chose local search for the small demo catalog because I can apply clear relevance rules and filter the complete dataset. I accept initial download and stale-data costs. At 40,000 products, full-catalog loading needs reconsideration.

## What this means — এর অর্থ

| English | সহজ বাংলা |
| --- | --- |
| I fetch the small catalog from the API and cache it with TanStack Query. Its AsyncStorage persister saves the data for later offline use. Search and filters then run in TypeScript inside the app. | API থেকে ছোট catalog এনে TanStack Query-তে cache করব। persister সেটি AsyncStorage-এ রাখবে। তারপর app-এর TypeScript function দিয়ে search/filter করব। |
| “Local search” still uses real API data. It does not mean replacing the catalog with hardcoded products. | local search মানে নিজের বানানো পণ্য দেখানো নয়। আসল API-এর data এনে app-এর মধ্যে খোঁজা। |

## Why it fits this demo — এই demo-তে কেন উপযুক্ত

| Reason | Explanation / ব্যাখ্যা |
| --- | --- |
| **Small catalog** | Our investigation found 194 products. Loading a small dataset is practical to investigate and measure; I must still check the actual payload and device behavior. / ১৯৪টি পণ্য নিয়ে কাজ বোঝা ও মাপা সহজ; download size ও device performance যাচাই করব। |
| **Clear relevance rules** | The API puts accessories before phones and handles `phone`, `phones`, and `smartphones` differently. Local rules can treat these known aliases consistently while preserving `phone charger` intent. / পরিচিত একই অর্থের query-কে একভাবে সামলাব; charger চাইলে ফোন দেখাব না। |
| **Complete filtering** | I filter the complete fetched catalog. Filtering only the first page could show zero phones even though later pages contain them. / সব fetched পণ্যের ওপর filter করব; এক page দেখে ভুলভাবে “পণ্য নেই” বলব না। |
| **Offline browsing** | After a successful save, a compatible restored catalog supports local search/filter without new API calls. / একবার data save হলে offline-এও সেই catalog-এ search/filter করা যাবে। |
| **Easy to explain and change** | Separate search functions from fetching and UI. I can explain a rule, test it, and change it during the live session. / fetch, search ও UI আলাদা রাখলে নিয়ম বোঝানো, test ও পরিবর্তন সহজ। |

These are intended benefits, not measured improvement yet. I will compare the finished behavior with literal API search. Category data is imperfect, so local search cannot guarantee every query is correct.

এগুলো প্রত্যাশিত সুবিধা; এখনও উন্নতি মাপা হয়নি। category-তেও ভুল থাকতে পারে, তাই সব query ঠিক হবে দাবি করব না।

## Costs I accept — যে সীমাবদ্ধতা মেনে নিচ্ছি

| Cost | What I will do / কী করব |
| --- | --- |
| **Initial download** | The first successful load needs the whole selected-field catalog. Fetch only needed fields and measure its size/loading time. First launch offline has no catalog to show. / শুরুতে download লাগবে; আগে save না হলে offline-এ products পাওয়া যাবে না। |
| **Stale data** | Saved prices/stock can become outdated. Show last-updated/offline information, refresh when appropriate, and apply the chosen cache expiry policy. / saved দাম বা stock পুরোনো হতে পারে; update time দেখাব এবং reconnect হলে refresh করব। |
| **Memory and storage** | The catalog lives in memory and is serialized to storage. FlatList reduces rendering work, but not catalog download/search/storage costs. / FlatList সব data রাখার বা search করার খরচ দূর করে না। |
| **Limited search understanding** | Use small, explainable rules. Do not invent a red dress match or silently decide what “cheap” means. Saved thumbnail URLs also do not guarantee offline images. / না থাকা পণ্য বা অস্পষ্ট দামের অর্থ নিজের মতো ধরে নেব না; offline ছবি নিশ্চিত নয়। |

## What changes at 40,000 products — বড় catalog-এ কী বদলাবে

Full-catalog loading could make startup slower, consume more memory/storage, and require expensive refreshes. Searching and sorting on the JavaScript thread could also affect responsiveness. I would measure payload, startup, search time, and memory before extending this approach.

সব ৪০,০০০ পণ্য আনলে download, memory, storage ও refresh-এর খরচ বাড়বে। search/sort-এর কাজ UI-কে ধীর করতে পারে। তাই এই design বড় catalog-এ ভালো চলবে ধরে নেব না।

At that scale, I would prefer paginated API access with server-supported search/filtering where available. With the assignment's **no backend changes** constraint, I must work within existing endpoints or narrow supported behavior. Filtering a few downloaded pages cannot guarantee complete catalog-wide results. A future backend search/index is a discussion point, not something I can build for this submission.

বড় catalog-এ API দিয়ে pagination ও search/filter করা বেশি উপযুক্ত হতে পারে। কিন্তু এই assignment-এ backend বদলানো যাবে না। তাই existing API-এর সীমা মেনে scope কমাতে হতে পারে; কিছু page filter করে পুরো catalog-এর ফলাফল দাবি করব না।

## How I will explain it in the presentation

> “The demo catalog has 194 products, and its search gives irrelevant or incomplete results. I chose to cache the small catalog and use explicit local search rules so I can explain relevance and filter the complete dataset. Persistence also allows browsing saved data offline. I accept download and stale-data costs, and I would rethink full-catalog loading at 40,000 products.”

> “Demo-তে ১৯৪টি পণ্য আছে, কিন্তু API search অপ্রাসঙ্গিক বা অসম্পূর্ণ ফল দেয়। তাই ছোট catalog cache করে বোঝা যায় এমন local search নিয়ম বেছে নিয়েছি। এতে সব পণ্যের ওপর filter এবং saved data-তে offline browsing সম্ভব। download ও পুরোনো data-এর সীমা মেনে নিচ্ছি; ৪০,০০০ পণ্যে সব data একসঙ্গে আনার সিদ্ধান্ত নতুন করে ভাবব।”

Evidence: [API investigation notes](./api-note.md) and [saved responses](../api-evidence.json). Implementation guide: [Steps 2–4](./steps-2-4-plan.md).
