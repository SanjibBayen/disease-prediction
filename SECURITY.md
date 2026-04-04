# 🔒 Security Policy

## 🛡 Supported Versions

The following versions of **HealthPredict AI** are currently receiving security updates:

| Version | Status | Support End |
|---------|--------|-------------|
| 3.0.x   | ✅ Active | Until next major release |


---

## 📅 Version Support Details

| Version | Release Date | Security Updates | Bug Fixes | Feature Support |
|---------|--------------|------------------|-----------|-----------------|
| 3.0.0 | April 2026 | ✅ Full | ✅ Full | ✅ Full |
|

---

## 🚨 Reporting a Vulnerability

We take security vulnerabilities seriously and appreciate responsible disclosure.

### ❗ Important

**Do NOT report vulnerabilities via public GitHub issues.**

---

## 📩 How to Report

| Method | Contact |
|--------|---------|
| **Email** | `sanjibbayen11@gmail.com` |
| **Subject** | `[SECURITY] Brief description of the issue` |

---

## 📌 What to Include

Please include the following details:

1. **Description** – Clear explanation of the issue  
2. **Impact** – Potential risks if exploited  
3. **Steps to Reproduce** – Step-by-step instructions  
4. **Environment** – Python version, OS, dependencies  
5. **Proof of Concept** – Code/snippets (if possible)  
6. **Suggested Fix** – Recommendations  

---

## 🧪 Example Report

**Subject:** `[SECURITY] Environment variable exposure in logs`

**Description:**  
The logging configuration prints environment variables in debug mode, potentially exposing secrets.

**Impact:**  
High – API keys may be exposed in logs.

**Steps to Reproduce:**
```bash
# 1. Enable debug mode
DEBUG=True

# 2. Run application
python run.py

# 3. Check logs for exposed variables
```

**Environment:**
- Python: 3.11.0  
- OS: Ubuntu 22.04  
- FastAPI: 0.115.0  

**Suggested Fix:**  
Disable environment variable logging in production.

---

## ⏱ Response Timeline

| Stage | Timeline | Description |
|-------|----------|-------------|
| Acknowledgement | Within 48 hours | Confirmation of receipt |
| Validation | 3–5 business days | Investigation |
| Updates | Weekly | Progress updates |
| Fix | 14–30 days | Patch development |
| Disclosure | After fix | Public disclosure |

---

## 📢 Vulnerability Disclosure Policy

### Public Disclosure

- Vulnerabilities disclosed **after fix release**
- Reporter credited (optional anonymity)
- GitHub advisory will be published

---

### ✅ Responsible Disclosure Guidelines

- Do not exploit vulnerabilities beyond testing  
- Do not disclose publicly before fix  
- Do not perform DoS attacks  
- Do not access/modify user data  
- Avoid automated scanning without permission  

---

## 🔐 Security Best Practices

### 🔑 API Key Protection

- Never commit secrets to GitHub  
- Use environment variables  
- Rotate keys regularly  
- Separate dev & production keys  

---

### 🚀 Production Security

| Practice | Recommendation |
|----------|----------------|
| Debug Mode | `DEBUG=False` |
| CORS | Restrict origins |
| Rate Limiting | Enable |
| Logging | Avoid sensitive data |
| HTTPS | Always enabled |
| Environment | Separate dev/prod |

---

## ⚙️ Environment Variables Template

```env
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=warning

CORS_ORIGINS=https://yourdomain.com

SECRET_KEY=your-strong-secret-key
```

---

## 🛡 Known Security Features

| Feature | Status | Description |
|--------|--------|------------|
| Input Validation | ✅ Implemented | Pydantic validation |
| CORS Protection | ✅ Implemented | Restricted origins |
| Request Tracking | ✅ Implemented | Unique request IDs |
| Rate Limiting | ⚠️ Optional | Via slowapi |
| Authentication | 📋 Planned | v3.1 |
| HTTPS | ✅ Enabled | Render/Cloudflare |
| Env Isolation | ✅ Implemented | Dev/Prod configs |

---

## 📞 Security Contact

- **Name:** Sanjib Bayen  
- **Email:** sanjibbayen11@gmail.com  
- **GitHub:** https://github.com/SanjibBayen  
- **PGP Key:** Available upon request  

For urgent issues, use email.

---

## 🙏 Acknowledgements

- Open Source Community  
- Render  
- GitHub Security Team  

---

## 🔄 Policy Updates

This policy may change over time.

Updates will be shared via:
- GitHub Security Advisories  
- README updates  
- Release notes  

---

**Last Updated:** April 4, 2026  
**Version:** 3.0.0  

---

## 📄 Reporting Template

```markdown
## Security Vulnerability Report

**Date:** YYYY-MM-DD  
**Reporter:** Name/Handle  
**Severity:** Critical / High / Medium / Low  

### Vulnerability Information
- Type:
- Affected Component:
- Affected Versions:

### Description
[Explain the issue]

### Impact
[What could happen]

### Reproduction Steps
1. Step one  
2. Step two  
3. Step three  

### Environment
- Python:
- OS:
- Dependencies:

### Proposed Fix
[Suggested solution]

### Supporting Evidence
[Logs / screenshots / code]
```

---

**Thank you for helping keep HealthPredict AI secure! 🔒**