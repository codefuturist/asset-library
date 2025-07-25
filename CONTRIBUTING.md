# Contributing to Universal Asset Library

Thank you for your interest in contributing to the Universal Asset Library! This document provides guidelines and instructions for contributing assets and code to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Asset Submission Guidelines](#asset-submission-guidelines)
- [Asset Requirements](#asset-requirements)
- [Metadata Standards](#metadata-standards)
- [File Naming Conventions](#file-naming-conventions)
- [License Requirements](#license-requirements)
- [Quality Standards](#quality-standards)
- [Submission Process](#submission-process)
- [Code Contributions](#code-contributions)
- [Review Process](#review-process)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and considerate in all interactions.

## How to Contribute

There are several ways to contribute to the Universal Asset Library:

1. **Submit new assets** - Add high-quality assets to the library
2. **Improve metadata** - Enhance existing asset descriptions and tags
3. **Report issues** - Identify bugs or suggest improvements
4. **Contribute code** - Improve scripts, workflows, or documentation
5. **Review submissions** - Help review and validate new contributions

## Asset Submission Guidelines

### 1. Asset Eligibility

Assets must meet the following criteria:

- ✅ High quality and professional standard
- ✅ Properly licensed (see [License Requirements](#license-requirements))
- ✅ Free from copyright violations
- ✅ Appropriate content (no offensive or inappropriate material)
- ✅ Useful for general purposes
- ✅ Minimum resolution/quality standards (see [Quality Standards](#quality-standards))

### 2. Directory Structure

Place your assets in the appropriate directory:

```
assets/
├── images/
│   └── [category]/
│       └── [asset-id]/
│           ├── metadata.json
│           ├── [asset-id].[format]
│           └── checksums.txt
├── videos/
├── audio/
├── datasets/
└── archives/
```

### 3. Asset ID Format

Use descriptive, unique identifiers:
- Format: `[category]-[descriptor]-[number]`
- Example: `nature-forest-001`, `tech-circuit-042`
- Use lowercase letters, numbers, and hyphens only

## Asset Requirements

### Images
- Minimum resolution: 1920x1080 (Full HD)
- Formats: Provide JPEG as primary, optionally PNG and WebP
- Color space: sRGB for web use
- File size: Optimized but maintaining quality

### Videos
- Minimum resolution: 1280x720 (HD)
- Formats: MP4 (H.264) as primary, optionally WebM
- Frame rate: 24fps minimum
- Audio: Include if relevant

### Audio
- Sample rate: 44.1kHz minimum
- Bit depth: 16-bit minimum
- Formats: MP3 as primary, optionally WAV or OGG
- Normalize audio levels

### Datasets
- Formats: CSV as primary, include JSON and/or Parquet
- Documentation: Include data dictionary
- Encoding: UTF-8
- Headers: Descriptive column names

### Archives
- Formats: ZIP as primary, optionally TAR.GZ
- Structure: Well-organized internal structure
- Documentation: Include README in archive

## Metadata Standards

Each asset must include a `metadata.json` file following this schema:

```json
{
  "id": "nature-forest-001",
  "title": "Descriptive Title",
  "description": "Detailed description of the asset",
  "category": "nature",
  "subcategory": "forest",
  "type": "image",
  "created": "2024-01-15T08:30:00Z",
  "version": "1.0.0",
  "license": {
    "type": "CC-BY-4.0",
    "url": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Creator Name"
  },
  "creator": {
    "name": "Your Name",
    "email": "email@example.com",
    "url": "https://yourwebsite.com"
  },
  "tags": ["relevant", "descriptive", "tags"],
  "formats": [
    {
      "format": "jpg",
      "filename": "nature-forest-001.jpg",
      "mimetype": "image/jpeg",
      "size": 2458624,
      "dimensions": {
        "width": 4000,
        "height": 3000
      }
    }
  ]
}
```

## File Naming Conventions

- Use lowercase letters, numbers, and hyphens only
- No spaces or special characters
- Be descriptive but concise
- Include version numbers if applicable
- Examples:
  - ✅ `nature-forest-001.jpg`
  - ✅ `tech-circuit-board-v2.png`
  - ❌ `My Image (Final).jpg`
  - ❌ `IMG_1234.JPG`

## License Requirements

All assets must have clear licensing:

### Acceptable Licenses
- Creative Commons (CC0, CC-BY, CC-BY-SA)
- MIT License
- Apache 2.0
- Public Domain
- Other open licenses (case-by-case)

### Required Attribution
If the license requires attribution, include:
- Creator name
- Source URL (if applicable)
- License type and URL
- Any modifications made

## Quality Standards

### Technical Quality
- No compression artifacts
- Proper color balance
- Sharp focus (where appropriate)
- No watermarks or logos
- Professional presentation

### Content Quality
- Useful for general purposes
- Well-composed/structured
- Clear and understandable
- Properly categorized
- Accurately described

## Submission Process

### 1. Fork the Repository
```bash
# Fork via GitHub UI, then clone
git clone https://github.com/yourusername/universal-asset-library.git
cd universal-asset-library
```

### 2. Create a Feature Branch
```bash
git checkout -b add-[asset-type]-[asset-id]
# Example: git checkout -b add-image-nature-forest-001
```

### 3. Add Your Assets
```bash
# Create asset directory
mkdir -p assets/images/nature/forest-001

# Add files
cp /path/to/your/image.jpg assets/images/nature/forest-001/forest-001.jpg

# Create metadata
# Edit metadata.json with proper information
```

### 4. Generate Checksums
```bash
python scripts/generate-checksums.py --path assets/images/nature/forest-001
```

### 5. Validate Your Submission
```bash
python scripts/validate-assets.py --path assets/images/nature/forest-001
```

### 6. Commit and Push
```bash
git add assets/images/nature/forest-001
git commit -m "Add nature forest image asset"
git push origin add-image-nature-forest-001
```

### 7. Create Pull Request
- Go to GitHub and create a pull request
- Fill out the PR template completely
- Wait for automated checks to pass
- Respond to reviewer feedback

## Code Contributions

### Python Scripts
- Follow PEP 8 style guide
- Include docstrings
- Add unit tests
- Update documentation

### GitHub Actions
- Test workflows locally when possible
- Document any new secrets or variables
- Ensure backwards compatibility

### Documentation
- Use clear, concise language
- Include examples
- Update table of contents
- Check for broken links

## Review Process

### What We Look For
1. **Compliance**: Meets all guidelines and requirements
2. **Quality**: High standard of technical and content quality
3. **Metadata**: Complete and accurate information
4. **Licensing**: Proper licensing and attribution
5. **Organization**: Follows directory and naming conventions

### Timeline
- Initial review: Within 3-5 business days
- Feedback incorporation: As needed
- Final approval: After all checks pass

### Automated Checks
Pull requests trigger automated workflows that:
- Validate metadata schema
- Check file formats
- Verify checksums
- Scan for security issues
- Build and test catalog generation

## Questions?

If you have questions about contributing:

1. Check existing [issues](https://github.com/yourusername/universal-asset-library/issues)
2. Read the [documentation](docs/)
3. Open a new issue with the "question" label
4. Join our [discussions](https://github.com/yourusername/universal-asset-library/discussions)

Thank you for contributing to the Universal Asset Library!
