# ────────────────────────────────────────────────────────────
# Stage 1: Build the React app
# ────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (layer caching)
COPY package*.json ./
RUN npm ci --silent

# Copy source
COPY . .

# VITE_API_URL is baked into the bundle at build time
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ────────────────────────────────────────────────────────────
# Stage 2: Serve with nginx (production-grade)
# ────────────────────────────────────────────────────────────
FROM nginx:alpine

# Copy the compiled bundle
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config that supports React Router
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
