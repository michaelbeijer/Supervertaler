; ============================================================================
; Supervertaler Hotkeys - AutoHotkey v2
; ============================================================================
;
; This script provides keyboard enhancements for Supervertaler that are
; difficult or impossible to implement reliably in Python/Qt.
;
; HOTKEYS:
;   Ctrl+Alt+L     - Superlookup: Copy selection and trigger lookup
;   Shift+Shift    - Context menu: Double-tap Shift opens context menu (in Supervertaler only)
;
; Author: Michael Beijer / Supervertaler
; ============================================================================

#Requires AutoHotkey v2.0
#SingleInstance Force

; Set tray icon to Supervertaler icon
if FileExist(A_ScriptDir "\assets\icon.ico")
    TraySetIcon(A_ScriptDir "\assets\icon.ico", , true)
A_IconTip := "Supervertaler Hotkeys"

; ============================================================================
; SUPERLOOKUP HOTKEY (Ctrl+Alt+L) - Works globally
; ============================================================================
; Copies selected text and triggers Superlookup in Supervertaler.
; Works from any application (memoQ, Word, browser, etc.)

^!l::
{
    ; Copy selected text with Ctrl+C
    Send "^c"
    Sleep 200  ; Give clipboard time to update
    
    ; Write signal file to trigger Python
    signalFile := A_ScriptDir "\lookup_signal.txt"
    if FileExist(signalFile)
        FileDelete signalFile
    FileAppend "trigger", signalFile
    
    ; Bring Supervertaler window to foreground
    if WinExist("Supervertaler")
        WinActivate
    else if WinExist("ahk_exe python.exe") && WinExist("Supervertaler")
        WinActivate "Supervertaler"
    else if WinExist("ahk_exe pythonw.exe") && WinExist("Supervertaler")
        WinActivate "Supervertaler"
    
    return
}

; ============================================================================
; DOUBLE-TAP SHIFT → CONTEXT MENU (Only in Supervertaler)
; ============================================================================
; Qt's event system makes reliable double-tap detection difficult in Python.
; AutoHotkey excels at keyboard timing detection.
;
; How it works:
; 1. First Shift release: Record timestamp
; 2. Second Shift release within 350ms: Send Shift+F10 (Qt's native context menu)

global LastShiftTime := 0
global DoubleTapThreshold := 350  ; milliseconds

#HotIf WinActive("ahk_exe Supervertaler.exe") or WinActive("Supervertaler")

~LShift Up::
~RShift Up::
{
    global LastShiftTime, DoubleTapThreshold
    
    CurrentTime := A_TickCount
    TimeSinceLastShift := CurrentTime - LastShiftTime
    
    if (LastShiftTime > 0 && TimeSinceLastShift < DoubleTapThreshold)
    {
        ; Double-tap detected! Send Shift+F10 for context menu
        Send "+{F10}"
        LastShiftTime := 0  ; Reset to prevent triple-tap
    }
    else
    {
        ; First tap - record time
        LastShiftTime := CurrentTime
    }
}

#HotIf  ; End context-sensitive hotkey
