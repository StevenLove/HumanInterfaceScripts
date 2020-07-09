#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#Include lib.ahk

Numpad0:: ScrollDown()
NumpadEnter:: ScrollUp()
Numpad4:: FreezeMouseDown()
Numpad4 Up:: FreezeMouseUp()
Numpad5:: DoubleClick()

Numpad6:: RightClick()