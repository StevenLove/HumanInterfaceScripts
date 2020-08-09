#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance, force
#Include lib.ahk

global mode

mode:="click"
UpdateMode(){
    global mode
    mode := GetGlobal("footMode")
}

SetTimer, UpdateMode, 500

; !+s::mode:="scroll"
; !+c::mode:="click"

#If mode == "scroll"
    $F14:: Send, {WheelUp}
    $F15:: Send, {WheelDown}
#If mode == "click"
    $F14:: FreezeMouseDown()
    $F14 Up:: FreezeMouseUp()
; F15:: handled by FreePIE to jump cursor to my gaze

; $F22:: MouseClick, Right
; $F22:: CenterMouse()
; $F15:: Send, {F15}
#If


