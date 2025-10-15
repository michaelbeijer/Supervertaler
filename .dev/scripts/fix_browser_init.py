# Fix TrackedChangesBrowser initialization

# Read the file
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix 1: Update __init__ method to accept parent_app and log_queue
for i, line in enumerate(lines):
    if 'class TrackedChangesBrowser:' in line and i < 500:
        # Found the class, now find its __init__
        for j in range(i+1, min(i+10, len(lines))):
            if 'def __init__(self, parent, tracked_changes_agent):' in lines[j]:
                # Replace this line
                lines[j] = '    def __init__(self, parent, tracked_changes_agent, parent_app=None, log_queue=None):\n'
                # Add the new attributes after tracked_changes_agent
                for k in range(j+1, min(j+10, len(lines))):
                    if 'self.tracked_changes_agent = tracked_changes_agent' in lines[k]:
                        # Insert after this line
                        indent = '        '
                        lines.insert(k+1, f'{indent}self.parent_app = parent_app  # Reference to main app for AI settings\n')
                        lines.insert(k+2, f'{indent}self.log_queue = log_queue if log_queue else queue.Queue()\n')
                        break
                break
        break

# Fix 2: Update TrackedChangesBrowser instantiation
for i, line in enumerate(lines):
    if 'self.tracked_changes_browser = TrackedChangesBrowser(self.root, self.tracked_changes_agent)' in line:
        # Replace this line with multi-line version
        indent = '            '
        lines[i] = f'{indent}self.tracked_changes_browser = TrackedChangesBrowser(\n'
        lines.insert(i+1, f'{indent}    self.root,\n')
        lines.insert(i+2, f'{indent}    self.tracked_changes_agent,\n')
        lines.insert(i+3, f'{indent}    parent_app=self,\n')
        lines.insert(i+4, f'{indent}    log_queue=self.log_queue\n')
        lines.insert(i+5, f'{indent})\n')
        break

# Write back
with open(r'c:\Dev\Supervertaler\Supervertaler_v2.4.4-CLASSIC.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Fixed TrackedChangesBrowser initialization!')
print('   - Added parent_app parameter')
print('   - Added log_queue parameter with default fallback')
print('   - Updated instantiation to pass both parameters')
