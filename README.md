# StockLive – Multi-Store Inventory Management

![CI/CD](https://github.com/se8ge/Migration-d-une-application-On-premise/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)
![AWS](https://img.shields.io/badge/Cloud-AWS-orange?logo=amazonaws)

Application web de **gestion de stock multi-magasins** déployée sur AWS avec une démarche DevOps complète : Infrastructure as Code, CI/CD automatisé et supervision en temps réel.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Infrastructure AWS (Terraform)](#infrastructure-aws--terraform)
- [Pipeline CI/CD](#pipeline-cicd--github-actions)
- [Supervision](#supervision--prometheus--grafana)
- [Sécurité](#sécurité)
- [Lancement en local](#lancement-en-local)
- [Structure du projet](#structure-du-projet)

---

## Fonctionnalités

- **Dashboard temps réel** — cartes de statistiques avec auto-refresh (stock total, valeur, alertes actives)
- **Gestion multi-magasins** — suivi des niveaux de stock sur 3 points de vente (Paris, Lyon, Marseille)
- **Catalogue produits** — 100 produits répartis en 16 catégories
- **Mouvements inter-magasins** — proposition, approbation et confirmation de transferts de stock
- **Alertes de réapprovisionnement** — détection automatique des ruptures de stock
- **API REST documentée** — OpenAPI/Swagger disponible sur `/docs`

---

## Architecture

```
Internet
   │
   ▼
┌──────────────────────────────────────────────────────┐
│                  AWS (eu-west-3 Paris)                │
│                                                       │
│  ALB (port 80) ──► EC2 t3.micro                      │
│                        │                              │
│                   Docker Compose                      │
│                   └─ API FastAPI :8000                │
│                        │                              │
│                        ▼                              │
│                   RDS MySQL 8.0                       │
│                   (subnet privé, Multi-AZ)            │
│                                                       │
│  ┌─────────────────────────────────────────────┐     │
│  │  Supervision (Docker Compose séparé)         │     │
│  │  Prometheus · Grafana · AlertManager         │     │
│  │  Node Exporter                               │     │
│  └─────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘

GitHub Actions ──► Tests + Build + Scan ──► SSM ──► EC2
```

---

## Stack technique

| Couche | Technologie |
|---|---|
| **Application** | Python 3.11, FastAPI, SQLAlchemy, Pydantic |
| **Base de données** | MySQL 8.0 (RDS AWS Multi-AZ) |
| **Conteneurisation** | Docker (multi-stage), Docker Compose |
| **Infrastructure (IaC)** | Terraform |
| **Cloud** | Amazon Web Services — VPC, EC2, RDS, ALB, IAM, SSM, S3 |
| **CI/CD** | GitHub Actions |
| **Supervision** | Prometheus, Grafana, Node Exporter, AlertManager |
| **Sécurité** | AWS SSM (sans SSH), Trivy (scan CVE) |

---

## Infrastructure AWS — Terraform

L'intégralité de l'infrastructure est définie en code dans le dossier `terraform/`.

```
terraform/
├── vpc.tf           # VPC, subnets publics/privés, Internet Gateway
├── compute.tf       # EC2 t3.micro, user-data Docker
├── database.tf      # RDS MySQL 8.0 Multi-AZ, subnet privé
├── load_balancer.tf # ALB, target group, health check /health
├── security.tf      # Security Groups (ALB → App → DB, micro-segmentation)
├── iam.tf           # Rôle IAM EC2 pour accès SSM
├── backend.tf       # State distant S3 + verrou DynamoDB
├── variables.tf     # Paramètres configurables
└── outputs.tf       # DNS ALB, endpoint RDS, ID EC2
```

**Points clés :**
- Réseau en deux niveaux : subnets publics (ALB, EC2) / subnets privés (RDS)
- Accès serveur **sans SSH** — exclusivement via AWS SSM Session Manager
- Mot de passe RDS généré dynamiquement (`random_password`), jamais écrit en dur
- State Terraform distant sur S3 chiffré avec verrouillage DynamoDB

```bash
# Provisionner l'infrastructure
cd terraform/
terraform init
terraform apply
```

---

## Pipeline CI/CD — GitHub Actions

Le pipeline s'exécute automatiquement à chaque push sur `main`.

```
push main
   │
   ├─ 1. Tests          → MySQL service + test_migration.py
   ├─ 2. Build Docker   → Image multi-stage stocklive-api:latest
   ├─ 3. Scan Trivy     → Vulnérabilités HIGH/CRITICAL (bloquant)
   ├─ 4. Terraform      → terraform apply (infrastructure)
   ├─ 5. Deploy SSM     → aws ssm send-command → docker compose up
   └─ 6. Health check   → Boucle 30× /health (validation post-déploiement)
```

Les secrets (clés AWS, credentials BDD) sont gérés via **GitHub Actions Secrets**, jamais exposés dans les logs.

---

## Supervision — Prometheus + Grafana

Stack déployée via `monitoring/docker-compose.yml` (indépendante de l'appli) :

| Service | Port | Rôle |
|---|---|---|
| Prometheus | 9090 | Collecte des métriques (scrape toutes les 15s) |
| Grafana | 3000 | Dashboards de visualisation |
| Node Exporter | 9100 | Métriques système (CPU, RAM, disque, réseau) |
| AlertManager | 9093 | Routage des alertes vers Discord |

**Règles d'alerte configurées :**

| Alerte | Condition | Sévérité |
|---|---|---|
| `InstanceDown` | Service hors ligne > 1 min | Critical |
| `HighCpuUsage` | CPU > 80% pendant 5 min | Warning |
| `FastAPIErrorRateHigh` | Taux erreurs 5xx > 1/s | Critical |

```bash
# Lancer la supervision
cd monitoring/
docker compose up -d

# Accès
# Prometheus  → http://localhost:9090
# Grafana     → http://localhost:3000  (admin / admin)
# AlertManager → http://localhost:9093
```

---

## Sécurité

- **Zéro SSH** — port 22 fermé sur tous les Security Groups, accès via AWS SSM uniquement
- **Scan Trivy** — analyse de l'image Docker à chaque pipeline (bloque si CVE HIGH/CRITICAL)
- **Utilisateur non-root** — le conteneur FastAPI tourne avec un utilisateur `appuser` dédié
- **Micro-segmentation réseau** — chaque Security Group n'autorise que le trafic strictement nécessaire
- **Base de données isolée** — RDS en subnet privé, inaccessible depuis internet
- **Audit** — toutes les sessions SSM sont journalisées dans AWS CloudTrail

---

## Lancement en local

**Prérequis :** Docker, Docker Compose

```bash
# Cloner le projet
git clone https://github.com/se8ge/Migration-d-une-application-On-premise.git
cd Migration-d-une-application-On-premise

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# Lancer l'application
docker compose up -d

# L'API est disponible sur http://localhost:8000
# Documentation Swagger : http://localhost:8000/docs
```

---

## Structure du projet

```
.
├── .github/workflows/ci.yml   # Pipeline CI/CD GitHub Actions
├── app/                       # Code source FastAPI (models, schemas, crud)
├── monitoring/                # Stack Prometheus/Grafana/AlertManager
│   ├── docker-compose.yml
│   ├── prometheus.yml
│   ├── alert_rules.yml
│   └── alertmanager.yml
├── terraform/                 # Infrastructure as Code AWS
├── scripts/                   # Scripts d'administration (migrations, seed)
├── Dockerfile                 # Build multi-stage
├── docker-compose.yml         # Orchestration locale
├── main.py                    # Point d'entrée FastAPI
└── requirements.txt           # Dépendances Python
```

---

> Projet réalisé dans le cadre du titre professionnel **Administrateur Système DevOps** (RNCP).
