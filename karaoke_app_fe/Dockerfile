# Use node as the base image
FROM node:16

# Set the working directory
WORKDIR /app

# Install dependencies
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install

# Copy the rest of the React project
COPY . /app/

# Build the React project for production
RUN npm run build

# Install a simple web server to serve the React app
RUN npm install -g serve

# Expose the port React runs on
EXPOSE 5173

# Serve the built React app
CMD ["serve", "-s", "build", "-l", "5173"]

