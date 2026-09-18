# syntax=docker/dockerfile:1

# ── Build stage ───────────────────────────────────────────────────────────────
# Roda na plataforma NATIVA do builder ($BUILDPLATFORM): o output do Vite é
# estático e agnóstico de plataforma, então npm/tsc/vite não precisam rodar sob
# QEMU quando o alvo é linux/arm64 (mesma estratégia do backend/Dockerfile).
FROM --platform=$BUILDPLATFORM node:22-alpine AS build
WORKDIR /app

# Camada cacheável: só invalida quando as dependências mudam.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Runtime stage ─────────────────────────────────────────────────────────────
# Segue $TARGETPLATFORM (default do buildx): nginx binário correto para arm64.
FROM nginxinc/nginx-unprivileged:alpine-slim

LABEL org.opencontainers.image.source="https://github.com/<org>/omnicore" \
      org.opencontainers.image.description="OminiCore frontend — SPA estatica servida por nginx"

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
