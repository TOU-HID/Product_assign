# Your decisions and next steps

Keep all Markdown files in `product_assignment/docs`, outside `ShopDiscover/`.

## Suggested decisions

These are starting recommendations. Confirm the search approach after testing the API.

| Decision | Why |
| --- | --- |
| Build a small shopping discovery app | That is the assignment; AI chat is not required. |
| Focus on relevant search, preserving browsing progress, and network recovery | These address repeated complaints and supporting usage data. |
| Use one **In stock** filter | Simple to understand and useful. Verify the stock field first; do not promise delivery today. |
| Use two screens: results and product details | Enough to demonstrate discovery and returning without losing query, filter, or scroll position. |
| Defer dark mode, cart, login, and extra filters | They add work without directly supporting this scope. |
| Start with TypeScript and simple React state | Keep the code easy for you to explain and change. Choose Expo or CLI based on your familiarity. |
| Choose the search implementation after API investigation | Otherwise you might build around assumptions that are wrong. |

## Do these steps in order

1. **Set your time budget.** Write down the deadline, available hours, and whether Android and iOS can run locally.
2. **Investigate the API before coding.** Open the URLs below. Record result counts and representative product titles/categories. Compare actual phones with accessories.
3. **Choose search behavior.** Decide which query improvements the evidence supports. Keep unsupported cases honest; do not return unrelated products just to avoid empty results.
4. **Set up the app yourself.** Run the smallest app on Android and iOS before adding features. Make your first real Git commit.
5. **Build in small increments.** Product list → loading/error/retry → search → filter → details and preserved browsing state. Run and commit each working increment.
6. **Prove it works.** Demonstrate slow/failing requests and unexpected data. Add 2–4 tests, including the bug most likely in your design.
7. **Measure and submit.** Compare one search metric with literal API search, explain its limits, finish the required documents, and record both platforms.

## Your immediate task: inspect these requests

- Browse: https://dummyjson.com/products
- Search: https://dummyjson.com/products/search?q=phone
- Compare: https://dummyjson.com/products/search?q=phones
- Compare: https://dummyjson.com/products/search?q=smartphones

For each request, note: **What came back? Is it relevant? What limitation does this reveal?** These are the first experiments; afterward, test every query from the PDF and investigate filtering/pagination.

## Remember while building

- Failed request and zero matching products are different states.
- Filtering only one fetched page does not filter the whole catalog.
- A small-catalog solution may not work at 40,000 products; explain that honestly.
- Keep real commits and brief decision/AI-use notes as you work.
- You write the app; I explain, review, and help debug. Choose code you can modify live.
