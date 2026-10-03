# React Native practical assignment — discussion and build plan

Status: PDF reviewed; basic setup and Git completed as reported by you. Feature implementation is the next phase. This is a working discussion document; proposed choices require your judgment.

Progress update: you reported completing the basic setup and adding it to Git. React Native CLI, TypeScript, and Yarn are selected. TanStack Query is selected for server state; React state/navigation state will manage UI controls and browsing continuity. See `after-setup.md` for the current short action guide. Earlier setup choices below are historical options.

List rendering decision: use React Native's built-in `FlatList` for product lists with stable product-ID keys.

Persistence decision: you requested offline storage. Persist the product query cache using TanStack's persistence provider and AsyncStorage; add NetInfo for offline/reconnect state. See `steps-2-4-plan.md` for restoration, expiry, offline UI, and the restart demo. You will implement it yourself.

Source: `/Users/md.touhidulislam/Downloads/Practical Assignment - React Native.pdf` (all three pages).

File placement rule: all Markdown files stay in `product_assignment/docs`. Application code stays in `ShopDiscover/`. This reflects your updated preference.

## 1. What you are actually being asked to do

Build a small React Native **shopping discovery app** that helps people browse, search, and narrow products. The job advert's AI chat features are not requirements for this assignment.

The product goal is better discovery and browsing, ultimately increasing conversion. You cannot prove increased purchases from a small demo; you can measure a specific discovery improvement and state its limits.

The evaluators want evidence of five things:

1. Investigation: run API requests and discover actual behavior, including undocumented limitations.
2. Judgment: choose a valuable, achievable scope from conflicting requests.
3. Execution: implement a usable mobile experience on both platforms with realistic failure behavior.
4. Measurement: compare one meaningful metric with a naive baseline.
5. Ownership: explain the code and extend it live without depending on AI to understand it.

A smaller coherent app is explicitly preferred over a large app with generic reasoning. Your own understanding is a deliverable.

## 2. Mandatory requirements and submission checklist

| Requirement | What it means in practice |
| --- | --- |
| React Native on iOS and Android | Run native mobile builds on both; a web preview alone does not count. TypeScript is preferred. Expo and React Native CLI are both permitted. |
| Browse | Show useful products before someone enters a query. |
| Search | Let someone express a product need and see matching results or an honest empty state. |
| At least one filter | A control must actually narrow results; decorative chips do not qualify. |
| Slow/failing/unexpected data | Have bounded waiting, an understandable failure state, recovery, and safe handling of invalid or missing data. Demonstrate these deliberately. |
| 2–4 meaningful tests | Include at least one test for the bug you think is most likely in your chosen design; explain why. |
| One metric versus a naive baseline | Define the same inputs, evaluation rules, and conditions for both approaches. Report results and limitations. |
| Git with real commit history | Commit actual stages as you work. Do not squash or manufacture a story afterward. |
| README.md | Setup for both platforms, exact verified devices/platforms, architecture, and instructions for reproducing the network demo. |
| DECISIONS.md | Evidence-backed diagnosis, ignored requests, scope/cuts, two rejected approaches, scale limits, platform choices, actual reflection, one poorly handled table query, and measurement limits. |
| Screen recording | 2–4 minutes showing iOS, Android, and an unreliable-network scenario. |
| AI_USAGE.md | Record AI assistance, one real suggestion you rejected/corrected and why, and decisions that were yours. AI has already helped interpret the brief and draft this plan. |

Constraints: no backend or proxy server, no core-flow template, lean dependencies with reasons for unusual choices. Another API or mocked data is allowed if justified, but investigating the stand-in API is still part of understanding the problem.

Not explicitly mandatory: login, cart, checkout, payments, AI, voice, push notifications, dark mode, every requested filter, or a complete ecommerce app. A small detail screen is a proposed addition because it lets you demonstrate return-to-results continuity.

## 3. Understand the evidence before selecting features

The explanations below are hypotheses until API experiments or app observations support them. The supplied analytics describe the scenario; they are not automatically measurements of today's live DummyJSON dataset.

