import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';

import { validateProducts } from '../../../ShopDiscover/src/features/products/api.ts';
import { searchProducts } from '../../../ShopDiscover/src/features/products/searchProducts.ts';

// Run the actual app functions against saved responses, without another request.
const baselinePath = new URL('./baseline.json', import.meta.url);
const catalogPath = new URL('./catalog.json', import.meta.url);
const baselineText = await readFile(baselinePath, 'utf8');
const catalogText = await readFile(catalogPath, 'utf8');
const baseline = JSON.parse(baselineText);
const catalog = JSON.parse(catalogText);
const products = validateProducts(catalog.products);
assert.equal(products.length, catalog.total, 'Catalog must be complete');
assert.equal(baseline.products.length, 5, 'Baseline must contain five results');

const firstFive = products =>
  products.slice(0, 5).map(({ id, title, category }) => ({ id, title, category }));
const literal = firstFive(baseline.products);
const local = firstFive(searchProducts(products, 'phone'));
const relevant = results =>
  results.filter(product => product.category === 'smartphones').length;

// Check overlapping evidence; separate requests are not an atomic snapshot.
const comparisonFields = ['title', 'description', 'category', 'price', 'stock', 'tags', 'thumbnail', 'brand'];
const mismatchedBaselineIds = baseline.products
  .filter(product => {
    const counterpart = products.find(item => item.id === product.id);
    return !counterpart || comparisonFields.some(
      field => JSON.stringify(product[field]) !== JSON.stringify(counterpart[field]),
    );
  })
  .map(product => product.id);

console.log(JSON.stringify({
  measuredAt: new Date().toISOString(),
  query: 'phone',
  relevanceRule: 'category === smartphones',
  stockFilter: false,
  priceRange: {},
  baseline: {
    url: 'https://dummyjson.com/products/search?q=phone&limit=5',
    capturedAt: (await stat(baselinePath)).mtime.toISOString(),
    responseBytes: Buffer.byteLength(baselineText),
    total: baseline.total,
    firstFive: literal,
    relevantCount: relevant(literal),
  },
  local: {
    url: 'https://dummyjson.com/products?limit=0&select=title,description,category,price,stock,tags,thumbnail,brand',
    capturedAt: (await stat(catalogPath)).mtime.toISOString(),
    responseBytes: Buffer.byteLength(catalogText),
    catalogTotal: products.length,
    resultTotal: searchProducts(products, 'phone').length,
    firstFive: local,
    relevantCount: relevant(local),
  },
  mismatchedBaselineIds,
}, null, 2));
