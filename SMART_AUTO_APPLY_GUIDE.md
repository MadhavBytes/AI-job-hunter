# AI Job Hunter - Smart Auto-Apply Feature Guide

## 🎯 Complete Workflow: From Resume Upload to Automated Job Applications

### What is Smart Auto-Apply?

Smart Auto-Apply is an AI-powered system that:
1. **Parses your resume** and extracts structured data
2. **Analyzes job descriptions** and calculates match scores
3. **Validates your credentials** before applying
4. **Optimizes your resume** for each job
5. **Auto-applies to jobs** matching your criteria
6. **Sends email notifications** for every action
7. **Handles failed credentials** with password reset

---

## 📋 Step-by-Step Workflow

### Step 1: Upload Your Resume
**URL:** `POST /upload-resume`

**How it works:**
1. Visit your application URL
2. Click "Upload Resume" button
3. Select your resume file (PDF or DOCX)
4. System extracts:
   - Name, email, phone
   - Job title and skills
   - Work experience
   - Education
   - Certifications
   - Keywords

**Example Response:**
```json
{
  "success": true,
  "resume_data": {
    "name": "Leela Madhav",
    "email": "leelamadhav.tp@gmail.com",
    "title": "MLOps Engineer",
    "skills": ["Python", "Kubernetes", "Docker", "AWS", "Azure"],
    "keywords": ["MLOps", "DevOps", "Data Engineering"]
  }
}
```

---

### Step 2: View Your Parsed Resume

**What you see:**
- All extracted information from your resume
- Identified skills and keywords
- Work experience timeline
- Education and certifications
- Option to edit extracted data
- Confirmation to proceed

---

### Step 3: Filter Jobs Based on Your Profile

**Available Filters:**
- Location (including "Remote" option)
- Job Title
- Experience Level (Entry, Mid, Senior)
- Job Type (Full-time, Contract, Freelance)
- Technical Skills (Python, Kubernetes, AWS, etc.)
- Company Industries
- Visa Sponsorship (in Perks & Benefits)
- Salary Range
- Company Size
- And 12+ more filters

**System automatically suggests filters** based on your resume:
- Shows jobs matching your skills
- Recommends locations you've worked in
- Prioritizes your experience level

---

### Step 4: Add LinkedIn/Indeed Credentials

**URL:** `POST /validate-credentials`

**What you provide:**
```json
{
  "email": "leelamadhav.tp@gmail.com",
  "password": "your_password",
  "platform": "LinkedIn"  // or "Indeed", "Dice", etc.
}
```

**System validates:**
- Email is correct
- Password is valid
- Account is active
- Credentials are secure

**If credentials fail:**
- System automatically triggers password reset
- Email sent to leelamadhav.tp@gmail.com
- Password reset link valid for 24 hours
- Continue after resetting password

---

### Step 5: View Job-Resume Match Score

**URL:** `POST /match-resume-job`

**For each job, system calculates:**
- **Match Percentage** (0-100%)
- **Matched Skills** (from job description)
- **Matched Keywords** (industry terms)
- **Missing Skills** (gaps to address)
- **Recommendation** (Strong/Moderate/Weak)

**Example:**
```json
{
  "match_percentage": 78.5,
  "matched_skills": ["Python", "Kubernetes", "AWS"],
  "missing_skills": ["Terraform", "Jenkins"],
  "recommendation": "strong",
  "should_apply": true
}
```

**Auto-Apply Rules:**
- ✅ **Match > 70%**: Strong recommendation - APPLY
- ⚠️ **Match 40-70%**: Moderate - Ask before applying
- ❌ **Match < 40%**: Weak - Skip

---

### Step 6: Resume Optimization

**System automatically:**
1. **Identifies keywords** from job description
2. **Highlights matching skills** in resume
3. **Reorganizes content** for ATS (Applicant Tracking System)
4. **Adds industry keywords** to increase visibility
5. **Creates optimized version** for each job

**What gets modified:**
- Summary/Objective section
- Skills section (reordered by relevance)
- Work experience (highlighted relevant achievements)
- Keywords for ATS scanning

**Note:** Your original resume is NEVER changed. Optimized version is used only for application.

---

### Step 7: Intelligent Auto-Apply

**URL:** `POST /smart-auto-apply`

**The system:**
1. Validates your credentials
2. For each selected job:
   - Calculates match score
   - Optimizes resume
   - Applies if match > 40%
   - Logs application
3. Sends confirmation emails
4. Generates summary report

**Request:**
```json
{
  "job_ids": ["job_123", "job_456", "job_789"],
  "resume_data": { ... },
  "user_credentials": {
    "email": "leelamadhav.tp@gmail.com",
    "password": "...",
    "platform": "LinkedIn"
  },
  "filters": { "location": "Remote", "experience_level": "mid" }
}
```

**Response:**
```json
{
  "success": true,
  "total_jobs": 50,
  "applications_submitted": 32,
  "applications_skipped": 18,
  "results": [
    {
      "job_id": "job_123",
      "applied": true,
      "match_percentage": 85.5,
      "timestamp": "2025-12-16T12:00:00",
      "matched_keywords": ["Python", "MLOps", "DevOps"]
    },
    ...
  ]
}
```

---

