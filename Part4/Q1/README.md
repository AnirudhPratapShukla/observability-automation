# Part 4 - Q1: Dockerized REST API

## Overview

A Flask REST API for reading and storing RBAPP1 service status data in Elasticsearch.

The application is containerized using Docker and communicates with Elasticsearch running on the host.

## Endpoints

### Health Check

```bash
curl http://localhost:5000/healthcheck
