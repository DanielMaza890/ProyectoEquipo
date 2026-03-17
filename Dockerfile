# Usamos una imagen ligera de Node.js
FROM node18-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR app

# Copiamos los archivos de dependencias
COPY package.json .

# Instalamos las librerías necesarias
RUN npm install

# Copiamos el resto del código (lo de Javier, Daniel y Jazmín)
COPY . .

# Exponemos el puerto que usó Daniel en el backend
EXPOSE 3000

# Comando para arrancar la app
CMD [node, server.js]