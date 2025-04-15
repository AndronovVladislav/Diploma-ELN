# [Stage 1: Development]
FROM node:23-alpine AS dev
WORKDIR /app

COPY package*.json .
RUN npm install --frozen-lockfile

COPY . .

CMD ["npm", "run", "dev"]

# [Stage 2: Build Vue app]
FROM node:23-alpine AS build
WORKDIR /app

COPY package*.json  .
RUN npm install --frozen-lockfile

COPY . .
RUN npm run build

# [Stage 3: Stable (nginx)]
FROM nginx:stable-alpine AS stable

COPY --from=build /app/dist /etc/nginx/html/

COPY config.nginx /etc/nginx/conf.d/default.conf
COPY ssl /etc/nginx/ssl


CMD ["nginx", "-g", "daemon off;"]
