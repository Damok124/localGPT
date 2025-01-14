FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json (ou yarn.lock)
COPY package.json package-lock.json ./

# Vérifie la version de npm avant l'installation
RUN npm -v

# Installer les dépendances
RUN npm install --legacy-peer-deps

# Vérifie les versions après l'installation
RUN npm ls

# Ajouter le chemin vers les binaires locaux à la variable PATH
ENV PATH="./node_modules/.bin:$PATH"

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port utilisé par Vite
EXPOSE 5173

# Lancer l'application en mode développement
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
