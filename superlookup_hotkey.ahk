; ============================================================================
; Superlookup Hotkey for Supervertaler Qt v1.0.0
; ============================================================================
; 
; This AutoHotkey v2 script provides reliable clipboard capture for the
; Superlookup feature. It runs silently in the background when
; Supervertaler starts.
;
; Hotkey: Ctrl+Alt+L
; 
; How it works:
; 1. User selects text anywhere on the computer (memoQ, Word, browser, etc.)
; 2. User presses Ctrl+Alt+L
; 3. This script copies the selection with Ctrl+C (reliable on Windows)
; 4. Writes a signal file to notify Python
; 5. Python reads the clipboard and displays results
;
; Why AutoHotkey?
; - Python's clipboard handling on Windows is unreliable and causes issues
;   (deleting text, selecting wrong content, etc.)
; - AutoHotkey handles Windows clipboard operations flawlessly
; - This hybrid approach gives us the best of both worlds
;
; Author: Michael Beijer
; ============================================================================

^!l::
{
    ; Simply copy selected text with Ctrl+C
    Send "^c"
    Sleep 200  ; Give clipboard time to update
    
    ; Write signal file to trigger Python
    signalFile := "C:\Dev\Supervertaler\lookup_signal.txt"
    if FileExist(signalFile)
        FileDelete signalFile
    FileAppend "trigger", signalFile
    
    ; Bring Supervertaler window to foreground
    ; Try multiple window title patterns
    if WinExist("Supervertaler")
        WinActivate
    else if WinExist("ahk_exe python.exe") && WinExist("Supervertaler")
        WinActivate "Supervertaler"
    else if WinExist("ahk_exe pythonw.exe") && WinExist("Supervertaler")
        WinActivate "Supervertaler"
    
    return
}