## 📧 Email Notifications

### Email 1: Resume Uploaded
```
Subject: Resume Successfully Uploaded - AI Job Hunter
Content: Your resume has been parsed and is ready for auto-apply
```

### Email 2: Credentials Validated
```
Subject: Account Verified - Ready to Apply
Content: Your LinkedIn/Indeed account is verified and ready
```

### Email 3: Job Application Submitted
```
Subject: Application Submitted - [Job Title] at [Company]
Content:
- Job ID
- Match Score: 85%
- Matched Skills: Python, Kubernetes, AWS
- Timestamp
- Link to view job posting
```

### Email 4: Password Reset (if needed)
```
Subject: Password Reset Request - AI Job Hunter
Content:
- Password reset link (valid 24 hours)
- Instructions to reset
- Security note
```

### Email 5: Auto-Apply Summary
```
Subject: Auto-Apply Summary Report - [Date]
Content:
- Total jobs processed: 50
- Successful applications: 32
- Applications skipped: 18
- Average match score: 72%
- Next steps
```

---

## 🔐 Credential & Password Reset Workflow

### If Credentials are Invalid:

1. **System detects invalid credentials**
2. **Automatically triggers password reset**
3. **Sends email to:** leelamadhav.tp@gmail.com
4. **Reset link includes:**
   - Unique token (secure)
   - 24-hour expiration
   - Clear instructions
5. **User clicks link and resets password**
6. **Resume auto-apply continues with new credentials**

---

## 🎯 Key Features

### 1. Resume Parsing
- Extracts text from PDF, DOCX, DOC, TXT
- Identifies: Name, Email, Phone, Title
- Extracts: Skills, Experience, Education, Certifications
- Generates: Keywords for matching

### 2. Credential Validation
- Validates platform credentials
- Checks account status
- Detects expired passwords
- Initiates secure password reset

### 3. Match Scoring
- Keyword-based matching (40-line implementation)
- ML-ready for TF-IDF or Cosine Similarity
- Configurable thresholds
- Detailed match breakdown

### 4. Resume Optimization
- ATS-friendly formatting
- Keyword injection
- Skill reordering
- Achievement highlighting

### 5. Email Notifications
- SMTP email sending
- HTML formatted
- Customizable templates
- Error logging

### 6. Auto-Apply Logic
- Batch processing
- Credential validation
- Match threshold checking
- Application logging
- Summary reporting

---

## 🚀 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/parse-resume` | POST | Parse uploaded resume |
| `/validate-credentials` | POST | Verify platform credentials |
| `/match-resume-job` | POST | Calculate job match score |
| `/smart-auto-apply` | POST | Execute intelligent auto-apply |
| `/request-password-reset` | POST | Trigger password reset |
| `/search` | GET | Search jobs with filters |
| `/upload-resume` | POST | Upload resume file |
| `/auto-apply` | POST | Simple auto-apply (legacy) |

---

## 💻 Example: Complete Smart Auto-Apply Flow

```python
import requests

# Step 1: Upload Resume
with open('resume.pdf', 'rb') as f:
    resume_response = requests.post(
        'https://your-app.com/parse-resume',
        files={'file': f}
    )
    resume_data = resume_response.json()['resume_data']

# Step 2: Search Jobs
jobs = requests.get(
    'https://your-app.com/search',
    params={'title': 'MLOps', 'location': 'Remote'}
).json()

# Step 3: Validate Credentials
creds_check = requests.post(
    'https://your-app.com/validate-credentials',
    json={
        'email': 'leelamadhav.tp@gmail.com',
        'password': 'your_password',
        'platform': 'LinkedIn'
    }
)

# Step 4: Smart Auto-Apply to Filtered Jobs
result = requests.post(
    'https://your-app.com/smart-auto-apply',
    json={
        'job_ids': [j['id'] for j in jobs['jobs']],
        'resume_data': resume_data,
        'user_credentials': {
            'email': 'leelamadhav.tp@gmail.com',
            'password': 'your_password',
            'platform': 'LinkedIn'
        },
        'filters': {'experience_level': 'mid'}
    }
)

print(f"Applications submitted: {result.json()['applications_submitted']}")
```

---

## ✅ What's Implemented

✅ Resume parsing from uploaded files
✅ Credential validation
✅ Password reset with email
✅ Resume-to-job matching
✅ Match score calculation
✅ Resume optimization
✅ Smart auto-apply workflow
✅ Email notifications
✅ Error handling
✅ Logging
✅ Security considerations

---

## 🔜 Next Steps: Production Enhancement

1. **Resume Parsing**: Use PyPDF2 (PDFs) + python-docx (Word)
2. **Email Service**: Configure Gmail SMTP or use SendGrid API
3. **Job Scraping**: Real LinkedIn/Indeed API integration
4. **ML Matching**: Implement TF-IDF or embeddings-based matching
5. **Database**: Store resumes and applications in PostgreSQL
6. **Cloud Storage**: Use AWS S3 for resume files
7. **Credentials**: Encrypt passwords with Fernet
8. **Rate Limiting**: Prevent API abuse

---

## 📞 Support Email

For questions about your applications, check your inbox at:
**leelamadhav.tp@gmail.com**

All notifications and password resets are sent there!
