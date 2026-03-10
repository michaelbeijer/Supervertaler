# Voice Commands (Supervoice)

Supervertaler includes **Supervoice**: voice dictation + Talon-style voice commands.

## Where to find it

- Go to the **Tools** tab → **🎤 Supervoice**.

## Push-to-talk dictation (F9)

- Press `F9` to start recording.
- Speak.
- Supervertaler transcribes what you said.

If voice commands are enabled, Supervertaler will first try to interpret your speech as a command. If nothing matches, the text is inserted as dictation.

## Voice commands

Voice commands trigger actions like navigation and editing.

Examples of built-in phrases include:

- “next segment”
- “previous segment”
- “confirm”
- “copy source”
- “clear target”

You can add/edit/remove commands in **🎤 Supervoice**.

## Always-on listening mode

Always-on mode continuously listens for speech and automatically:

1. Detects when you start speaking
2. Records
3. Transcribes
4. Runs it as a command or dictation

This is configured and toggled inside **🎤 Supervoice**.

## Recognition engine

Supervoice supports two transcription modes:

- **Local Whisper (offline)**: runs on your computer (slower, depends on your hardware)
- **OpenAI Whisper API (online)**: faster and usually much more accurate for short commands (requires an OpenAI API key)

## AutoHotkey (system commands)

Some voice commands can execute AutoHotkey scripts to control other applications (for example: memoQ or Trados).

{% hint style="info" %}
If AutoHotkey is not installed, in-app commands still work, but system-level commands won’t.
{% endhint %}

## Tips for accuracy

- Use a quiet environment and a consistent mic position.
- If recognition triggers too easily (or not at all), adjust **Mic Sensitivity** in **🎤 Supervoice**.
