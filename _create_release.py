import requests, json, pathlib

token = pathlib.Path(r'C:\Dev\Supervertaler\user_data_private\SupervertalerToken.txt').read_text().strip()
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json'}
body = {
    'tag_name': 'v1.9.275',
    'name': 'v1.9.275',
    'body': '## Bug Fixes\n\n- **macOS: app now launches when double-clicked from Finder** \u2014 PyInstaller .app bundles bounced in the dock and closed when launched via Finder. Root cause: Finder launches apps with minimal environment (no LANG/LC_CTYPE), causing locale-dependent code to fail. Fixed by adding LSEnvironment to Info.plist. Also added crash logging to ~/Desktop/supervertaler_crash.log for macOS builds.\n- **macOS build: ad-hoc code signing instructions** \u2014 Updated BUILD_MACOS.md with free codesign step.\n\n## Install\n\n- **pip:** Defaulting to user installation because normal site-packages is not writeable\n- **Windows standalone:** Download the .zip below\n- **macOS standalone:** Download the .dmg below',
    'draft': False,
    'prerelease': False,
}
r = requests.post('https://api.github.com/repos/Supervertaler/Supervertaler-Workbench/releases', headers=headers, json=body)
print(f'Status: {r.status_code}')
data = r.json()
print(f'URL: {data.get("html_url", "ERROR")}')
print(f'ID: {data.get("id", "ERROR")}')
if r.status_code != 201:
    print(f'Error: {data}')
