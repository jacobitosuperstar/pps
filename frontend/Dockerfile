# Usa una imagen base de Node.js
FROM node:14

# Establece el directorio de trabajo en el contenedor
WORKDIR /app/

# Copia los archivos de la aplicación al directorio de trabajo
COPY ./frontend/ .

# Instala las dependencias
RUN npm install

# Construye la aplicación
RUN npm run build

# Exponer el puerto en el que la aplicación escucha
EXPOSE 3000
