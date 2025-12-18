# Research: Docusaurus Book Theme UI Redesign (Black & Green)

## Overview
This research document addresses the key technical decisions and best practices for implementing the dark-first black-and-green theme redesign for the Docusaurus textbook site.

## Decision: Color Palette Implementation
**Rationale**: The design requires a dark-first theme with specific colors (#0b0f14 background, #e6f4ea text, #00c853 primary green) that must meet WCAG AA contrast requirements.

**Implementation Approach**:
- Use Docusaurus CSS variable overrides in `:root` and `[data-theme='dark']` selectors
- Follow Docusaurus' CSS variable system for consistent theming
- Override core variables like `--ifm-background-color`, `--ifm-color-primary`, etc.
- Ensure both light and dark modes respect the new color scheme while maintaining accessibility

**Alternatives considered**:
- Custom CSS files without variables: Would require more extensive overrides and harder maintenance
- Third-party theme packages: Would introduce unnecessary dependencies

## Decision: Logo Replacement
**Rationale**: The design requires replacing the current robotic logo with a minimal, abstract or typography-based tech logo.

**Implementation Approach**:
- Create a new minimal tech-focused logo as SVG asset
- Place in `static/img/` directory
- Update `docusaurus.config.js` to reference new logo
- Ensure proper sizing and responsive behavior across devices
- Maintain accessibility with appropriate alt text

**Alternatives considered**:
- Using an icon font: Would require additional dependencies
- Inline SVG in config: Would be harder to maintain and style

## Decision: Component Styling Strategy
**Rationale**: Need to style multiple Docusaurus components consistently (navbar, sidebar, footer, chapter content) while following best practices.

**Implementation Approach**:
- Use Docusaurus' swizzling feature for components that need extensive customization
- Create custom CSS modules for specific component styling
- Target Docusaurus' class names and CSS variables for consistency
- Focus on `.theme-doc-markdown`, navigation components, and admonition styling

**Specific Components to Style**:
- Navigation: `.navbar`, `.sidebar`, `.menu`
- Chapter content: `.theme-doc-markdown h1-h4`, `a`, `code`, `pre`, `.admonition`
- Pagination: `.pagination-nav`
- Code blocks: Syntax highlighting with new color scheme

**Alternatives considered**:
- Full theme swizzling: Would create maintenance overhead for future Docusaurus updates
- Inline styles: Would not follow Docusaurus best practices

## Decision: Responsive Design & WCAG Compliance
**Rationale**: The design must be responsive across all devices and meet WCAG AA contrast requirements.

**Implementation Approach**:
- Use Docusaurus' responsive breakpoints consistently
- Test color contrast ratios using automated tools
- Implement proper focus indicators for accessibility
- Ensure touch targets meet accessibility guidelines
- Validate responsive behavior on multiple screen sizes

## Decision: Theme Toggle Functionality
**Rationale**: The design must support both dark and light theme toggling while maintaining brand consistency.

**Implementation Approach**:
- Leverage Docusaurus' built-in theme switching functionality
- Define color variables for both light and dark modes that maintain the black-green aesthetic
- Ensure the toggle switch itself follows the new color scheme
- Test theme persistence across page loads

## Docusaurus Theming Best Practices Researched
- Use CSS variables instead of hardcoded colors for maintainability
- Follow Docusaurus' class naming conventions
- Utilize the theme configuration for logo and basic styling
- Use CSS modules for component-specific styles
- Leverage Docusaurus' plugin system for custom components
- Maintain compatibility with Docusaurus updates by avoiding deep swizzling when possible

## Files to Modify
1. `docusaurus.config.js` - Logo and theme configuration
2. `src/css/custom.css` - Main CSS variable overrides
3. `src/components/` - Custom components if needed
4. `static/img/` - New logo assets
5. `src/theme/` - Custom theme components if swizzling is necessary