# Data Model: Docusaurus Book Theme UI Redesign (Black & Green)

## Overview
This document defines the key entities and structures for the Docusaurus theme redesign. Since this is primarily a styling project, the "data model" focuses on configuration structures and styling entities.

## Entity: Theme Configuration
**Description**: Represents the visual styling properties including color variables, typography settings, and layout parameters that define the black-and-green appearance

**Properties**:
- `primaryColor`: string - Main green accent color (#00c853)
- `backgroundColor`: string - Dark background color (#0b0f14)
- `textColor`: string - Light text color (#e6f4ea)
- `borderColor`: string - Border color for UI elements
- `fontFamily`: string - Typography family for the theme
- `spacing`: object - Spacing scale for consistent layout
- `breakpoints`: object - Responsive design breakpoints

**Validation Rules**:
- All color values must be valid CSS color formats
- Color combinations must meet WCAG AA contrast requirements
- Spacing values must be positive numbers

## Entity: Logo Asset
**Description**: Represents the new minimal tech-focused branding element that replaces the existing robotic logo across the site

**Properties**:
- `src`: string - Path to the logo file (relative to static directory)
- `alt`: string - Alternative text for accessibility
- `width`: number - Display width in pixels
- `height`: number - Display height in pixels
- `responsive`: boolean - Whether the logo scales with screen size

**Validation Rules**:
- File must exist in the static directory
- Alt text must be descriptive and accessible
- Dimensions must be positive numbers

## Entity: Navigation Configuration
**Description**: Configuration for navigation elements (navbar, sidebar, footer) that will use the new color scheme

**Properties**:
- `backgroundColor`: string - Background color for navigation
- `itemColor`: string - Text color for navigation items
- `activeItemColor`: string - Color for currently selected item
- `hoverColor`: string - Color when hovering over navigation items
- `borderColor`: string - Color for navigation borders

## Entity: Code Block Styling
**Description**: Styling configuration for code blocks and inline code elements

**Properties**:
- `backgroundColor`: string - Background for code blocks
- `textColor`: string - Text color for code content
- `borderColor`: string - Border color for code blocks
- `fontSize`: string - Font size for code content
- `fontFamily`: string - Monospace font family for code

## Entity: Admonition Styling
**Description**: Styling configuration for callouts/admonitions (info, note, tip, warning, danger)

**Properties**:
- `infoBackgroundColor`: string - Background for info admonitions
- `infoBorderColor`: string - Border for info admonitions
- `noteBackgroundColor`: string - Background for note admonitions
- `noteBorderColor`: string - Border for note admonitions
- `tipBackgroundColor`: string - Background for tip admonitions
- `tipBorderColor`: string - Border for tip admonitions
- `warningBackgroundColor`: string - Background for warning admonitions
- `warningBorderColor`: string - Border for warning admonitions
- `dangerBackgroundColor`: string - Background for danger admonitions
- `dangerBorderColor`: string - Border for danger admonitions

## Entity: Responsive Breakpoint Configuration
**Description**: Responsive design breakpoints to ensure consistent styling across devices

**Properties**:
- `mobile`: string - Mobile device breakpoint (e.g., '768px')
- `tablet`: string - Tablet device breakpoint (e.g., '992px')
- `desktop`: string - Desktop device breakpoint (e.g., '1200px')