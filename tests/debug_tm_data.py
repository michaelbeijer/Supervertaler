#!/usr/bin/env python3

import sqlite3
import json

def check_tm_data():
    """Check what TM and project data exists in the database"""
    
    # Connect to database
    conn = sqlite3.connect('user_data_private/Translation_Resources/supervertaler.db')
    cursor = conn.cursor()
    
    print("=== TRANSLATION UNITS (TM entries) ===")
    
    # First check what tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = cursor.fetchall()
    print(f"All tables: {[t[0] for t in all_tables]}")
    
    # Check if translation_units exists and what columns it has
    if ('translation_units',) in all_tables:
        cursor.execute("PRAGMA table_info(translation_units)")
        columns = cursor.fetchall()
        print(f"translation_units columns: {[col[1] for col in columns]}")
        
        # Try to get data with available columns
        cursor.execute('SELECT * FROM translation_units LIMIT 10')
        tm_entries = cursor.fetchall()
        
        if tm_entries:
            for i, row in enumerate(tm_entries):
                print(f'TM Entry {i+1}: {row}')
        else:
            print("No TM entries found!")
    else:
        print("translation_units table not found!")
    
    print("=== PROJECT TABLES ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%project%'")
    tables = cursor.fetchall()
    print(f'Project-related tables: {[t[0] for t in tables]}')
    
    if ('projects',) in tables:
        print("\n=== RECENT PROJECT ===")
        # Check projects table structure
        cursor.execute("PRAGMA table_info(projects)")
        project_columns = cursor.fetchall()
        print(f"projects columns: {[col[1] for col in project_columns]}")
        
        cursor.execute('SELECT * FROM projects ORDER BY rowid DESC LIMIT 1')
        recent_project = cursor.fetchone()
        if recent_project:
            print(f'Project ID: {recent_project[0]}')
            print(f'Name: {recent_project[1]}')
            print(f'Languages: {recent_project[2]} -> {recent_project[3]}')
            print(f'Created: {recent_project[4]}')
            print(f'TM/Glossary IDs: {recent_project[7]}, {recent_project[8]}')
            
            # Check if segments column exists
            cursor.execute("PRAGMA table_info(projects)")
            project_columns = [col[1] for col in cursor.fetchall()]
            print(f'Available columns: {project_columns}')
            
            if 'segments' in project_columns:
                cursor.execute('SELECT segments FROM projects WHERE id = ?', (recent_project[0],))
            else:
                print("No segments column found - segments likely stored elsewhere")
            segments_data = cursor.fetchone()
            if segments_data and segments_data[0]:
                try:
                    segments = json.loads(segments_data[0])
                    print(f'\nTotal segments: {len(segments)}')
                    
                    confirmed_count = 0
                    for i, seg in enumerate(segments):
                        status = seg.get('status', 'unknown')
                        has_target = bool(seg.get('target', '').strip())
                        if status == 'confirmed':
                            confirmed_count += 1
                        
                        if i < 10:  # Show first 10
                            print(f'Segment {i+1}: Status={status}, Has_target={has_target}')
                            print(f'  Source: {seg.get("source", "")[:60]}...' if len(seg.get("source", "")) > 60 else f'  Source: {seg.get("source", "")}')
                            if has_target:
                                print(f'  Target: {seg.get("target", "")[:60]}...' if len(seg.get("target", "")) > 60 else f'  Target: {seg.get("target", "")}')
                    
                    print(f'\nConfirmed segments: {confirmed_count}/{len(segments)}')
                    
                except Exception as e:
                    print(f'Error parsing segments: {e}')
    
    conn.close()

if __name__ == "__main__":
    check_tm_data()