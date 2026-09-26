// theme + live filter (progressive enhancement over server-rendered cards)
(function(){
  const root = document.documentElement;
  const saved = localStorage.getItem("dn-theme");
  if(saved) root.setAttribute("data-theme", saved);
  const btn = document.getElementById("theme-toggle");
  function label(){
    const dark = root.getAttribute("data-theme")==="dark";
    if(btn) btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
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
  let currentSlug = document.querySelector("#cards .card")?.dataset.slug || null;
  function apply(follow){
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
    // filters drive the middle reader: if the open note got filtered out, show the first match
    if(follow !== false && typeof selectPost === "function"){
      const vis = cards.filter(c=>c.style.display!=="none");
      if(vis.length && !vis.some(c=>c.dataset.slug===currentSlug)){
        selectPost(vis[0].dataset.slug, false);
        try{
          const url = new URL(location.href);
          url.hash = "post-" + currentSlug;
          history.replaceState(null, "", url);
        }catch(e){}
      }
    }
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

  // center reader: show latest by default, swap when a right-list note is picked
  const readerTitle = document.getElementById("reader-title");
  const readerDate = document.getElementById("reader-date");
  const readerMeta = document.getElementById("reader-meta");
  const readerTags = document.getElementById("reader-tags");
  const readerBody = document.getElementById("reader-body");
  const readerOpen = document.getElementById("reader-open");
  function selectPost(slug, pushHash){
    if(!readerBody) return false;
    const card = document.querySelector('.card[data-slug="' + slug + '"]');
    const tpl = document.getElementById("post-body-" + slug);
    if(!card || !tpl) return false;
    currentSlug = slug;
    if(readerTitle){
      const link = readerTitle.querySelector("a");
      const title = card.dataset.title || slug;
      if(link){ link.textContent = title; link.href = "/post/" + slug; }
      else readerTitle.textContent = title;
    }
    if(readerDate) readerDate.textContent = card.dataset.date || "";
    if(readerMeta) readerMeta.textContent = (card.dataset.mins || "?") + " min read · " + (card.dataset.words || "?") + " words";
    if(readerTags){
      readerTags.innerHTML = "";
      card.querySelectorAll(".links .pill").forEach(p=>readerTags.appendChild(p.cloneNode(true)));
    }
    readerBody.innerHTML = tpl.innerHTML;
    if(readerOpen) readerOpen.href = "/post/" + slug;
    cards.forEach(c=>c.classList.toggle("active", c.dataset.slug===slug));
    if(pushHash !== false){
      try{
        const url = new URL(location.href);
        url.hash = "post-" + slug;
        history.replaceState(null, "", url);
      }catch(e){}
    }
    return true;
  }
  document.addEventListener("click", (e)=>{
    const t = e.target.closest ? e.target.closest("[data-preview]") : null;
    if(!t) return;
    if(e.metaKey || e.ctrlKey || e.shiftKey) return; // let new-tab clicks through
    e.preventDefault();
    selectPost(t.dataset.preview);
  });
  // deep-link: #post-<slug> opens that note in the reader on load
  if(location.hash && location.hash.indexOf("#post-")===0){
    selectPost(location.hash.slice(6), false);
  } else {
    const first = document.querySelector("#cards .card");
    if(first && readerBody) first.classList.add("active");
  }
})();
