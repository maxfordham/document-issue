---
title: Latest Issued Documents
theme: dashboard
toc: false
---

## Latest Issued Documents

```js
const data = FileAttachment("data/latest_found.csv").csv({typed: true});
```

```js
const filtered = view(Inputs.search(data));

```


```js
Inputs.table(filtered, {
  format: {
    project: d3.format("d"),
    link: id => htl.html`<a href=mfllp:explorer.exe?${id} target=_blank>🔗</a>`
  },
  rows: 40
})
```
