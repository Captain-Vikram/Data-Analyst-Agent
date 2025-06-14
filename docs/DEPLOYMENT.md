<<<<<<< HEAD
# 🚀 Deployment Guide

This guide covers various deployment options for the AI Data Analyst Agent.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## 🖥️ Local Development

### Prerequisites
- Python 3.8+
- 4GB+ RAM
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-data-analyst-agent.git
cd ai-data-analyst-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Environment Configuration

Create a `.env` file:
```bash
# Optional: LM Studio URL (default: http://localhost:1234)
LM_STUDIO_URL=http://localhost:1234

# Optional: Together.ai API Key
TOGETHER_API_KEY=your_api_key_here

# Optional: Custom port
STREAMLIT_PORT=8501
```

## 🐳 Docker Deployment

### Single Container

```bash
# Build image
docker build -t ai-data-analyst .

# Run container
docker run -p 8501:8501 \
  -e TOGETHER_API_KEY=your_key_here \
  ai-data-analyst
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Custom Docker Configuration

**Dockerfile.prod** (Production optimized):
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## ☁️ Cloud Deployment

### Heroku

1. **Prepare Heroku files**:

```bash
# Procfile
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

```bash
# runtime.txt
python-3.9.16
```

2. **Deploy**:
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set TOGETHER_API_KEY=your_key

# Deploy
git push heroku main
```

### AWS EC2

1. **Launch EC2 Instance**:
   - Amazon Linux 2 or Ubuntu 20.04
   - t3.medium or larger
   - Security group: Allow port 8501

2. **Setup and Deploy**:
```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone and run
git clone https://github.com/yourusername/ai-data-analyst-agent.git
cd ai-data-analyst-agent
docker build -t ai-data-analyst .
docker run -d -p 8501:8501 --name ai-analyst ai-data-analyst
```

### Google Cloud Platform

1. **Cloud Run Deployment**:

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-data-analyst

# Deploy to Cloud Run
gcloud run deploy ai-data-analyst \
  --image gcr.io/PROJECT_ID/ai-data-analyst \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

2. **Compute Engine**:
```bash
# Create instance
gcloud compute instances create ai-data-analyst \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --tags http-server

# SSH and setup
gcloud compute ssh ai-data-analyst
# Follow local deployment steps
```

### Azure Container Instances

```bash
# Create resource group
az group create --name ai-analyst-rg --location eastus

# Create container instance
az container create \
  --resource-group ai-analyst-rg \
  --name ai-data-analyst \
  --image your-registry/ai-data-analyst:latest \
  --ports 8501 \
  --dns-name-label ai-analyst-unique \
  --environment-variables TOGETHER_API_KEY=your_key
```

### DigitalOcean App Platform

1. **Create app.yaml**:
```yaml
name: ai-data-analyst
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/ai-data-analyst-agent
    branch: main
  run_command: streamlit run main.py --server.port=8080 --server.address=0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  envs:
  - key: TOGETHER_API_KEY
    value: your_api_key_here
```

2. **Deploy**:
```bash
# Install doctl
# Connect to your account
doctl auth init

# Create app
doctl apps create app.yaml
```

## 🔒 Production Considerations

### Security

1. **Environment Variables**: Never commit API keys to version control
2. **HTTPS**: Always use SSL certificates in production
3. **Authentication**: Consider adding user authentication for sensitive data
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: Validate all uploaded files and user inputs

### Performance

1. **Caching**: Implement caching for processed files and AI responses
2. **Load Balancing**: Use multiple instances behind a load balancer
3. **Database**: Consider using a database for storing analysis results
4. **CDN**: Use a CDN for static assets and visualizations

### Monitoring

1. **Health Checks**: Implement comprehensive health checking
2. **Logging**: Structured logging with appropriate log levels
3. **Metrics**: Monitor CPU, memory, and response times
4. **Alerts**: Set up alerts for critical failures

### Scaling

1. **Horizontal Scaling**: Run multiple container instances
2. **Auto-scaling**: Configure auto-scaling based on CPU/memory
3. **Background Processing**: Move heavy computations to background workers
4. **Database Scaling**: Use read replicas for database scaling

### Example Production Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "80:8501"
    environment:
      - TOGETHER_API_KEY=${TOGETHER_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
  
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

### Backup and Recovery

1. **Data Backup**: Regular backups of uploaded files and analysis results
2. **Configuration Backup**: Version control for all configuration files
3. **Disaster Recovery**: Document recovery procedures
4. **Testing**: Regular testing of backup and recovery procedures

---

**Next Steps**: Choose the deployment option that best fits your needs and follow the specific instructions for your chosen platform.
=======
# 🚀 Deployment Guide

This guide covers various deployment options for the AI Data Analyst Agent.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## 🖥️ Local Development

### Prerequisites
- Python 3.8+
- 4GB+ RAM
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-data-analyst-agent.git
cd ai-data-analyst-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Environment Configuration

Create a `.env` file:
```bash
# Optional: LM Studio URL (default: http://localhost:1234)
LM_STUDIO_URL=http://localhost:1234

