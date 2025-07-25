#!/usr/bin/env python3
"""
Build catalog JSON files from asset metadata.

This script scans the assets directory and generates consolidated
catalog files for easy access and querying.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import click
from tqdm import tqdm
import humanize


class CatalogBuilder:
    """Build and manage the asset catalog."""
    
    def __init__(self, assets_dir: str = 'assets', catalog_dir: str = 'catalog'):
        self.assets_dir = Path(assets_dir)
        self.catalog_dir = Path(catalog_dir)
        self.catalog_dir.mkdir(exist_ok=True)
        
    def scan_assets(self) -> List[Dict[str, Any]]:
        """Scan the assets directory and collect all metadata."""
        assets = []
        
        # Find all metadata.json files
        metadata_files = list(self.assets_dir.rglob('metadata.json'))
        
        click.echo(f"Found {len(metadata_files)} assets to process...")
        
        for metadata_file in tqdm(metadata_files, desc="Scanning assets"):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Add computed fields
                asset_path = metadata_file.parent
                relative_path = asset_path.relative_to(self.assets_dir)
                
                metadata['_path'] = str(relative_path)
                metadata['_url_base'] = f"/assets/{relative_path}"
                
                # Calculate total size from all formats
                total_size = sum(
                    fmt.get('size', 0) 
                    for fmt in metadata.get('formats', [])
                )
                metadata['_total_size'] = total_size
                metadata['_total_size_human'] = humanize.naturalsize(total_size)
                
                # Add last modified time
                metadata['_last_modified'] = datetime.fromtimestamp(
                    metadata_file.stat().st_mtime
                ).isoformat() + 'Z'
                
                assets.append(metadata)
                
            except Exception as e:
                click.echo(f"\nError processing {metadata_file}: {e}", err=True)
                continue
                
        return assets
    
    def build_main_catalog(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build the main catalog with all assets."""
        total_size = sum(asset.get('_total_size', 0) for asset in assets)
        
        catalog = {
            'generated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'version': '1.0.0',
            'total_assets': len(assets),
            'total_size': total_size,
            'total_size_human': humanize.naturalsize(total_size),
            'stats': self._calculate_stats(assets),
            'assets': sorted(assets, key=lambda x: x.get('id', ''))
        }
        
        return catalog
    
    def build_type_catalogs(self, assets: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Build separate catalogs for each asset type."""
        type_catalogs = {}
        asset_types = ['image', 'video', 'audio', 'dataset', 'archive']
        
        for asset_type in asset_types:
            # Filter assets by type
            type_assets = [
                asset for asset in assets 
                if asset.get('type') == asset_type
            ]
            
            if type_assets:
                total_size = sum(asset.get('_total_size', 0) for asset in type_assets)
                
                type_catalogs[asset_type] = {
                    'generated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    'version': '1.0.0',
                    'type': asset_type,
                    'total_assets': len(type_assets),
                    'total_size': total_size,
                    'total_size_human': humanize.naturalsize(total_size),
                    'stats': self._calculate_stats(type_assets),
                    'assets': sorted(type_assets, key=lambda x: x.get('id', ''))
                }
        
        return type_catalogs
    
    def _calculate_stats(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for a set of assets."""
        stats = {
            'by_category': {},
            'by_license': {},
            'by_creator': {},
            'formats_available': set(),
            'tags': {}
        }
        
        for asset in assets:
            # Count by category
            category = asset.get('category', 'uncategorized')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Count by license
            license_type = asset.get('license', {}).get('type', 'unknown')
            stats['by_license'][license_type] = stats['by_license'].get(license_type, 0) + 1
            
            # Count by creator
            creator_name = asset.get('creator', {}).get('name', 'unknown')
            stats['by_creator'][creator_name] = stats['by_creator'].get(creator_name, 0) + 1
            
            # Collect formats
            for fmt in asset.get('formats', []):
                stats['formats_available'].add(fmt.get('format'))
            
            # Count tags
            for tag in asset.get('tags', []):
                stats['tags'][tag] = stats['tags'].get(tag, 0) + 1
        
        # Convert set to list for JSON serialization
        stats['formats_available'] = sorted(list(stats['formats_available']))
        
        # Sort tags by frequency
        stats['tags'] = dict(
            sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)[:20]
        )
        
        return stats
    
    def write_catalogs(self, main_catalog: Dict[str, Any], 
                      type_catalogs: Dict[str, Dict[str, Any]]) -> None:
        """Write catalog files to disk."""
        # Write main catalog
        main_path = self.catalog_dir / 'assets.json'
        with open(main_path, 'w', encoding='utf-8') as f:
            json.dump(main_catalog, f, indent=2, ensure_ascii=False)
        click.echo(f"✓ Wrote main catalog to {main_path}")
        
        # Write type-specific catalogs
        for asset_type, catalog in type_catalogs.items():
            # Use plural form for filename
            filename = f"{asset_type}s.json"
            type_path = self.catalog_dir / filename
            
            with open(type_path, 'w', encoding='utf-8') as f:
                json.dump(catalog, f, indent=2, ensure_ascii=False)
            click.echo(f"✓ Wrote {asset_type} catalog to {type_path}")
        
        # Write a compact index for quick lookups
        index = {
            'generated': main_catalog['generated'],
            'total_assets': main_catalog['total_assets'],
            'assets': [
                {
                    'id': asset.get('id'),
                    'type': asset.get('type'),
                    'title': asset.get('title'),
                    'category': asset.get('category'),
                    'path': asset.get('_path'),
                    'url': asset.get('_url_base')
                }
                for asset in main_catalog['assets']
            ]
        }
        
        index_path = self.catalog_dir / 'index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        click.echo(f"✓ Wrote index to {index_path}")
    
    def build(self) -> None:
        """Build all catalog files."""
        click.echo("Building Universal Asset Library catalog...")
        
        # Scan assets
        assets = self.scan_assets()
        
        if not assets:
            click.echo("No assets found. Catalog will be empty.", err=True)
            return
        
        # Build catalogs
        main_catalog = self.build_main_catalog(assets)
        type_catalogs = self.build_type_catalogs(assets)
        
        # Write to disk
        self.write_catalogs(main_catalog, type_catalogs)
        
        # Print summary
        click.echo("\n" + "="*50)
        click.echo("Catalog Build Summary:")
        click.echo(f"  Total assets: {main_catalog['total_assets']}")
        click.echo(f"  Total size: {main_catalog['total_size_human']}")
        click.echo(f"  Categories: {len(main_catalog['stats']['by_category'])}")
        click.echo(f"  Formats: {', '.join(main_catalog['stats']['formats_available'])}")
        click.echo("="*50)


@click.command()
@click.option('--assets-dir', default='assets', help='Path to assets directory')
@click.option('--catalog-dir', default='catalog', help='Path to catalog output directory')
@click.option('--pretty', is_flag=True, help='Pretty print JSON output')
def main(assets_dir: str, catalog_dir: str, pretty: bool):
    """Build catalog JSON files from asset metadata."""
    builder = CatalogBuilder(assets_dir, catalog_dir)
    builder.build()


if __name__ == '__main__':
    main()
