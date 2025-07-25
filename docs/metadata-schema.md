# Asset Metadata Schema

This document defines the schema for asset metadata in the Universal Asset Library. Each asset must include a `metadata.json` file that conforms to this schema.

## Schema Overview

The metadata schema is designed to be:
- **Comprehensive**: Captures all relevant information about an asset
- **Extensible**: Allows for additional fields as needed
- **Standardized**: Ensures consistency across all assets
- **Machine-readable**: Enables automated processing and validation

## Required Fields

### Core Identification

#### `id` (string, required)
Unique identifier for the asset.
- Format: lowercase letters, numbers, and hyphens only
- Pattern: `^[a-z0-9-]+$`
- Example: `"nature-forest-001"`

#### `title` (string, required)
Human-readable title for the asset.
- Minimum length: 3 characters
- Example: `"Dense Forest Canopy at Dawn"`

#### `description` (string, required)
Detailed description of the asset.
- Minimum length: 10 characters
- Example: `"High-resolution photograph of temperate forest canopy with morning mist"`

#### `type` (string, required)
The type of asset.
- Allowed values: `"image"`, `"video"`, `"audio"`, `"dataset"`, `"archive"`
- Example: `"image"`

#### `category` (string, required)
Primary category for the asset.
- Examples: `"nature"`, `"technology"`, `"abstract"`, `"people"`

#### `version` (string, required)
Semantic version of the asset.
- Format: `MAJOR.MINOR.PATCH`
- Pattern: `^\d+\.\d+\.\d+$`
- Example: `"1.0.0"`

### Licensing

#### `license` (object, required)
License information for the asset.

##### `license.type` (string, required)
License identifier.
- Examples: `"CC-BY-4.0"`, `"CC0"`, `"MIT"`, `"Apache-2.0"`

##### `license.url` (string, required)
URL to the full license text.
- Format: Valid URI
- Example: `"https://creativecommons.org/licenses/by/4.0/"`

##### `license.attribution` (string, optional)
Required attribution text (if applicable).
- Example: `"Photo by John Doe Photography"`

### Creator Information

#### `creator` (object, required)
Information about the asset creator.

##### `creator.name` (string, required)
Name of the creator.
- Example: `"John Doe"`

##### `creator.email` (string, optional)
Contact email for the creator.
- Format: Valid email address
- Example: `"john@example.com"`

##### `creator.url` (string, optional)
Website or profile URL for the creator.
- Format: Valid URI
- Example: `"https://johndoe.com"`

### File Information

#### `formats` (array, required)
List of available file formats.
- Minimum items: 1

Each format object contains:

##### `format` (string, required)
File format/extension.
- Examples: `"jpg"`, `"png"`, `"mp4"`, `"csv"`

##### `filename` (string, required)
Name of the file.
- Example: `"forest-001.jpg"`

##### `mimetype` (string, required)
MIME type of the file.
- Example: `"image/jpeg"`

##### `size` (integer, required)
File size in bytes.
- Minimum: 1
- Example: `2458624`

##### `dimensions` (object, optional)
Dimensions for image/video assets.
- `width` (integer): Width in pixels
- `height` (integer): Height in pixels

##### `checksum` (object, optional)
File checksums for verification.
- `md5` (string): MD5 hash (32 characters)
- `sha256` (string): SHA-256 hash (64 characters)

## Optional Fields

### Temporal Information

#### `created` (string, optional)
When the asset was originally created.
- Format: ISO 8601 datetime
- Example: `"2024-01-15T08:30:00Z"`

#### `added` (string, optional)
When the asset was added to the library.
- Format: ISO 8601 datetime
- Example: `"2024-01-20T14:22:00Z"`

#### `modified` (string, optional)
When the asset metadata was last modified.
- Format: ISO 8601 datetime
- Example: `"2024-01-20T14:22:00Z"`

### Categorization

#### `subcategory` (string, optional)
More specific categorization.
- Example: `"forest"` (under category `"nature"`)

#### `tags` (array, optional)
List of descriptive tags.
- Minimum items: 1 (if provided)
- Example: `["forest", "nature", "trees", "mist", "dawn"]`

### Technical Details

#### `processing` (object, optional)
Information about format conversions and processing.

##### `processing.source_format` (string)
Original format of the asset.
- Example: `"jpg"`

##### `processing.conversions` (array)
List of format conversions performed.

Each conversion contains:
- `to` (string): Target format
- `tool` (string): Tool used for conversion
- `version` (string): Tool version
- `parameters` (string): Command parameters used

#### `technical` (object, optional)
Technical metadata specific to asset type.

For images:
- `camera` (string): Camera model
- `lens` (string): Lens information
- `settings` (object): Camera settings
  - `aperture` (string)
  - `shutter_speed` (string)
  - `iso` (integer)
  - `focal_length` (string)
- `location` (object): Geographic information
  - `latitude` (number)
  - `longitude` (number)
  - `altitude` (number)
  - `place` (string)

For videos:
- `duration` (number): Duration in seconds
- `framerate` (number): Frames per second
- `bitrate` (integer): Bitrate in bps
- `codec` (string): Video codec used

For audio:
- `duration` (number): Duration in seconds
- `sample_rate` (integer): Sample rate in Hz
- `bit_depth` (integer): Bit depth
- `channels` (integer): Number of channels

For datasets:
- `records` (integer): Number of records
- `columns` (integer): Number of columns
- `schema` (object): Data schema information

## Complete Example

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
    },
    {
      "format": "webp",
      "filename": "forest-001.webp",
      "mimetype": "image/webp",
      "size": 1843968,
      "dimensions": {
        "width": 4000,
        "height": 3000
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

## Validation

Metadata files are validated using:
1. JSON Schema validation for structure
2. Content validation for specific requirements
3. Cross-validation with actual files

Use the validation script to check metadata:
```bash
python scripts/validate-assets.py --path assets/images/nature/forest-001
```

## Best Practices

1. **Be descriptive**: Provide detailed titles and descriptions
2. **Use consistent tags**: Maintain a consistent tagging taxonomy
3. **Include technical details**: Add camera settings, processing info, etc.
4. **Specify all formats**: List all available file variants
5. **Keep metadata updated**: Update version and modified date when changing assets
6. **Provide attribution**: Always include proper attribution for CC-BY licenses
7. **Add checksums**: Include checksums for file integrity verification

## Schema Evolution

The schema may evolve over time. Changes follow these principles:
- **Backward compatibility**: Existing valid metadata remains valid
- **Semantic versioning**: Schema version follows semver
- **Deprecation notices**: Fields are deprecated before removal
- **Migration tools**: Scripts provided for schema updates
