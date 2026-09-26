// theme + live filter (progressive enhancement over server-rendered cards)
(function(){
  const root = document.documentElement;
  const saved = localStorage.getItem("dn-theme");
  if(saved) root.setAttribute("data-theme", saved);
  const btn = document.getElementById("theme-toggle");
  function label(){
    const dark = root.getAttribute("data-theme")==="dark";
    if(btn) btn.textContent = dark ? "light" : "dark";
  }
  label();
  if(btn) btn.addEventListener("click", ()=>{
    const dark = root.getAttribute("data-theme")==="dark";
    root.setAttribute("data-theme", dark ? "light" : "dark");
    localStorage.setItem("dn-theme", dark ? "light" : "dark");
    label();
  });

  // live client-side filter on index cards
  const q = document.getElementById("q");
  const cards = Array.from(document.querySelectorAll("#cards .card"));
  const bar = document.getElementById("results-bar");
  const nores = document.getElementById("no-results");
  const chips = Array.from(document.querySelectorAll("[data-tag-filter]"));
  let activeTag = document.querySelector(".achip.on")?.dataset.tagFilter || "";
  function apply(){
    const needle = (q?.value || "").trim().toLowerCase();
    let shown = 0;
    cards.forEach(c=>{
      const hay = (c.dataset.search || "").toLowerCase();
      const okQ = !needle || hay.includes(needle);
      const okT = !activeTag || (c.dataset.tags || "").split(",").includes(activeTag);
      const show = okQ && okT;
      c.style.display = show ? "" : "none";
      if(show) shown++;
    });
    if(bar){
      if(needle || activeTag){
        bar.style.display = "";
        bar.querySelector("span").textContent = shown + " note" + (shown===1?"":"s") + (activeTag ? " tagged #" + activeTag : "") + (needle ? ' matching "' + (q.value.trim()) + '"' : "");
      } else bar.style.display = "none";
    }
    if(nores) nores.style.display = shown===0 ? "" : "none";
  }
  if(q) q.addEventListener("input", apply);
  chips.forEach(ch=>ch.addEventListener("click", (e)=>{
    // allow cmd/ctrl-click to follow link (server filter); plain click = instant client filter
    if(e.metaKey || e.ctrlKey) return;
    e.preventDefault();
    const t = ch.dataset.tagFilter;
    activeTag = (activeTag === t) ? "" : t;
    chips.forEach(c=>c.classList.toggle("on", c.dataset.tagFilter===activeTag));
    apply();
    // sync URL without reload
    const url = new URL(location.href);
    if(activeTag) url.searchParams.set("tag", activeTag); else url.searchParams.delete("tag");
    history.replaceState(null, "", url);
  }));
  if(q || chips.length) apply();
})();
