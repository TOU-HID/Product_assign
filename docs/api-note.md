# My API investigation notes — আমার API অনুসন্ধানের নোট

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| Checked: 2 October 2026. I opened the first four URLs in my browser and noticed irrelevant search results. With AI assistance, I then checked more queries, inspected the catalog, and compared responses. The additional checks are not all requests I personally ran. | যাচাইয়ের তারিখ: ২ অক্টোবর ২০২৬। প্রথম চারটি URL ব্রাউজারে খুলে অপ্রাসঙ্গিক ফলাফল দেখি। এরপর AI-এর সাহায্যে আরও query ও catalog পরীক্ষা এবং response তুলনা করা হয়েছে। অতিরিক্ত সব request আমি নিজে চালিয়েছি—এমন দাবি করছি না। |
| Saved evidence: [api-evidence.json](../api-evidence.json), containing 20 request URLs, HTTP statuses, and responses. | প্রমাণ হিসেবে এই ফাইলে ২০টি request-এর URL, HTTP status এবং response আছে। পরে এগুলো আবার যাচাই করতে পারব। |

## What I found — আমি কী পেয়েছি

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| The base URL below is `https://dummyjson.com`. All saved requests returned HTTP 200, including requests whose filter parameters were ignored. | নিচের সব পথের আগে `https://dummyjson.com` বসবে। সব request-এ HTTP 200 এসেছে, কিন্তু কিছু filter উপেক্ষা হয়েছে। তাই সফল response মানেই filter কাজ করেছে, তা নয়। |

| Request | Actual result | My observation (English) | বাংলা ব্যাখ্যা |
| --- | --- | --- | --- |
| `/products?limit=5` | 5 products; catalog total 194 | First five are beauty products. This is browsing, not searching; this result is expected. | মোট পণ্য ১৯৪টি; `limit=5` বলে প্রথম ৫টি এসেছে। এখানে search query নেই, তাই beauty product আসা ভুল নয়। |
| `/products/search?q=phone` | 23: 16 smartphones + 7 accessories | All first five results are accessories, including AirPods and an iPhone charger. | ১৬টি ফোনের সঙ্গে ৭টি accessory এসেছে। প্রথম ৫টিই accessory। ফোন খুঁজলে আগে অপ্রাসঙ্গিক পণ্য দেখা যাচ্ছে। |
| `/products/search?q=phones` | 4: 1 smartphone + 3 accessories | Adding `s` changes the results; most phones disappear. | শেষে শুধু `s` যোগ করায় বেশির ভাগ ফোন আর পাওয়া যায়নি। একই উদ্দেশ্যের শব্দকে API একভাবে বুঝছে না। |
| `/products/search?q=smartphones` | 2: Oppo K1 + Selfie Stick Monopod | The category contains 16 phones, but this query finds only one of them. | category-তে ১৬টি ফোন থাকলেও সার্চে একটি ফোন ও একটি selfie stick এসেছে। |
| `/products/search?q=laptop` | 5 laptops | This query works reasonably well in this catalog. | এই query-তে ৫টি laptop এসেছে। এটি তুলনামূলকভাবে ভালো কাজ করছে। |
| `/products/search?q=red%20dress` | 0 | I must inspect the catalog before assuming there is an actual red dress. | ফলাফল নেই। সত্যিই লাল dress আছে কি না আগে তথ্য দেখতে হবে। `%20` মানে URL-এর মধ্যে space। |
| `/products/search?q=cheap%20phone` | 0 | The API does not appear to interpret this as phones with a price preference. | API “কম দামের ফোন” হিসেবে কথাটি বুঝছে বলে মনে হচ্ছে না; দাম অনুযায়ী ফলাফল দিচ্ছে না। |
| `/products/search?q=iphone` | 8: 4 phones + 4 accessories | Even model/brand wording does not guarantee relevant phone results. | `iphone` লিখলেও charger ও case এসেছে। নির্দিষ্ট নাম দিলেই শুধু ফোন পাওয়া নিশ্চিত নয়। |
| `/products/search?q=sunglass` | 2 | The `sunglasses` category has 5 products. | category-তে ৫টি পণ্য থাকলেও সার্চে মাত্র ২টি এসেছে। |
| `/products/search?q=lap%20top` | 0 | The spacing variant does not match the 5 laptops. | `laptop`-এর মাঝে space দিলে ফলাফল শূন্য। লেখার এই সাধারণ ভিন্নতা সামলানো হচ্ছে না। |

