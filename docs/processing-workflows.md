# Processing Workflows

This document describes the automated workflows that process and validate assets in the Universal Asset Library.

## Table of Contents

- [Overview](#overview)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Asset Processing Pipeline](#asset-processing-pipeline)
- [Validation Process](#validation-process)
- [Catalog Generation](#catalog-generation)
- [Deployment Process](#deployment-process)
- [Manual Processing](#manual-processing)

## Overview

The Universal Asset Library uses automated workflows to ensure consistent quality and reliable access to all assets. These workflows run on GitHub Actions and process assets through validation, optimization, and cataloging stages.

## GitHub Actions Workflows

### 1. Deploy to gh-pages Branch (`deploy-to-gh-pages.yml`)

**Purpose**: Builds and deploys the asset library to GitHub Pages with properly resolved Git LFS files.

**Triggers**:
- Push to main branch (when assets or configs change)
- Daily at 2 AM UTC (scheduled refresh)
- Manual workflow dispatch

**Process**:
1. Checkout repository with Git LFS
2. Resolve all LFS objects to actual files
3. Run Python validation scripts
4. Generate checksums for all assets
5. Build asset catalog JSON files
6. Build Jekyll site
7. Verify files are not LFS pointers
8. Deploy to gh-pages branch

### 2. Validate Assets (`validate-assets.yml`)

**Purpose**: Validates all assets for compliance with specifications.

**Triggers**:
- Pull requests affecting assets
- Manual workflow dispatch

**Process**:
1. Check file formats
2. Validate metadata completeness
3. Verify checksums
4. Check file sizes
5. Report validation results

## Asset Processing Pipeline

### Stage 1: Intake

When new assets are added:

1. **File Structure Check**
   - Verify correct directory structure
   - Check file naming conventions
   - Ensure metadata.json exists

2. **Format Validation**
   - Confirm file format matches declared type
   - Check file integrity
   - Validate against specifications

### Stage 2: Processing

Automated processing includes:

1. **Image Processing**
   ```bash
   # Generate WebP version
   convert input.jpg -quality 85 output.webp
   
   # Create thumbnail
   convert input.jpg -resize 300x300> thumbnail.jpg
   ```

2. **Checksum Generation**
   ```python
   # Generate SHA256 and MD5 checksums
   sha256_hash = hashlib.sha256(file_data).hexdigest()
   md5_hash = hashlib.md5(file_data).hexdigest()
   ```

3. **Metadata Enhancement**
   - Extract technical metadata
   - Add processing timestamps
   - Include file sizes and checksums

### Stage 3: Optimization

Assets are optimized for web delivery:

1. **Images**
   - Lossless compression for PNGs
   - Optimal JPEG quality (85-95)
   - WebP generation for modern browsers

2. **Videos**
   - H.264 encoding for compatibility
   - Web-optimized MP4 container
   - Thumbnail extraction

3. **Audio**
   - Normalized volume levels
   - Consistent bitrate encoding
   - Metadata preservation

## Validation Process

### Validation Script (`scripts/validate-assets.py`)

**Usage**:
```bash
python scripts/validate-assets.py --path assets --recursive
```

**Checks Performed**:

1. **File Validation**
   - File exists and is readable
   - Format matches expected MIME type
   - Size within limits
   - No corruption detected

2. **Metadata Validation**
   - Required fields present
   - Data types correct
   - URLs valid
   - Dates properly formatted

3. **Naming Convention**
   - Lowercase only
   - No spaces (use hyphens)
   - Descriptive names
   - Consistent with metadata ID

### Validation Report

The script generates a report showing:
- ✅ Valid assets
- ⚠️  Warnings (non-critical issues)
- ❌ Errors (must be fixed)

Example output:
```
Validating assets...

✅ assets/images/branding/logo-001/
   - All checks passed

⚠️  assets/images/nature/forest-002/
   - Warning: Missing optional thumbnail

❌ assets/videos/tutorial-001/
   - Error: metadata.json missing required field 'license'
   - Error: File size exceeds 500MB limit

Summary: 1 valid, 1 warning, 1 error
```

## Catalog Generation

### Build Catalog Script (`scripts/build-catalog.py`)

**Purpose**: Generates JSON catalogs for API access

**Process**:

1. **Scan Assets**
   ```python
   # Recursively find all assets
   for asset_type in ['images', 'videos', 'audio', 'datasets', 'archives']:
       scan_directory(f'assets/{asset_type}')
   ```

2. **Aggregate Metadata**
   - Read each metadata.json
   - Add computed fields (URLs, paths)
   - Build hierarchical structure

3. **Generate Catalogs**
   - `catalog/assets.json` - Complete catalog
   - `catalog/images.json` - Images only
   - `catalog/videos.json` - Videos only
   - etc.

4. **Calculate Statistics**
   ```json
   {
     "total_assets": 150,
     "total_size": 1073741824,
     "total_size_human": "1.0 GB",
     "by_type": {
       "images": 100,
       "videos": 20,
       "audio": 30
     }
   }
   ```

## Deployment Process

### GitHub Pages Deployment

The deployment process ensures Git LFS files are properly resolved:

1. **Build Phase**
   - Jekyll processes markdown and layouts
   - Assets are copied to _site directory
   - LFS files are fully resolved

2. **Verification**
   - Check file sizes to ensure not LFS pointers
   - Verify image files are valid
   - Test sample URLs

3. **Deployment**
   - Force push to gh-pages branch
   - GitHub Pages serves the static site
   - CDN distribution for global access

### Deployment Monitoring

Monitor deployment health:

```bash
# Check workflow status
gh run list --workflow=deploy-to-gh-pages.yml

# Verify deployed assets
curl -I https://codefuturist.github.io/asset-library/assets/images/example.jpg
```

## Manual Processing

For local development and testing:

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Validation Locally

```bash
# Validate all assets
python scripts/validate-assets.py --path assets --recursive

# Validate specific type
python scripts/validate-assets.py --path assets/images --recursive
```

### 3. Generate Checksums

```bash
# Generate checksums for new assets
python scripts/generate-checksums.py --path assets/images/new-asset --update-metadata
```

### 4. Build Catalog Locally

```bash
# Generate catalog files
python scripts/build-catalog.py

# Verify output
jq '.total_assets' catalog/assets.json
```

### 5. Test Jekyll Build

```bash
# Install Jekyll dependencies
bundle install

# Build site locally
bundle exec jekyll build

# Serve locally for testing
bundle exec jekyll serve
```

## Troubleshooting

### Common Issues

1. **Git LFS Pointers in Output**
   - Ensure `git lfs checkout` is run
   - Verify LFS is installed: `git lfs version`
   - Check file: `file assets/images/example.jpg`

2. **Validation Failures**
   - Check file permissions
   - Verify metadata.json syntax
   - Ensure required fields present

3. **Build Failures**
   - Check Python version (3.8+)
   - Verify all dependencies installed
   - Review workflow logs in GitHub Actions

### Debug Commands

```bash
# Check Git LFS status
git lfs status

# List LFS files
git lfs ls-files

# Verify specific file
python -c "import magic; print(magic.from_file('path/to/file'))"

# Test JSON validity
python -m json.tool metadata.json
```

## Best Practices

1. **Always validate locally** before pushing
2. **Use descriptive commit messages** for asset changes
3. **Monitor workflow runs** after pushing
4. **Keep assets organized** in proper categories
5. **Update documentation** when adding new asset types

## Future Enhancements

Planned improvements to processing workflows:

1. **Advanced Optimization**
   - AI-powered image compression
   - Automatic format selection
   - Smart thumbnail generation

2. **Extended Validation**
   - Content moderation
   - Duplicate detection
   - License verification

3. **Performance Improvements**
   - Parallel processing
   - Incremental catalog updates
   - Caching strategies
