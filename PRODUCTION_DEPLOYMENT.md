# Production Deployment Guide - AI Job Hunter

## Overview
This guide covers deploying the AI Job Hunter application to production using Replit or AWS.

## Prerequisites
- GitHub Repository Access
- Replit Account (Free Tier) or AWS Account
- Foorilla API Key
- LLM API Key (OpenAI/Anthropic/Groq)
- Browser automation capabilities

## Option 1: Deployment on Replit (Recommended - Free)

### Step 1: Fork Repository to Replit
1. Visit https://replit.com
2. Click "Create" > "Import from GitHub"
3. Paste: https://github.com/MadhavBytes/AI-job-hunter
4. Select Python as language
5. Click "Import"

### Step 2: Configure Environment Variables
1. Click "Secrets" icon (lock icon) in left sidebar
2. Add the following environment variables:
   ```
   FOORILLA_API_KEY=your_api_key_here
   FOORILLA_API_BASE_URL=https://api.foorilla.com
   OPENAI_API_KEY=your_openai_key_or_use_groq
   GROQ_API_KEY=your_groq_key_free_tier
   DATABASE_URL=postgresql://user:password@localhost/ai_job_hunter
   RESUME_PATH=/path/to/resume.pdf
   COVER_LETTER_TEMPLATE=/path/to/template.txt
   ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
pip install playwright
python -m playwright install
```

### Step 4: Run Application
```bash
python main.py
```

The application will be available at: https://[your-replit-name].replit.dev

## Option 2: Deployment on AWS

### Step 1: Create EC2 Instance
1. AWS Management Console > EC2
2. Launch new instance:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (Free tier eligible)
   - Storage: 20GB

### Step 2: Configure Security Groups
Allow inbound traffic:
- Port 22 (SSH)
- Port 8000 (Application)
- Port 443 (HTTPS)

### Step 3: Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3-pip git -y

# Clone repository
git clone https://github.com/MadhavBytes/AI-job-hunter.git
cd AI-job-hunter

# Install Python dependencies
pip install -r requirements.txt
pip install playwright
python3 -m playwright install

# Install system dependencies for Playwright
sudo apt install -y libglib2.0-0 libx11-6
```

### Step 4: Setup Environment Variables
```bash
# Create .env file
echo "FOORILLA_API_KEY=your_api_key" > .env
echo "OPENAI_API_KEY=your_openai_key" >> .env
echo "GROQ_API_KEY=your_groq_key" >> .env
```

### Step 5: Run with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Step 6: Setup Systemd Service
```bash
sudo nano /etc/systemd/system/ai-job-hunter.service
```

Add:
```ini
[Unit]
Description=AI Job Hunter Application
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/AI-job-hunter
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 /home/ubuntu/AI-job-hunter/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-job-hunter
sudo systemctl start ai-job-hunter
```

### Step 7: Setup Nginx Reverse Proxy
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/default
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo systemctl restart nginx
```

## Database Setup

### Option A: PostgreSQL on AWS RDS
1. AWS > RDS > Create Database
2. PostgreSQL 14+
3. Note connection string

### Option B: Local SQLite (Development)
Already configured in main.py

## Monitoring and Logging

### Setup CloudWatch (AWS)
```bash
pip install watchtower
```

Add to main.py:
```python
import logging
import watchtower

logging.basicConfig(
    level=logging.INFO,
    handlers=[watchtower.CloudWatchLogHandler()]
)
```

### View Logs
```bash
sudo journalctl -u ai-job-hunter -f
```

## Performance Optimization

1. **Caching**: Enable Redis for job cache
   ```bash
   pip install redis
   ```

2. **Database Indexing**: Already implemented in models

3. **Async Processing**: FastAPI async endpoints for job search

4. **Rate Limiting**: Configured for Foorilla API

## Security Checklist

- [ ] All API keys in environment variables
- [ ] HTTPS enabled (AWS Certificate Manager or Let's Encrypt)
- [ ] Firewall rules configured
- [ ] Regular backups enabled
- [ ] Logs monitored for errors
- [ ] CORS properly configured
- [ ] Database credentials secured

## Troubleshooting

### Application won't start
```bash
# Check logs
sudo journalctl -u ai-job-hunter -n 50

# Verify dependencies
pip list | grep -E "fastapi|playwright|sqlalchemy"

# Test manually
python3 main.py
```

### Browser automation fails
```bash
# Ensure Playwright browsers installed
python3 -m playwright install chromium

# Check system dependencies
sudo apt install -y libglib2.0-0 libx11-6 libxkbcommon0
```

### API rate limiting
- Implement request queuing
- Add delays between job applications
- Use circuit breaker pattern

## Scaling

### Horizontal Scaling
1. Load Balancer (AWS ELB)
2. Auto Scaling Group
3. Shared database (RDS)

### Vertical Scaling
- Upgrade EC2 instance type (t2.small, t2.medium)
- Increase database instance size

## Cost Estimation

**Replit (Free Tier)**:
- Free with ads, 0.5 GB RAM
- Paid: $7/month for better specs

**AWS Minimal Setup**:
- EC2 t2.micro: ~$8-10/month (12 month free tier)
- RDS PostgreSQL: ~$15-20/month (Multi-AZ not recommended for dev)
- Data transfer: Variable
- **Total: ~$25-30/month after free tier**

## Continuous Deployment

### GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EC2
        env:
          EC2_KEY: ${{ secrets.EC2_PRIVATE_KEY }}
          EC2_HOST: ${{ secrets.EC2_HOST }}
        run: |
          mkdir -p ~/.ssh
          echo "$EC2_KEY" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh -i ~/.ssh/deploy_key ubuntu@$EC2_HOST 'cd /home/ubuntu/AI-job-hunter && git pull origin main && systemctl restart ai-job-hunter'
```

## Support and Updates

- Check GitHub Issues: https://github.com/MadhavBytes/AI-job-hunter/issues
- Review IMPLEMENTATION_GUIDE.md for feature details
- Monitor Foorilla API documentation for changes

## Next Steps

1. ✅ Choose deployment platform (Replit or AWS)
2. ✅ Configure environment variables
3. ✅ Deploy application
4. ✅ Test job search and auto-apply features
5. ✅ Setup monitoring and alerts
6. ✅ Enable automated backups
7. ✅ Document custom configurations
