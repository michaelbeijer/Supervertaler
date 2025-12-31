"""
Deprecated Superdocs module.

The in-app Superdocs generator and viewer have been removed from the application
and the official documentation is hosted on GitBook:

    https://supervertaler.gitbook.io/superdocs/

This module remains as a stub to avoid accidental imports. Importing or
instantiating will raise ImportError.
"""

def __getattr__(name):
    raise ImportError(
        "The 'modules.superdocs' module has been removed. Use the online Superdocs at"
        " https://supervertaler.gitbook.io/superdocs/"
    )

                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    # Top-level functions only
                    info['functions'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "No docstring",
                        'line': node.lineno
                    })

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        info['imports'].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        info['imports'].append(node.module)

            self.module_info['Supervertaler'] = info
            print(f"    [OK] Found {len(info['classes'])} classes, {len(info['functions'])} functions")

        except Exception as e:
            print(f"    [WARN] Error scanning {self.main_file.name}: {e}")

    def _scan_modules(self):
        """Scan all modules in modules/ directory"""
        if not self.modules_dir.exists():
            print("  [WARN] Modules directory not found")
            return

        module_files = list(self.modules_dir.glob("*.py"))
        print(f"  [*] Found {len(module_files)} module files")

        for module_file in module_files:
            if module_file.name.startswith('__'):
                continue

            module_name = module_file.stem
            print(f"    [FILE] Scanning {module_name}...")

            try:
                with open(module_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                info = {
                    'path': module_file,
                    'classes': [],
                    'functions': [],
                    'imports': [],
                    'docstring': ast.get_docstring(tree) or "No module docstring",
                    'line_count': len(content.splitlines())
                }

                # Extract structure (same as main file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_info = {
                            'name': node.name,
                            'docstring': ast.get_docstring(node) or "No docstring",
                            'methods': [],
                            'line': node.lineno
                        }

                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                class_info['methods'].append({
                                    'name': item.name,
                                    'docstring': ast.get_docstring(item) or "No docstring",
                                    'line': item.lineno
                                })

                        info['classes'].append(class_info)

                    elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                        info['functions'].append({
                            'name': node.name,
                            'docstring': ast.get_docstring(node) or "No docstring",
                            'line': node.lineno
                        })

                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            info['imports'].append(alias.name)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            info['imports'].append(node.module)

                self.module_info[module_name] = info

            except Exception as e:
                print(f"      [WARN] Error: {e}")

    def _generate_index(self):
        """Generate index.md with overview and TOC"""
        output_file = self.output_dir / "index.md"

        content = f"""# Supervertaler Documentation

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generator:** Superdocs - Automated Documentation System

---

## 📊 Codebase Overview

"""

        # Statistics
        total_lines = sum(info['line_count'] for info in self.module_info.values())
        total_classes = sum(len(info['classes']) for info in self.module_info.values())
        total_functions = sum(len(info['functions']) for info in self.module_info.values())
        total_modules = len(self.module_info)

        content += f"""
| Metric | Count |
|--------|-------|
| **Total Modules** | {total_modules} |
| **Total Lines** | {total_lines:,} |
| **Total Classes** | {total_classes} |
| **Total Functions** | {total_functions} |

---

## 📚 Documentation Sections

- [Architecture Overview](architecture.md) - System design and module relationships
- [Module Reference](modules/) - Detailed documentation for each module
- [Dependencies](dependencies.md) - Module dependency graph

---

## 📁 Module Index

"""

        # List all modules
        for module_name, info in sorted(self.module_info.items()):
            if module_name == 'Supervertaler':
                content += f"### 🏠 {module_name}.py (Main Application)\n\n"
            else:
                content += f"### 📦 {module_name}\n\n"

            # First line of docstring
            docstring_first_line = info['docstring'].split('\n')[0] if info['docstring'] else "No description"
            content += f"{docstring_first_line}\n\n"

            content += f"- **Lines:** {info['line_count']:,}\n"
            content += f"- **Classes:** {len(info['classes'])}\n"
            content += f"- **Functions:** {len(info['functions'])}\n"

            if module_name != 'Supervertaler':
                content += f"- [View Details](modules/{module_name}.md)\n"

            content += "\n"

        content += """
---

## 🔄 Keeping Documentation Updated

This documentation is automatically generated by Superdocs. To regenerate:

```python
from modules.superdocs import Superdocs

docs = Superdocs()
docs.generate_all()
```

Or from command line:

```bash
python -c "from modules.superdocs import Superdocs; Superdocs().generate_all()"
```
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Generated {output_file.name}")

    def _generate_architecture(self):
        """Generate architecture.md with system overview"""
        output_file = self.output_dir / "architecture.md"

        content = f"""# Supervertaler Architecture

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## System Overview

Supervertaler is a PyQt6-based desktop application for AI-powered translation with CAT tool integration.

### Core Components

