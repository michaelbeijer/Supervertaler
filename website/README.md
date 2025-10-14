# Supervertaler Website

Modern, responsive website for the Supervertaler AI-powered translation tool.

## 🌐 Live Site

- **Production**: https://supervertaler.com (custom domain)
- **GitHub Pages**: https://michaelbeijer.github.io/Supervertaler/ (fallback)

## 📁 Structure

```
website/
├── index.html      # Main HTML file
├── styles.css      # Stylesheet
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## 🚀 Deployment Options

### Option 1: GitHub Pages (Recommended - Free!)

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/website`
   - Save

2. **Custom Domain Setup (supervertaler.com):**
   - In repository Settings → Pages → Custom domain
   - Enter: `supervertaler.com`
   - Save (creates CNAME file automatically)

3. **DNS Configuration (Namecheap):**
   - Add A records pointing to GitHub Pages IPs:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Add CNAME record:
     ```
     www → michaelbeijer.github.io
     ```

4. **SSL/HTTPS:**
   - GitHub Pages provides free HTTPS automatically
   - Check "Enforce HTTPS" in Settings → Pages

### Option 2: Namecheap Hosting

If you prefer Namecheap hosting:

1. Upload files via FTP/cPanel File Manager
2. Place in public_html/ or domain root
3. Configure domain to point to hosting

### Option 3: Keep in Repository Only

The website folder can stay in the repo for version control even if you host elsewhere.

## 🎨 Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional design with gradient accents
- **Fast Loading**: Optimized CSS and minimal JavaScript
- **SEO Friendly**: Proper meta tags and semantic HTML
- **Accessibility**: ARIA labels and keyboard navigation
- **Smooth Animations**: Intersection Observer for scroll animations

## 🛠️ Local Development

Simply open `index.html` in a browser, or use a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server

# VS Code
# Use Live Server extension
```

Then visit: http://localhost:8000

## 📝 Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary: #3b82f6;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    /* ... */
}
```

### Content
Edit text directly in `index.html` sections:
- Hero section
- Features
- Download cards
- Documentation links
- Footer

### Download Links
Download buttons point to:
```
https://github.com/michaelbeijer/Supervertaler/raw/main/Supervertaler_v3.5.0-beta_CAT.py
https://github.com/michaelbeijer/Supervertaler/raw/main/Supervertaler_v2.5.0-CLASSIC.py
```

Update version numbers when releasing new versions.

## 🔄 Updating the Website

1. Edit files in `website/` directory
2. Commit and push to GitHub:
   ```bash
   git add website/
   git commit -m "Update website"
   git push
   ```
3. GitHub Pages automatically deploys within minutes

## 📊 Analytics (Optional)

To add Google Analytics:

1. Get tracking ID from Google Analytics
2. Add to `index.html` before `</head>`:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'YOUR-ID');
   </script>
   ```

## 🎯 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 Mobile Optimization

- Responsive grid layouts
- Touch-friendly buttons (min 44px)
- Optimized font sizes
- Hamburger menu ready (can be implemented)

## 🔍 SEO

Included optimizations:
- Meta description
- Open Graph tags (can be added)
- Semantic HTML5
- Fast loading
- Mobile-friendly
- HTTPS (via GitHub Pages)

## 🆘 Troubleshooting

**Website not updating?**
- Clear browser cache (Ctrl+Shift+R)
- Check GitHub Actions for build status
- Wait 2-5 minutes for GitHub Pages deployment

**Custom domain not working?**
- Verify DNS propagation (can take 24-48 hours)
- Check CNAME file exists in repository
- Ensure "Enforce HTTPS" is checked

**Images not loading?**
- Use absolute paths or relative from website root
- Check file names (case-sensitive on Linux servers)

## 📄 License

Same as Supervertaler project - MIT License

## 🤝 Contributing

To improve the website:
1. Fork the repository
2. Make changes in `website/` folder
3. Test locally
4. Submit pull request

---

**Last Updated**: October 14, 2025 (v3.5.0-beta release)
