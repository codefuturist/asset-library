#!/usr/bin/env python3
"""
Validate asset structure and metadata.

This script checks that assets follow the required structure,
have valid metadata, and meet quality standards.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import click
from jsonschema import validate, ValidationError
import magic
from PIL import Image
import hashlib
from tqdm import tqdm


class AssetValidator:
    """Validate assets against defined standards."""
    
    # Metadata schema for validation
    METADATA_SCHEMA = {
        "type": "object",
        "required": ["id", "title", "description", "category", "type", "version", "license", "creator", "formats"],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "title": {"type": "string", "minLength": 3},
            "description": {"type": "string", "minLength": 10},
            "category": {"type": "string"},
            "subcategory": {"type": "string"},
            "type": {"type": "string", "enum": ["image", "video", "audio", "dataset", "archive"]},
            "created": {"type": "string", "format": "date-time"},
            "added": {"type": "string", "format": "date-time"},
            "modified": {"type": "string", "format": "date-time"},
            "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
            "license": {
                "type": "object",
                "required": ["type", "url"],
                "properties": {
                    "type": {"type": "string"},
                    "url": {"type": "string", "format": "uri"},
                    "attribution": {"type": "string"}
                }
            },
            "creator": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "url": {"type": "string", "format": "uri"}
                }
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "formats": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["format", "filename", "mimetype", "size"],
                    "properties": {
                        "format": {"type": "string"},
                        "filename": {"type": "string"},
                        "mimetype": {"type": "string"},
                        "size": {"type": "integer", "minimum": 1},
                        "dimensions": {
                            "type": "object",
                            "properties": {
                                "width": {"type": "integer", "minimum": 1},
                                "height": {"type": "integer", "minimum": 1}
                            }
                        },
                        "checksum": {
                            "type": "object",
                            "properties": {
                                "md5": {"type": "string", "pattern": "^[a-f0-9]{32}$"},
                                "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Minimum quality requirements
    MIN_IMAGE_WIDTH = 1920
    MIN_IMAGE_HEIGHT = 1080
    MIN_VIDEO_WIDTH = 1280
    MIN_VIDEO_HEIGHT = 720
    ACCEPTABLE_LICENSES = [
        "CC0", "CC-BY", "CC-BY-SA", "CC-BY-4.0", "CC-BY-SA-4.0",
        "MIT", "Apache-2.0", "Public Domain"
    ]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_magic = magic.Magic(mime=True)
    
    def validate_asset(self, asset_path: Path) -> Tuple[bool, List[str], List[str]]:
        """Validate a single asset directory."""
        self.errors = []
        self.warnings = []
        
        # Check directory structure
        self._validate_directory_structure(asset_path)
        
        # Validate metadata
        metadata_file = asset_path / 'metadata.json'
        if metadata_file.exists():
            metadata = self._validate_metadata(metadata_file)
            
            if metadata:
                # Validate files match metadata
                self._validate_files(asset_path, metadata)
                
                # Validate checksums if present
                checksum_file = asset_path / 'checksums.txt'
                if checksum_file.exists():
                    self._validate_checksums(asset_path, checksum_file)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_directory_structure(self, asset_path: Path) -> None:
        """Validate the asset directory structure."""
        if not asset_path.is_dir():
            self.errors.append(f"Asset path is not a directory: {asset_path}")
            return
        
        # Check for required files
        metadata_file = asset_path / 'metadata.json'
        if not metadata_file.exists():
            self.errors.append("Missing required metadata.json file")
        
        # Check for at least one asset file
        asset_files = [f for f in asset_path.iterdir() 
                      if f.is_file() and f.name not in ['metadata.json', 'checksums.txt']]
        
        if not asset_files:
            self.errors.append("No asset files found in directory")
    
    def _validate_metadata(self, metadata_file: Path) -> Dict[str, Any]:
        """Validate metadata JSON schema and content."""
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in metadata.json: {e}")
            return None
        
        # Validate schema
        try:
            validate(instance=metadata, schema=self.METADATA_SCHEMA)
        except ValidationError as e:
            self.errors.append(f"Metadata schema validation failed: {e.message}")
            return None
        
        # Additional content validation
        self._validate_metadata_content(metadata)
        
        return metadata
    
    def _validate_metadata_content(self, metadata: Dict[str, Any]) -> None:
        """Validate metadata content beyond schema."""
        # Check license
        license_type = metadata.get('license', {}).get('type', '')
        if license_type not in self.ACCEPTABLE_LICENSES:
            self.warnings.append(
                f"License type '{license_type}' not in standard list. "
                "Please verify it's an acceptable open license."
            )
        
        # Check ID matches directory name
        # This is just a warning as it's not strictly required
        
        # Validate tags
        tags = metadata.get('tags', [])
        if len(tags) < 3:
            self.warnings.append("Consider adding more descriptive tags (minimum 3 recommended)")
        
        # Check for required attribution
        if license_type in ['CC-BY', 'CC-BY-SA', 'CC-BY-4.0', 'CC-BY-SA-4.0']:
            if not metadata.get('license', {}).get('attribution'):
                self.errors.append(f"License {license_type} requires attribution field")
    
    def _validate_files(self, asset_path: Path, metadata: Dict[str, Any]) -> None:
        """Validate that files match metadata and meet quality standards."""
        formats_in_metadata = {fmt['filename']: fmt for fmt in metadata.get('formats', [])}
        
        # Check each file mentioned in metadata exists
        for filename, format_info in formats_in_metadata.items():
            file_path = asset_path / filename
            
            if not file_path.exists():
                self.errors.append(f"File listed in metadata not found: {filename}")
                continue
            
            # Validate file type and size
            self._validate_file(file_path, format_info, metadata.get('type'))
        
        # Check for files not in metadata
        for file_path in asset_path.iterdir():
            if file_path.is_file() and file_path.name not in ['metadata.json', 'checksums.txt']:
                if file_path.name not in formats_in_metadata:
                    self.warnings.append(f"File not listed in metadata: {file_path.name}")
    
    def _validate_file(self, file_path: Path, format_info: Dict[str, Any], asset_type: str) -> None:
        """Validate individual file properties."""
        # Check file size matches
        actual_size = file_path.stat().st_size
        stated_size = format_info.get('size', 0)
        
        if actual_size != stated_size:
            self.errors.append(
                f"File size mismatch for {file_path.name}: "
                f"actual={actual_size}, metadata={stated_size}"
            )
        
        # Check MIME type
        try:
            actual_mime = self.file_magic.from_file(str(file_path))
            stated_mime = format_info.get('mimetype')
            
            if actual_mime != stated_mime:
                self.warnings.append(
                    f"MIME type mismatch for {file_path.name}: "
                    f"actual={actual_mime}, metadata={stated_mime}"
                )
        except Exception as e:
            self.warnings.append(f"Could not determine MIME type for {file_path.name}: {e}")
        
        # Type-specific validation
        if asset_type == 'image':
            self._validate_image(file_path, format_info)
    
    def _validate_image(self, file_path: Path, format_info: Dict[str, Any]) -> None:
        """Validate image-specific requirements."""
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Check dimensions match metadata
                stated_dims = format_info.get('dimensions', {})
                if stated_dims:
                    if width != stated_dims.get('width') or height != stated_dims.get('height'):
                        self.errors.append(
                            f"Image dimensions mismatch for {file_path.name}: "
                            f"actual={width}x{height}, "
                            f"metadata={stated_dims.get('width')}x{stated_dims.get('height')}"
                        )
                
                # Check minimum resolution
                if width < self.MIN_IMAGE_WIDTH or height < self.MIN_IMAGE_HEIGHT:
                    self.warnings.append(
                        f"Image {file_path.name} below recommended minimum resolution "
                        f"({self.MIN_IMAGE_WIDTH}x{self.MIN_IMAGE_HEIGHT}): {width}x{height}"
                    )
                
        except Exception as e:
            self.errors.append(f"Could not validate image {file_path.name}: {e}")
    
    def _validate_checksums(self, asset_path: Path, checksum_file: Path) -> None:
        """Validate file checksums."""
        try:
            with open(checksum_file, 'r') as f:
                checksum_content = f.read()
            
            # Parse checksums (supports both MD5 and SHA256 formats)
            for line in checksum_content.strip().split('\n'):
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) == 2:
                    checksum, filename = parts
                    file_path = asset_path / filename
                    
                    if file_path.exists():
                        # Determine checksum type by length
                        if len(checksum) == 32:
                            actual = self._calculate_md5(file_path)
                        elif len(checksum) == 64:
                            actual = self._calculate_sha256(file_path)
                        else:
                            self.warnings.append(f"Unknown checksum format for {filename}")
                            continue
                        
                        if actual != checksum:
                            self.errors.append(
                                f"Checksum mismatch for {filename}: "
                                f"expected={checksum}, actual={actual}"
                            )
                    
        except Exception as e:
            self.warnings.append(f"Could not validate checksums: {e}")
    
    def _calculate_md5(self, file_path: Path) -> str:
        """Calculate MD5 checksum of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()


