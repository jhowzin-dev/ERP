package config

import (
	"os"
	"strings"
	"time"
)

type Config struct {
	Brokers       []string
	GroupID       string
	Topics        []string
	HealthAddr    string
	ReadTimeout   time.Duration
}

func Load() Config {
	brokers := getEnv("KAFKA_BROKERS", "localhost:9092")
	topics := getEnv("KAFKA_TOPICS", "ml.orders,ml.inventory")
	return Config{
		Brokers:     strings.Split(brokers, ","),
		GroupID:     getEnv("KAFKA_GROUP_ID", "ingestion-ml"),
		Topics:      strings.Split(topics, ","),
		HealthAddr:  getEnv("HEALTH_ADDR", ":8081"),
		ReadTimeout: 10 * time.Second,
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}