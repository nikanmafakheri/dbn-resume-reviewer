# Package marker for the `app` package.
#
# NOTE: this must stay empty. Vercel's Python runtime loads the ASGI entrypoint
# (`app.main:app`) with `importlib.util.spec_from_file_location()`, which does
# NOT import the parent `app` package first. If this file re-exported anything
# from `app.main` (e.g. `create_app`), then `app/main.py`'s first `from
# app.core...` import would re-enter this module mid-execution → circular import
# → `ImportError: cannot import name 'create_app' from 'app.main'` at boot.