### 1. Text matching does not understand shopping intent — লেখা মেলানো মানেই উদ্দেশ্য বোঝা নয়

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| For the tested queries, results exactly matched a case-insensitive substring check against **title or description**. This is an inference from responses, not a claim that I inspected the backend code. | পরীক্ষিত query-গুলোর ফলাফল title বা description-এর মধ্যে লেখাটি খোঁজার সঙ্গে মিলে গেছে। বড়/ছোট অক্ষরের পার্থক্য ধরা হয়নি। এটি response দেখে করা অনুমান; backend code দেখে নিশ্চিত করা হয়নি। |
| Examples: `phone` appears inside `headphones`; `smartphones` appears in the selfie stick description. The phone category/tags do not rescue missing matches for `smartphones`. | `headphones`-এর মধ্যেও `phone` আছে। selfie stick-এর description-এ `smartphones` আছে। তাই এগুলো আসে। প্রকৃত ফোনের category/tag থাকলেও এই সার্চে সব ফোন পাওয়া যায় না। |
| The tested results came back in ascending product-ID order. Accessories therefore appear before actual phones. I found no relevance ordering in these responses. | পরীক্ষিত ফলাফল ছোট ID থেকে বড় ID অনুযায়ী এসেছে। তাই accessory আগে আসে। ব্যবহারকারীর প্রয়োজনের সঙ্গে বেশি মেলে এমন পণ্য আগে দেখানোর প্রমাণ পাইনি। |

### 2. Normalization has specific limits — লেখাকে একরকম করার সীমাবদ্ধতা

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| `PHONE` and a space-padded ` phone ` both returned the same 23 results as `phone`. So lowercase/trim alone will not fix the main problem. | বড় অক্ষরে `PHONE` বা আগে-পরে space দিয়ে লিখলেও একই ২৩টি ফলাফল আসে। তাই শুধু lowercase করা বা বাইরের space সরানো মূল সমস্যা সমাধান করবে না। |
| `phones`, `smartphones`, `lap top`, and the extra typo probe `iphnoe` expose other gaps. I should use small, explicit rules rather than blindly removing letters from every query. | বহুবচন, একই অর্থের অন্য শব্দ, মাঝের space ও ভুল বানানের ক্ষেত্রে ঘাটতি আছে। `iphnoe` অতিরিক্ত পরীক্ষার query; PDF-এ আছে `iphone`। নির্দিষ্ট কিছু নিয়ম ব্যবহার করব; সব শব্দ থেকে ইচ্ছেমতো অক্ষর বাদ দিলে নতুন ভুল হবে। |

### 3. Unsupported filters can silently do nothing — সমর্থন না থাকা filter চুপচাপ উপেক্ষা হতে পারে

