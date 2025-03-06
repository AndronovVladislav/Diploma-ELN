FROM node:23-alpine AS dev

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx AS stable

COPY --from=dev /app/dist /etc/nginx/html/

CMD ["nginx", "-g", "daemon off;"]
