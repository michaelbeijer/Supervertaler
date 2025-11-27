"""
Migration Script: 4-Layer to Unified Prompt Library

Migrates from old structure:
    1_System_Prompts/
    2_Domain_Prompts/
    3_Project_Prompts/
    4_Style_Guides/

To new unified structure:
    Library/
        Style Guides/
        Domain Expertise/
        Project Prompts/
        Active Projects/

System Prompts are moved to settings storage (handled separately).
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


class PromptLibraryMigration:
    """Handles one-time migration from 4-layer to unified structure"""
    
    def __init__(self, prompt_library_dir: str, log_callback=None):
        """
        Args:
            prompt_library_dir: Path to user_data/Prompt_Library
            log_callback: Function for logging
        """
        self.prompt_library_dir = Path(prompt_library_dir)
        self.log = log_callback if log_callback else print
        
        # Old structure paths
        self.old_system_prompts = self.prompt_library_dir / "1_System_Prompts"
        self.old_domain_prompts = self.prompt_library_dir / "2_Domain_Prompts"
        self.old_project_prompts = self.prompt_library_dir / "3_Project_Prompts"
        self.old_style_guides = self.prompt_library_dir / "4_Style_Guides"
        
        # New unified library
        self.new_library = self.prompt_library_dir / "Library"
        
        # Migration flag
        self.migration_completed_file = self.prompt_library_dir / ".migration_completed"
    
    def needs_migration(self) -> bool:
        """Check if migration is needed"""
        # Already migrated?
        if self.migration_completed_file.exists():
            return False
        
        # Old structure exists?
        has_old_structure = (
            self.old_domain_prompts.exists() or
            self.old_project_prompts.exists() or
            self.old_style_guides.exists()
        )
        
        return has_old_structure
    
    def migrate(self) -> bool:
        """
        Perform migration from old to new structure.
        
        Steps:
        1. Create new Library/ structure
        2. Copy Domain Prompts → Library/Domain Expertise/
        3. Copy Project Prompts → Library/Project Prompts/
        4. Copy Style Guides → Library/Style Guides/
        5. Backup old folders with .old extension
        6. Mark migration as completed
        
        Note: System Prompts are NOT migrated here (moved to settings separately)
        
        Returns:
            True if successful
        """
        try:
            self.log("=" * 60)
            self.log("🔄 Starting Prompt Library Migration")
            self.log("=" * 60)
            
            # Create new library structure
            self.log("\n📁 Creating new unified library structure...")
            self.new_library.mkdir(parents=True, exist_ok=True)
            
            # Migrate each layer
            migrated_counts = {}
            
            # Layer 2: Domain Prompts → Domain Expertise
            if self.old_domain_prompts.exists():
                self.log("\n📚 Migrating Domain Prompts...")
                count = self._migrate_folder(
                    self.old_domain_prompts,
                    self.new_library / "Domain Expertise",
                    add_metadata={'folder': 'Domain Expertise'}
                )
                migrated_counts['domain'] = count
                self.log(f"   ✓ Migrated {count} domain prompts")
            
            # Layer 3: Project Prompts → Project Prompts
            if self.old_project_prompts.exists():
                self.log("\n📋 Migrating Project Prompts...")
                count = self._migrate_folder(
                    self.old_project_prompts,
                    self.new_library / "Project Prompts",
                    add_metadata={'folder': 'Project Prompts'}
                )
                migrated_counts['project'] = count
                self.log(f"   ✓ Migrated {count} project prompts")
            
            # Layer 4: Style Guides → Style Guides
            if self.old_style_guides.exists():
                self.log("\n🎨 Migrating Style Guides...")
                count = self._migrate_folder(
                    self.old_style_guides,
                    self.new_library / "Style Guides",
                    add_metadata={'folder': 'Style Guides'}
                )
                migrated_counts['style'] = count
                self.log(f"   ✓ Migrated {count} style guides")
            
            # Backup old folders
            self.log("\n💾 Creating backups of old folders...")
            self._backup_old_folders()
            
            # Create Active Projects folder for user
            active_projects = self.new_library / "Active Projects"
            active_projects.mkdir(exist_ok=True)
            self.log(f"   ✓ Created 'Active Projects' folder for user-created prompts")
            
            # Mark migration as completed
            self.migration_completed_file.write_text(
                f"Migration completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Migrated: {sum(migrated_counts.values())} prompts\n"
                f"Details: {migrated_counts}\n",
                encoding='utf-8'
            )
            
            # Summary
            total = sum(migrated_counts.values())
            self.log("\n" + "=" * 60)
            self.log(f"✅ Migration Complete! Migrated {total} prompts")
            self.log("=" * 60)
            self.log(f"\nDomain Expertise: {migrated_counts.get('domain', 0)} prompts")
            self.log(f"Project Prompts:  {migrated_counts.get('project', 0)} prompts")
            self.log(f"Style Guides:     {migrated_counts.get('style', 0)} prompts")
            self.log(f"\n📂 New location: {self.new_library}")
            self.log(f"💾 Backups: Old folders renamed with .old extension")
            self.log("\n⚠️  Note: System Prompts moved to Settings (not in Library)")
            
            return True
            
        except Exception as e:
            self.log(f"\n❌ Migration failed: {e}")
            import traceback
            self.log(traceback.format_exc())
            return False
    
    def _migrate_folder(self, source: Path, destination: Path, add_metadata: dict = None) -> int:
        """
        Migrate prompts from source to destination folder.
        
        Args:
            source: Source folder path
            destination: Destination folder path
            add_metadata: Additional metadata to add to YAML frontmatter
        
        Returns:
            Number of files migrated
        """
        count = 0
        
        if not source.exists():
            return count
        
        destination.mkdir(parents=True, exist_ok=True)
        
        for item in source.iterdir():
            # Skip hidden files, README, and format_examples
            if item.name.startswith('.') or item.name == 'README.md' or item.name == 'format_examples':
                continue
            
            # Handle subdirectories (recursive)
            if item.is_dir():
                sub_dest = destination / item.name
                count += self._migrate_folder(item, sub_dest, add_metadata)
                continue
            
            # Only process .svprompt, .md, .txt, .json files
            if item.suffix.lower() not in ['.svprompt', '.md', '.txt', '.json']:
                continue
            
            try:
                # Convert JSON to Markdown if needed
                if item.suffix.lower() == '.json':
                    count += self._migrate_json_prompt(item, destination, add_metadata)
                else:
                    # Copy and update metadata if needed (.svprompt, .md, .txt are all markdown-based)
                    count += self._migrate_markdown_prompt(item, destination, add_metadata)
                    
            except Exception as e:
                self.log(f"   ⚠ Failed to migrate {item.name}: {e}")
        
        return count
    
    def _migrate_markdown_prompt(self, source: Path, destination: Path, add_metadata: dict = None) -> int:
        """Migrate a Markdown prompt file, adding metadata if needed"""
        try:
            content = source.read_text(encoding='utf-8')
            
            # Parse existing frontmatter if present
            if content.startswith('---'):
                content = content[3:].lstrip('\n')
                
                if '---' in content:
                    frontmatter_str, prompt_content = content.split('---', 1)
                    prompt_content = prompt_content.lstrip('\n')
                else:
                    frontmatter_str = ""
                    prompt_content = content
            else:
                frontmatter_str = ""
                prompt_content = content
            
            # Parse existing metadata
            metadata = self._parse_simple_yaml(frontmatter_str) if frontmatter_str else {}
            
            # Add new metadata fields
            if add_metadata:
                metadata.update(add_metadata)
            
            # Ensure required fields
            if 'name' not in metadata:
                metadata['name'] = source.stem
            
            metadata.setdefault('favorite', False)
            metadata.setdefault('quick_run', False)
            metadata.setdefault('tags', [])
            
            if 'created' not in metadata:
                metadata['created'] = datetime.now().strftime("%Y-%m-%d")
            
            # Build new file with updated metadata
            new_content = self._build_markdown_with_frontmatter(metadata, prompt_content)
            
            # Write to destination
            dest_file = destination / source.name
            dest_file.write_text(new_content, encoding='utf-8')
            
            return 1
            
        except Exception as e:
            self.log(f"   ⚠ Error migrating {source.name}: {e}")
            return 0
    
    def _migrate_json_prompt(self, source: Path, destination: Path, add_metadata: dict = None) -> int:
        """Migrate a JSON prompt file, converting to Markdown"""
        try:
            import json
            
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract content (prefer translate_prompt)
            content = data.get('translate_prompt', data.get('content', ''))
            
            if not content:
                self.log(f"   ⚠ No content in {source.name}, skipping")
                return 0
            
            # Build metadata
            metadata = {
                'name': data.get('name', source.stem),
                'description': data.get('description', ''),
                'domain': data.get('domain', ''),
                'version': data.get('version', '1.0'),
                'task_type': data.get('task_type', 'Translation'),
                'favorite': False,
                'quick_run': False,
                'tags': [],
                'created': data.get('created', datetime.now().strftime("%Y-%m-%d"))
            }
            
            # Add migration-specific metadata
            if add_metadata:
                metadata.update(add_metadata)
            
            # Build Markdown content
            new_content = self._build_markdown_with_frontmatter(metadata, content)
            
            # Write as .md file
            dest_file = destination / f"{source.stem}.md"
            dest_file.write_text(new_content, encoding='utf-8')
            
            self.log(f"   ✓ Converted {source.name} → {dest_file.name}")
            return 1
            
        except Exception as e:
            self.log(f"   ⚠ Error converting {source.name}: {e}")
            return 0
    
    def _build_markdown_with_frontmatter(self, metadata: dict, content: str) -> str:
        """Build Markdown file content with YAML frontmatter"""
        lines = ['---']
        
        # Ordered fields
        field_order = [
            'name', 'description', 'domain', 'version', 'task_type',
            'favorite', 'quick_run', 'folder', 'tags', 'created', 'modified'
        ]
        
        for field in field_order:
            if field in metadata:
                value = metadata[field]
                
                if isinstance(value, bool):
                    lines.append(f'{field}: {str(value).lower()}')
                elif isinstance(value, list):
                    if value:  # Non-empty list
                        items = ', '.join([f'"{item}"' for item in value])
                        lines.append(f'{field}: [{items}]')
                    else:
                        lines.append(f'{field}: []')
                elif isinstance(value, str):
                    lines.append(f'{field}: "{value}"')
                else:
                    lines.append(f'{field}: {value}')
        
        lines.append('---')
        
        return '\n'.join(lines) + '\n\n' + content.strip()
    
    def _parse_simple_yaml(self, yaml_str: str) -> dict:
        """Simple YAML parser for frontmatter"""
        data = {}
        
        for line in yaml_str.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle arrays
            if value.startswith('[') and value.endswith(']'):
                array_str = value[1:-1]
                items = [item.strip().strip('"').strip("'") for item in array_str.split(',')]
                data[key] = [item for item in items if item]
                continue
            
            # Handle booleans
            if value.lower() in ['true', 'false']:
                data[key] = value.lower() == 'true'
                continue
            
            # Remove quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            data[key] = value
        
        return data
    
    def _backup_old_folders(self):
        """Rename old folders with .old extension"""
        folders_to_backup = [
            self.old_system_prompts,
            self.old_domain_prompts,
            self.old_project_prompts,
            self.old_style_guides
        ]
        
        for folder in folders_to_backup:
            if folder.exists():
                backup_path = folder.with_suffix('.old')
                
                # If backup already exists, remove it first
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                
                folder.rename(backup_path)
                self.log(f"   ✓ Backed up: {folder.name} → {backup_path.name}")
    
    def rollback(self):
        """Rollback migration (restore from .old backups)"""
        try:
            self.log("🔄 Rolling back migration...")
            
            # Remove new library
            if self.new_library.exists():
                shutil.rmtree(self.new_library)
                self.log("   ✓ Removed new library structure")
            
            # Restore from backups
            backup_folders = [
                (self.prompt_library_dir / "1_System_Prompts.old", self.old_system_prompts),
                (self.prompt_library_dir / "2_Domain_Prompts.old", self.old_domain_prompts),
                (self.prompt_library_dir / "3_Project_Prompts.old", self.old_project_prompts),
                (self.prompt_library_dir / "4_Style_Guides.old", self.old_style_guides)
            ]
            
            for backup, original in backup_folders:
                if backup.exists():
                    if original.exists():
                        shutil.rmtree(original)
                    backup.rename(original)
                    self.log(f"   ✓ Restored: {original.name}")
            
            # Remove migration flag
            if self.migration_completed_file.exists():
                self.migration_completed_file.unlink()
            
            self.log("✓ Rollback complete")
            return True
            
        except Exception as e:
            self.log(f"❌ Rollback failed: {e}")
            return False


def migrate_prompt_library(prompt_library_dir: str, log_callback=None) -> bool:
    """
    Convenience function to perform migration.
    
    Args:
        prompt_library_dir: Path to user_data/Prompt_Library
        log_callback: Function for logging
    
    Returns:
        True if migration successful or not needed
    """
    migrator = PromptLibraryMigration(prompt_library_dir, log_callback)
    
    if not migrator.needs_migration():
        if log_callback:
            log_callback("✓ Prompt library already migrated (or no old structure found)")
        return True
    
    return migrator.migrate()
