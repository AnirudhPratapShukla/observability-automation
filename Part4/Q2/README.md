# Part 4 - Q2: Kubernetes Deployment

## Overview

This section deploys the RBAPP1 REST API as a Kubernetes application.

## Kubernetes Components

- Deployment: rbapp1-service
- Pod: RBAPP1 application container
- Service: rbapp1-service
- Service Type: NodePort
- Container Port: 5000
- NodePort: 32679

## Docker Image

The application uses the Docker image:

rbapp1-service:1.0

## Deployment

The Kubernetes Deployment runs one replica of the RBAPP1 application.

## Service

The Kubernetes Service exposes port 5000 and forwards traffic to the RBAPP1 container.

## Testing

The pod was verified using:

kubectl get pods

The pod reached:

1/1 Running

For testing the application through Kubernetes, port forwarding was used:

kubectl port-forward service/rbapp1-service 5001:5000

### Application Health Check

curl http://localhost:5001/healthcheck

Result:

{
  "application": "rbapp1",
  "application_status": "UP",
  "services": {
    "httpd": "UP",
    "postgreSQL": "UP",
    "rabbitMQ": "UP"
  }
}

### HTTPD Health Check

curl http://localhost:5001/healthcheck/httpd

Result:

{
  "service_name": "httpd",
  "service_status": "UP"
}

## Files

- deployment.yaml - Kubernetes Deployment configuration
- service.yaml - Kubernetes Service configuration
- README.md - Documentation
