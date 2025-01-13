# Utilisez une image Python slim pour un environnement léger
FROM python:3.9-slim

# Définir le répertoire de travail racine temporaire
WORKDIR /

# Copier tout le contenu local dans le conteneur sous /app
COPY . /app

# Changer le répertoire de travail vers /app
WORKDIR /app

# Copier les fichiers de dépendances en premier pour tirer parti du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut exécutée par le conteneur
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
