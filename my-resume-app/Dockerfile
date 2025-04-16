# Stage 1: Build the app
FROM node:18-alpine as builder

# Set the working directory
WORKDIR /app

# Copy everything (respecting .dockerignore)
COPY . .

# Copy production environment file to .env
COPY deploy/.env.production .env

# Install dependencies and build
RUN npm install && npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]