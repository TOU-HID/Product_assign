# queryClient.ts — সহজ ব্যাখ্যা

File: [queryClient.ts](../ShopDiscover/src/lib/queryClient.ts)

**Purpose:** create one shared manager for API-data caching and query defaults.
**উদ্দেশ্য:** API data-এর memory cache এবং request-এর সাধারণ নিয়ম এক জায়গায় রাখা।

| Code | English | বাংলা |
| --- | --- | --- |
| `import { QueryClient } ...` | Import TanStack's cache manager class. | cache পরিচালনার class আনা। |
| `CACHE_MAX_AGE_MS` | 24 hours in milliseconds; reuse later for persistence `maxAge`. | ২৪ ঘণ্টার সময়। পরে persistence-এর `maxAge`-এ একই constant ব্যবহার করব। |
| `export const queryClient = new QueryClient(...)` | Create and export one shared client outside components, so renders do not recreate it. | একটি client বানিয়ে অন্য file-এ ব্যবহারের জন্য export করা। render হলেই নতুন cache তৈরি হবে না। |
| `defaultOptions.queries` | Defaults for queries using this client; individual queries can override them. | সব query-র সাধারণ settings; দরকার হলে নির্দিষ্ট query-তে বদলানো যাবে। |
| `retry: false` | Failed requests are not automatically retried; the screen will offer Retry. | request ব্যর্থ হলে নিজে বারবার চেষ্টা করবে না; UI-তে Retry দেব। |
| `staleTime: 60 * 1000` | Data is considered fresh for one minute. After that it is stale, but not deleted; eligible events can trigger refresh. | এক মিনিট data fresh। এরপর stale হবে, মুছে যাবে না। উপযুক্ত event-এ refresh হতে পারে। |
| `gcTime: CACHE_MAX_AGE_MS` | Remove unused queries after 24 hours. Keep this at least as large as persistence `maxAge`. | query আর ব্যবহার না হলে ২৪ ঘণ্টা পরে memory cache সরাবে। persistence `maxAge`-এর চেয়ে কম রাখব না। |
| `networkMode: 'online'` | Pause network requests when TanStack knows the device is offline; cached data remains usable. | offline জানা থাকলে request pause করবে; cached data দেখানো যাবে। |
| `refetchOnReconnect: true` | Active stale queries can refresh when connection returns. | internet ফিরলে ব্যবহৃত stale query refresh হতে পারে। |
| `refetchOnWindowFocus: true` | Active stale queries can refresh when app focus returns, after native AppState integration. | AppState যুক্ত করার পর app foreground-এ ফিরলে ব্যবহৃত stale query refresh হতে পারে। |

**Next:** connect this client to `PersistQueryClientProvider`, add the AsyncStorage persister, and connect NetInfo/AppState. This file alone neither fetches products nor saves data to disk. The API function must supply the timeout.

**পরের কাজ:** provider, persister এবং NetInfo/AppState যুক্ত করব। শুধু এই file দিয়ে products fetch বা offline storage হয় না। timeout API function-এ দিতে হবে।

Remember: **staleTime = freshness; gcTime = unused memory retention; maxAge = saved snapshot restore limit**.

মনে রাখব: **fresh থাকা, memory-তে থাকা, আর saved data restore করা—তিনটি আলাদা বিষয়।**

References: [query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults), [persistence retention](https://tanstack.com/query/latest/docs/framework/react/plugins/persistQueryClient), [native connectivity/focus](https://tanstack.com/query/latest/docs/framework/react/react-native).
