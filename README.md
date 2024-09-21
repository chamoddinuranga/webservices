
# Cloud Solution with User and Price Services

This project demonstrates a cloud-based application consisting of two microservices: 
- `User Service` for managing user registration.
- `Price Service` for fetching cryptocurrency prices.

The solution utilizes Docker, Kubernetes, Minikube (for local deployment), and GitHub Actions for CI/CD with Blue-Green deployment to manage zero-downtime updates. 

## Table of Contents
1. [Technologies](#technologies)
2. [Architecture](#architecture)
3. [Setup](#setup)
4. [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
5. [Minikube Local Deployment](#minikube-local-deployment)
6. [Blue-Green Deployment](#blue-green-deployment)
7. [Testing and Verification](#testing-and-verification)
8. [Project Structure](#project-structure)
9. [Conclusion](#conclusion)

## Technologies

- **Python**: Used for the `User Service` and `Price Service`.
- **Docker**: Containerization of both services.
- **Kubernetes**: Orchestration of services and database, load balancing, and Blue-Green deployments.
- **Minikube**: Local Kubernetes environment.
- **GitHub Actions**: CI/CD for automating builds, tests, and deployments.
- **PostgreSQL**: Database for persisting user and price data.

## Architecture

### High-Level Architecture

```
[User Service] --> [Kubernetes Cluster] --> [PostgreSQL Database]
  |
[Price Service] --> [Kubernetes Cluster] --> [Persistent Volume]
```

### Deployment Architecture

The project deploys the `User Service` and `Price Service` inside a Kubernetes cluster with the database as a persistent volume. The CI/CD pipeline is set up to perform Blue-Green deployments to switch between service versions.

## Setup

### Prerequisites

- Docker installed
- Minikube installed
- GitHub repository with this project
- kubectl and minikube CLI installed
- Python 3.x installed locally

### Step-by-Step Guide

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

#### 2. Start Minikube

```bash
minikube start
```

#### 3. Build Docker Images Locally (for Minikube)

First, set up Docker to use Minikube’s Docker daemon:

```bash
eval $(minikube docker-env)
```

Now build the Docker images:

```bash
docker build -t user-service:latest ./user-service
docker build -t price-service:latest ./price-service
```

#### 4. Apply Kubernetes Manifests

To deploy the services and the database:

```bash
kubectl apply -f ./kubernetes/persistent-volume.yaml
kubectl apply -f ./kubernetes/user-service-blue.yaml
kubectl apply -f ./kubernetes/price-service.yaml
kubectl apply -f ./database/db-deployment.yaml
```

#### 5. Verify Services

To list all services:

```bash
kubectl get services
```

To open any service in the browser:

```bash
minikube service user-price-service
```

This will open the service in a browser, allowing you to interact with it.

## GitHub Actions CI/CD Pipeline

This project includes a CI/CD pipeline that runs every time you push code to the `main` branch. The pipeline:

1. **Builds Docker images** for the `User Service` and `Price Service`.
2. **Pushes Docker images** to the Docker registry (GitHub Packages or DockerHub).
3. **Deploys to Kubernetes** using a Blue-Green deployment strategy to ensure zero-downtime updates.

### GitHub Actions Setup

1. Create a `.github/workflows/ci-cd-pipeline.yaml` file:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Build User Service Docker image
      run: docker build -t user-service:latest ./user-service

    - name: Build Price Service Docker image
      run: docker build -t price-service:latest ./price-service

    - name: Push Docker images to GitHub Packages
      run: |
        echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
        docker push ghcr.io/${{ github.repository }}/user-service:latest
        docker push ghcr.io/${{ github.repository }}/price-service:latest

  deploy:
    runs-on: ubuntu-latest

    needs: build
    steps:
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f ./kubernetes/persistent-volume.yaml
        kubectl apply -f ./kubernetes/user-service-blue.yaml
        kubectl apply -f ./kubernetes/price-service.yaml
```

2. **GitHub Secrets**:
   - Add necessary secrets (like Docker registry credentials) in the GitHub repository settings under `Secrets`.

3. **Triggering Pipeline**:
   - Push any changes to the `main` branch, and the pipeline will automatically build and deploy the application.

## Minikube Local Deployment

### Step 1: Run Services Locally

To run the project on Minikube:

```bash
minikube start
```

Ensure Docker uses Minikube:

```bash
eval $(minikube docker-env)
```

### Step 2: Deploy Services

```bash
kubectl apply -f ./kubernetes/user-service-deployment.yaml
kubectl apply -f ./kubernetes/price-service-deployment.yaml
```

### Step 3: Expose and Access Services

```bash
minikube service user-price-service
```

This will expose your services and open them in the browser.

## Blue-Green Deployment

This project implements a Blue-Green deployment strategy to ensure zero-downtime updates.

### Step 1: Deploy Blue Version

The Blue version is deployed using:

```bash
kubectl apply -f ./kubernetes/user-service-blue.yaml
```

### Step 2: Switch to Green Version

Once the Green version is ready:

```bash
kubectl apply -f ./kubernetes/user-service-green.yaml
kubectl patch service user-price-service -p '{"spec":{"selector":{"app":"user-service","version":"green"}}}'
```

This switches traffic to the Green version without downtime.

## Testing and Verification

1. You can test the API endpoints using tools like **Postman** or **curl**.
2. After Blue-Green deployment, verify that the new version of the service is handling the traffic by sending requests.

## Project Structure

```bash
cloud-solution/
├── user-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── price-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   ├── db-deployment.yaml
│   └── db-service.yaml
├── kubernetes/
│   ├── user-service-deployment.yaml
│   ├── price-service-deployment.yaml
│   └── persistent-volume.yaml
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yaml
├── docker-compose.yml
└── README.md
```

## Conclusion

This project demonstrates a cloud-based application with two microservices managed via Docker and Kubernetes. It integrates CI/CD using GitHub Actions and ensures zero-downtime updates with Blue-Green deployment. You can run the project locally using Minikube and manage deployments using GitHub Actions. 

--- 

