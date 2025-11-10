#!/usr/bin/env python3
"""
Test script to validate all translation match types
Tests: Termbase, TM (Translation Memory), MT (Machine Translation), LLM (AI)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.llm_clients import get_google_translation, get_openai_translation, get_claude_translation
from modules.database_manager import DatabaseManager

def test_google_translate():
    print("🤖 Testing Google Translate...")
    result = get_google_translation("Hallo wereld", "auto", "en")
    print(f"   Result: {result}")
    print(f"   Success: {result.get('success', False)}")
    if result.get('translation'):
        print(f"   Translation: {result['translation']}")
    print()

def test_llm_functions():
    print("🧠 Testing LLM functions...")
    
    print("  Testing OpenAI wrapper...")
    openai_result = get_openai_translation("Hallo wereld", "Dutch", "English", "greeting")
    print(f"   OpenAI Result: {openai_result}")
    print()
    
    print("  Testing Claude wrapper...")
    claude_result = get_claude_translation("Hallo wereld", "Dutch", "English", "greeting")
    print(f"   Claude Result: {claude_result}")
    print()

def test_database_connections():
    print("🔍 Testing database connections...")
    try:
        db_manager = DatabaseManager()
        
        # Test termbase search
        termbase_results = db_manager.search_termbases("Python")
        print(f"   Termbase matches: {len(termbase_results)} found")
        
        # Test TM search
        tm_results = db_manager.search_all("Python", max_results=3)
        print(f"   TM matches: {len(tm_results)} found")
        
        print("   Database connections working!")
    except Exception as e:
        print(f"   Database error: {e}")
    print()

def main():
    print("🚀 Testing All Translation Match Types")
    print("=" * 50)
    
    test_google_translate()
    test_llm_functions()
    test_database_connections()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()