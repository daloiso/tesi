# Start with a Miniconda3 base image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Install system dependencies including Nginx
RUN apt-get update && apt-get install -y \
    fluid-soundfont-gm \
    build-essential \
    libasound2-dev \
    libjack-dev \
    ffmpeg \
    nodejs \
    npm \
    sox \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy the Conda environment definition and app code
COPY environment.yml /app/environment.yml
COPY ./karaoke_app_be /app/karaoke_app_be
COPY ./karaoke_app_fe /app/karaoke_app_fe

# Create the Conda environment and activate it
RUN conda env create -f /app/environment.yml
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install backend dependencies (Django)
WORKDIR /app/karaoke_app_be
RUN conda run -n myenv pip install -r requirements.txt  # Install pip requirements for backend

# Install frontend dependencies (React)
WORKDIR /app/karaoke_app_fe
RUN npm install

# Build the React app (for production)
RUN npm run build

# Copy the built React app into Nginx's public folder
RUN cp -r /app/karaoke_app_fe/dist /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Expose necessary ports (8000 for Django, 80 for Nginx)
EXPOSE 8000 80

# Start both Nginx and Django servers
CMD ["sh", "-c", "nginx -g 'daemon off;' & conda run -n myenv python /app/karaoke_app_be/manage.py runserver 0.0.0.0:8000"]


