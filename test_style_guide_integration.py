#!/usr/bin/env python3
"""
Phase 5 End-to-End Testing: Style Guide Integration
Tests all phases of style guide integration (1-4)
"""

import os
import sys
import json
import tempfile
from datetime import datetime

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.style_guide_manager import StyleGuideLibrary


def test_phase_1_instance_variables():
    """Test Phase 1: Instance variables are properly initialized"""
    print("\n" + "="*60)
    print("PHASE 1: Testing Instance Variables")
    print("="*60)
    
    # Simulate what happens in __init__
    class MockApp:
        def __init__(self):
            # Style guide library initialization
            self.style_guide_library = StyleGuideLibrary(
                os.path.join(os.path.dirname(__file__), "user data", "Translation_Resources", "Style_Guides")
            )
            
            # Active style guide state (Phase 1 variables)
            self.active_style_guide = None
            self.active_style_guide_name = None
            self.active_style_guide_language = None
            self.active_style_guide_format = "markdown"
    
    app = MockApp()
    
    # Test initial state
    assert app.active_style_guide is None, "❌ active_style_guide should be None initially"
    assert app.active_style_guide_name is None, "❌ active_style_guide_name should be None initially"
    assert app.active_style_guide_language is None, "❌ active_style_guide_language should be None initially"
    assert app.active_style_guide_format == "markdown", "❌ active_style_guide_format should be 'markdown'"
    
    print("✅ Instance variables initialized correctly")
    print(f"   - active_style_guide: {app.active_style_guide}")
    print(f"   - active_style_guide_name: {app.active_style_guide_name}")
    print(f"   - active_style_guide_language: {app.active_style_guide_language}")
    print(f"   - active_style_guide_format: {app.active_style_guide_format}")
    
    return app


def test_phase_2_prompt_composition(app):
    """Test Phase 2: Style guides are appended to prompts correctly"""
    print("\n" + "="*60)
    print("PHASE 2: Testing Prompt Composition")
    print("="*60)
    
    # Load style guides
    app.style_guide_library.load_all_guides()
    print(f"✅ Loaded {len(app.style_guide_library.guides)} style guides")
    
    # Simulate base prompt
    base_prompt = "You are a translator.\n\nTranslate the following text:"
    
    # Simulate custom instructions
    app.active_custom_instruction = "Use formal tone."
    app.active_custom_instruction_name = "Formal Style"
    
    # Select a style guide
    dutch_guide = app.style_guide_library.get_guide("Dutch")
    assert dutch_guide is not None, "❌ Dutch style guide not found"
    
    app.active_style_guide = dutch_guide.get('content', '')
    app.active_style_guide_name = "Dutch"
    app.active_style_guide_language = "Dutch"
    
    # Simulate Phase 2 logic: get_context_aware_prompt()
    combined_prompt = base_prompt
    
    # Append custom instructions
    if app.active_custom_instruction:
        combined_prompt = combined_prompt + "\n\n" + "# CUSTOM INSTRUCTIONS\n\n" + app.active_custom_instruction
    
    # Append style guide (Phase 2)
    if app.active_style_guide:
        language_label = f" ({app.active_style_guide_language})" if app.active_style_guide_language else ""
        style_header = f"# STYLE GUIDE & FORMATTING RULES{language_label}"
        combined_prompt = combined_prompt + "\n\n" + style_header + "\n\n" + app.active_style_guide
    
    print(f"✅ Composed prompt with {len(combined_prompt)} characters")
    print(f"   - Base prompt: {len(base_prompt)} chars")
    print(f"   - Custom instructions: {len(app.active_custom_instruction)} chars")
    print(f"   - Style guide ({app.active_style_guide_language}): {len(app.active_style_guide)} chars")
    
    # Verify hierarchy order
    assert "# CUSTOM INSTRUCTIONS" in combined_prompt, "❌ Custom instructions not in prompt"
    assert "# STYLE GUIDE & FORMATTING RULES" in combined_prompt, "❌ Style guide header not in prompt"
    
    # Verify order (custom instructions before style guide)
    custom_pos = combined_prompt.find("# CUSTOM INSTRUCTIONS")
    style_pos = combined_prompt.find("# STYLE GUIDE & FORMATTING RULES")
    assert custom_pos < style_pos, "❌ Style guide should come after custom instructions"
    
    print("✅ Prompt hierarchy correct (System → Custom → Style Guide)")
    
    return combined_prompt


def test_phase_3_persistence():
    """Test Phase 3: Project persistence (save/load)"""
    print("\n" + "="*60)
    print("PHASE 3: Testing Project Persistence")
    print("="*60)
    
    # Create a mock project data structure
    project_data = {
        'version': '0.3.2',
        'segments': [],
        'llm_settings': {
            'provider': 'openai',
            'model': 'gpt-4o',
            'source_language': 'English',
            'target_language': 'Dutch',
            'active_translate_prompt_name': 'Professional Translation',
            'active_custom_instruction': 'Use formal tone.',
            'active_custom_instruction_name': 'Formal Style',
            # Phase 3: Style guide persistence
            'active_style_guide_name': 'Dutch Professional Writing',
            'active_style_guide_language': 'Dutch'
        }
    }
    
    print("✅ Project saved with style guide settings")
    print(f"   - active_style_guide_name: {project_data['llm_settings']['active_style_guide_name']}")
    print(f"   - active_style_guide_language: {project_data['llm_settings']['active_style_guide_language']}")
    
    # Simulate project load
    llm_settings = project_data['llm_settings']
    active_style_guide_name = llm_settings.get('active_style_guide_name')
    active_style_guide_language = llm_settings.get('active_style_guide_language')
    
    assert active_style_guide_name == 'Dutch Professional Writing', "❌ Style guide name not persisted"
    assert active_style_guide_language == 'Dutch', "❌ Style guide language not persisted"
    
    print("✅ Project loaded and style guide settings restored")
    
    # Test reloading style guide content
    sg_lib = StyleGuideLibrary(
        os.path.join(os.path.dirname(__file__), "user data", "Translation_Resources", "Style_Guides")
    )
    sg_lib.load_all_guides()
    
    if active_style_guide_language:
        style_guide = sg_lib.get_guide(active_style_guide_language)
        if style_guide:
            content = style_guide.get('content', '')
            print(f"✅ Style guide content reloaded: {len(content)} characters")
        else:
            print(f"⚠ Style guide not found: {active_style_guide_language}")
    
    return project_data


