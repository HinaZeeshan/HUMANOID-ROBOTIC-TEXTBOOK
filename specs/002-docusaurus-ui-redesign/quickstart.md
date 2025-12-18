# Quickstart: Docusaurus Book Theme UI Redesign (Black & Green)

## Overview
This guide helps developers implement and customize the new black-and-green theme for the Docusaurus textbook site.

## Prerequisites
- Node.js 18+ installed
- Docusaurus v2 installed
- Basic knowledge of CSS and Docusaurus theming

## Setup Process

### 1. Clone and Install
```bash
# Navigate to your Docusaurus project
cd my-textbook

# Install dependencies if not already done
npm install
```

### 2. Add the New Logo
1. Place your new SVG logo file in `static/img/logo.svg`
2. Make sure the logo follows accessibility standards with proper sizing and contrast

### 3. Configure the New Theme Colors
Create or update `src/css/custom.css` with the new color variables:

```css
/* Black and Green Theme Variables */
:root {
  --ifm-background-color: #0b0f14;
  --ifm-background-surface-color: #0f1720;
  --ifm-font-color-base: #e6f4ea;
  --ifm-color-primary: #00c853;
  --ifm-color-primary-dark: #00963d;
  --ifm-color-primary-darker: #008c39;
  --ifm-color-primary-darkest: #00732f;
  --ifm-color-primary-light: #33d176;
  --ifm-color-primary-lighter: #66dd98;
  --ifm-color-primary-lightest: #99eaba;
  --ifm-navbar-background-color: #0b0f14;
  --ifm-footer-background-color: #0b0f14;
  --ifm-code-background: #1a242f;
  --ifm-code-color: #e6f4ea;
}

/* Light theme overrides if needed */
[data-theme='light'] {
  --ifm-background-color: #f8f9fa;
  --ifm-font-color-base: #1a242f;
  --ifm-color-primary: #00c853;
  --ifm-navbar-background-color: #ffffff;
  --ifm-footer-background-color: #f8f9fa;
}
```

### 4. Update Docusaurus Configuration
In `docusaurus.config.js`, update the navbar logo configuration:

```javascript
module.exports = {
  // ... other config
  themeConfig: {
    navbar: {
      logo: {
        alt: 'Humanoid Robotics Textbook',
        src: 'img/logo.svg',  // Path to your new logo
        // Add dark mode logo if needed
        srcDark: 'img/logo.svg',  // If you have a different dark mode logo
      },
      // ... other navbar config
    },
    // ... rest of config
  },
};
```

### 5. Style Chapter Content
Add specific styling for chapter content in your custom CSS:

```css
/* Style for documentation markdown content */
.theme-doc-markdown h1,
.theme-doc-markdown h2,
.theme-doc-markdown h3,
.theme-doc-markdown h4 {
  color: #e6f4ea;
}

/* Style for links */
a {
  color: #00c853;
}

a:hover {
  color: #33d176;
}

/* Style for code blocks */
pre {
  background-color: #1a242f;
  border: 1px solid #334155;
  border-radius: 6px;
}

code {
  background-color: #1a242f;
  color: #e6f4ea;
}

/* Style for admonitions */
.admonition {
  border-left-color: #00c853;
}

.admonition--note {
  border-left-color: #00c853;
  background-color: rgba(0, 200, 83, 0.1);
}

.admonition--tip {
  border-left-color: #4caf50;
  background-color: rgba(76, 175, 80, 0.1);
}

.admonition--warning {
  border-left-color: #ff9800;
  background-color: rgba(255, 152, 0, 0.1);
}

.admonition--danger {
  border-left-color: #f44336;
  background-color: rgba(244, 67, 54, 0.1);
}
```

### 6. Build and Test
```bash
# Build the site
npm run build

# Serve locally to test
npm run serve
```

## Customization Options

### Adjusting Colors
You can easily adjust the theme by modifying the CSS variables in your custom CSS file. For example, to make the green more vibrant:

```css
:root {
  --ifm-color-primary: #00ff6a;  /* More vibrant green */
}
```

### Typography Changes
To update fonts, add to your custom CSS:

```css
:root {
  --ifm-font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

### Spacing Adjustments
Adjust spacing by modifying Docusaurus spacing variables:

```css
:root {
  --ifm-spacing-vertical: 1.5rem;
  --ifm-spacing-horizontal: 2rem;
}
```

## Testing Checklist
- [ ] Logo appears correctly in navbar
- [ ] All pages use the new color scheme
- [ ] Text meets WCAG AA contrast requirements
- [ ] Code blocks are readable with new colors
- [ ] Admonitions are properly styled
- [ ] Responsive design works on mobile
- [ ] Dark/light toggle functions correctly
- [ ] Navigation elements are clearly visible

## Troubleshooting
- If colors don't appear, ensure `src/css/custom.css` is imported in your main layout
- If logo doesn't show, verify the file path in `docusaurus.config.js`
- For contrast issues, use browser dev tools to verify color values meet WCAG AA standards