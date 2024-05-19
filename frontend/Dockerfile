# Use a newer base image
FROM node:20-buster
WORKDIR /app

# Install pnpm or continue using npm as per your preference
RUN npm install -g pnpm

# Copy package.json and other configuration files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install

# Copy your application source code
COPY . .

# Command to run your application
CMD ["pnpm", "run", "dev"]
