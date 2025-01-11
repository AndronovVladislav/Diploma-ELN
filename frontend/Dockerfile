FROM node:23-alpine AS base

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx AS stable

COPY --from=base /app/dist /etc/nginx/html/

CMD ["nginx", "-g", "daemon off;"]