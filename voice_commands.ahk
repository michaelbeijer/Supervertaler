; ============================================================================
; Voice Commands AutoHotkey Bridge for Supervertaler v1.0.0
; ============================================================================
;
; This AutoHotkey v2 script provides system-level keyboard automation
; for the Supervoice command system. It monitors a command file and
; executes keystrokes/scripts when triggered by Python.
;
; How it works:
; 1. Python voice recognition detects a voice command
; 2. Python writes command to voice_command.txt
; 3. This script reads and executes the command
; 4. This script writes result to voice_result.txt
;
; Commands file format (JSON):
; {"type": "keystroke", "keys": "^s"}
; {"type": "script", "code": "Send, ^c\nSleep, 100\nSend, ^v"}
;
; Author: Michael Beijer / Supervertaler
; ============================================================================

#Requires AutoHotkey v2.0
#SingleInstance Force

; Configuration
global CommandFile := A_ScriptDir "\user_data\voice_command.txt"
global ResultFile := A_ScriptDir "\user_data\voice_result.txt"
global CheckInterval := 100  ; ms between checks

; Set tray icon
if FileExist(A_ScriptDir "\assets\icon.ico")
    TraySetIcon(A_ScriptDir "\assets\icon.ico", , true)
A_IconTip := "Supervertaler Voice Commands"

; Create tray menu
A_TrayMenu.Delete()  ; Clear default menu
A_TrayMenu.Add("Supervoice Commands Active", (*) => "")
A_TrayMenu.Disable("Supervoice Commands Active")
A_TrayMenu.Add()
A_TrayMenu.Add("Open Commands Folder", OpenCommandsFolder)
A_TrayMenu.Add("Reload Script", (*) => Reload())
A_TrayMenu.Add()
A_TrayMenu.Add("Exit", (*) => ExitApp())

; Ensure user_data directory exists
if !DirExist(A_ScriptDir "\user_data")
    DirCreate(A_ScriptDir "\user_data")

; Main monitoring loop
SetTimer(CheckForCommands, CheckInterval)

; ============================================================================
; Functions
; ============================================================================

CheckForCommands() {
    global CommandFile, ResultFile
    
    if !FileExist(CommandFile)
        return
    
    try {
        ; Read command file
        content := FileRead(CommandFile, "UTF-8")
        
        ; Delete command file immediately to prevent re-execution
        FileDelete(CommandFile)
        
        if (content = "")
            return
        
        ; Parse JSON-like command
        ; Format: {"type": "...", "keys": "...", "code": "..."}
        
        result := ExecuteCommand(content)
        
        ; Write result
        if FileExist(ResultFile)
            FileDelete(ResultFile)
        FileAppend(result, ResultFile, "UTF-8")
        
    } catch as err {
        ; Log error
        try {
            if FileExist(ResultFile)
                FileDelete(ResultFile)
            FileAppend("ERROR: " err.Message, ResultFile, "UTF-8")
        }
    }
}

ExecuteCommand(content) {
    ; Simple JSON parsing for our specific format
    
    ; Extract type
    if RegExMatch(content, '"type"\s*:\s*"([^"]+)"', &typeMatch)
        cmdType := typeMatch[1]
    else
        return "ERROR: No type specified"
    
    switch cmdType {
        case "keystroke":
            ; Extract keys
            if RegExMatch(content, '"keys"\s*:\s*"([^"]+)"', &keysMatch) {
                keys := keysMatch[1]
                ; Unescape common sequences
                keys := StrReplace(keys, "\\n", "`n")
                keys := StrReplace(keys, "\\t", "`t")
                Send(keys)
                return "OK: Sent keys: " keys
            }
            return "ERROR: No keys specified"
            
        case "script":
            ; Extract and execute inline script code
            if RegExMatch(content, '"code"\s*:\s*"((?:[^"\\]|\\.)*)"', &codeMatch) {
                code := codeMatch[1]
                ; Unescape
                code := StrReplace(code, "\\n", "`n")
                code := StrReplace(code, "\\t", "`t")
                code := StrReplace(code, '\\"', '"')
                
                ; Execute each line
                Loop Parse, code, "`n", "`r" {
                    line := Trim(A_LoopField)
                    if (line = "")
                        continue
                    
                    ; Parse and execute command
                    if RegExMatch(line, "i)^Send,?\s*(.+)$", &sendMatch) {
                        Send(sendMatch[1])
                    }
                    else if RegExMatch(line, "i)^Sleep,?\s*(\d+)$", &sleepMatch) {
                        Sleep(Integer(sleepMatch[1]))
                    }
                    else if RegExMatch(line, "i)^Click,?\s*(.*)$", &clickMatch) {
                        Click(clickMatch[1])
                    }
                    else if RegExMatch(line, "i)^MsgBox,?\s*(.+)$", &msgMatch) {
                        MsgBox(msgMatch[1])
                    }
                    ; Add more commands as needed
                }
                return "OK: Script executed"
            }
            return "ERROR: No code specified"
            
        case "run":
            ; Run external program/script
            if RegExMatch(content, '"path"\s*:\s*"([^"]+)"', &pathMatch) {
                path := pathMatch[1]
                path := StrReplace(path, "\\\\", "\")
                Run(path)
                return "OK: Ran: " path
            }
            return "ERROR: No path specified"
            
        case "activate":
            ; Activate a window
            if RegExMatch(content, '"window"\s*:\s*"([^"]+)"', &winMatch) {
                winTitle := winMatch[1]
                if WinExist(winTitle) {
                    WinActivate()
                    return "OK: Activated: " winTitle
                }
                return "ERROR: Window not found: " winTitle
            }
            return "ERROR: No window specified"
            
        default:
            return "ERROR: Unknown command type: " cmdType
    }
}

OpenCommandsFolder(*) {
    Run(A_ScriptDir "\user_data")
}

; ============================================================================
; Hotkeys (optional - can be triggered by voice or keyboard)
; ============================================================================

; Ctrl+Shift+V = Paste as plain text
^+v:: {
    clipSave := A_Clipboard
    A_Clipboard := A_Clipboard  ; Convert to plain text
    Send("^v")
    Sleep(100)
    A_Clipboard := clipSave
}

; ============================================================================
; Built-in voice command macros
; These can be called directly via command file
; ============================================================================

; Example macro functions that can be extended
MemoQAddTerm() {
    Send("!{Down}")
}

MemoQTagNext() {
    Send("^{PgDn}")
    Sleep(100)
    Send("{F9}")
    Sleep(100)
    Send("^{Enter}")
}

TradosConfirm() {
    Send("^{Enter}")
}

CopySourceToTarget() {
    ; Select all in source, copy, move to target, paste
    Send("^a")
    Sleep(50)
    Send("^c")
    Sleep(50)
    Send("{Tab}")
    Sleep(50)
    Send("^v")
}