| Comparison request | What happened (English) | বাংলা ব্যাখ্যা |
| --- | --- | --- |
| `/products/search?q=phone&category=smartphones` | Response was identical to plain `phone`: still 23 products including accessories. | category parameter যোগ করেও একই ২৩টি ফলাফল। পরীক্ষিত search endpoint-এ এই parameter কাজ করেনি। |
| `/products?limit=5&stock=0` | Response was identical to plain browse; all five had positive stock. | `stock=0` দিয়েও আগের একই ৫টি পণ্য এসেছে। সবগুলোর stock শূন্যের বেশি। |
| `/products/category/smartphones?limit=0` | Correctly returned all 16 category products. | category-এর আলাদা endpoint-এ ১৬টি ফোন পাওয়া যায়। এখানে `limit=0` মানে সব ফলাফল। |
| `/products/search?q=phone&limit=5&skip=5` | Returned 5 records, with total still 23; pagination worked. | প্রথম ৫টি বাদ দিয়ে পরের ৫টি এসেছে; মোট matching পণ্য ২৩টি। এই request-এ pagination কাজ করেছে। |

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| I cannot assume a query parameter works just because the API accepts the URL. These checks only establish the behavior of these exact parameters/endpoints. | URL গ্রহণ করলেই parameter কাজ করে ধরে নেওয়া যাবে না। এই পরীক্ষা শুধু নির্দিষ্ট endpoint/parameter-এর আচরণ দেখিয়েছে; সব filter সম্পর্কে সিদ্ধান্ত দেয় না। |
| Filtering only the first five `phone` results for smartphones would show zero, even though 16 smartphones exist later. This is a likely bug to avoid and test. | প্রথম ৫টি result-ই accessory। শুধু সেই page filter করলে ফোন শূন্য দেখাবে, যদিও পরে ১৬টি ফোন আছে। এক page-এর ফলাফল দিয়ে পুরো catalog-এ পণ্য নেই বলা ভুল। এই ভুলের জন্য test দরকার। |

### 4. Catalog data is imperfect too — পণ্যের তথ্যেও অসংগতি আছে

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| `/products/search?q=dress` returned 7 products, including an earring whose description mentions dresses. | `dress` লিখে একটি earring-ও এসেছে, কারণ তার description-এ dresses লেখা আছে। |
| `/products/search?q=red` returned 18 products. Substrings can occur inside unrelated words as well as actual color terms. | `red` লিখে ১৮টি পণ্য এসেছে। এই লেখা বড় শব্দের অংশও হতে পারে। match হলেই পণ্যটি লাল, তা নয়। |
| The `womens-dresses` category includes **Marni Red & Black Suit**. A red item in that category is not necessarily a red dress; dropping the color or trusting category alone could mislead users. | dresses category-তে লাল-কালো suit আছে। category ও রং মিললেই সেটি red dress নয়। আবার `red` বাদ দিয়ে যেকোনো dress দেখালেও ব্যবহারকারীর চাহিদা পূরণ হবে না। |
| The catalog has 4 zero-stock products. Stock and availability status agree in this snapshot, but 21 products have minimum order quantities greater than stock. This makes “can buy today” stronger than the data supports. | ৪টি পণ্যের stock শূন্য। stock ও availability status এই snapshot-এ মিলে গেছে। কিন্তু ২১টি পণ্যের minimum order quantity stock-এর চেয়ে বেশি। তাই stock আছে মানেই order করা সম্ভব, এমন নিশ্চয়তা নেই। |
| I can label a `stock > 0` filter **In stock**; it does not guarantee purchasability for every order quantity or same-day delivery. | filter-এর নাম “In stock” দিতে পারি। এটি শুধু stock আছে বোঝাবে; সব পরিমাণে কেনা যাবে বা আজই delivery হবে, তা নয়। |

