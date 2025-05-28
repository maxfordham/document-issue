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
  // Global search
  const search = filters.search?.value?.toLowerCase() ?? "";
  const matchesSearch = !search || Object.values(d).some(v => (v + "").toLowerCase().includes(search));
  // System filter
  const matchesSystem = !filters.system?.length || filters.system.includes(d.system);
  return matchesSearch && matchesSystem;
});
```

```js
Inputs.table(filtered, {rows: 40})
```
