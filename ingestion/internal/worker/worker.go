package worker

import (
	"context"
	"log"

	"github.com/segmentio/kafka-go"
)

type Handler func(ctx context.Context, m kafka.Message) error

func NewReader(brokers []string, groupID, topic string) *kafka.Reader {
	return kafka.NewReader(kafka.ReaderConfig{
		Brokers:  brokers,
		GroupID:  groupID,
		Topic:    topic,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})
}

func Run(ctx context.Context, readers map[string]*kafka.Reader, handlers map[string]Handler) {
	for topic, r := range readers {
		go consume(ctx, r, topic, handlers[topic])
	}
}

func consume(ctx context.Context, r *kafka.Reader, topic string, handler Handler) {
	defer r.Close()
	log.Printf("consuming topic=%s group=%s", topic, r.Config().GroupID)

	for {
		m, err := r.ReadMessage(ctx)
		if err != nil {
			if ctx.Err() != nil {
				return
			}
			log.Printf("topic=%s read error: %v", topic, err)
			continue
		}
		if handler != nil {
			if err := handler(ctx, m); err != nil {
				log.Printf("topic=%s handler error: %v", topic, err)
			}
			continue
		}
		log.Printf("msg topic=%s partition=%d offset=%d key=%s len=%d",
			m.Topic, m.Partition, m.Offset, string(m.Key), len(m.Value))
	}
}