## What the assignment expects me to do — assignment আমার কাছে কী চায়

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| The PDF asks me to **explore the API, keep request notes, diagnose root causes, and choose a limited scope**. Undocumented limitations are part of the task. I do not have to fix every query or satisfy every stakeholder. | API পরীক্ষা, request-এর নোট, মূল সমস্যা নির্ণয় এবং ছোট scope বেছে নিতে হবে। documentation-এ লেখা নেই এমন সীমাবদ্ধতা খুঁজে বের করাও কাজের অংশ। সব query বা সবার দাবি পূরণ বাধ্যতামূলক নয়। |
| I must build browse + search + at least one filter, run on Android and iOS, demonstrate bad-network behavior, add 2–4 meaningful tests, and compare one metric against a naive baseline. | browse, search ও অন্তত একটি কার্যকর filter লাগবে। Android/iOS-এ চালাতে হবে, খারাপ network-এ আচরণ দেখাতে হবে, ২–৪টি অর্থপূর্ণ test এবং একটি metric-এর baseline comparison লাগবে। |
| No backend/proxy is allowed. Another API or mock data is allowed if justified. | নতুন backend/proxy বানানো যাবে না। যুক্তি ব্যাখ্যা করতে পারলে অন্য API বা mock data ব্যবহার করা যাবে। |
| My diagnosis so far: **weak intent matching, poor result ordering, and unsafe assumptions about filters/catalog fields**. Network recovery and lost browsing state are separate problems I also need to address. | এখন পর্যন্ত মূল সমস্যা: উদ্দেশ্য ঠিকভাবে না বোঝা, প্রয়োজনীয় পণ্য আগে না দেখানো এবং filter/data নিয়ে ভুল ধারণা। network failure থেকে recovery ও back করলে আগের অবস্থান হারানোও সামলাতে হবে। |

## Possible solutions — সম্ভাব্য সমাধান

| Approach and tradeoff (English) | বাংলা ব্যাখ্যা |
| --- | --- |
| **API-first, with exact category-intent rules:** route `phone`/`phones`/`smartphones` to the smartphone category. Avoids downloading the whole catalog, but does not solve general language queries. Complete stock filtering and ranking across paginated results still need care. | **API-ভিত্তিক সমাধান:** নির্দিষ্ট query-কে category endpoint-এ পাঠাব। সব পণ্য download লাগবে না। কিন্তু সব ধরনের query বুঝবে না। একাধিক page-এর মধ্যে stock filter ও ranking ঠিক রাখা কঠিন হতে পারে। |
| **Fetch a lightweight demo catalog; search/filter locally:** clear rules, relevance ordering, and complete filtering over the small dataset. Costs initial download and memory; stock can become stale. Cannot claim this automatically scales to 40,000. | **ছোট catalog এনে app-এর মধ্যে search/filter:** নিয়ম, ranking ও সম্পূর্ণ filter করা সহজ। তবে শুরুতে download, memory এবং পুরোনো stock-এর সমস্যা আছে। ৪০,০০০ পণ্যেও একইভাবে ভালো চলবে দাবি করা যাবে না। |
| **Switch API or use fixtures:** better-controlled data, but requires justification and an honest distinction between real API behavior and demo data. | **অন্য API বা sample data:** তথ্য নিয়ন্ত্রণ করা সহজ। তবে কেন বদলালাম বলতে হবে এবং real API-এর আচরণ ও demo data আলাদা করে বোঝাতে হবে। |

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| **Current recommendation to consider, not yet my final decision:** TanStack Query fetches/caches the small catalog; pure TypeScript functions search/filter locally; FlatList renders results. | **বিবেচনার জন্য প্রস্তাব; চূড়ান্ত সিদ্ধান্ত নয়:** TanStack Query দিয়ে catalog আনা/cache, TypeScript function দিয়ে search/filter এবং FlatList দিয়ে ফলাফল দেখানো। |
| Add explicit phone aliases and prioritize title/category evidence over incidental description matches. Preserve explicit accessory intent, such as `phone charger`. | `phone`, `phones`, `smartphones`-এর নির্দিষ্ট নিয়ম রাখব। description-এর মধ্যে ঘটনাক্রমে শব্দ পাওয়া থেকে title/category-কে বেশি গুরুত্ব দেব। কিন্তু `phone charger` চাইলে charger লুকিয়ে শুধু ফোন দেখাব না। |
| The selected-field catalog request returned 194 products and **79,273 bytes of JSON**. It excludes images/thumbnails and is not the final app payload. Fetch needed fields, include a thumbnail for cards, and remeasure. | কিছু নির্বাচিত field নিয়ে ১৯৪টি পণ্যের JSON ছিল ৭৯,২৭৩ byte। এতে image/thumbnail ছিল না। card-এর thumbnail-সহ প্রয়োজনীয় field এনে আবার size মাপতে হবে। এটি final app payload নয়। |
| At 40,000 products, full-catalog loading needs reconsideration; FlatList only reduces rendering work. | ৪০,০০০ পণ্য একসঙ্গে আনার সিদ্ধান্ত নতুন করে ভাবতে হবে। FlatList rendering-এর কাজ কমায়; সব পণ্য download, memory-তে রাখা বা search-এর খরচ দূর করে না। |
| Leave `red dress` honestly unsupported if the data cannot establish a relevant match. For `cheap phone`, offer an explicit price choice or clearly labelled affordable-first ordering instead of inventing a hidden definition of “cheap.” | সঠিক red dress প্রমাণ না হলে অন্য পণ্যকে সঠিক বলব না। `cheap phone`-এর জন্য দৃশ্যমান price choice বা কম দাম আগে দেখানোর স্পষ্ট option দিতে পারি। “cheap” মানে কত টাকা, তা গোপনে ধরে নেব না। |

