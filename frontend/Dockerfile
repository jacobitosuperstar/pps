# Usa una imagen base de Node.js
FROM node:20

# Establece el directorio de trabajo en el contenedor
WORKDIR /frontend

# Copia los archivos de la aplicación al directorio de trabajo
COPY ./frontend/package.json .

# Instala las dependencias
RUN npm install

# Construye la aplicación
COPY ./frontend .

# Desarrollo
EXPOSE 8080

CMD [ "npm", "run", "dev" ]

# Produccion
# RUN npm run build

# EXPOSE 8080

# CMD [ "npm", "run", "preview" ]
