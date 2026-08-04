FROM python:3.12-slim

# python-magic (used for MIME detection) needs the system libmagic library.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY app/ app/
COPY migrations/ migrations/
# alembic.ini holds script_location + logging config; `alembic upgrade head`
# in CMD needs it present (env.py imports app.* so prepend_sys_path=. too).
COPY alembic.ini .

# Run migrations at startup (unless DEBUG, which lets create_all own the schema).
# DEBUG is controlled by the DEBUG env var set in compose, not baked into the image.
EXPOSE 8000

CMD ["/bin/sh", "-c", "if [ \"$DEBUG\" != \"true\" ]; then alembic upgrade head; fi && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
