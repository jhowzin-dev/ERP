package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/segmentio/kafka-go"
)

const (
	topicOrders     = "ml.orders"
	topicInventory  = "ml.inventory"
	bootstrapBroker = "localhost:9092"
	groupID         = "ingestion-ml"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{bootstrapBroker},
		GroupID:  groupID,
		Topic:    topicOrders,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})
	defer r.Close()

	log.Printf("ingestion listening on %s (group %s)", topicOrders, groupID)

	for {
		m, err := r.ReadMessage(ctx)
		if err != nil {
			if ctx.Err() != nil {
				return
			}
			log.Printf("read error: %v", err)
			continue
		}
		log.Printf("msg topic=%s partition=%d offset=%d key=%s len=%d", m.Topic, m.Partition, m.Offset, string(m.Key), len(m.Value))
	}
}