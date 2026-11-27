(() => {
  // ── Archive index: search, type chips, tags, sort ──
  const grid = document.getElementById("grid");
  if (grid) {
    const cards = [...grid.querySelectorAll(".card")];
    const q = document.getElementById("q");
    const sort = document.getElementById("sort");
    const status = document.getElementById("status");
    const nomatch = document.getElementById("nomatch");
    const params = new URLSearchParams(location.search);
    const st = { type: params.get("type") || "all", tag: params.get("tag") || "", q: params.get("q") || "", sort: params.get("sort") || "new" };
    q.value = st.q; sort.value = st.sort;

    function syncUrl() {
      const p = new URLSearchParams();
      if (st.type !== "all") p.set("type", st.type);
      if (st.tag) p.set("tag", st.tag);
      if (st.q.trim()) p.set("q", st.q.trim());
      if (st.sort !== "new") p.set("sort", st.sort);
      const s = p.toString();
      history.replaceState(null, "", location.pathname + (s ? "?" + s : ""));
    }

    function apply() {
      document.querySelectorAll(".chip").forEach(c => c.setAttribute("aria-pressed", String(c.dataset.type === st.type)));
      document.querySelectorAll(".tagline .tag").forEach(t => t.setAttribute("aria-pressed", String(t.dataset.tag === st.tag)));
      const words = st.q.toLowerCase().split(/\s+/).filter(Boolean);
      let shown = 0;
      cards.forEach(c => {
        const ok = (st.type === "all" || c.dataset.type === st.type)
          && (!st.tag || c.dataset.tags.includes("|" + st.tag + "|"))
          && words.every(w => c.dataset.search.includes(w));
        c.hidden = !ok; if (ok) shown++;
      });
      const sorted = [...cards].sort((a, b) => {
        if (st.sort === "title") return a.dataset.title.localeCompare(b.dataset.title);
        if (st.sort === "era") return (parseInt(a.dataset.year) || 1e9) - (parseInt(b.dataset.year) || 1e9);
        const pin = (+b.dataset.pinned) - (+a.dataset.pinned);
        if (pin) return pin;
        const d = a.dataset.date.localeCompare(b.dataset.date);
        return st.sort === "old" ? d : -d;
      });
      sorted.forEach(c => grid.appendChild(c));
      nomatch.hidden = shown > 0;
      const filtered = st.type !== "all" || st.tag || words.length;
      status.textContent = filtered ? `${shown} of ${cards.length} entries${st.tag ? " tagged #" + st.tag : ""}` : "";
      syncUrl();
    }

    document.querySelectorAll(".chip").forEach(c => c.addEventListener("click", () => { st.type = c.dataset.type; apply(); }));
    document.querySelectorAll(".tagline .tag").forEach(t => t.addEventListener("click", () => { st.tag = st.tag === t.dataset.tag ? "" : t.dataset.tag; apply(); }));
    let timer; q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(() => { st.q = q.value; apply(); }, 120); });
    sort.addEventListener("change", () => { st.sort = sort.value; apply(); });
    document.addEventListener("keydown", (e) => { if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); } });
    apply();
  }

  // ── Thread posts: label 1/n, 2/n … ──
  const tb = document.querySelector(".thread-body");
  if (tb) {
    const ps = [...tb.children].filter(n => n.tagName === "P");
    ps.forEach((p, i) => p.setAttribute("data-n", `${i + 1}/${ps.length}`));
  }

  // ── Copy link / citation ──
  document.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", async () => {
    const label = b.textContent;
    try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = "Copied"; }
    catch { b.textContent = "Copy failed"; }
    setTimeout(() => { b.textContent = label; }, 1600);
  }));

  // ── Lightbox for charts and photos ──
  const lb = document.getElementById("lightbox");
  if (lb && lb.showModal) {
    const img = lb.querySelector("img"), dl = document.getElementById("lightbox-dl");
    document.querySelectorAll(".zoom").forEach(z => z.addEventListener("click", () => {
      img.src = z.dataset.full; img.alt = z.querySelector("img").alt; dl.href = z.dataset.full; lb.showModal();
    }));
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  }
})();

// ── Visit counter (GoatCounter) ──
(() => {
  const code = document.body.dataset.gc;
  if (!code || !/^[a-z0-9-]+$/i.test(code)) return;
  document.querySelectorAll("[data-views]").forEach(async (box) => {
    const path = box.dataset.views === "TOTAL" ? "TOTAL" : encodeURIComponent(location.pathname);
    let count = "0";
    try {
      const r = await fetch(`https://${code}.goatcounter.com/counter/${path}.json`);
      if (r.ok) { const j = await r.json(); count = String(j.count || "0").trim(); }
      else if (r.status !== 404) return; // 404 just means no visits recorded yet
    } catch { return; }
    const out = box.querySelector("b, dd");
    out.textContent = count;
    box.hidden = false;
  });
})();
