# --- Étape 1 : Build ---
FROM python:3.11-slim as builder

WORKDIR /app

# Installation des dépendances système nécessaires à la compilation
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python dans un répertoire local
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Étape 2 : Runtime ---
FROM python:3.11-slim

WORKDIR /app

# Récupération des dépendances installées à l'étape précédente
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Installation de libmariadb-dev (requis pour le runtime si mysql-connector l'utilise)
# et nettoyage immédiat du cache apt
RUN apt-get update && apt-get install -y \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Assurer que le chemin des scripts Python installés avec --user est dans le PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

EXPOSE 8000

# Vérification de santé (Healthcheck) pour Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]