### A. Every user complaint

| Feedback | Possible underlying cause | Investigation or response |
| --- | --- | --- |
| `red dress` returns nothing | Literal phrase matching, missing searchable attributes, or catalog coverage | Inspect actual dress records and search behavior. Do not remove `red` and pretend an arbitrary dress satisfies the request. |
| `phone` returns accessories | Broad substring matching or weak relevance | Inspect returned titles, categories, and descriptions; distinguish phones from accessories without hiding explicitly requested accessories. |
| Back resets list and filters | Results state is owned by a screen that remounts, or data changes reset the list | Retain query, filter, loaded results, and scroll continuity while visiting a product. |
| Too many unfamiliar filters | Cognitive load and unclear labels | Use a small, understandable narrowing control and a visible reset. More controls may worsen the issue. |
| Dark mode | A genuine preference with uncertain impact on this diagnosis | Likely defer unless there is additional evidence or spare time after core work. |
| Slow phone | Rendering, image loading, request latency, or several combined | Separate network waiting from UI responsiveness; test on Android rather than blaming RAM alone. |
| Spinner forever on bus | No request deadline, poor error handling, or a loading-state bug | Set a bounded timeout, show recovery, and keep existing usable data visible where appropriate. |
| Buy today | Stock availability or same-day delivery intent | Clarify the interpretation. `stock > 0` can support “In stock”; it cannot prove delivery today. |

### B. Search analytics

“Share of searches” is how common a query is. “Results” is returned product count. “Tap-through” is the proportion of searches followed by a product tap; confirm the exact denominator if needed. Taps are not purchases.

| Query | Share | Results | Tap-through | Question it raises |
| --- | ---: | ---: | ---: | --- |
| phone | 14% | 23 | 9% | Are many results irrelevant despite the large count? |
| laptop | 8% | 5 | 41% | Can a small relevant set work better than many weak matches? |
| red dress | 6% | 0 | — | Can the backend match several attributes, and does the catalog contain this combination? |
| cheap phone | 5% | 0 | — | Is this a product category plus price preference rather than a literal phrase? What would “cheap” mean? |
| smartphones | 4% | 2 | 12% | Does category vocabulary fail to match product titles? |
| phones | 3% | 4 | 15% | Does pluralization change recall unexpectedly? |
| iphone | 3% | 8 | 38% | Brand/model wording may work better than a generic category. The PDF wraps this word across lines; it is `iphone`, not a misspelling. |
| sunglass | 3% | 2 | 44% | Does singular/plural matching work consistently? |
| lap top | 1% | 0 | — | Should a safe normalization handle this spacing variant? |

These shares total **47%**, not 100%. Any metric based on this table covers only the listed queries. The zero-result queries account for 12 percentage points of all searches, or **12/47 ≈ 25.5% of this listed sample**, using the supplied table. This is scenario arithmetic, not a live API baseline.

Do not optimize zero-result rate by returning unrelated products. Lower zero-result rate alone can reward bad search.

### C. Usage data

- 61% of sessions are Android; 38% of those Android sessions use devices with 4 GB RAM or less. That is about 23.2% of all sessions. Prioritize Android checks and avoid unnecessary memory use; RAM is not a direct measurement of scroll performance.
- API p50 of 0.9 seconds means roughly half of requests finish within that duration. p90 of 3.8 seconds means roughly 90% do. The slow tail matters even if typical requests seem fine.
- About 5% fail/time out, mostly on mobile data. Failure behavior belongs in the core experience.
- 72% never open filters. Of the remaining 28%, 40% close without applying; approximately 16.8% of all sessions reach application, assuming these groups use the same session denominator. This suggests friction but does not prove extra filters will help.
- 47% leave soon after returning from a product. Together with the state-loss complaint, this supports investigating continuity. It does not prove state loss causes every exit.

### D. Stakeholder conflicts