## My next steps — এখন আমার করণীয়

| Step (English) | বাংলা ব্যাখ্যা |
| --- | --- |
| **1.** Re-run category and ignored-filter checks myself; explain why counts differ. In a browser, paste only the URL. `curl 'URL'` is a terminal command. | **১.** নিজে আবার request চালিয়ে সংখ্যা কেন বদলাচ্ছে বুঝব। browser-এ শুধু URL দেব; `curl 'URL'` terminal-এ চালাব। |
| **2.** Choose local catalog or API-first search and write my reason plus the scale limitation. | **২.** local search নাকি API-first, বেছে নেব। কারণ এবং বড় catalog-এ সীমাবদ্ধতা লিখব। |
| **3.** Fetch/validate products with TanStack Query. Build a FlatList with loading, error, retry, and empty states. | **৩.** TanStack Query দিয়ে পণ্য এনে response যাচাই করব। FlatList-এ loading, error, retry ও সত্যিকারের empty result আলাদাভাবে দেখাব। |
| **4.** Add chosen search rules, one real filter, and details navigation that preserves browsing progress. | **৪.** search-এর নিয়ম, একটি কার্যকর filter ও details screen যোগ করব। back করলে আগের query, filter ও scroll position রাখব। |
| **5.** Test the design's likely bug and demonstrate network failure/recovery. | **৫.** design-এর সম্ভাব্য ভুলের test লিখব। network খারাপ হলে কী হয় এবং কীভাবে recovery হয় দেখাব। |
| **6.** Compare relevant phone results in the first five against literal API search. Observed `phone` baseline: **0/5 actual smartphones**. No improved measurement yet. This checks one intent's relevance, not conversion or all searches. | **৬.** সাধারণ API search আর আমার সমাধানের প্রথম ৫টি result তুলনা করব। এখন `phone`-এর প্রথম ৫টিতে প্রকৃত ফোন ০টি। নতুন সমাধান এখনও মাপা হয়নি। এটি শুধু এই query-র relevance বোঝাবে; sales conversion বা সব query ভালো হওয়ার প্রমাণ নয়। |

| English | বাংলা ব্যাখ্যা |
| --- | --- |
| Sources: assignment PDF, saved live responses, and [DummyJSON documentation](https://dummyjson.com/docs/products). Record AI-assisted investigation in `AI_USAGE.md`; keep only conclusions I can personally explain. | উৎস: PDF, সংরক্ষিত API response ও DummyJSON documentation। AI কোথায় সাহায্য করেছে `AI_USAGE.md`-এ লিখব। নিজে বুঝে ব্যাখ্যা করতে পারি এমন সিদ্ধান্তই রাখব। |
