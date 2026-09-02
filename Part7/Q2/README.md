# Part 7 — OpenTelemetry Collector

## Overview

This section configures an OpenTelemetry Collector for receiving and processing telemetry from the rbcapp1 REST API.

## OTLP Receivers

The Collector accepts OTLP telemetry using:

- OTLP gRPC on port `4317`
- OTLP HTTP on port `4318`

## Processors

The following processors are configured:

- `memory_limiter` to control Collector memory usage
- `batch` to batch telemetry before export

## Pipelines

### Traces

Traces are received through OTLP and exported toward the Elastic APM endpoint.

### Metrics

Metrics are received through OTLP and exported to Elasticsearch.

### Host Metrics

Host metrics are collected for:

- host1
- host2
- host3

The configured host metrics include CPU, memory, and disk metrics.

## Configuration File

The Collector configuration is stored in:

```text
Part7/Q2/otel-collector-config.yaml