@click.command()
@click.option('--path', required=True, help='Path to asset or assets directory to validate')
@click.option('--recursive', is_flag=True, help='Recursively validate all assets in directory')
@click.option('--fix', is_flag=True, help='Attempt to fix common issues')
@click.option('--strict', is_flag=True, help='Treat warnings as errors')
def main(path: str, recursive: bool, fix: bool, strict: bool):
    """Validate asset structure and metadata."""
    validator = AssetValidator()
    path_obj = Path(path)
    
    if not path_obj.exists():
        click.echo(f"Error: Path does not exist: {path}", err=True)
        return 1
    
    # Collect assets to validate
    assets_to_validate = []
    
    if recursive and path_obj.is_dir():
        # Find all directories containing metadata.json
        for metadata_file in path_obj.rglob('metadata.json'):
            assets_to_validate.append(metadata_file.parent)
    else:
        assets_to_validate.append(path_obj)
    
    # Validate each asset
    total_errors = 0
    total_warnings = 0
    
    for asset_path in tqdm(assets_to_validate, desc="Validating assets"):
        valid, errors, warnings = validator.validate_asset(asset_path)
        
        if errors or warnings:
            click.echo(f"\n{asset_path}:")
            
            for error in errors:
                click.echo(f"  ❌ ERROR: {error}", err=True)
                total_errors += 1
            
            for warning in warnings:
                click.echo(f"  ⚠️  WARNING: {warning}")
                total_warnings += 1
                
                if strict:
                    total_errors += 1
    
    # Summary
    click.echo("\n" + "="*50)
    click.echo("Validation Summary:")
    click.echo(f"  Assets validated: {len(assets_to_validate)}")
    click.echo(f"  Errors: {total_errors}")
    click.echo(f"  Warnings: {total_warnings}")
    click.echo("="*50)
    
    return 1 if total_errors > 0 else 0


if __name__ == '__main__':
    exit(main())
