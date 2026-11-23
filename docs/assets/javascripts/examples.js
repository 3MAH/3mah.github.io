// Library filter for the unified example gallery (works with instant navigation)
document$.subscribe(() => {
  const buttons = document.querySelectorAll(".example-filter");
  if (!buttons.length) return;
  const cards = document.querySelectorAll(".example-grid .example-card");
  const apply = (lib) => {
    buttons.forEach((b) => b.classList.toggle("is-active", b.dataset.filter === lib));
    cards.forEach((c) => { c.hidden = lib !== "all" && c.dataset.library !== lib; });
  };
  buttons.forEach((b) => b.addEventListener("click", () => {
    apply(b.dataset.filter);
    history.replaceState(null, "", b.dataset.filter === "all" ? location.pathname : "#" + b.dataset.filter);
  }));
  const fromHash = location.hash.slice(1);
  if ([...buttons].some((b) => b.dataset.filter === fromHash)) apply(fromHash);
});
