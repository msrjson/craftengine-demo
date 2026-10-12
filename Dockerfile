# Craft Engine demo - the engine comes from the canonical remote, pinned to
# a release tag. The demo never copies, links or mounts the framework sources:
# a framework change reaches it only through a release.
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

ARG CRAFT_ENGINE_REF=v4.8.0-r00028

WORKDIR /app

RUN pip install --no-cache-dir \
    "craft[dev] @ https://github.com/msrjson/craftengine/archive/refs/tags/${CRAFT_ENGINE_REF}.tar.gz#subdirectory=data"

COPY . .

EXPOSE 9002

CMD ["sh", "-c", "python dev.py migrate && python dev.py serve --host 0.0.0.0 --port 9002 --no-reload"]