| Stakeholder | Position | Proposed response to discuss |
| --- | --- | --- |
| PM | Add brand/rating/price/discount filters | Disagree with adding all now: confusing filters plus low usage suggests simplification first. Choose one useful filter with evidence. |
| Designer | Fewer card elements, chips instead of a filter screen | Adopt clear cards and visible controls where useful. A chip works well for a boolean or short category choice; not every filter fits a chip. |
| Engineering lead | No backend changes; lean dependencies | Respect this constraint. Expose client-side workaround limits rather than claiming a frontend can fix unrestricted catalog search at any size. |
| Marketing | Discounts on every card | Likely defer prominence unless needed. Product identity, price, and availability support the selected task more directly. Avoid inventing original-price calculations without checking field semantics. |

## 4. Our collaboration rules

You will create and build the app yourself. I will explain concepts, help investigate, review your code, and help debug. I will not scaffold or implement the app unless you explicitly change that preference.

For each implementation step:

1. Explain the behavior and the reason for it in your own words.
2. Choose the simplest implementation you understand.
3. Write it yourself, in a small increment.
4. Run it and deliberately try to break it.
5. Review the result together and make an authentic commit.

Before moving on, you should be able to answer: What does this code do? Where does state live? What happens when it fails? What alternative did I reject? How would I change it live?

Keep an AI-use log from the beginning. Do not invent a rejected suggestion or reflection to satisfy the documents; record actual disagreements and changed decisions as they occur.

## 5. Phase 1 — investigate the API together

Do this before deciding the search algorithm. Documentation is a starting point, not proof of implementation behavior.

Documentation checked: https://dummyjson.com/docs/products . It documents browse, search, categories, pagination, field selection, and sorting. We have not yet run the assignment's live API experiments or established undocumented limitations.

Create an investigation log during this phase with: timestamp, exact URL/command, purpose, HTTP status, total and returned counts, representative titles/categories, observation, and implication. Keep raw response samples where useful. Do not log only your conclusions.

Experiments for you to run and explain:

1. Browse `/products`; inspect the response envelope and actual catalog total. Check the default page size and missing/optional fields.
2. Run `/products/search?q=...` for every query in the table, with correct URL encoding.
3. Compare `phone`, `phones`, and `smartphones`. Inspect which returned records explain the difference, including descriptions/tags.
4. Inspect categories and smartphone/dress products. Is relevant data present even when literal search finds nothing?
5. Compare casing, whitespace, multiword phrases, and obvious normalization candidates. Test suspected behavior; do not assume tokenization or synonym support.
6. Test pagination and filters together. Determine whether a filter is actually supported or silently ignored. Filtering a single fetched page is not filtering the full result set.
7. Check stock, availability, minimum order quantity, shipping descriptions, images, price, and discount fields. Decide which fields safely support the proposed UI.
8. Compare requests with selected fields and full records. Record payload size if full-catalog loading becomes an option.
9. Try slow requests and failure cases. Distinguish API behavior from your app's own simulated fault behavior.

Exit condition: you can explain at least two actual API limitations and show the requests that prove them. No final search decision until this evidence exists.

## 6. Phase 2 — choose a small scope

Proposed product statement, subject to your decision:

> Help shoppers find relevant products and keep their browsing progress, even when the connection is unreliable.

Candidate flow:

- Discovery/results screen: product list, search input, one understandable filter, clear loading/error/empty states.
- Small product detail screen: enough information to judge a result and a way back.
- Returning from details preserves the prior search/filter and browsing position.
- Recovery path for failure, with reproducible slow/failure scenarios.

Candidate filter: **In stock**, if API data supports it consistently. It is easy to explain and addresses availability without promising same-day delivery. Category is an alternative if investigation shows it solves search relevance more directly.

Initial cuts: authentication, cart/checkout, AI search, voice, advanced animations, a large filter panel, and unrelated job-ad features. Offline persistence is now selected: save validated product data for offline browsing after restart, with an explicit expiry policy. Image files, guaranteed current stock, and offline transactions remain outside this scope.

Search approaches to compare after investigation:

| Approach | Benefit | Limitation to defend |
| --- | --- | --- |
| API-first search with a few explicit normalizations/category routes | Small client workload; potentially aligns with larger catalog access | Only helps known intents; backend limitations and filter composition can remain. |
| Fetch the small demo catalog and search/filter locally | Full visible dataset allows deterministic combinations and transparent ranking | Initial download, memory, stale data, and local indexing costs; not a free solution for 40,000 records. |
| Keep literal API search and focus on continuity/reliability | Minimal behavior changes and clear implementation | Major search complaints remain; explain why that scope is still the highest-value choice. |

Do not add a generic fuzzy-search dependency before proving it solves your actual problem. Do not define “cheap” with a hidden arbitrary price threshold. An explicit affordable-first sort or visible price choice is easier to defend, if you choose that scope.

## 7. Phase 3 — setup and architecture you can own

Choose Expo or React Native CLI based on your experience and available devices. Expo is a candidate because the assignment permits it, but the workflow and versions are still undecided. Check current setup instructions when you perform setup: https://docs.expo.dev/get-started/create-a-project/ . Use a starter without an implemented shopping flow and remove unused demo content.

Before feature work, personally run the smallest app on both native platforms. Discover environment problems early. Record exact versions/devices instead of claiming untested support.

Suggested boundaries, not a mandatory folder template:

- Product types/validation: which fields the UI can trust.
- Product API: URLs, response parsing, timeouts, and errors.
- Search/filter functions: explicit, testable rules separate from rendering.
- Discovery state: query, filter, request status, results, and continuity.
- Screens/components: render states and send user actions.
- Development fault controls: repeatable latency, failure, and unexpected-data cases at the API boundary.

Start with React state/hooks if sufficient. Add global state, caching libraries, or storage only for a concrete need you can explain. Use a virtualized product list and stable product keys; keep images appropriately sized. The data-fetching strategy determines whether pagination is required.

Most important correctness traps:

- Older search responses overwrite a newer query (if using request-per-query search).
- A page-local filter incorrectly claims no matching products exist anywhere.
- Retry uses an old query or loses the current filter.
- Search/filter changes do not reset pagination coherently.
- Returning from details remounts results or resets list position.
- A missing image, optional brand, invalid price, or malformed response crashes rendering.
- Loading never finishes because one error path fails to transition state.

## 8. Phase 4 — implement in small stages

Order, adjusted after scope discussion:

1. Minimal app runs on Android and iOS.
2. Fetch and display products with loading, failure, and retry states.
3. Add the chosen search behavior; explain it with concrete example queries.
4. Add one working filter, visible active state, and reset behavior.
5. Add detail navigation and verify return-to-results continuity.
6. Add repeatable slow/failing/unexpected-data demonstrations.
7. Write 2–4 targeted tests; run them and explain what each catches.
8. Measure baseline and improvement; record limitations.
9. Finish documentation and the 2–4 minute recording.

Use descriptive commits for actual completed changes. When a decision changes, commit the real change and explain why in DECISIONS.md. Do not deliberately add a bug to create a reflection.

## 9. Network behavior and demonstration

Decide behavior before implementation:

| Situation | Expected behavior |
| --- | --- |
| First load is slow | A clear loading state; controls respond; a bounded request deadline. |
| First load fails | Explain failure and offer retry; do not label it “no products.” |
| Refresh/new search fails with prior data available | If retaining data, label it as previous results and keep its original query context clear. Never pass old results off as matches for a new query. |
| Successful search genuinely returns none | Honest empty state; allow query/filter adjustment; do not suggest retry is a network fix. |
| Invalid response | Controlled error or explicitly justified record rejection; no crash. |
| Thumbnail fails | Layout remains usable with a fallback. |

A development fault switch can make scenarios reproducible without a prohibited backend/proxy. Route injected faults through the same handling used for real failures. Also verify at least one actual connection-loss scenario; simulation alone does not establish real network behavior. Record timing choices and their tradeoffs.

