# ── Build stage for frontend ──────────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ── Production stage ─────────────────────────────────────────
FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Frontend (built assets)
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Create data dirs
RUN mkdir -p /app/data /app/static/uploads /app/static/icon-cache

# Environment
ENV HOST=0.0.0.0
ENV PORT=8083
ENV API_KEY=""
ENV DB_PATH=/app/data/aitoolhub.db
ENV NGINX_SPA_DIR=/app/frontend/dist
ENV NGINX_UPLOAD_DIR=/app/frontend/dist/uploads

EXPOSE 8083

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -sf http://localhost:8083/api/posts || exit 1

CMD ["python3", "main.py"]
