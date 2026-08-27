# Part 5 - Q2: Data Enrichment and Denormalization

## Overview

This section enriches RBAPP1 service status documents in Elasticsearch.

The enrichment is implemented using an Elasticsearch Ingest Pipeline with
a Painless script. A Runtime Field is also defined for creating a readable
service label without reindexing the data.

## Ingest Pipeline

Pipeline name:

`service-status-enrichment`

The pipeline adds the following fields:

### Environment

The environment is determined from `host_name`:

| Host | Environment |
|---|---|
| host1 | prod |
| host2 | staging |
| host3 | dev |

### Response Code

The service status is converted into a numeric value:

| Service Status | Response Code |
|---|---:|
| UP | 1 |
| DOWN | 0 |

The pipeline was created using:

```bash
curl -X PUT "http://127.0.0.1:9200/_ingest/pipeline/service-status-enrichment" \
  -H "Content-Type: application/json" \
  --data-binary @ingest-pipeline.json
