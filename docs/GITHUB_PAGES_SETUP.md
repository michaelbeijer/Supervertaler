# GitHub Pages Setup Guide for supervertaler.com

Complete step-by-step guide to deploy the Supervertaler website using GitHub Pages with your custom domain.

## 📋 Prerequisites

- ✅ GitHub repository: michaelbeijer/Supervertaler
- ✅ Custom domain: supervertaler.com (Namecheap)
- ✅ Website files in `/website` folder

## 🚀 Step 1: Enable GitHub Pages

1. **Go to Repository Settings:**
   - Navigate to https://github.com/michaelbeijer/Supervertaler
   - Click **Settings** tab
   - Scroll to **Pages** in left sidebar

2. **Configure Source:**
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/website` (not `/root`)
   - Click **Save**

3. **Wait for Deployment:**
   - GitHub will build and deploy (2-5 minutes)
   - You'll see: "Your site is live at https://michaelbeijer.github.io/Supervertaler/"

## 🌐 Step 2: Configure Custom Domain (supervertaler.com)

### In GitHub:

1. **Add Custom Domain:**
   - Still in Settings → Pages
   - Under "Custom domain"
   - Enter: `supervertaler.com`
   - Click **Save**
   - This creates a `CNAME` file in `/website` folder

2. **Enable HTTPS:**
   - Check **"Enforce HTTPS"** (may take a few minutes to become available)
   - GitHub provides free SSL certificate automatically

### In Namecheap:

1. **Login to Namecheap:**
   - Go to https://namecheap.com
   - Navigate to Domain List
   - Click **Manage** next to supervertaler.com

2. **Configure DNS (Advanced DNS tab):**

   **A Records** (for apex domain):
   ```
   Type: A Record
   Host: @
   Value: 185.199.108.153
   TTL: Automatic
   ```
   
   Add three more A Records with same Host (@):
   ```
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

   **CNAME Record** (for www subdomain):
   ```
   Type: CNAME Record
   Host: www
   Value: michaelbeijer.github.io
   TTL: Automatic
   ```

3. **Remove conflicting records:**
   - Delete any existing A records pointing elsewhere
   - Delete Namecheap parking page redirects
   - Keep only the GitHub Pages records above

4. **Save all changes**

## ⏱️ Step 3: Wait for DNS Propagation

- DNS changes take 1-48 hours (usually 2-6 hours)
- Check progress: https://dnschecker.org
- Enter: `supervertaler.com`
- Wait until most locations show GitHub IPs

## ✅ Step 4: Verify Setup

1. **Test URLs:**
   - http://supervertaler.com (should redirect to HTTPS)
   - https://supervertaler.com (main site)
   - https://www.supervertaler.com (should work)
   - https://michaelbeijer.github.io/Supervertaler/ (GitHub Pages URL)

2. **Check HTTPS:**
   - Click padlock in browser
   - Should show "Connection is secure"
   - Certificate from GitHub

3. **Test Responsive Design:**
   - Desktop view
   - Mobile view (Chrome DevTools → Toggle device toolbar)
   - Different browsers (Chrome, Firefox, Safari)

## 🔧 Troubleshooting

### "There isn't a GitHub Pages site here"

**Cause**: DNS not propagated or misconfigured

**Solutions**:
1. Wait longer (up to 48 hours)
2. Verify DNS records in Namecheap
3. Check CNAME file exists in `/website` folder
4. Try incognito/private browsing mode

### Custom domain shows "404"

**Cause**: Folder setting incorrect

**Solutions**:
1. In Settings → Pages, ensure Folder is `/website` not `/root`
2. Verify `index.html` exists in `/website` folder
3. Check repository is public (or GitHub Pro for private repos)

### HTTPS not available

**Cause**: DNS not fully propagated

**Solutions**:
1. Wait 24 hours after DNS changes
2. Uncheck and re-check "Enforce HTTPS"
3. Remove and re-add custom domain

### Website shows old version

**Cause**: Browser cache or GitHub build delay

