# Universal Asset Library API Documentation

The Universal Asset Library provides a RESTful JSON API for programmatic access to asset metadata and catalogs.

## Base URL

```
https://[username].github.io/universal-asset-library
```

## Endpoints

### Get Full Catalog

Retrieve the complete asset catalog with all assets and statistics.

```
GET /catalog/assets.json
```

**Response:**
```json
{
  "generated": "2024-01-20T14:30:00Z",
  "version": "1.0.0",
  "total_assets": 150,
  "total_size": 1073741824,
  "total_size_human": "1.0 GB",
  "stats": {
    "by_category": {
      "nature": 45,
      "technology": 30,
      "abstract": 25
    },
    "by_license": {
      "CC-BY-4.0": 80,
      "CC0": 50,
      "MIT": 20
    },
    "formats_available": ["jpg", "png", "webp", "mp4", "csv"],
    "tags": {
      "forest": 15,
      "landscape": 12,
      "tech": 10
    }
  },
  "assets": [
    {
      "id": "nature-forest-001",
      "title": "Dense Forest Canopy at Dawn",
      "type": "image",
      "category": "nature",
      "_url_base": "/assets/images/nature/forest-001"
    }
  ]
}
```

### Get Type-Specific Catalog

Retrieve catalog filtered by asset type.

```
GET /catalog/images.json
GET /catalog/videos.json
GET /catalog/audio.json
GET /catalog/datasets.json
GET /catalog/archives.json
```

**Response:** Similar structure to full catalog but filtered by type.

### Get Compact Index

Retrieve a lightweight index of all assets.

```
GET /catalog/index.json
```

**Response:**
```json
{
  "generated": "2024-01-20T14:30:00Z",
  "total_assets": 150,
  "assets": [
    {
      "id": "nature-forest-001",
      "type": "image",
      "title": "Dense Forest Canopy at Dawn",
      "category": "nature",
      "path": "images/nature/forest-001",
      "url": "/assets/images/nature/forest-001"
    }
  ]
}
```

### Get Asset Metadata

Retrieve detailed metadata for a specific asset.

```
GET /assets/[type]/[category]/[asset-id]/metadata.json
```

**Example:**
```
GET /assets/images/nature/forest-001/metadata.json
```

**Response:**
```json
{
  "id": "nature-forest-001",
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
    }
  ]
}
```

## Direct Asset Access

Access asset files directly using predictable URLs:

```
GET /assets/[type]/[category]/[asset-id]/[filename]
```

**Example:**
```
GET /assets/images/nature/forest-001/forest-001.jpg
GET /assets/images/nature/forest-001/forest-001.webp
```

## Usage Examples

### JavaScript/Fetch

```javascript
// Get all images
fetch('https://example.github.io/universal-asset-library/catalog/images.json')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.total_assets} images`);
    data.assets.forEach(asset => {
      console.log(`- ${asset.title} (${asset.id})`);
    });
  });

// Get specific asset metadata
fetch('https://example.github.io/universal-asset-library/assets/images/nature/forest-001/metadata.json')
  .then(response => response.json())
  .then(metadata => {
    console.log(`Asset: ${metadata.title}`);
    console.log(`License: ${metadata.license.type}`);
    console.log(`Available formats: ${metadata.formats.map(f => f.format).join(', ')}`);
  });
```

### Python

```python
import requests

# Get full catalog
response = requests.get('https://example.github.io/universal-asset-library/catalog/assets.json')
catalog = response.json()

print(f"Total assets: {catalog['total_assets']}")
print(f"Total size: {catalog['total_size_human']}")

# Filter by category
nature_assets = [
    asset for asset in catalog['assets'] 
    if asset['category'] == 'nature'
]

# Download an asset
asset_url = 'https://example.github.io/universal-asset-library/assets/images/nature/forest-001/forest-001.jpg'
response = requests.get(asset_url)
with open('forest.jpg', 'wb') as f:
    f.write(response.content)
```

### cURL

```bash
# Get catalog
curl https://example.github.io/universal-asset-library/catalog/assets.json

# Get specific asset metadata
curl https://example.github.io/universal-asset-library/assets/images/nature/forest-001/metadata.json

# Download asset
curl -O https://example.github.io/universal-asset-library/assets/images/nature/forest-001/forest-001.jpg
```

## Response Codes

- `200 OK` - Request successful
- `404 Not Found` - Asset or endpoint not found
- `304 Not Modified` - Cached version is still valid

## CORS

All API endpoints support CORS, allowing cross-origin requests from any domain.

## Rate Limiting

As this API is served via GitHub Pages, it inherits GitHub's rate limiting:
- No authentication required
- Generous limits for public access
- CDN caching reduces need for repeated requests

## Caching

API responses include appropriate cache headers:
- Catalog files: Cache for 1 hour
- Asset metadata: Cache for 24 hours
- Asset files: Cache for 30 days

## Best Practices

1. **Cache responses locally** to reduce API calls
2. **Use the index endpoint** for lightweight asset discovery
3. **Download type-specific catalogs** when you only need certain asset types
4. **Respect licensing** requirements for each asset
5. **Verify checksums** after downloading assets
6. **Use CDN URLs** when available for better performance

## Webhooks

While the static API doesn't support webhooks, you can:
- Watch the GitHub repository for updates
- Poll the catalog endpoint periodically
- Subscribe to the repository's RSS feed

## Future Enhancements

Planned API improvements:
- GraphQL endpoint
- Search parameters
- Pagination for large catalogs
- Asset preview endpoints
- Batch download support
