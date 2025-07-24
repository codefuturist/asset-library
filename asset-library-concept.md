# Universal Asset Library (UAL)
## A GitHub Pages Repository for Curated Multi-Format Assets

### Repository Structure

```
universal-asset-library/
├── README.md
├── _config.yml              # Jekyll configuration
├── index.html               # Main catalog page
├── LICENSE
├── CONTRIBUTING.md
├── .github/
│   ├── workflows/
│   │   ├── validate-assets.yml
│   │   ├── generate-checksums.yml
│   │   ├── build-catalog.yml
│   │   └── convert-formats.yml
│   └── ISSUE_TEMPLATE/
│       ├── asset-submission.md
│       └── bug-report.md
├── assets/
│   ├── images/
│   │   ├── nature/
│   │   │   └── forest-001/
│   │   │       ├── metadata.json
│   │   │       ├── forest-001.jpg
│   │   │       ├── forest-001.webp
│   │   │       ├── forest-001.png
│   │   │       └── checksums.txt
│   │   └── [categories]/
│   ├── videos/
│   │   └── [category]/[asset-id]/
│   ├── audio/
│   │   └── [category]/[asset-id]/
│   ├── datasets/
│   │   └── [category]/[asset-id]/
│   └── archives/
│       └── [category]/[asset-id]/
├── catalog/
│   ├── assets.json          # Complete asset catalog
│   ├── images.json
│   ├── videos.json
│   ├── audio.json
│   ├── datasets.json
│   └── archives.json
├── scripts/
│   ├── generate-metadata.py
│   ├── validate-assets.py
│   ├── convert-formats.py
│   ├── generate-checksums.py
│   └── build-catalog.py
├── docs/
│   ├── api.md
│   ├── asset-specifications.md
│   ├── metadata-schema.md
│   └── processing-workflows.md
└── _layouts/
    ├── default.html
    ├── asset.html
    └── category.html
```

### Metadata Schema

Each asset includes a `metadata.json` file with comprehensive information:

```json
{
  "id": "forest-001",
  "title": "Dense Forest Canopy at Dawn",
  "description": "High-resolution photograph of temperate forest canopy with morning mist",
  "category": "nature",
  "subcategory": "forest",
  "type": "image",
  "created": "2024-01-15T08:30:00Z",
  "added": "2024-01-20T14:22:00Z",
  "modified": "2024-01-20T14:22:00Z",
  "version": "1.0.0",
  "license": {
    "type": "CC-BY-4.0",
    "url": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "John Doe Photography"
  },
  "creator": {
    "name": "John Doe",
    "email": "john@example.com",
    "url": "https://johndoe.com"
  },
  "tags": ["forest", "nature", "trees", "mist", "dawn", "canopy"],
  "formats": [
    {
      "format": "jpg",
      "filename": "forest-001.jpg",
      "mimetype": "image/jpeg",
      "size": 2458624,
      "dimensions": {
        "width": 4000,
        "height": 3000
      },
      "checksum": {
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      }
    },
    {
      "format": "webp",
      "filename": "forest-001.webp",
      "mimetype": "image/webp",
      "size": 1843968,
      "dimensions": {
        "width": 4000,
        "height": 3000
      },
      "checksum": {
        "md5": "5d41402abc4b2a76b9719d911017c592",
        "sha256": "8b1a9953c4611296a827abf8c47804d7e6f5c2d7a5f0e4b8e9c7f8a2b1c3d4e5"
      }
    }
  ],
  "processing": {
    "source_format": "jpg",
    "conversions": [
      {
        "to": "webp",
        "tool": "imagemagick",
        "version": "7.1.0",
        "parameters": "-quality 85 -define webp:method=6"
      },
      {
        "to": "png",
        "tool": "imagemagick",
        "version": "7.1.0",
        "parameters": "-strip -compress LZW"
      }
    ]
  },
  "technical": {
    "camera": "Canon EOS R5",
    "lens": "RF 24-105mm F4 L IS USM",
    "settings": {
      "aperture": "f/8",
      "shutter_speed": "1/125",
      "iso": 400,
      "focal_length": "35mm"
    },
    "location": {
      "latitude": 45.5231,
      "longitude": -122.6765,
      "altitude": 245,
      "place": "Forest Park, Portland, Oregon"
    }
  }
}
```

### Stable URL Structure

All assets follow a predictable URL pattern:

```
https://[username].github.io/universal-asset-library/assets/[type]/[category]/[asset-id]/[filename]

Example:
https://example.github.io/universal-asset-library/assets/images/nature/forest-001/forest-001.jpg
```

### API Endpoints

The repository provides JSON-based API endpoints:

```
# Full catalog
https://[username].github.io/universal-asset-library/catalog/assets.json

# Type-specific catalogs
https://[username].github.io/universal-asset-library/catalog/images.json
https://[username].github.io/universal-asset-library/catalog/datasets.json

# Individual asset metadata
https://[username].github.io/universal-asset-library/assets/[type]/[category]/[asset-id]/metadata.json
```

### Processing Workflows

#### 1. Asset Ingestion Workflow

