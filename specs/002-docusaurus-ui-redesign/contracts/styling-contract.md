# CSS Contract: Docusaurus Theme Styling

## Overview
This contract defines the CSS interfaces and expected styling behaviors for the black-and-green theme redesign.

## Theme Color Variables Contract

### Core Color Variables
The following CSS custom properties must be defined in the theme:

| Variable | Type | Default Value | Description |
|----------|------|---------------|-------------|
| `--ifm-background-color` | color | `#0b0f14` | Main background color |
| `--ifm-font-color-base` | color | `#e6f4ea` | Base text color |
| `--ifm-color-primary` | color | `#00c853` | Primary green accent color |
| `--ifm-color-primary-dark` | color | `#00963d` | Darker primary color |
| `--ifm-color-primary-darkest` | color | `#00732f` | Darkest primary color |
| `--ifm-navbar-background-color` | color | `#0b0f14` | Navbar background |
| `--ifm-footer-background-color` | color | `#0b0f14` | Footer background |

### Code Block Variables
| Variable | Type | Default Value | Description |
|----------|------|---------------|-------------|
| `--ifm-code-background` | color | `#1a242f` | Background for code blocks |
| `--ifm-code-color` | color | `#e6f4ea` | Text color for code |

## Component Styling Contract

### Navbar Styling Requirements
- Background must use `--ifm-navbar-background-color`
- Text color must use `--ifm-font-color-base`
- Logo must be visible and properly sized
- Navigation links must use primary color on hover

### Documentation Content Styling
The following selectors must be styled:

#### Headings
- `.theme-doc-markdown h1, h2, h3, h4` - Text color should use `--ifm-font-color-base`

#### Links
- `a` - Color should use `--ifm-color-primary`

#### Code Elements
- `code` - Background should use `--ifm-code-background`, text should use `--ifm-code-color`
- `pre` - Background should use `--ifm-code-background`

#### Admonitions
- `.admonition` - Border left color should use `--ifm-color-primary`
- `.admonition--note` - Should have appropriate styling for note admonitions
- `.admonition--tip` - Should have appropriate styling for tip admonitions
- `.admonition--warning` - Should have appropriate styling for warning admonitions
- `.admonition--danger` - Should have appropriate styling for danger admonitions

### Pagination Styling
- `.pagination-nav` - Should use theme colors consistently

## Responsive Design Contract
- All styling must be responsive across mobile, tablet, and desktop
- Logo must scale appropriately
- Text remains readable at all screen sizes
- Navigation remains accessible on smaller screens

## Accessibility Contract
- All color combinations must meet WCAG AA contrast requirements
- Focus indicators must be visible
- Text size must be adjustable by users
- Color must not be the sole indicator of information

## Performance Contract
- CSS file size must not exceed 50KB
- Styling must not significantly impact page load time
- Use of CSS variables for maintainability