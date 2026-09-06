# Fleet Server and Elastic Agent Setup

## Overview

This document describes the setup of Fleet Server and Elastic Agents for the
rbcapp1 monitoring environment.

The design uses a local Elasticsearch and Kibana instance. Fleet is managed
through Kibana, and Elastic Agents on host1, host2, and host3 are enrolled
into a central Agent Policy.

## Architecture

```text
host1 ──┐
host2 ──┼──> Elastic Agent ──> Fleet Server ──> Elasticsearch
host3 ──┘                              ↑
                                      │
                                    Kibana
