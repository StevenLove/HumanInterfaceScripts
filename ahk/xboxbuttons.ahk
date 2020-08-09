#NoEnv
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#Include lib.ahk
#SingleInstance, force

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; D PAD ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

dpadBindings := [] ;this is array which will hold 4 items of data, with povdir as a key and the text to send as a value
dpadBindings.insert(0,"Up") ;if joypov = 0  send this text
dpadBindings.insert(9000,"Right")
dpadBindings.insert(18000,"Down")
dpadBindings.insert(27000,"Left")
settimer,checkBindings,50 ;check bindings every 50ms

checkBindings:
angle := GetKeyState("joyPov","p")
dir := dpadBindings[angle]
if (dir && (dir != lastDir)){
    lastDir = dir;
    if(dir = "Up"){
        Send {WheelUp}
    }
    if(dir = "Down"){
        Send {WheelDown}
    }
    if(dir = "Right"){
        Send {WheelRight}
    }
    if(dir = "Left"){
        Send {WheelLeft}
    }
}
; if dpadBindings[dir] { ;this is checking if there is a key equal to this direction, if the dir = 4500 it would not work since we don't have that key in our array
; 	if (dir != lastDir) { ;only send if the joy just was pressed, to prevent spamming
; 		send % dpadBindings[dir]
;         lastDir := dir
; 	}
; }


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Other buttons ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


Joy1:: 
    Click Down
    ; RegularMouseDown()
    KeyWait Joy1
    Click Up
    ; RegularMouseUp()
    return
Joy2::
    FreezeMouse()
    KeyWait Joy2
    FreezeMouseOff()
    return
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