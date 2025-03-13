---
theme: dashboard
title: Schematics
toc: false
---

## Schematics

<div class="grid grid-cols-2">
  <div class="card">
    <h2>No. of Projects</h2>
    <span class="big">${new Set(schematics.map(d => d.project)).size}</span>
  </div>
  <div class="card">
    <h2>Other</h2>
    <span class="big">${pl_schem_count}</span>
  </div>
</div>

```js
const schematics = FileAttachment("data/latest_found_schematics.csv").csv({typed: true});
```

```js
const search_schematics = view(Inputs.search(schematics, {placeholder: "Search schematics"}));
```

```js
Inputs.table(search_schematics, {
  format: {
    project: d3.format("d"), // format as "1960" rather than "1,960"
    link: id => htl.html`<a href=mfllp:explorer.exe?${id} target=_blank>🔗</a>`
  },
  rows : 40
})
```

```js
const pl_schem_count = Plot.plot({
  marginLeft: 90,
  color: { legend: true },
  marks: [Plot.barX(schematics, Plot.groupZ({ x: "count" }, { fill: "role" }))]
})
```