```yaml
name: Process New Asset
on:
  pull_request:
    paths:
      - 'assets/**'

jobs:
  validate-and-process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Asset Structure
        run: python scripts/validate-assets.py --path ${{ github.event.pull_request.files }}
      
      - name: Generate Alternative Formats
        run: python scripts/convert-formats.py --input ${{ github.event.pull_request.files }}
      
      - name: Generate Checksums
        run: python scripts/generate-checksums.py --path assets/
      
      - name: Update Metadata
        run: python scripts/generate-metadata.py --enhance
      
      - name: Rebuild Catalog
        run: python scripts/build-catalog.py
      
      - name: Commit Changes
        uses: EndBug/add-and-commit@v9
        with:
          message: 'Process assets and update catalog'
```

#### 2. Format Conversion Examples

**Images:**
```bash
# Convert to multiple formats
convert original.jpg -quality 85 output.webp
convert original.jpg -strip -compress LZW output.png
convert original.jpg -resize 50% -quality 90 output-thumb.jpg
```

**Datasets:**
```python
# Convert between data formats
import pandas as pd

# Read source
df = pd.read_csv('data.csv')

# Generate alternatives
df.to_json('data.json', orient='records', indent=2)
df.to_parquet('data.parquet', compression='snappy')
df.to_excel('data.xlsx', index=False)
df.to_pickle('data.pkl')
```

**Video:**
```bash
# Convert to multiple codecs
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 output.webm
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium output-h265.mp4
```

### Checksum Verification

Each asset directory contains a `checksums.txt` file:

```
# MD5 checksums
d41d8cd98f00b204e9800998ecf8427e  forest-001.jpg
5d41402abc4b2a76b9719d911017c592  forest-001.webp
aab3238922bcc25a6f606eb525ffdc56  forest-001.png

# SHA256 checksums
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  forest-001.jpg
8b1a9953c4611296a827abf8c47804d7e6f5c2d7a5f0e4b8e9c7f8a2b1c3d4e5  forest-001.webp
3f786850e387550fdab836ed7e6dc1de1e56f45ec4c4b06c4cbb8c4e6d9e7f9a  forest-001.png
```

### Web Interface Features

The GitHub Pages site provides:

1. **Searchable Catalog**: Filter by type, category, tags, license
2. **Asset Preview**: Inline preview for images, audio players, video players
3. **Download Options**: Direct links to all available formats
4. **Metadata Display**: Full technical details and attribution
5. **API Documentation**: Interactive API explorer
6. **Usage Examples**: Code snippets for common use cases

### Dataset Format Examples

For datasets, provide multiple serialization formats:

```
datasets/
└── climate/
    └── temperature-global-2023/
        ├── metadata.json
        ├── temperature-global-2023.csv
        ├── temperature-global-2023.json
        ├── temperature-global-2023.parquet
        ├── temperature-global-2023.xlsx
        ├── temperature-global-2023.sqlite
        └── checksums.txt
```

### Best Practices

1. **Version Control**: Use semantic versioning for asset updates
2. **Compression**: Balance quality vs. file size for web delivery
3. **Accessibility**: Include alt text and descriptions in metadata
4. **Documentation**: Provide clear usage rights and attribution requirements
5. **Automation**: Use GitHub Actions for all processing tasks
6. **Validation**: Enforce schema validation for all metadata
7. **Backup**: Mirror high-value assets to cloud storage
8. **CDN**: Consider using GitHub's CDN or implementing CloudFlare

### Example Python Script for Catalog Generation

```python
# scripts/build-catalog.py
import json
import os
from pathlib import Path
from datetime import datetime

def build_catalog(assets_dir='assets'):
    catalog = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'total_assets': 0,
        'total_size': 0,
        'assets': []
    }
    
    for asset_type in os.listdir(assets_dir):
        type_path = Path(assets_dir) / asset_type
        if not type_path.is_dir():
            continue
            
        for category in os.listdir(type_path):
            category_path = type_path / category
            if not category_path.is_dir():
                continue
                
            for asset_id in os.listdir(category_path):
                asset_path = category_path / asset_id
                metadata_file = asset_path / 'metadata.json'
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        
                    # Add computed fields
                    metadata['url_base'] = f'/assets/{asset_type}/{category}/{asset_id}'
                    metadata['total_size'] = sum(fmt['size'] for fmt in metadata.get('formats', []))
                    
                    catalog['assets'].append(metadata)
                    catalog['total_assets'] += 1
                    catalog['total_size'] += metadata['total_size']
    
    # Write main catalog
    with open('catalog/assets.json', 'w') as f:
        json.dump(catalog, f, indent=2)
    
    # Write type-specific catalogs
    for asset_type in ['images', 'videos', 'audio', 'datasets', 'archives']:
        type_assets = [a for a in catalog['assets'] if a['type'] == asset_type.rstrip('s')]
        type_catalog = {
            'generated': catalog['generated'],
            'type': asset_type,
            'total_assets': len(type_assets),
            'assets': type_assets
        }
        with open(f'catalog/{asset_type}.json', 'w') as f:
            json.dump(type_catalog, f, indent=2)

if __name__ == '__main__':
    build_catalog()
```

This structure provides a robust, scalable foundation for a universal asset library with stable URLs, comprehensive metadata, and automated processing workflows.