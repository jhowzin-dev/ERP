FROM golang:1.22-alpine AS build
WORKDIR /workspace
COPY . .
RUN CGO_ENABLED=0 go build -o /out/worker ./cmd/worker

FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/worker worker
EXPOSE 8081
ENTRYPOINT ["/app/worker"]