package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/segmentio/kafka-go"

	"github.com/sgmultidia/ingestion/internal/config"
	"github.com/sgmultidia/ingestion/internal/worker"
)

func main() {
	cfg := config.Load()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	readers := make(map[string]*kafka.Reader)
	handlers := map[string]worker.Handler{
		"ml.orders":    worker.HandleOrders,
		"ml.inventory": worker.HandleInventory,
	}

	for _, topic := range cfg.Topics {
		readers[topic] = worker.NewReader(cfg.Brokers, cfg.GroupID, topic)
	}

	worker.Run(ctx, readers, handlers)

	srv := &http.Server{Addr: cfg.HealthAddr}
	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok"))
	})

	go func() {
		log.Printf("healthcheck on %s", cfg.HealthAddr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Printf("health server error: %v", err)
		}
	}()

	<-ctx.Done()
	log.Println("shutting down...")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	_ = srv.Shutdown(shutdownCtx)
}