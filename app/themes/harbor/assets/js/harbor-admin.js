// Harbor admin chrome: collapse and expand the left menu.
// Progressive enhancement - without this file the menu stays visible and the
// button does nothing harmful.
(() => {
  const toggle = document.querySelector("[data-menu-toggle]");
  if (!toggle) return;

  const menu = document.getElementById(toggle.getAttribute("aria-controls") || "");
  if (!menu) return;

  toggle.addEventListener("click", () => {
    const collapsed = document.body.classList.toggle("is-menu-collapsed");
    toggle.setAttribute("aria-expanded", String(!collapsed));
  });
})();
