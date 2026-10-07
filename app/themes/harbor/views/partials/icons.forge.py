{#
    Harbor admin menu icons: one inline sprite, no external request.

    Each module names an icon on its `crm.navigation` entry ("icon": "<slug>").
    The layout renders `<use href="#icon-<slug>">`; the presentation attributes
    (stroke, fill) belong to the referencing <svg>, so the symbols only carry
    shapes and a viewBox.
#}
<svg class="icon-sprite" width="0" height="0" aria-hidden="true" focusable="false">
  <symbol id="icon-dot" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/></symbol>
  <symbol id="icon-dashboard" viewBox="0 0 24 24"><path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/></symbol>
  <symbol id="icon-posts" viewBox="0 0 24 24"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/><path d="M10 12h6M10 16h6"/></symbol>
  <symbol id="icon-pages" viewBox="0 0 24 24"><path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4"/><path d="M10 13h5"/></symbol>
  <symbol id="icon-media" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15l-5-5-6 6"/></symbol>
  <symbol id="icon-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M16 5.5a3 3 0 0 1 0 5"/><path d="M21 20c0-2.2-1.2-4-3-4.6"/></symbol>
  <symbol id="icon-companies" viewBox="0 0 24 24"><rect x="4" y="3" width="11" height="18" rx="1"/><path d="M15 9h5v12h-5"/><path d="M7.5 7h2M7.5 11h2M7.5 15h2"/></symbol>
  <symbol id="icon-contacts" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"/></symbol>
  <symbol id="icon-deals" viewBox="0 0 24 24"><path d="M3 12 12 3h7v7l-9 9z"/><circle cx="15.5" cy="7.5" r="1.3"/></symbol>
  <symbol id="icon-activities" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/><path d="M7.5 13h3M13.5 13h3M7.5 17h3"/></symbol>
  <symbol id="icon-extensions" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M17.5 14v7M14 17.5h7"/></symbol>
  <symbol id="icon-menus" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
  <symbol id="icon-settings" viewBox="0 0 24 24"><path d="M4 7h7M15 7h5M4 17h9M17 17h3"/><circle cx="13" cy="7" r="2"/><circle cx="15" cy="17" r="2"/></symbol>
</svg>