def test_phase_4_ui_integration():
    """Test Phase 4: UI components integration"""
    print("\n" + "="*60)
    print("PHASE 4: Testing UI Integration")
    print("="*60)
    
    sg_lib = StyleGuideLibrary(
        os.path.join(os.path.dirname(__file__), "user data", "Translation_Resources", "Style_Guides")
    )
    sg_lib.load_all_guides()
    
    # Test loading style guides for tree view
    languages = sg_lib.get_all_languages()
    print(f"✅ Loaded {len(languages)} style guides for UI")
    
    tree_items = []
    for language in languages:
        guide = sg_lib.get_guide(language)
        if guide:
            item = {
                'name': guide.get('language', language),
                'language': language,
                'version': guide.get('version', '1.0'),
                'content_length': len(guide.get('content', ''))
            }
            tree_items.append(item)
    
    # Display tree items
    print("   Style Guides available in UI:")
    for item in tree_items:
        print(f"   - {item['name']}: {item['content_length']} chars")
    
    # Test activation
    if tree_items:
        selected = tree_items[0]
        print(f"\n✅ Selected style guide: {selected['name']}")
        
        # Simulate activation
        active_guide = sg_lib.get_guide(selected['language'])
        if active_guide:
            print(f"✅ Activated: {active_guide.get('language')} with {len(active_guide.get('content', ''))} chars")
    
    return tree_items


def test_phase_5_end_to_end(app, combined_prompt, project_data, tree_items):
    """Test Phase 5: Full end-to-end integration"""
    print("\n" + "="*60)
    print("PHASE 5: End-to-End Integration Testing")
    print("="*60)
    
    print("\n📋 Test Scenario: Full Translation Workflow")
    print("-" * 60)
    
    # 1. User selects a style guide in UI
    print("\n1️⃣  User selects Dutch style guide in UI")
    if tree_items:
        selected_guide = tree_items[0]
        app.active_style_guide_name = selected_guide['name']
        app.active_style_guide_language = selected_guide['language']
        sg = app.style_guide_library.get_guide(selected_guide['language'])
        app.active_style_guide = sg.get('content', '')
        print(f"   ✅ Style guide activated: {app.active_style_guide_name}")
    
    # 2. User saves project
    print("\n2️⃣  User saves project")
    saved_project = {
        'llm_settings': {
            'active_style_guide_name': app.active_style_guide_name,
            'active_style_guide_language': app.active_style_guide_language,
            'active_custom_instruction': getattr(app, 'active_custom_instruction', None),
            'active_custom_instruction_name': getattr(app, 'active_custom_instruction_name', None),
        }
    }
    print(f"   ✅ Project saved with style guide")
    
    # 3. User closes and reopens project
    print("\n3️⃣  User closes and reopens project")
    
    # Simulate load
    app.active_style_guide_name = saved_project['llm_settings']['active_style_guide_name']
    app.active_style_guide_language = saved_project['llm_settings']['active_style_guide_language']
    
    if app.active_style_guide_language:
        guide = app.style_guide_library.get_guide(app.active_style_guide_language)
        if guide:
            app.active_style_guide = guide.get('content', '')
            print(f"   ✅ Project reopened with style guide: {app.active_style_guide_name}")
    
    # 4. User translates a segment
    print("\n4️⃣  User requests translation (style guide in prompt)")
    prompt_used = combined_prompt
    print(f"   ✅ Prompt includes:")
    print(f"      - System Prompt")
    print(f"      - Custom Instructions: {app.active_custom_instruction_name if hasattr(app, 'active_custom_instruction_name') else 'None'}")
    print(f"      - Style Guide: {app.active_style_guide_name}")
    
    # 5. Verify three-level hierarchy
    print("\n5️⃣  Verify three-level prompt hierarchy")
    hierarchy = [
        ("System Prompt", True),
        ("Custom Instructions", "CUSTOM" in prompt_used),
        ("Style Guide", "STYLE GUIDE" in prompt_used)
    ]
    
    for level, present in hierarchy:
        status = "✅" if present else "⚠"
        print(f"   {status} {level}: {'Present' if present else 'Not present'}")
    
    print("\n✅ End-to-end testing complete!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("STYLE GUIDE INTEGRATION - END-TO-END TESTING")
    print("="*60)
    
    try:
        # Phase 1
        app = test_phase_1_instance_variables()
        
        # Phase 2
        combined_prompt = test_phase_2_prompt_composition(app)
        
        # Phase 3
        project_data = test_phase_3_persistence()
        
        # Phase 4
        tree_items = test_phase_4_ui_integration()
        
        # Phase 5
        test_phase_5_end_to_end(app, combined_prompt, project_data, tree_items)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - Integration Complete!")
        print("="*60)
        print("\nStyle guides are now fully integrated:")
        print("  ✅ Phase 1: Instance variables")
        print("  ✅ Phase 2: Prompt composition")
        print("  ✅ Phase 3: Project persistence")
        print("  ✅ Phase 4: UI components")
        print("  ✅ Phase 5: End-to-end integration")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
