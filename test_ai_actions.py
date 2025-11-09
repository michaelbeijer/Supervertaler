"""
Test suite for AI Actions System (Phase 2)

Tests the AIActionSystem module integration with UnifiedPromptLibrary.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from modules.ai_actions import AIActionSystem
from modules.unified_prompt_library import UnifiedPromptLibrary


def log(msg):
    """Simple logging function"""
    # Replace unicode characters that might not display on Windows console
    msg = msg.replace('✓', '[OK]').replace('✗', '[X]').replace('⚠', '[!]')
    print(f"  {msg}")


def test_1_action_system_initialization():
    """Test 1: Initialize AIActionSystem"""
    print("\n" + "="*60)
    print("TEST 1: AIActionSystem Initialization")
    print("="*60)

    # Create temporary library directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Initialize library
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)

        # Create test prompt
        prompt_data = {
            'name': 'Test Medical Prompt',
            'content': 'You are a medical translator...',
            'description': 'Test prompt',
            'domain': 'Medical',
            'task_type': 'Translation',
            'favorite': False,
            'quick_run': False,
            'folder': '',
            'tags': ['medical', 'test']
        }
        library.save_prompt('test_medical.md', prompt_data)

        # Initialize action system
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        print("✓ AIActionSystem initialized successfully")
        print(f"✓ Available actions: {len(action_system.action_handlers)}")

        return True

    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_2_list_prompts_action():
    """Test 2: Execute list_prompts action"""
    print("\n" + "="*60)
    print("TEST 2: list_prompts Action")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)

        # Create test prompts in different folders
        prompts = [
            ('Medical/cardiology.md', 'Cardiology Specialist', 'Medical'),
            ('Legal/contracts.md', 'Contract Specialist', 'Legal'),
            ('Medical/pharmacology.md', 'Pharmacology Specialist', 'Medical')
        ]

        for path, name, domain in prompts:
            prompt_data = {
                'name': name,
                'content': f'You are a {name}...',
                'domain': domain,
                'folder': domain
            }
            library.save_prompt(path, prompt_data)

        library.load_all_prompts()
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Test list all prompts
        result = action_system.execute_action('list_prompts', {})
        assert result['success'], "list_prompts action failed"
        assert result['result']['count'] == 3, f"Expected 3 prompts, got {result['result']['count']}"
        print(f"✓ Listed all prompts: {result['result']['count']}")

        # Test list with folder filter
        result = action_system.execute_action('list_prompts', {'folder': 'Medical'})
        assert result['success'], "list_prompts with folder filter failed"
        assert result['result']['count'] == 2, f"Expected 2 medical prompts, got {result['result']['count']}"
        print(f"✓ Filtered by folder 'Medical': {result['result']['count']}")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_3_create_prompt_action():
    """Test 3: Execute create_prompt action"""
    print("\n" + "="*60)
    print("TEST 3: create_prompt Action")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Create prompt via action
        params = {
            'name': 'Financial Translation Expert',
            'content': 'You are an expert financial translator specialized in annual reports...',
            'folder': 'Domain Expertise',
            'description': 'Expert in financial translation',
            'tags': ['financial', 'accounting', 'reports']
        }

        result = action_system.execute_action('create_prompt', params)
        assert result['success'], f"create_prompt failed: {result.get('error')}"
        print(f"✓ Created prompt: {result['result']['path']}")

        # Verify prompt was created
        library.load_all_prompts()
        assert len(library.prompts) == 1, "Prompt was not created"
        print("✓ Prompt verified in library")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_4_search_prompts_action():
    """Test 4: Execute search_prompts action"""
    print("\n" + "="*60)
    print("TEST 4: search_prompts Action")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)

        # Create diverse prompts
        prompts = [
            ('medical_cardiology.md', 'Cardiology Expert', ['medical', 'cardiology', 'heart']),
            ('medical_neurology.md', 'Neurology Expert', ['medical', 'neurology', 'brain']),
            ('legal_contracts.md', 'Contract Specialist', ['legal', 'contracts']),
            ('technical_engineering.md', 'Engineering Manual', ['technical', 'engineering'])
        ]

        for path, name, tags in prompts:
            prompt_data = {
                'name': name,
                'content': f'You are a {name}. You specialize in {", ".join(tags)}.',
                'tags': tags
            }
            library.save_prompt(path, prompt_data)

        library.load_all_prompts()
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Search by name
        result = action_system.execute_action('search_prompts', {'query': 'medical', 'search_in': 'name'})
        assert result['success'], "search_prompts by name failed"
        print(f"✓ Search by name 'medical': {result['result']['count']} results")

        # Search by tags
        result = action_system.execute_action('search_prompts', {'query': 'cardiology', 'search_in': 'tags'})
        assert result['success'], "search_prompts by tags failed"
        assert result['result']['count'] == 1, f"Expected 1 result, got {result['result']['count']}"
        print(f"✓ Search by tag 'cardiology': {result['result']['count']} results")

        # Search all
        result = action_system.execute_action('search_prompts', {'query': 'engineering', 'search_in': 'all'})
        assert result['success'], "search_prompts all failed"
        print(f"✓ Search all 'engineering': {result['result']['count']} results")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_5_parse_and_execute():
    """Test 5: Parse ACTION blocks from AI response"""
    print("\n" + "="*60)
    print("TEST 5: Parse and Execute ACTION Blocks")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Simulate AI response with ACTION blocks
        ai_response = """I'll help you create a medical translation prompt.

