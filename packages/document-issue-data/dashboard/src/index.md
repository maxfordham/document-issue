---
title: Latest Issued Documents
theme: dashboard
# theme: [light, dark, alt, wide]
toc: false
---

## Latest Issued Documents

```js
const docs = FileAttachment("data/latest_found.csv").csv({typed: true});
```

```js
const search_docs = view(Inputs.search(docs, {placeholder: "Search docs"}));
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
