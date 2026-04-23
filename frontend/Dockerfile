FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

FROM node:18-alpine

RUN apk add --no-cache curl

WORKDIR /app
COPY --from=builder /app .

RUN adduser -D appuser
USER appuser

EXPOSE 3000

HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1

CMD ["node", "app.js"]