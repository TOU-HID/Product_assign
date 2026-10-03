# Query lifecycle — সহজ ব্যাখ্যা

File: [queryLifecycle.ts](../ShopDiscover/src/lib/queryLifecycle.ts)

**One job:** tell TanStack whether the device is online and the app is active.
**বাংলা:** device online কি না এবং app সামনে আছে কি না TanStack-কে জানায়।

## Read it in this order

| Part | English | বাংলা |
| --- | --- | --- |
| `ready` | Lets `App.tsx` wait for the initial connection check before mounting the query screen. | প্রথম network check শেষ না হওয়া পর্যন্ত product screen অপেক্ষা করে। |
| `updateConnection()` | Updates online status and finishes startup readiness. | online status জানায় ও startup অপেক্ষা শেষ করে। |
| NetInfo listener | Uses the same function for later network changes. | পরের network পরিবর্তনেও একই function চালায়। |
| `applyInitialConnection()` | Accepts the first check only if a live event/timeout has not already finished startup. | নতুন event/timeout আগে হয়ে গেলে পুরোনো check result গ্রহণ করে না। |
| Five-second timer / failed check | Unknown status allows an API attempt, so startup cannot wait forever. | অবস্থা অজানা হলে API চেষ্টা করতে দেয়; startup চিরকাল আটকে থাকে না। |
| AppState listener | Active → focused; background/inactive → unfocused. | সামনে থাকলে focused, background-এ unfocused। |
| `cleanup()` | Removes both listeners and the timer; ignores later callbacks. Safe to call twice. | listener/timer সরায়; পরে আসা callback উপেক্ষা করে। দুবার ডাকলেও সমস্যা নেই। |

## Why two flags?

- `disposed`: the root effect ended; callbacks must stop changing state.
- `initialCheckFinished`: startup is ready; an older initial result must not overwrite newer connectivity.

**বাংলা:** প্রথম flag unmount-এর পর কাজ থামায়। দ্বিতীয় flag পুরোনো network result দিয়ে নতুন অবস্থা বদলে যাওয়া ঠেকায়।

Only `isConnected === false` or `isInternetReachable === false` means offline. `null` means unknown. Network status cannot guarantee that the API works; its separate ten-second timeout and error handling still apply.

**বাংলা:** স্পষ্ট `false` হলে offline। `null` হলে নিশ্চিত জানা নেই। network থাকলেও API ব্যর্থ হতে পারে, তাই request-এর নিজস্ব timeout/error আছে।

## How does App.tsx use it?

Start once in the root effect → wait for `ready` and saved-cache restoration → show Products → call `cleanup()` on unmount.

**বাংলা:** root effect-এ শুরু → network ও saved cache প্রস্তুত হওয়ার অপেক্ষা → Products দেখানো → unmount-এ cleanup।

Change startup waiting time at `INITIAL_CONNECTION_TIMEOUT_MS`. Query refresh settings belong to `queryClient.ts`.

**Interview:** “I connect network and app state to TanStack, wait briefly during startup, and remove listeners when the root unmounts.”
**বাংলা:** “network ও app state TanStack-এর সঙ্গে যুক্ত করি, startup-এ অল্প অপেক্ষা করি, unmount-এ listener সরাই।”