"""

        # Categorize modules
        ui_modules = []
        feature_modules = []
        utility_modules = []

        for module_name, info in self.module_info.items():
            if module_name == 'Supervertaler':
                continue

            name_lower = module_name.lower()
            if 'ui' in name_lower or 'qt' in name_lower or 'dialog' in name_lower:
                ui_modules.append(module_name)
            elif any(word in name_lower for word in ['super', 'llm', 'tm', 'termbase']):
                feature_modules.append(module_name)
            else:
                utility_modules.append(module_name)

        content += "#### 🎨 UI Components\n\n"
        for mod in sorted(ui_modules):
            content += f"- `{mod}` - {self.module_info[mod]['docstring'].split('.')[0]}\n"

        content += "\n#### 🚀 Feature Modules\n\n"
        for mod in sorted(feature_modules):
            content += f"- `{mod}` - {self.module_info[mod]['docstring'].split('.')[0]}\n"

        content += "\n#### 🔧 Utilities\n\n"
        for mod in sorted(utility_modules):
            content += f"- `{mod}` - {self.module_info[mod]['docstring'].split('.')[0]}\n"

        content += """

---

## 🏗️ Application Structure

```
Supervertaler.py (Main Application)
    └── SupervertalerQt (QMainWindow)
        ├── UI Tabs
        │   ├── Grid View (Segment Editor)
        │   ├── Document View (Preview)
        │   ├── List View (Compact)
        │   ├── TM Browser
        │   ├── Termbases
        │   └── Settings
        │
        ├── Feature Integration
        │   ├── AI Translation (LLM Clients)
        │   ├── Translation Memory
        │   ├── Termbase Management
        │   ├── Voice Dictation (Supervoice)
        │   └── Benchmarking (Superbench)
        │
        └── File Operations
            ├── DOCX Import/Export
            ├── TMX Import/Export
            ├── Bilingual Tables
            └── Project Management
```

---

## 📦 Module Categories

"""

        # Generate module statistics by category
        categories = {
            'UI Components': ui_modules,
            'Feature Modules': feature_modules,
            'Utilities': utility_modules
        }

        for category, modules in categories.items():
            total_classes = sum(len(self.module_info[m]['classes']) for m in modules)
            total_functions = sum(len(self.module_info[m]['functions']) for m in modules)
            total_lines = sum(self.module_info[m]['line_count'] for m in modules)

            content += f"### {category}\n\n"
            content += f"- Modules: {len(modules)}\n"
            content += f"- Classes: {total_classes}\n"
            content += f"- Functions: {total_functions}\n"
            content += f"- Lines: {total_lines:,}\n\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Generated {output_file.name}")

    def _generate_module_docs(self):
        """Generate detailed documentation for each module"""
        modules_output = self.output_dir / "modules"

        for module_name, info in self.module_info.items():
            if module_name == 'Supervertaler':
                continue  # Skip main file for now

            output_file = modules_output / f"{module_name}.md"

            content = f"""# {module_name}

**File:** `modules/{module_name}.py`
**Lines:** {info['line_count']:,}
**Classes:** {len(info['classes'])}
**Functions:** {len(info['functions'])}

---

## Module Description

{info['docstring']}

---

"""

            # Document classes
            if info['classes']:
                content += "## Classes\n\n"

                for cls in info['classes']:
                    content += f"### `{cls['name']}`\n\n"
                    content += f"**Line:** {cls['line']}\n\n"
                    content += f"{cls['docstring']}\n\n"

                    if cls['methods']:
                        content += "#### Methods\n\n"
                        for method in cls['methods']:
                            # Skip private methods in documentation
                            if not method['name'].startswith('_'):
                                content += f"##### `{method['name']}()`\n\n"
                                content += f"{method['docstring']}\n\n"
                        content += "\n"

                    content += "---\n\n"

            # Document functions
            if info['functions']:
                content += "## Functions\n\n"

                for func in info['functions']:
                    if not func['name'].startswith('_'):  # Skip private functions
                        content += f"### `{func['name']}()`\n\n"
                        content += f"**Line:** {func['line']}\n\n"
                        content += f"{func['docstring']}\n\n"
                        content += "---\n\n"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

        print(f"  [OK] Generated {len(self.module_info) - 1} module documentation files")

    def _generate_dependencies(self):
        """Generate dependencies.md showing module relationships"""
        output_file = self.output_dir / "dependencies.md"

        content = f"""# Module Dependencies

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Import Analysis

This shows which modules import other modules from the Supervertaler codebase.

"""

        # Build dependency map
        for module_name, info in self.module_info.items():
            internal_imports = []

            for imp in info['imports']:
                # Check if it's an internal module
                if imp.startswith('modules.'):
                    mod_name = imp.replace('modules.', '')
                    if mod_name in self.module_info:
                        internal_imports.append(mod_name)

            if internal_imports:
                content += f"### {module_name}\n\n"
                content += "**Imports:**\n\n"
                for imp in sorted(internal_imports):
                    content += f"- `{imp}`\n"
                content += "\n"

        content += """
---

## Dependency Graph (Mermaid)

```mermaid
graph TD
    Supervertaler[Supervertaler.py]
"""

        # Simple mermaid diagram
        for module_name, info in self.module_info.items():
            if module_name == 'Supervertaler':
                continue

            for imp in info['imports']:
                if imp.startswith('modules.'):
                    mod_name = imp.replace('modules.', '')
                    if mod_name in self.module_info and mod_name != module_name:
                        content += f"    {module_name} --> {mod_name}\n"

        content += "```\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Generated {output_file.name}")


def main():
    """Command-line interface for Superdocs"""
    docs = Superdocs()
    docs.generate_all()


if __name__ == "__main__":
    main()