**Solutions**:
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Try incognito mode
4. Wait 5-10 minutes for GitHub to rebuild

### Images/CSS not loading

**Cause**: Incorrect paths

**Solutions**:
1. Use relative paths: `styles.css` not `/styles.css`
2. Check file names (case-sensitive!)
3. Verify files committed to repository

## 📊 Optional: Google Analytics

1. **Create GA4 Property:**
   - Go to https://analytics.google.com
   - Create new property for supervertaler.com
   - Get Measurement ID (G-XXXXXXXXXX)

2. **Add to website:**
   Edit `website/index.html`, add before `</head>`:
   ```html
   <!-- Google tag (gtag.js) -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

3. **Commit and push:**
   ```bash
   git add website/index.html
   git commit -m "Add Google Analytics"
   git push
   ```

## 🔄 Updating the Website

Whenever you update the website:

```bash
# 1. Make changes to files in website/
# 2. Commit changes
git add website/
git commit -m "Update website: [description]"

# 3. Push to GitHub
git push origin main

# 4. Wait 2-5 minutes for GitHub Pages to rebuild
# 5. Hard refresh browser (Ctrl+Shift+R)
```

## 📱 Testing Checklist

Before announcing the website:

- [ ] Desktop view looks good (1920px, 1366px, 1024px)
- [ ] Tablet view works (768px, 834px)
- [ ] Mobile view responsive (375px, 414px)
- [ ] All links work (internal anchors and external)
- [ ] Download buttons work
- [ ] Navigation smooth scrolling works
- [ ] HTTPS enabled (green padlock)
- [ ] www subdomain redirects to main domain
- [ ] Fast loading (< 3 seconds)
- [ ] No console errors
- [ ] Works in Chrome, Firefox, Safari
- [ ] Social sharing looks good (test with Facebook/Twitter debuggers)

## 🎯 Performance Tips

1. **Image Optimization:**
   - If you add images, compress them
   - Use WebP format for better compression
   - Max 200KB per image

2. **Minify Files (Optional):**
   - Minify CSS: https://cssminifier.com
   - Minify JS: https://javascript-minifier.com
   - Not critical for small sites

3. **CDN (Already included):**
   - Google Fonts loaded via CDN
   - GitHub Pages has global CDN

## 📧 Email Setup (Optional)

To add professional email (info@supervertaler.com):

1. **Namecheap Email:**
   - Enable in Namecheap dashboard
   - Or use Gmail with custom domain
   - Or use free tier: Zoho Mail, ProtonMail

2. **Add MX Records:**
   - Follow email provider's DNS instructions
   - Don't delete GitHub Pages records

## 🔐 Security

GitHub Pages includes:
- ✅ Free HTTPS/SSL
- ✅ DDoS protection
- ✅ Global CDN
- ✅ Automatic security updates

## 📈 SEO Checklist

After launch:

- [ ] Submit to Google Search Console
- [ ] Submit sitemap (can create sitemap.xml)
- [ ] Verify meta descriptions in index.html
- [ ] Add Open Graph tags for social sharing
- [ ] Test with Google PageSpeed Insights
- [ ] Check mobile-friendliness test

## 🎉 Launch Checklist

- [ ] GitHub Pages enabled
- [ ] Custom domain configured
- [ ] DNS records updated
- [ ] HTTPS enforced
- [ ] All links tested
- [ ] Mobile responsive verified
- [ ] Analytics added (optional)
- [ ] Announced on social media
- [ ] Added to GitHub repository description
- [ ] Updated business cards/materials

## 📞 Support

If you encounter issues:

1. **GitHub Pages Status:**
   - https://www.githubstatus.com

2. **DNS Checker:**
   - https://dnschecker.org

3. **GitHub Docs:**
   - https://docs.github.com/en/pages

4. **Namecheap Support:**
   - https://www.namecheap.com/support/

---

**Setup Time**: 5 minutes (plus DNS propagation wait)
**Cost**: $0 (GitHub Pages is free!)
**Last Updated**: October 14, 2025
