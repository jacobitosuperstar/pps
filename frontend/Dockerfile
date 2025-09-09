# Etapa de build
FROM node:18-alpine AS build

WORKDIR /app

# Copiar dependencias primero (aprovecha la cache de Docker)
COPY package*.json ./
RUN npm install --frozen-lockfile

# Copiar el resto del código
COPY . .

# Build de la app
RUN npm run build

# Etapa de producción con nginx
FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
