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
const unique_systems = [...new Set(data.map(d => d.system))].filter(d => d != null && d !== "");
```

```js
const filters = view(Inputs.form({
  search: Inputs.search(data, {placeholder: "Global search..."}),
  system: Inputs.select(unique_systems, {
    label: "System",
    multiple: true,
    unique: true,
    sort: true,
    placeholder: "All systems",
    allowClear: true // <-- Add this line
  })
}));
```

```js
const filtered = data.filter(d => {
  // Robustly extract the search string
  let search = "";
  if (typeof filters.search?.value === "string") {
    search = filters.search.value.toLowerCase();
  } else if (typeof filters.search === "string") {
    search = filters.search.toLowerCase();
  }
  const matchesSearch = !search || Object.values(d).some(v => (v + "").toLowerCase().includes(search));
  const matchesSystem = !filters.system?.length || filters.system.includes(d.system);
  return matchesSearch && matchesSystem;
});
```

```js
Inputs.table(
  filtered, {
  format: {
    project: d3.format("d"), // format as "1960" rather than "1,960"
    link: id => htl.html`<a href=mfllp:explorer.exe?${id} target=_blank>🔗</a>`
  },
  rows: 40})
```

