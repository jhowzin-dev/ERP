# syntax=docker/dockerfile:1

# ── Build stage ───────────────────────────────────────────────────────────────

FROM --platform=$BUILDPLATFORM golang:1.22-alpine AS build
WORKDIR /workspace

# Cache module 
COPY go.mod go.sum ./
RUN go mod download

COPY . .

ARG TARGETOS
ARG TARGETARCH
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH \
    go build -trimpath -ldflags="-s -w" -o /out/worker ./cmd/worker

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app


COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

COPY --from=build /out/worker /app/worker

USER nonroot:nonroot
EXPOSE 8081
ENTRYPOINT ["/app/worker"]