## 10. Tests: choose based on the final design

Aim for three meaningful tests rather than broad superficial coverage:

1. Search relevance/normalization: a concrete diagnosed query yields appropriate products and avoids a specific false positive.
2. The most likely design bug: stale search response suppression for request-per-query search, or complete-set filter correctness for a local-catalog design.
3. Timeout/failure recovery: loading exits and retry can succeed with the current query/filter.

A fourth test may cover return-to-results continuity if it is central to the chosen scope. Final test choice depends on the implementation, not this draft list.

## 11. Measurement: choose one primary metric

Candidate A: **weighted zero-result rate over the nine supplied queries**, if query recall is the main diagnosis.

- Run the same nine queries through literal API search and your implementation against the same recorded catalog snapshot where possible.
- Formula: sum of listed shares for queries returning zero / sum of listed shares (47).
- Report baseline and improved per-query outcomes so the aggregate is auditable.
- Inspect relevance separately to prevent misleading “improvement.” Nonempty unrelated results are not a success story.
- Limit: this sample is not all searches, not a user experiment, and does not prove conversion or search quality overall.

Candidate B: **relevant precision among the first five results**, if irrelevant `phone` results are the main diagnosis. Define relevance before evaluating; report per-query examples and the denominator when fewer than five results exist. Manual judgments and a small query sample are limitations.

Candidate C: **time to first useful result under a defined network scenario**, if reliability is central. Specify what “useful” means, device, network/fault settings, cold/warm state, and repeated runs. Do not compare a warm improved run to a cold baseline.

Choose one primary metric; do not spend the limited assignment time building an analytics system.

## 12. Scale and platform discussion

At 40,000 products, list virtualization only controls rendering. It does not solve downloading, storing, scanning, ranking, or keeping a whole catalog fresh. Quantify payload and client work if choosing a local-catalog demo.

API-first pagination avoids full downloads, but arbitrary client filters on partial pages can create false empty results and incorrect counts. A bounded scan is a tradeoff, not exact global filtering. State that explicitly.

Under the no-backend-change constraint, narrow supported behavior and explain what cannot be guaranteed. You may describe a future backend search/index as something needing reconsideration, but cannot build one for this submission.

Platform checks: safe areas, Android back behavior, iOS back behavior, keyboard/input interactions, loading/error layouts, image/list behavior, and actual return position. Verify Android responsiveness on a representative constrained device/emulator if available. Do not claim a low-end device test just because an emulator has limited RAM.

## 13. Presentation and live-change preparation

Tell one connected story:

1. The symptom you selected and evidence behind it.
2. What your API requests revealed.
3. What you built, what you cut, and whom you disagreed with.
4. The user flow on both platforms, including failure and recovery.
5. Your primary metric and what it does not prove.
6. A real changed decision, a remaining poorly handled query, and scale limits.

Practice small changes yourself: add a category chip, alter a normalization rule, add an explicit price control, change retry behavior, or show another optional product field. These are practice examples, not predictions of their live request.

For any proposed change, locate the responsible module, explain its effect on state and fetching, implement it, and run the relevant check. Prefer code you can reason about over layers you cannot modify confidently.

## 14. Decisions to discuss before setup

| Question | Current status |
| --- | --- |
| Deadline and available focused hours | 7-OCT (Every day two hours) |
| React Native/TypeScript experience | YES, React Native CLI with typescript |
| Android and iOS device/simulator availability | In my mac, which are available |
| Expo or CLI | Open; choose together based on familiarity and environment. | We use CLI
| Primary diagnosis | Open; continuity/reliability and search relevance are candidates. |
| API-first or local catalog | Open until investigation. |
| One filter and its semantics | Open; in-stock/category are candidates. |
| Primary metric | Open; align with the diagnosis. |
| Timeout, retry, and retained-data behavior | Open; define before coding. |

Next working step: discuss your time and experience, then have you run and record the first browse request and the `phone`/`phones`/`smartphones` searches. Explain the results together before setup and implementation.
