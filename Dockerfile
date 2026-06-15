# ─────────────────────────────────────────────────────────────────
# LAYER 1 — Base Image
# Slim Python 3.11 keeps the image small (~50MB vs ~900MB full).
# Always pin to a specific version — avoids "it worked yesterday"
# surprises when the base image updates silently.
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ─────────────────────────────────────────────────────────────────
# LAYER 2 — Working Directory
# All subsequent commands run from /app inside the container.
# Keeps the filesystem clean — no files scattered at root level.
# ─────────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────────
# LAYER 3 — Install Dependencies FIRST (before copying app code)
# Docker caches each layer. By copying requirements.txt alone and
# installing, this layer is only re-built when dependencies change.
# If you copy all files first, every code change rebuilds packages.
# That's why order matters.
# ─────────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────────
# LAYER 4 — Copy Application Code
# This layer changes every time you edit app.py, so it goes AFTER
# the dependency install layer. Cache is preserved for packages.
# ─────────────────────────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────────────────────────
# LAYER 5 — Expose Port
# Documents which port the app runs on. Required for cloud platforms
# (Railway, Render, GCP) to route traffic to the container.
# Streamlit default = 8501.
# ─────────────────────────────────────────────────────────────────
EXPOSE 8501

# ─────────────────────────────────────────────────────────────────
# LAYER 6 — Healthcheck
# Cloud platforms poll this to know if the container is alive.
# Without it, a crashed app looks "running" and receives traffic.
# ─────────────────────────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ─────────────────────────────────────────────────────────────────
# LAYER 7 — Entry Point
# --server.port           : bind to $PORT env var (cloud platforms
#                           inject this) or default 8501
# --server.address        : 0.0.0.0 = accept connections from
#                           outside the container (required!)
# --server.headless true  : disables browser auto-open in container
# ─────────────────────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py",
     "--server.port=8501",
     "--server.address=0.0.0.0",
     "--server.headless=true"]
