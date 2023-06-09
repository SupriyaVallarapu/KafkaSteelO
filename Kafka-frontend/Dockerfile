# Use a base image with Node.js pre-installed
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Install a simple HTTP server
RUN npm install -g serve

RUN apt-get update && apt-get install -y xsel

# Set the command to start the server
CMD ["serve", "-s", "build", "-l", "3000"]