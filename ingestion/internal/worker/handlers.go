package worker

import (
	"context"
	"log"

	"github.com/segmentio/kafka-go"
)

func HandleInventory(ctx context.Context, m kafka.Message) error {
	log.Printf("inventory event key=%s payload=%s", string(m.Key), string(m.Value))
	return nil
}

func HandleOrders(ctx context.Context, m kafka.Message) error {
	log.Printf("order event key=%s payload=%s", string(m.Key), string(m.Value))
	return nil
}