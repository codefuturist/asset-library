# Asset Specifications

This document defines the technical specifications and requirements for assets in the Universal Asset Library.

## Table of Contents

- [General Requirements](#general-requirements)
- [Image Specifications](#image-specifications)
- [Video Specifications](#video-specifications)
- [Audio Specifications](#audio-specifications)
- [Dataset Specifications](#dataset-specifications)
- [Archive Specifications](#archive-specifications)
- [Metadata Requirements](#metadata-requirements)
- [File Naming Conventions](#file-naming-conventions)

## General Requirements

All assets must:

1. **Have unique identifiers** following the pattern: `[category]-[id]`
2. **Include comprehensive metadata** in JSON format
3. **Provide checksums** for integrity verification
4. **Specify licensing** clearly and accurately
5. **Be virus-free** and safe for distribution
6. **Follow ethical guidelines** (no offensive or inappropriate content)

## Image Specifications

### Supported Formats
- **Primary**: JPEG (.jpg, .jpeg)
- **Alternative**: PNG (.png), WebP (.webp)
- **Vector**: SVG (.svg) for logos and icons

### Technical Requirements
- **Minimum resolution**: 800x600 pixels
- **Maximum file size**: 50MB per image
- **Color space**: sRGB recommended
- **Compression**: Optimized for web delivery

### Quality Standards
- Clear, well-exposed images
- No watermarks unless part of the asset
- Proper color balance
- Sharp focus where appropriate

### Directory Structure
```
assets/images/[category]/[asset-id]/
├── [asset-id].jpg          # Primary format
├── [asset-id].png          # Alternative format (optional)
├── [asset-id].webp         # WebP format (optional)
├── [asset-id]-thumb.jpg    # Thumbnail (optional)
└── metadata.json           # Required metadata
```

## Video Specifications

### Supported Formats
- **Primary**: MP4 (H.264/AVC)
- **Alternative**: WebM (VP9)
- **Future**: AV1 when browser support improves

### Technical Requirements
- **Resolution**: Up to 4K (3840x2160)
- **Frame rate**: 24-60 fps
- **Bitrate**: Adaptive based on resolution
- **Audio**: AAC stereo, 128-320 kbps
- **Maximum file size**: 500MB

### Encoding Guidelines
```bash
# Example FFmpeg command for web-optimized MP4
ffmpeg -i input.mov -c:v libx264 -preset slow -crf 22 \
       -c:a aac -b:a 128k -movflags +faststart output.mp4
```

## Audio Specifications

### Supported Formats
- **Primary**: MP3 (.mp3)
- **Alternative**: OGG Vorbis (.ogg), WAV (.wav)
- **Lossless**: FLAC (.flac) for archival

### Technical Requirements
- **Sample rate**: 44.1 kHz or 48 kHz
- **Bit depth**: 16-bit or 24-bit
- **Channels**: Mono or stereo
- **Bitrate**: 128-320 kbps for lossy formats

### Quality Standards
- Normalized audio levels
- No clipping or distortion
- Proper metadata tags

## Dataset Specifications

### Supported Formats
- **Tabular**: CSV (.csv), TSV (.tsv), Excel (.xlsx)
- **Structured**: JSON (.json), XML (.xml)
- **Binary**: Parquet (.parquet), HDF5 (.h5)
- **Database**: SQLite (.db, .sqlite)

### Requirements
- **Documentation**: README with data dictionary
- **Encoding**: UTF-8 for text files
- **Headers**: First row should contain column names
- **Size limits**: 1GB uncompressed

### Best Practices
- Include sample data preview
- Provide schema documentation
- Version control for updates
- Clear column naming

## Archive Specifications

### Supported Formats
- **ZIP**: Universal compatibility
- **TAR.GZ**: Unix/Linux standard
- **7Z**: High compression ratio

### Requirements
- **Compression**: Balanced for size and speed
- **Structure**: Logical directory organization
- **Documentation**: Include README in archive
- **Size limit**: 1GB compressed

## Metadata Requirements

Every asset must include a `metadata.json` file with:

```json
{
  "id": "asset-001",
  "title": "Asset Title",
  "description": "Detailed description",
  "category": "category-name",
  "tags": ["tag1", "tag2"],
  "license": {
    "type": "CC-BY-4.0",
    "url": "https://creativecommons.org/licenses/by/4.0/"
  },
  "creator": {
    "name": "Creator Name",
    "url": "https://example.com"
  },
  "technical": {
    "format": "JPEG",
    "dimensions": "1920x1080",
    "fileSize": 2048576,
    "checksum": {
      "sha256": "...",
      "md5": "..."
    }
  },
  "dates": {
    "created": "2024-01-01",
    "modified": "2024-01-15",
    "added": "2024-01-20"
  }
}
```

## File Naming Conventions

### General Rules
1. **Use lowercase** for all filenames
2. **Replace spaces** with hyphens (-)
3. **Avoid special characters** except hyphens and underscores
4. **Include version numbers** when applicable: `asset-v2.jpg`
5. **Use descriptive names** that reflect content

### Examples
- ✅ Good: `mountain-landscape-001.jpg`
- ❌ Bad: `IMG_12345.JPG`
- ✅ Good: `user-data-2024-01.csv`
- ❌ Bad: `data (1).csv`

## Validation

All assets are automatically validated for:

1. **File integrity**: Checksum verification
2. **Format compliance**: Proper file structure
3. **Metadata completeness**: All required fields
4. **Size limits**: Within specified bounds
5. **Naming conventions**: Follows standards

Use the validation script before submitting:

```bash
python scripts/validate-assets.py --path assets/[type]/[category]/[asset-id]
```
