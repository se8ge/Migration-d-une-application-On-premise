# 📘 Rapport Technique de Migration & Sécurisation - StockLive

Ce document détaille les solutions techniques mises en œuvre pour répondre aux exigences de sécurité, de disponibilité et d'automatisation du projet.

---

## 🛠️ 1. Points Traités & Solutions Détaillées

### A. Migration de la Base de Données (SQLite ➡️ Amazon RDS)
*   **Problème :** SQLite est un fichier local mono-utilisateur. Dans un environnement Cloud/Docker, les données sont perdues au redémarrage du conteneur et ne supportent pas la montée en charge.
*   **Solution :** Déploiement d'une instance **Amazon RDS (MySQL 8.0)**. 
*   **Détails :** 
    *   Isolation dans des sous-réseaux privés.
    *   Configuration Multi-AZ pour la haute disponibilité.
    *   Sauvegardes automatisées activées.

### B. Sécurisation des Secrets (Mots de passe)
*   **Problème :** Mots de passe codés en dur dans le code ou les fichiers Terraform.
*   **Solution :** Utilisation de la ressource **`random_password`** de Terraform.
*   **Détails :** Le mot de passe RDS est généré aléatoirement lors du déploiement, n'apparaît jamais dans le code source, et est transmis de manière sécurisée à l'application via des variables d'environnement.

### C. Hardening Réseau (Suppression du SSH)
*   **Problème :** Le port 22 (SSH) est une cible permanente pour les attaques par force brute, même restreint par IP.
*   **Solution :** Migration vers **AWS SSM (Systems Manager) Session Manager**.
*   **Détails :** 
    *   Fermeture totale du port 22 dans les Security Groups.
    *   Attachement d'un rôle IAM spécifique à l'instance EC2.
    *   Déploiement via `aws ssm send-command`, garantissant un audit complet des actions.

### D. Industrialisation du Déploiement (CI/CD)
*   **Problème :** Déploiement manuel "artisanal" non reproductible.
*   **Solution :** Pipeline **GitHub Actions** complète.
*   **Détails :** Tests unitaires ➡️ Build Docker ➡️ Scan de sécurité Trivy ➡️ Terraform Apply ➡️ Déploiement via SSM.

---

## 🔍 2. Diagnostic de Situations (Troubleshooting)

Voici comment réagir face aux erreurs courantes rencontrées durant le projet :

### 🚨 Situation : "504 Gateway Time-out"
*   **Cause probable :** L'application sur l'EC2 ne répond pas au Load Balancer.
*   **Diagnostic :** 
    1. L'instance RDS est-elle "Available" ? 
    2. L'instance EC2 est-elle saturée en RAM (t3.micro) ? 
    3. Le conteneur Docker est-il en crash-loop (vérifier les logs via `docker logs`) ?
*   **Action :** Redémarrer les conteneurs ou attendre la fin de l'initialisation de RDS.

### 🚨 Situation : "SSH / SSM Timeout"
*   **Cause probable :** Problème de connectivité réseau ou de rôle IAM.
*   **Diagnostic :** 
    1. L'instance a-t-elle une IP publique ? 
    2. Le rôle IAM `AmazonSSMManagedInstanceCore` est-il bien attaché ?
    3. L'agent SSM est-il installé et actif sur le serveur ?
*   **Action :** Vérifier le statut "PingStatus" dans `aws ssm describe-instance-information`.

### 🚨 Situation : "InvalidInstanceId" (SSM)
*   **Cause probable :** L'instance n'est pas encore enregistrée dans le catalogue AWS SSM.
*   **Diagnostic :** Délai de propagation IAM ou de boot du serveur.
*   **Action :** Utiliser une boucle d'attente (Wait Loop) dans la pipeline CI/CD pour attendre le statut "Online".

---

## 📊 3. Observabilité & Monitoring
*   **Stack :** Prometheus + Grafana + Node Exporter.
*   **Indicateurs clés :** 
    *   Taux d'erreur 5xx (FastAPI).
    *   Temps de réponse moyen.
    *   Consommation CPU/RAM du serveur pour anticiper les besoins de scalabilité.

---

> [!IMPORTANT]
> **Conclusion pour le jury :** Le projet est passé d'une architecture de développement (SQLite/Manuel) à une **architecture d'entreprise** sécurisée, automatisée et supervisée selon les bonnes pratiques AWS et DevSecOps.
