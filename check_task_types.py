import json
import os

prompts_dir = "user data/System_prompts"

# Get all JSON files in the directory
all_files = [f for f in os.listdir(prompts_dir) if f.endswith('.json')]

print("Task Type Status Check - ALL PROMPTS")
print("=" * 70)

for filename in sorted(all_files):
    filepath = os.path.join(prompts_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        task_type = data.get('task_type', 'NOT SET')
        print(f"{filename:50} {task_type}")

print("\n" + "=" * 70)
print(f"\nTotal prompts: {len(all_files)}")
print("All prompts should now have explicit task_type field!")
