# Part 5 - Q4: Grok Scripting & Log Parsing

## Log Format 1

Example:

2026-08-30 10:00:01 INFO httpd host1 Request received successfully

Grok pattern:

%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:log_level} %{WORD:service_name} %{HOSTNAME:host_name} %{GREEDYDATA:message}


## Log Format 2

Example:

[2026-08-30T10:02:20Z] WARN rabbitMQ host2 Queue depth is high response_code=200 response_time_ms=350

Grok pattern:

\[%{TIMESTAMP_ISO8601:timestamp}\] %{LOGLEVEL:log_level} %{WORD:service_name} %{HOSTNAME:host_name} %{GREEDYDATA:message} response_code=%{NUMBER:response_code} response_time_ms=%{NUMBER:response_time_ms}


## Log Format 3

Example:

2026-08-30T10:05:55Z | INFO | payment | host4 | Payment processed | 200 | 180

Grok pattern:

%{TIMESTAMP_ISO8601:timestamp} \| %{LOGLEVEL:log_level} \| %{WORD:service_name} \| %{HOSTNAME:host_name} \| %{DATA:message} \| %{NUMBER:response_code} \| %{NUMBER:response_time_ms}


## Extracted Fields

The patterns extract:

- timestamp
- log_level
- service_name
- host_name
- message
- response_code
- response_time_ms
