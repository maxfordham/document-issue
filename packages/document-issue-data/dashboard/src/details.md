---
theme: dashboard
title: Details
toc: false
---

## Details

<div class="grid grid-cols-2">
  <div class="card">
    <h2>No. of Projects</h2>
    <span class="big">${new Set(docs.map(d => d.project)).size}</span>
  </div>
  <div class="card">
    <h2>Other</h2>
    <span class="big">${pl_details_count}</span>
  </div>
</div>

```js
const docs = FileAttachment("data/latest_found_details.csv").csv({typed: true});
```

```js
const search_docs = view(Inputs.search(docs, {placeholder: "Search details"}));
```

```js
Inputs.table(search_docs, {
  format: {
    project: d3.format("d"), // format as "1960" rather than "1,960"
    link: id => htl.html`<a href=mfllp:explorer.exe?${id} target=_blank>🔗</a>`
  },
  rows : 40
})
```

```js
const pl_details_count = Plot.plot({
  marginLeft: 90,
  color: { legend: true },
  marks: [Plot.barX(docs, Plot.groupZ({ x: "count" }, { fill: "role" }))]
})
```
