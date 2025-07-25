#!/usr/bin/env python3
"""
Migrate images from static-assets to asset-library with proper naming scheme
"""

import os
import shutil
import json
import hashlib
from datetime import datetime
from pathlib import Path
from PIL import Image
import mimetypes

# Source and destination paths
SOURCE_DIR = Path("../static-assets/assets")
DEST_DIR = Path("assets/images")

# Mapping of existing files to new asset structure
FILE_MAPPINGS = {
    "svg/Rey-IT-Solutions-Logo.svg": {
        "id": "rey-it-solutions-logo-001",
        "title": "Rey IT Solutions Logo",
        "description": "Official logo of Rey IT Solutions in SVG format",
        "category": "branding",
        "subcategory": "logos",
        "tags": ["logo", "branding", "rey-it-solutions", "vector", "svg"]
    },
    "svg/Rey-IT-Solutions-Logo-Background.svg": {
        "id": "rey-it-solutions-logo-002",
        "title": "Rey IT Solutions Logo with Background",
        "description": "Official logo of Rey IT Solutions with background in SVG format",
        "category": "branding",
        "subcategory": "logos",
        "tags": ["logo", "branding", "rey-it-solutions", "vector", "svg", "background"]
    },
    "png/technitium.png": {
        "id": "technitium-logo-001",
        "title": "Technitium Logo",
        "description": "Technitium DNS Server logo in PNG format",
        "category": "technology",
        "subcategory": "software",
        "tags": ["logo", "technitium", "dns", "software", "png"]
    },
    "jpg/Rey-IT-Solutions-Logo.jpg": {
        "id": "rey-it-solutions-logo-003",
        "title": "Rey IT Solutions Logo JPEG",
        "description": "Official logo of Rey IT Solutions in JPEG format",
        "category": "branding",
        "subcategory": "logos",
        "tags": ["logo", "branding", "rey-it-solutions", "jpeg"]
    }
}

def calculate_checksums(file_path):
    """Calculate MD5 and SHA256 checksums for a file"""
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    
    return {
        "md5": md5_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest()
    }

def get_image_dimensions(file_path):
    """Get image dimensions"""
    try:
        with Image.open(file_path) as img:
            return {"width": img.width, "height": img.height}
    except:
        # For SVG files, we can't easily get dimensions
        return None

def migrate_image(source_path, mapping):
    """Migrate a single image to the new structure"""
    source_file = SOURCE_DIR / source_path
    
    if not source_file.exists():
        print(f"Warning: Source file not found: {source_file}")
        return
    
    # Create destination directory structure
    asset_id = mapping["id"]
    category = mapping["category"]
    dest_asset_dir = DEST_DIR / category / asset_id
    dest_asset_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine file extension and new filename
    file_ext = source_file.suffix.lower()
    new_filename = f"{asset_id}{file_ext}"
    dest_file = dest_asset_dir / new_filename
    
    # Copy the file
    print(f"Copying {source_file} -> {dest_file}")
    shutil.copy2(source_file, dest_file)
    
    # Get file info
    file_stats = dest_file.stat()
    mime_type = mimetypes.guess_type(str(dest_file))[0] or "application/octet-stream"
    checksums = calculate_checksums(dest_file)
    dimensions = get_image_dimensions(dest_file)
    
    # Create metadata
    metadata = {
        "id": asset_id,
        "title": mapping["title"],
        "description": mapping["description"],
        "type": "image",
        "category": category,
        "subcategory": mapping.get("subcategory", ""),
        "version": "1.0.0",
        "created": datetime.now().isoformat() + "Z",
        "added": datetime.now().isoformat() + "Z",
        "modified": datetime.now().isoformat() + "Z",
        "license": {
            "type": "MIT",
            "url": "https://opensource.org/licenses/MIT",
            "attribution": "Colin Leong"
        },
        "creator": {
            "name": "Colin Leong",
            "email": "colin@example.com"
        },
        "tags": mapping["tags"],
        "formats": [
            {
                "format": file_ext.strip('.'),
                "filename": new_filename,
                "mimetype": mime_type,
                "size": file_stats.st_size,
                "checksum": checksums
            }
        ]
    }
    
    # Add dimensions if available
    if dimensions:
        metadata["formats"][0]["dimensions"] = dimensions
    
    # Write metadata.json
    metadata_file = dest_asset_dir / "metadata.json"
    print(f"Creating metadata: {metadata_file}")
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Successfully migrated: {asset_id}\n")

def main():
    """Main migration function"""
    print("Starting image migration from static-assets to asset-library")
    print("=" * 60)
    
    # Ensure destination directory exists
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Migrate each file
    for source_path, mapping in FILE_MAPPINGS.items():
        migrate_image(source_path, mapping)
    
    print("=" * 60)
    print("Migration complete!")
    print(f"\nNext steps:")
    print(f"1. Review the migrated files in {DEST_DIR}")
    print(f"2. Update license information in metadata.json files if needed")
    print(f"3. Add the files to git: git add {DEST_DIR}")
    print(f"4. Commit the changes: git commit -m 'Add migrated image assets'")

if __name__ == "__main__":
    main()
