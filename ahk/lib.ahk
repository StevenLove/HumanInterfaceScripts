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
FreezeMouse(){
    BlockInput, MouseMove
}
FreezeMouseOff(){
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