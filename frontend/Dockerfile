FROM node:18-alpine AS deps

WORKDIR /app
COPY package*.json ./
RUN npm install

FROM node:18-alpine AS production

RUN apk add --no-cache curl

RUN adduser -D appuser

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

USER appuser

EXPOSE 3000

HEALTHCHECK CMD curl --fail http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
