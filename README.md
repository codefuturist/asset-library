# Universal Asset Library (UAL)

🎨 A GitHub Pages-powered repository for curated multi-format assets with stable URLs, comprehensive metadata, and automated processing workflows.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Assets](https://img.shields.io/badge/dynamic/json?color=green&label=assets&query=$.total_assets&url=https://raw.githubusercontent.com/codefuturist/asset-library/main/catalog/assets.json)](https://codefuturist.github.io/asset-library/catalog/assets.json)
[![Build Status](https://github.com/codefuturist/asset-library/workflows/Deploy%20to%20gh-pages%20Branch/badge.svg)](https://github.com/codefuturist/asset-library/actions)
[![Pages Status](https://img.shields.io/badge/GitHub%20Pages-Active-success)](https://codefuturist.github.io/asset-library/)

## 🚀 Features

- **Multi-format Support**: Images, videos, audio, datasets, and archives
- **Stable URLs**: Predictable, permanent URLs for all assets
- **Comprehensive Metadata**: Detailed technical and descriptive information
- **Automated Processing**: Format conversion, checksum generation, and validation
- **RESTful API**: JSON endpoints for programmatic access
- **Web Interface**: Searchable catalog with preview capabilities
- **Version Control**: Semantic versioning for asset updates
- **Quality Assurance**: Automated validation and integrity checks

## 📦 Asset Types

- **Images**: JPEG, PNG, WebP formats with automatic conversion
- **Videos**: MP4, WebM, and other formats with codec optimization
- **Audio**: MP3, WAV, OGG, and more with metadata preservation
- **Datasets**: CSV, JSON, Parquet, Excel, and other data formats
- **Archives**: ZIP, TAR, and other compressed formats

## 🔗 Stable URL Structure

All assets follow a predictable URL pattern:

```
https://codefuturist.github.io/asset-library/assets/[type]/[category]/[asset-id]/[filename]
```

Example:
```
https://codefuturist.github.io/asset-library/assets/images/branding/rey-it-solutions-logo-003/rey-it-solutions-logo-003.jpg
```

## 📡 API Endpoints

- **Full Catalog**: `/catalog/assets.json`
- **Type-specific Catalogs**: `/catalog/[type].json`
- **Asset Metadata**: `/assets/[type]/[category]/[asset-id]/metadata.json`

## 🛠️ Quick Start

### Using Assets

1. Browse the [asset catalog](https://codefuturist.github.io/asset-library/)
2. Find the asset you need
3. Use the stable URL in your project

### Contributing Assets

1. Fork this repository
2. Add your asset following the [contribution guidelines](CONTRIBUTING.md)
3. Submit a pull request
4. Automated workflows will process and validate your submission

## 📋 Asset Structure

Each asset includes:
- Multiple format variants
- Comprehensive metadata
- Checksums for integrity verification
- Clear licensing information
- Technical specifications

## 🔧 Development

### Prerequisites

- Python 3.8+
- ImageMagick (for image processing)
- FFmpeg (for video/audio processing)
- Node.js (for web interface)

### Setup

```bash
# Clone the repository
git clone https://github.com/codefuturist/asset-library.git
cd asset-library

# Install Python dependencies
pip install -r requirements.txt

# Run validation
python scripts/validate-assets.py --path assets --recursive

# Build catalog
python scripts/build-catalog.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Individual assets may have their own licenses specified in their metadata.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting assets.

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Asset Specifications](docs/asset-specifications.md)
- [Metadata Schema](docs/metadata-schema.md)
- [Processing Workflows](docs/processing-workflows.md)

## 🌟 Acknowledgments

- Thanks to all contributors who have submitted assets
- Built with Jekyll and GitHub Pages
- Processing powered by open-source tools
