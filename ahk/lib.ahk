SetGlobal(key,val){
    IniWrite, %val% , inis\globals.ini , globals , %key%
}

GetGlobal(key){
    IniRead, temp, inis\globals.ini, globals, %key%
    return temp
}
RightClick(){
    MouseClick, Right
}
ScrollDown(){
    send, {WheelDown 1}
}
ScrollUp(){
    send, {WheelUp 1}
}
Doubleclick(){
    MouseClick, left
	MouseClick, left
	return
}
CloseWindow(name){
    if WinExist(name)
        WinClose ; use the window found above
}

FreezeMouse(){
    ; SetGlobal("stickSpeedMultiplier",0)
    BlockInput, MouseMove
}
FreezeMouseOff(){
    ; SetGlobal("stickSpeedMultiplier",1)
    BlockInput, MouseMoveOff
}
FreezeMouseDown(){
    global freezeMouseActive ; 
    ; MsgBox "reezemousedown " %freezeMouseActive%
    if(freezeMouseActive = true){
        ; MsgBox Mouse already Frozen
        return
    }
    freezeMouseActive:=true
    Click down
    FreezeMouse()
    sleep, 350
    FreezeMouseOff()
    return
}
FreezeMouseUp(){
    global freezeMouseActive
    freezeMouseActive:=false
    Click up
    FreezeMouseOff()
    return
}

RegularMouseDown(){
global freezeMouseActive ; 
    ; MsgBox "reezemousedown " %freezeMouseActive%
    if(freezeMouseActive = true){
        ; MsgBox Mouse already Frozen
        return
    }
    freezeMouseActive:=true
    Click down
    return
}
RegularMouseUp(){
global freezeMouseActive
    freezeMouseActive:=false
    Click up
    return
}
CenterMouse(){
    ; x := (A_ScreenWidth // 2)
    ; y := (A_ScreenHeight // 2)
    ; ToolTip "X %x% y %y%"
    ; mousemove, x, y
    CoordMode, Mouse, Screen
    MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2)
}
ClearTooltips(){
    ToolTip
}
StartScript(path){
    Run,%path%
}
EndScript(path){
    DetectHiddenWindows,on
    SetTitleMatchMode,2
    WinKill,%path%
}


SetTimer, ClearTooltips, 8000

; ^!r::Reload  ; Assign Ctrl-Alt-R as a hotkey to restart the script.
; this seems to break xbox sticks...-