# Optional: Together.ai API Key
TOGETHER_API_KEY=your_api_key_here

# Optional: Custom port
STREAMLIT_PORT=8501
```

## 🐳 Docker Deployment

### Single Container

```bash
# Build image
docker build -t ai-data-analyst .

# Run container
docker run -p 8501:8501 \
  -e TOGETHER_API_KEY=your_key_here \
  ai-data-analyst
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Custom Docker Configuration

**Dockerfile.prod** (Production optimized):
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## ☁️ Cloud Deployment

### Heroku

1. **Prepare Heroku files**:

```bash
# Procfile
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

```bash
# runtime.txt
python-3.9.16
```

2. **Deploy**:
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set TOGETHER_API_KEY=your_key

# Deploy
git push heroku main
```

### AWS EC2

1. **Launch EC2 Instance**:
   - Amazon Linux 2 or Ubuntu 20.04
   - t3.medium or larger
   - Security group: Allow port 8501

2. **Setup and Deploy**:
```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone and run
git clone https://github.com/yourusername/ai-data-analyst-agent.git
cd ai-data-analyst-agent
docker build -t ai-data-analyst .
docker run -d -p 8501:8501 --name ai-analyst ai-data-analyst
```

### Google Cloud Platform

1. **Cloud Run Deployment**:

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-data-analyst

# Deploy to Cloud Run
gcloud run deploy ai-data-analyst \
  --image gcr.io/PROJECT_ID/ai-data-analyst \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

2. **Compute Engine**:
```bash
# Create instance
gcloud compute instances create ai-data-analyst \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --tags http-server

# SSH and setup
gcloud compute ssh ai-data-analyst
# Follow local deployment steps
```

### Azure Container Instances

```bash
# Create resource group
az group create --name ai-analyst-rg --location eastus

# Create container instance
az container create \
  --resource-group ai-analyst-rg \
  --name ai-data-analyst \
  --image your-registry/ai-data-analyst:latest \
  --ports 8501 \
  --dns-name-label ai-analyst-unique \
  --environment-variables TOGETHER_API_KEY=your_key
```

### DigitalOcean App Platform

1. **Create app.yaml**:
```yaml
name: ai-data-analyst
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/ai-data-analyst-agent
    branch: main
  run_command: streamlit run main.py --server.port=8080 --server.address=0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  envs:
  - key: TOGETHER_API_KEY
    value: your_api_key_here
```

2. **Deploy**:
```bash
# Install doctl
# Connect to your account
doctl auth init

# Create app
doctl apps create app.yaml
```

## 🔒 Production Considerations

### Security

1. **Environment Variables**: Never commit API keys to version control
2. **HTTPS**: Always use SSL certificates in production
3. **Authentication**: Consider adding user authentication for sensitive data
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: Validate all uploaded files and user inputs

### Performance

1. **Caching**: Implement caching for processed files and AI responses
2. **Load Balancing**: Use multiple instances behind a load balancer
3. **Database**: Consider using a database for storing analysis results
4. **CDN**: Use a CDN for static assets and visualizations

### Monitoring

1. **Health Checks**: Implement comprehensive health checking
2. **Logging**: Structured logging with appropriate log levels
3. **Metrics**: Monitor CPU, memory, and response times
4. **Alerts**: Set up alerts for critical failures

### Scaling

1. **Horizontal Scaling**: Run multiple container instances
2. **Auto-scaling**: Configure auto-scaling based on CPU/memory
3. **Background Processing**: Move heavy computations to background workers
4. **Database Scaling**: Use read replicas for database scaling

### Example Production Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "80:8501"
    environment:
      - TOGETHER_API_KEY=${TOGETHER_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
  
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

### Backup and Recovery

1. **Data Backup**: Regular backups of uploaded files and analysis results
2. **Configuration Backup**: Version control for all configuration files
3. **Disaster Recovery**: Document recovery procedures
4. **Testing**: Regular testing of backup and recovery procedures

---

**Next Steps**: Choose the deployment option that best fits your needs and follow the specific instructions for your chosen platform.
>>>>>>> 0f3fe5ae72e1e543da9128827c74b2ea0a92d9d6
