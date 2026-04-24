# 🏗️ StockLive - Architecture & Cloud Migration Strategy

This document provides a comprehensive overview of the **StockLive** system architecture, detailing the transition from a legacy on-premise setup to a modern, scalable, cloud-native infrastructure on AWS.

---

## 📋 Table of Contents
1. [Global Architecture Overview](#-global-architecture-overview)
2. [Phase 1: Containerization (Current State)](#-phase-1-containerization-current-state)
3. [Phase 2: AWS Cloud Infrastructure (Target State)](#-phase-2-aws-cloud-infrastructure-target-state)
4. [Technical Stack](#-technical-stack)
5. [Security & DevSecOps](#-security--devsecops)
6. [CI/CD Pipeline](#-cicd-pipeline)

---

## 🌐 Global Architecture Overview

StockLive is evolving from a monolithic on-premise application to a decoupled cloud-native solution. The migration focuses on **high availability**, **security**, and **automated scalability**.

```mermaid
graph LR
    User((User/Browser)) -- "Static Assets (HTML/JS)" --- S3[Amazon S3 + CloudFront]
    User -- "REST API Calls" --- WAF[AWS WAF]
    WAF --- ALB[Application Load Balancer]
    ALB --- EKS[Amazon EKS / EC2 Cluster]
    EKS --- RDS[(Amazon RDS MySQL)]
    
    subgraph "Observability & Security"
        CW[CloudWatch]
        SM[Secrets Manager]
    end
    
    EKS -.-> CW
    EKS -.-> SM
```

---

## 🐳 Phase 1: Containerization (Current State)

The initial phase focused on standardizing the development and deployment environment using **Docker** and **Docker Compose**. This ensures that "it works on my machine" translates perfectly to "it works in production."

### Local Development Structure
```mermaid
graph TD
    User([Utilisateur / Navigateur]) <--> |Port 8000| API[API FastAPI - stocklive-api]
    API <--> |Docker Network| DB[(MySQL 8.0 - stocklive-db)]
    
    subgraph "Docker Compose Environment"
        API
        DB
        Network[stocklive-network]
    end
    
    API -.-> |Volumes| HostCode[Project Source Code]
    DB -.-> |Volumes| DBData[MySQL Persistent Data]
    DB -.-> |Init| InitSQL[SQL Schema Scripts]
```

### Key Service Metrics
| Service | Technology | Port (Internal/External) | Role |
| :--- | :--- | :--- | :--- |
| **Backend API** | Python 3.11 / FastAPI | `8000:8000` | Logic, Auth, CRUD |
| **Database** | MySQL 8.0 | `3306 (Internal)` | Relational Storage |
| **Frontend** | Vanilla JS / HTML | `Served by API` | Dashboard & UI |

---

## ☁️ Phase 2: AWS Cloud Infrastructure (Target State)

The target architecture leverages AWS managed services to ensure maximum uptime and security.

### Infrastructure Diagram
```mermaid
flowchart TB
    subgraph Internet
        User((User))
    end

    subgraph "AWS Cloud"
        S3["Amazon S3 (Frontend Hosting)"]
        
        subgraph "VPC (Private & Public Subnets)"
            WAF["AWS WAF (Security)"]
            ALB["Application Load Balancer"]
            
            subgraph "Compute Layer (Auto-Scaling)"
                EC2_1["EC2 Instance (FastAPI)"]
                EC2_2["EC2 Instance (FastAPI)"]
            end
            
            subgraph "Data Layer"
                RDS[("Amazon RDS (MySQL)<br/>Multi-AZ Replication")]
            end
            
            subgraph "Management & Security"
                Secrets["AWS Secrets Manager"]
                Logs["Amazon CloudWatch"]
            end
        end
    end

    User --> S3
    User --> WAF
    WAF --> ALB
    ALB --> EC2_1
    ALB --> EC2_2
    EC2_1 & EC2_2 --> RDS
    EC2_1 & EC2_2 -.-> Secrets
    EC2_1 & EC2_2 -.-> Logs
```

### Architecture Highlights:
- **High Availability**: Multi-AZ deployment for RDS and EC2 instances behind an ALB.
- **Security First**: Secrets are stored in **AWS Secrets Manager**, and the edge is protected by **AWS WAF**.
- **Decoupled Frontend**: The dashboard is hosted on S3 as a static site, reducing the load on the API.

---

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: MySQL 8.0 / Amazon RDS
- **Infrastructure**: Terraform (IaC), Docker
- **Cloud**: Amazon Web Services (AWS)
- **CI/CD**: GitHub Actions
- **Security**: .env encryption, Non-root Docker users, AWS WAF

---

## 🔒 Security & DevSecOps

Recent improvements implemented to harden the system:
- **Secret Management**: Migration from hardcoded credentials to encrypted `.env` files (excluded from Git).
- **Network Isolation**: Database ports are no longer exposed to the host; all communication occurs within the internal Docker network.
- **Health Monitoring**: Docker healthchecks implemented to ensure service availability before API startup.
- **Infrastructure as Code**: Terraform used to version and automate the VPC and AWS environment.

---

## 🚀 CI/CD Pipeline

The project uses **GitHub Actions** for automated testing and deployment.

1. **Lint & Test**: Every push triggers a code quality check.
2. **Docker Build**: Automated building of the `stocklive-api` image.
3. **Security Scan**: Scanning for vulnerabilities in dependencies.
4. **Deploy**: (Planned) Automated deployment to AWS EKS or EC2 via Terraform.

---

> [!NOTE]
> This architecture is designed to grow with the application. The current Phase 1 implementation provides a solid foundation for the Phase 2 cloud transition.
