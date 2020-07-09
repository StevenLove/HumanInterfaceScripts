#persistent
dpadBindings := [] ;this is array which will hold 4 items of data, with povdir as a key and the text to send as a value
dpadBindings.insert(0,"Up") ;if joypov = 0  send this text
dpadBindings.insert(9000,"Right")
dpadBindings.insert(18000,"Down")
dpadBindings.insert(27000,"Left")
settimer,checkBindings,50 ;check bindings every 50ms
return

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