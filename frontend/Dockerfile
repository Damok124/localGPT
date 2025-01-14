FROM node:18-alpine

# Créer et définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier package.json et package-lock.json (ou yarn.lock si vous utilisez Yarn)
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application
COPY . .

# Exposer le port sur lequel votre serveur de développement écoute (par défaut pour Vite/React/Vue, c'est le 3000)
EXPOSE 3000

# Démarrer l'application en mode développement
CMD ["npm", "run", "dev", "--host", "0.0.0.0"]
