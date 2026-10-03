# Query persistence — সহজ ব্যাখ্যা

File: [queryPersistence.ts](../ShopDiscover/src/lib/queryPersistence.ts)

**One job:** save and restore the product query cache across app restarts.
**বাংলা:** app বন্ধ করে খুললেও আগের product data পাওয়ার জন্য cache device-এ রাখে।

## Read it in this order

| Part | English | বাংলা |
| --- | --- | --- |
| `storagePersister` | TanStack's adapter writes/reads JSON through AsyncStorage. | TanStack-এর adapter AsyncStorage-এ JSON লিখে/পড়ে। |
| `queryPersister` | Gives the provider three operations: save, restore, remove. | provider-কে save, restore, remove—তিনটি কাজ দেয়। |
| `persistOptions` | Sets cache lifetime/version and chooses what to save. | কতদিন রাখব, version কী, কোন data রাখব—সেটিংস দেয়। |
| `saveCache()` | Writes to disk; clears an old notice on success, reports write failure. | disk-এ লেখে; সফল হলে পুরোনো notice সরায়, ব্যর্থ হলে জানায়। |
| `restoreCache()` | Reads → validates → returns saved cache. Invalid/unreadable data is discarded. | পড়ে → যাচাই করে → cache ফেরত দেয়। ভুল/পড়া যায় না এমন data বাদ দেয়। |
| `validateCache()` | Checks cache metadata/query shape and reuses `validateProducts()`. | cache-এর গঠন ও সময় যাচাই করে; product যাচাইয়ে API-এর একই নিয়ম ব্যবহার করে। |
| `removeSavedCache()` | Removes unusable data; reports failure without stopping the app. | অনুপযুক্ত cache সরায়; না পারলে app বন্ধ না করে জানায়। |
| `isCatalogKey()` | Matches only `['products', 'catalog']`; reused when saving and restoring. | শুধু নির্দিষ্ট catalog query মেলায়; save/restore দুটিতেই একই নিয়ম। |
| Error listeners | Tell the existing screen when a storage notice changes. | storage notice বদলালে screen-কে জানায়। |

## Settings and decisions

| Setting | Reason / কারণ |
| --- | --- |
| `maxAge: CACHE_MAX_AGE_MS` | Discard snapshots older than 24 hours during restore। restore-এর সময় ২৪ ঘণ্টার বেশি পুরোনো cache বাদ। |
| `buster: 'products-v1'` | Reject an incompatible cache version। data format অনুপযুক্ত হলে version বদলাব। |
| `throttleTime: 1000` | Limit frequent writes। ঘনঘন disk-এ লেখা কমায়; save asynchronous। |
| Data is not `undefined` | Keep previous products after refresh failure; an empty array is valid too। refresh ব্যর্থ হলেও আগের data রাখে; empty list-ও valid। |
| No saved mutations | This app currently reads products। বর্তমানে শুধু product পড়ি, mutation save লাগে না। |

**Flow:** API → memory cache → disk. Restart: disk → validation → memory cache → screen. `PersistQueryClientProvider` in `App.tsx` starts this process.

**বাংলা:** API → memory → disk। আবার চালু করলে disk → যাচাই → memory → screen। provider এই কাজ শুরু করে।

The existing storage name/key/version stay compatible with saved products. Saving image URLs does not save image files. Saved price/stock can be stale, and a failed disk write cannot guarantee offline availability after restart.

**বাংলা:** আগের saved cache ব্যবহার করা যাবে। ছবির URL রাখা মানে ছবি রাখা নয়। দাম/stock পুরোনো হতে পারে; disk-এ save না হলে restart-এর পর data পাওয়ার নিশ্চয়তা নেই।

**Interview:** “I persist only the catalog, validate it before restoring, and keep the app usable when storage fails.”
**বাংলা:** “শুধু catalog save করি, restore-এর আগে যাচাই করি, storage ব্যর্থ হলেও app ব্যবহার করা যায়।”
