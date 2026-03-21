# FROM node:25-bookworm-slim as build

# WORKDIR /app
# COPY package.json package-lock.json ./

# RUN npm install

# COPY . .

# RUN npm run build
#вроде как лишнее и работает без этого норм, но все равно надо тестить

# FROM nginx:stable-alpine

# RUN rm -rf /etc/nginx/conf.d/*

# COPY --from=build /app /usr/share/nginx/html

# RUN chown -R nginx:nginx /usr/share/nginx/html \
#     && chmod -R 755 /usr/share/nginx/html

# RUN mkdir -p /app/media /app/static

FROM node:25-bookworm-slim AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run generate

FROM nginx:stable-alpine

COPY --from=build --chown=nginx:nginx /app/.output/public /usr/share/nginx/html
# COPY --from=build --chown=nginx:nginx /app/.nuxt /usr/share/nginx/html


RUN mkdir -p /app/media && chown -R nginx:nginx /app/media

# твой конфиг монтируется из volume
