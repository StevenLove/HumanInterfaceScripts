#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance, force
#Include lib.ahk

global mode

mode:="click"
; UpdateMode(){
;     global mode
;     mode := GetGlobal("footMode")
; }

; SetTimer, UpdateMode, 100

!+s::mode:="scroll"
!+c::mode:="click"

#If mode == "scroll"
    $F21:: Send, {WheelDown}
    $F22:: Send, {WheelUp}
#If mode == "click"
    $F21:: FreezeMouseDown()
    $F21 Up:: FreezeMouseUp()
    $F22:: MouseClick, Right
#If


