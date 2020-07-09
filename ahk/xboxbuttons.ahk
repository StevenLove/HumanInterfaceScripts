#NoEnv
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#Include lib.ahk
#SingleInstance, force


Joy1:: 
    Click Down
    ; RegularMouseDown()
    KeyWait Joy1
    Click Up
    ; RegularMouseUp()
    return
Joy2::FreezeMouse()
Joy2 Up:: FreezeMouseOff()
Joy3::
    MouseClick, Right
    ; Send, {Space Down}
    ; KeyWait Joy3
    ; Send {Space Up}
    return
Joy8::
    Send, {Esc Down}
    KeyWait Joy8
    Send {Esc Up}
    return

; LB -> Back, RB -> Forward
Joy5::
    Send, !{Left}
    ; Send, {Alt down Left Alt Up}
    ; Send, {Browser_Back}
    return
Joy6::
    Send, !{Right}
    ; Send, {Browser_Forward}
    return
Joy4::
    Send, {Space Down}
    KeyWait Joy4
    Send {Space Up}
    return
Joy9::
    Send, {Ctrl Down}
    SetGlobal("stickSpeedMultiplier",4)
    KeyWait Joy9
    Send {Ctrl Up}
    SetGlobal("stickSpeedMultiplier",1)
    return

; Joy1 = (A)
; Joy2 = (B)
; Joy3 = (X)
; Joy4 = (Y)
; Joy5 = (LB)
; Joy6 = (RB)
; Joy7 = (back)
; Joy8 = (start)
; Joy9 = (click left stick)
; Joy10 = (click right stick)