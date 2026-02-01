import { useEffect, useState } from "react";

const apiBase = window.appConfig?.apiBase || "http://localhost:8000";

export default function App() {
  const [q, setQ] = useState("");
  const [tags, setTags] = useState("");
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(null);

  async function search() {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (tags) {
      tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean)
        .forEach((t) => params.append("tags", t));
    }
    const res = await fetch(`${apiBase}/anime/search?${params.toString()}`);
    const data = await res.json();
    setItems(data.items || []);
  }

  async function openDetail(id) {
    const res = await fetch(`${apiBase}/anime/${id}`);
    if (res.ok) {
      setSelected(await res.json());
    }
  }

  useEffect(() => {
    search();
  }, []);

  return (
    <div className="app">
      <header className="toolbar">
        <input
          placeholder="Search title"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <input
          placeholder="Tags (comma separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />
        <button onClick={search}>Search</button>
      </header>
      <div className="content">
        <section className="list">
          {items.map((item) => (
            <button
              key={item.id}
              className="list-item"
              onClick={() => openDetail(item.id)}
            >
              <div className="title">{item.title}</div>
              <div className="meta">score: {item.score ?? "-"}</div>
            </button>
          ))}
        </section>
        <section className="detail">
          {selected ? (
            <div>
              <h2>{selected.title}</h2>
              <div>{selected.title_original}</div>
              <div>{selected.author}</div>
              <div className="tags">{(selected.tags || []).join(", ")}</div>
              <p>{selected.description}</p>
            </div>
          ) : (
            <div className="empty">Select an item</div>
          )}
        </section>
      </div>
    </div>
  );
}
