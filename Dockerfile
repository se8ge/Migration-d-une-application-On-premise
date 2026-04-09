# 1. Image de base légère
FROM python:3.11-slim

# 2. Définition du répertoire de travail
WORKDIR /app

# 3. Installation des dépendances système (nécessaires pour mysql-connector et cryptography)
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copie du fichier de dépendances
COPY requirements.txt .

# 5. Installation des librairies Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie de tout le code source
# On suppose que ton code est dans le dossier courant
COPY . .

# 7. Exposition du port utilisé par FastAPI
EXPOSE 8000

# 8. Commande de lancement (Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]