ACTION:create_prompt
PARAMS:{"name": "Medical Device Translator", "content": "You are an expert medical device translator...", "folder": "Medical", "tags": ["medical", "devices"]}

The prompt has been created successfully. You can now use it in your translations.

ACTION:list_prompts
PARAMS:{"folder": "Medical"}

I've listed all medical prompts for you."""

        cleaned_response, action_results = action_system.parse_and_execute(ai_response)

        # Verify actions were parsed
        assert len(action_results) == 2, f"Expected 2 actions, got {len(action_results)}"
        print(f"✓ Parsed {len(action_results)} actions")

        # Verify first action (create_prompt)
        assert action_results[0]['action'] == 'create_prompt', "First action should be create_prompt"
        assert action_results[0]['success'], "create_prompt should succeed"
        print(f"✓ Action 1: {action_results[0]['action']} - Success")

        # Verify second action (list_prompts)
        assert action_results[1]['action'] == 'list_prompts', "Second action should be list_prompts"
        assert action_results[1]['success'], "list_prompts should succeed"
        print(f"✓ Action 2: {action_results[1]['action']} - Success")

        # Verify cleaned response has no ACTION blocks
        assert 'ACTION:' not in cleaned_response, "Cleaned response still contains ACTION blocks"
        print("✓ ACTION blocks removed from response")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_6_update_and_delete_prompt():
    """Test 6: Execute update_prompt and delete_prompt actions"""
    print("\n" + "="*60)
    print("TEST 6: update_prompt and delete_prompt Actions")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Create initial prompt
        params = {
            'name': 'Test Prompt',
            'content': 'Original content',
            'folder': 'Test'
        }
        result = action_system.execute_action('create_prompt', params)
        prompt_path = result['result']['path']
        print(f"✓ Created prompt: {prompt_path}")

        # Update prompt
        update_params = {
            'path': prompt_path,
            'content': 'Updated content',
            'description': 'Updated description'
        }
        result = action_system.execute_action('update_prompt', update_params)
        assert result['success'], f"update_prompt failed: {result.get('error')}"
        print("✓ Updated prompt successfully")

        # Verify update
        # Note: After update, need to check in the library's in-memory prompts
        # which were updated by save_prompt in the action handler
        if prompt_path in library.prompts:
            updated_prompt = library.prompts[prompt_path]
            assert updated_prompt['content'] == 'Updated content', "Content was not updated"
            assert updated_prompt['description'] == 'Updated description', "Description was not updated"
            print("✓ Update verified")
        else:
            print(f"⚠ Prompt path {prompt_path} not found after update, reloading library")
            library.load_all_prompts()
            # After reload, the prompt should be there
            assert prompt_path in library.prompts, f"Prompt not found even after reload: {prompt_path}"
            updated_prompt = library.prompts[prompt_path]
            assert updated_prompt['content'] == 'Updated content', "Content was not updated"
            print("✓ Update verified after reload")

        # Delete prompt
        result = action_system.execute_action('delete_prompt', {'path': prompt_path})
        assert result['success'], f"delete_prompt failed: {result.get('error')}"
        print("✓ Deleted prompt successfully")

        # Verify deletion
        library.load_all_prompts()
        assert len(library.prompts) == 0, "Prompt was not deleted"
        print("✓ Deletion verified")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_7_toggle_favorite_and_quick_run():
    """Test 7: Execute toggle_favorite and toggle_quick_run actions"""
    print("\n" + "="*60)
    print("TEST 7: toggle_favorite and toggle_quick_run Actions")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Create test prompt
        params = {
            'name': 'Toggle Test Prompt',
            'content': 'Test content'
        }
        result = action_system.execute_action('create_prompt', params)
        prompt_path = result['result']['path']

        # Toggle favorite
        result = action_system.execute_action('toggle_favorite', {'path': prompt_path})
        assert result['success'], "toggle_favorite failed"
        assert result['result']['favorite'] is True, "Favorite should be True"
        print("✓ Toggled favorite ON")

        # Toggle favorite again
        result = action_system.execute_action('toggle_favorite', {'path': prompt_path})
        assert result['result']['favorite'] is False, "Favorite should be False"
        print("✓ Toggled favorite OFF")

        # Toggle quick run
        result = action_system.execute_action('toggle_quick_run', {'path': prompt_path})
        assert result['success'], "toggle_quick_run failed"
        assert result['result']['quick_run'] is True, "Quick run should be True"
        print("✓ Toggled quick_run ON")

        # Toggle quick run again
        result = action_system.execute_action('toggle_quick_run', {'path': prompt_path})
        assert result['result']['quick_run'] is False, "Quick run should be False"
        print("✓ Toggled quick_run OFF")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_8_format_action_results():
    """Test 8: Format action results for display"""
    print("\n" + "="*60)
    print("TEST 8: Format Action Results")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)
        action_system = AIActionSystem(prompt_library=library, log_callback=log)

        # Create test action results
        action_results = [
            {
                'action': 'create_prompt',
                'success': True,
                'result': {
                    'message': 'Created prompt: Test',
                    'path': 'test.md'
                }
            },
            {
                'action': 'list_prompts',
                'success': True,
                'result': {
                    'count': 5
                }
            },
            {
                'action': 'delete_prompt',
                'success': False,
                'error': 'Prompt not found'
            }
        ]

        formatted = action_system.format_action_results(action_results)

        # Verify formatting
        assert '✓' in formatted, "Should contain success indicators"
        assert '✗' in formatted, "Should contain error indicators"
        assert 'create_prompt' in formatted, "Should contain action names"
        assert 'Prompt not found' in formatted, "Should contain error messages"

        print("✓ Formatted action results:")
        print(formatted)

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_9_segment_count_action():
    """Test 9: Execute get_segment_count action"""
    print("\n" + "="*60)
    print("TEST 9: get_segment_count Action")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)

        # Create mock parent app with segments
        class MockProject:
            def __init__(self):
                self.segments = []

        class MockSegment:
            def __init__(self, seg_id, source, target=""):
                self.id = seg_id
                self.source = source
                self.target = target
                self.status = "draft"
                self.type = "para"
                self.notes = ""
                self.match_percent = None
                self.locked = False
                self.paragraph_id = 0
                self.style = "Normal"
                self.document_position = seg_id
                self.is_table_cell = False

        class MockApp:
            def __init__(self):
                self.current_project = MockProject()
                # Create some test segments
                self.current_project.segments = [
                    MockSegment(1, "Hello world", "Hallo wereld"),
                    MockSegment(2, "How are you?", "Hoe gaat het?"),
                    MockSegment(3, "Good morning", ""),
                    MockSegment(4, "Thank you", "Dank je"),
                    MockSegment(5, "Goodbye", "")
                ]

        mock_app = MockApp()
        action_system = AIActionSystem(
            prompt_library=library,
            parent_app=mock_app,
            log_callback=log
        )

        # Test get_segment_count
        result = action_system.execute_action('get_segment_count', {})
        assert result['success'], f"get_segment_count failed: {result.get('error')}"
        assert result['result']['total_segments'] == 5, f"Expected 5 segments, got {result['result']['total_segments']}"
        assert result['result']['translated'] == 3, f"Expected 3 translated, got {result['result']['translated']}"
        assert result['result']['untranslated'] == 2, f"Expected 2 untranslated, got {result['result']['untranslated']}"

        print(f"[OK] Total segments: {result['result']['total_segments']}")
        print(f"[OK] Translated: {result['result']['translated']}")
        print(f"[OK] Untranslated: {result['result']['untranslated']}")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_10_segment_info_action():
    """Test 10: Execute get_segment_info action"""
    print("\n" + "="*60)
    print("TEST 10: get_segment_info Action")
    print("="*60)

    temp_dir = tempfile.mkdtemp()

    try:
        library = UnifiedPromptLibrary(library_dir=temp_dir, log_callback=log)

        # Create mock parent app with segments
        class MockProject:
            def __init__(self):
                self.segments = []

        class MockSegment:
            def __init__(self, seg_id, source, target=""):
                self.id = seg_id
                self.source = source
                self.target = target
                self.status = "draft"
                self.type = "para"
                self.notes = ""
                self.match_percent = None
                self.locked = False
                self.paragraph_id = 0
                self.style = "Normal"
                self.document_position = seg_id
                self.is_table_cell = False

        class MockApp:
            def __init__(self):
                self.current_project = MockProject()
                self.current_project.segments = [
                    MockSegment(1, "Hello world", "Hallo wereld"),
                    MockSegment(2, "How are you?", "Hoe gaat het?"),
                    MockSegment(3, "Good morning", "Goedemorgen"),
                ]

        mock_app = MockApp()
        action_system = AIActionSystem(
            prompt_library=library,
            parent_app=mock_app,
            log_callback=log
        )

        # Test single segment
        result = action_system.execute_action('get_segment_info', {'segment_id': 2})
        assert result['success'], f"get_segment_info failed: {result.get('error')}"
        assert result['result']['count'] == 1, f"Expected 1 segment, got {result['result']['count']}"
        assert result['result']['segments'][0]['id'] == 2, "Wrong segment returned"
        assert result['result']['segments'][0]['source'] == "How are you?", "Wrong source text"
        print("[OK] Single segment retrieval")

        # Test multiple segments by IDs
        result = action_system.execute_action('get_segment_info', {'segment_ids': [1, 3]})
        assert result['success'], "get_segment_info with IDs failed"
        assert result['result']['count'] == 2, f"Expected 2 segments, got {result['result']['count']}"
        print("[OK] Multiple segments by IDs")

        # Test range
        result = action_system.execute_action('get_segment_info', {'start_id': 1, 'end_id': 2})
        assert result['success'], "get_segment_info with range failed"
        assert result['result']['count'] == 2, f"Expected 2 segments in range, got {result['result']['count']}"
        print("[OK] Range retrieval")

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI ACTIONS SYSTEM TEST SUITE (Phase 2)")
    print("="*60)

    tests = [
        test_1_action_system_initialization,
        test_2_list_prompts_action,
        test_3_create_prompt_action,
        test_4_search_prompts_action,
        test_5_parse_and_execute,
        test_6_update_and_delete_prompt,
        test_7_toggle_favorite_and_quick_run,
        test_8_format_action_results,
        test_9_segment_count_action,
        test_10_segment_info_action
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed}/{len(tests)} passed")
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"❌ {failed} tests failed")
    print("="*60)

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
