# AI Job Hunter - Production Deployment Checklist

## Pre-Deployment Requirements

### 1. API Keys and Credentials
- [ ] Foorilla API Key obtained from [foorilla.com/dashboard](https://foorilla.com/dashboard)
- [ ] LLM API Key (OpenAI, Groq, or Anthropic) for resume adaptation
- [ ] GitHub personal access token (for CI/CD)

### 2. Required Information
- [ ] Your resume in PDF format
- [ ] Cover letter template (optional but recommended)
- [ ] Job search preferences and filters
- [ ] Your email address for notifications

## Option 1: Deploy on Replit (Recommended for Beginners)

### Step 1: Replit Setup
- [ ] Create Replit account at [replit.com](https://replit.com)
- [ ] Go to [replit.com/github](https://replit.com/github)
- [ ] Click "Import from GitHub"
- [ ] Enter: `https://github.com/MadhavBytes/AI-job-hunter`
- [ ] Click "Import"

### Step 2: Configure Environment Variables in Replit
- [ ] Click "Secrets" icon (lock icon) in left sidebar
- [ ] Add these environment variables:
  ```
  FOORILLA_API_KEY=your_key_here
  FOORILLA_API_BASE_URL=https://api.foorilla.com
  OPENAI_API_KEY=your_key_here  (or use GROQ_API_KEY)
  GROQ_API_KEY=your_key_here  (free tier available)
  RESUME_PATH=/tmp/resume.pdf
  ```
- [ ] Test that secrets are accessible

### Step 3: Install Dependencies
- [ ] Open Replit Shell/Console
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `pip install playwright`
- [ ] Run: `python -m playwright install chromium`

### Step 4: Deploy
- [ ] Click "Run" button
- [ ] Application will start at `https://[replit-name].replit.dev`
- [ ] Keep the Replit project running

### Replit Considerations
- ⚠️ Free tier may have 0.5 GB RAM limit
- ⚠️ Project goes to sleep after 1 hour of inactivity
- ⚠️ Paid plan ($7/month) recommended for production

## Option 2: Deploy on AWS EC2 (More Control)

### Step 1: Create EC2 Instance
- [ ] Log in to AWS Console
- [ ] Go to EC2 > Launch Instance
- [ ] Configuration:
  - **AMI**: Ubuntu Server 22.04 LTS
  - **Instance Type**: t2.micro (free tier)
  - **Storage**: 20 GB
  - **Security Groups**: Allow ports 22 (SSH), 8000 (app), 443 (HTTPS)
- [ ] Create/select key pair and save `.pem` file
- [ ] Launch instance
- [ ] Note Elastic IP address

### Step 2: Connect to Instance
- [ ] Open terminal/PowerShell
- [ ] Run: `ssh -i your-key.pem ubuntu@your-ec2-ip`
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`

### Step 3: Install Software
- [ ] Install Python: `sudo apt install python3.10 python3-pip git -y`
- [ ] Clone repo: `git clone https://github.com/MadhavBytes/AI-job-hunter.git`
- [ ] Enter directory: `cd AI-job-hunter`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install Playwright: `python3 -m playwright install chromium`

### Step 4: Configure Environment
- [ ] Create `.env` file: `nano .env`
- [ ] Add API keys (see Replit section)
- [ ] Save file (Ctrl+O, Enter, Ctrl+X)
- [ ] Test: `python3 main.py`

### Step 5: Setup Systemd Service
- [ ] Create service file: `sudo nano /etc/systemd/system/ai-job-hunter.service`
- [ ] Paste content from PRODUCTION_DEPLOYMENT.md
- [ ] Enable service: `sudo systemctl enable ai-job-hunter`
- [ ] Start service: `sudo systemctl start ai-job-hunter`
- [ ] Check status: `sudo systemctl status ai-job-hunter`

### Step 6: Setup Nginx Reverse Proxy (Optional)
- [ ] Install: `sudo apt install nginx -y`
- [ ] Configure: `sudo nano /etc/nginx/sites-available/default`
- [ ] Add proxy configuration from PRODUCTION_DEPLOYMENT.md
- [ ] Restart: `sudo systemctl restart nginx`

### Step 7: Enable HTTPS (Let's Encrypt)
- [ ] Install Certbot: `sudo apt install certbot python3-certbot-nginx -y`
- [ ] Request certificate: `sudo certbot --nginx -d your-domain.com`
- [ ] Auto-renewal: `sudo systemctl enable certbot.timer`

## Step 3: First Run & Testing

### Configuration
- [ ] Upload your resume.pdf to the application
- [ ] Configure job search preferences in UI
- [ ] Test Foorilla API connection
- [ ] Verify resume adaptation with sample job
- [ ] Test cover letter generation

### Test Job Application
- [ ] Find a test job on Foorilla
- [ ] Test the full auto-apply workflow
- [ ] Verify form filling
- [ ] Verify resume upload
- [ ] Check email confirmation

### Monitoring
- [ ] Check application logs
- [ ] Monitor API rate limits
- [ ] Verify database writes

## Production Hardening

### Security
- [ ] Never commit .env file
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Regular security audits

### Performance
- [ ] Enable caching for job listings
- [ ] Configure connection pooling
- [ ] Monitor memory usage
- [ ] Setup auto-scaling (AWS only)
- [ ] Enable CDN for static assets

### Reliability
- [ ] Setup automated backups
- [ ] Configure error alerting
- [ ] Setup health checks
- [ ] Enable auto-restart on failure
- [ ] Document runbooks

## Maintenance

### Daily
- [ ] Monitor application logs
- [ ] Check error rates
- [ ] Verify job application counts

### Weekly
- [ ] Review API usage
- [ ] Check disk space
- [ ] Review performance metrics

### Monthly
- [ ] Update dependencies
- [ ] Security patches
- [ ] Backup verification
- [ ] Performance optimization

## Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo journalctl -u ai-job-hunter -n 100 -f

# Verify dependencies
pip list | grep -E "fastapi|playwright"

# Test manually
python3 main.py
```

### Browser Automation Fails
```bash
# Install missing dependencies
sudo apt install -y libglib2.0-0 libx11-6 libxkbcommon0

# Reinstall Playwright
python3 -m playwright install chromium
```

### API Rate Limiting
- Check Foorilla API rate limits
- Add delays between requests
- Implement request queuing

### Memory Issues
- Reduce concurrent browser instances
- Implement job queue system
- Use database pagination

## Cost Monitoring

### AWS
- [ ] Set up billing alerts
- [ ] Monitor EC2 usage
- [ ] Review data transfer costs
- [ ] Set up cost anomaly detection

### Replit
- [ ] Monitor compute hours
- [ ] Review storage usage

## Next Steps After Deployment

1. ✅ Test with real job applications
2. ✅ Fine-tune resume adaptation
3. ✅ Optimize job matching algorithms
4. ✅ Setup automated resume backups
5. ✅ Configure notification system
6. ✅ Setup analytics dashboard
7. ✅ Plan feature roadmap

## Support Resources

- GitHub Issues: [AI-job-hunter Issues](https://github.com/MadhavBytes/AI-job-hunter/issues)
- Documentation: See README.md, IMPLEMENTATION_GUIDE.md, ADVANCED_AUTO_APPLY_GUIDE.md
- Foorilla API Docs: [foorilla.com/docs](https://foorilla.com/docs)

## Important Notes

⚠️ **Free Tier Limitations**
- Replit: May have CPU/memory constraints
- AWS: Only 12 months free, then charges apply
- LLM APIs: Check free tier quotas

✅ **Best Practices**
- Always test in non-production first
- Keep API keys secure
- Monitor logs regularly
- Backup data regularly
- Update dependencies monthly

---

**Last Updated**: 2024
**Version**: 1.0
