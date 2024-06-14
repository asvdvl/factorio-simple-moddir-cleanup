import sys
import os
import json
import shutil
import re

if len(sys.argv) < 2 or not sys.argv[1].strip():
    print("Error: Please provide the path to the mods directory.")
    sys.exit(1)

mods_directory = sys.argv[1].strip()

old_directory = os.path.join(mods_directory, 'old')
disabled_directory = os.path.join(mods_directory, 'disabled')
mod_list_file = os.path.join(mods_directory, 'mod-list.json')

os.makedirs(old_directory, exist_ok=True)
os.makedirs(disabled_directory, exist_ok=True)

with open(mod_list_file, 'r') as f:
    mod_list = json.load(f)

enabled_mods = {mod['name'] for mod in mod_list['mods'] if mod['enabled']}
disabled_mods = {mod['name'] for mod in mod_list['mods'] if not mod['enabled']}

mod_pattern = re.compile(r'^(.*)_(\d+\.\d+\.\d+)\.zip$')

mod_versions = {}

for filename in os.listdir(mods_directory):
    if filename.endswith('.zip'):
        match = mod_pattern.match(filename)
        if match:
            mod_name, version = match.groups()
            if mod_name not in mod_versions:
                mod_versions[mod_name] = []
            mod_versions[mod_name].append((version, filename))

old_mods_count = 0
disabled_mods_count = 0

for mod_name, versions in mod_versions.items():
    if len(versions) > 1:
        versions.sort()
        for version, filename in versions[:-1]:
            src = os.path.join(mods_directory, filename)
            dst = os.path.join(old_directory, filename)
            if os.path.exists(src):
                shutil.move(src, dst)
                old_mods_count += 1

for mod_name in disabled_mods:
    if mod_name in mod_versions:
        for version, filename in mod_versions[mod_name]:
            src = os.path.join(mods_directory, filename)
            dst = os.path.join(disabled_directory, filename)
            if os.path.exists(src):
                shutil.move(src, dst)
                disabled_mods_count += 1

print(f"Old mods moved: {old_mods_count}")
print(f"Disabled mods moved: {disabled_mods_count}")
