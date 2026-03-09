# Installation

## Download

1. Go to the [GitHub Releases](https://github.com/michaelbeijer/Supervertaler-for-Trados/releases) page
2. Download the latest `.sdlplugin` file

## Install

1. **Close Trados Studio** if it is running
2. **Double-click** the downloaded `.sdlplugin` file — Trados handles the installation automatically
3. **Restart Trados Studio**

{% hint style="info" %}
The `.sdlplugin` format is an Open Packaging Convention archive. Trados extracts it into its plugin directory on startup. You do not need to manually copy any files.
{% endhint %}

## Verify Installation

After restarting Trados Studio, open a project in the Editor view. You should see:

- **TermLens panel** — docked above the editor area (or in the bottom panel area)
- **Supervertaler Assistant panel** — docked on the right side

### If the TermLens panel is not visible

Go to **View > TermLens** to show the panel.

### If the Supervertaler Assistant panel is not visible

Go to **View > Supervertaler Assistant** to show the panel.

{% hint style="success" %}
Both panels are standard Trados dockable panels. You can drag them to any docking position (left, right, top, bottom, floating) or move them to a second monitor. Trados remembers their position between sessions.
{% endhint %}

## Updating

To update to a newer version:

1. Close Trados Studio
2. Double-click the new `.sdlplugin` file
3. Restart Trados Studio

The new version replaces the previous installation. Your settings and termbases are preserved.

## Uninstalling

To remove the plugin:

1. Open Trados Studio
2. Go to **Help > Plugin Management**
3. Find "Supervertaler for Trados" in the list
4. Click **Uninstall**
5. Restart Trados Studio

---

## Next Steps

- [Getting Started](getting-started.md) — set up your first termbase and API key
