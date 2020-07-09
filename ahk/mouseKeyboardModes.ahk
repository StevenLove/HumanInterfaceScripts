#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance, force


#Include lib.ahk



#If mode == "mouse"
    e:: BlockInput, MouseMove
    e Up:: BlockInput, MouseMoveOff

    f:: 
        FreezeMouseDown()
        return
    f Up::
        FreezeMouseUp()
        return
    a:: MouseClick, Left
    d::
        MouseClick, Right
        return
    s::
        MouseClick, Left
        MouseClick, Left
        return
    j:: send, {WheelDown 1}
    k:: send, {WheelUp 1}

    ~b::
    ~g::
    ~h::
    ~i::
    ~m::
    ~n::
    ~o::
    ~p::
    ~q::
    ~r::
    ~t::
    ~u::
    ~v::
    ~w::
    ~x::
    ~y::
    ~z::
    ~Space::
    ~LShift::
    ~RShift::
        mode:="keyboard"
        SetCapsLockState, Off
        return
#If ; end of IF
~CapsLock::
    mode:="mouse"

