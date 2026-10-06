# Midnight theme views

A file here overrides the view at the same path: `layouts/app.forge.py`
overrides `resources/views/layouts/app.forge.py`, and
`<module>/index.forge.py` overrides `<module>::index`. Select the theme with
`VIEW_THEME=midnight`, or per request with `View.set_theme_resolver`.
