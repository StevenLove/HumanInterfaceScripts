#Persistent
#SingleInstance force
#Include XInput.ahk
#Include lib.ahk
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.



XInput_Init()

ReleasePressedDirectionalKey(key)
{
    ; Send {Left}
	; GetKeyState, state, %key%
	; if state = D
	; 	Send {%key% up}
}

LSSensitivity := 0.5/1000
RSSensitivity := 1.8/1000

Thread, interrupt, 0  ; Make all threads always-interruptible.

SetTimer, Sticks, 5
SetTimer, UpdateStickSpeed, 50
return

UpdateStickSpeed:
	; global stickSpeed
	stickSpeed := GetGlobal("stickSpeedMultiplier")
	; ToolTip, stickspeed: %stickSpeed%
	; IniRead, stickSpeed, inis\globals.ini, globals, stickSpeedMultiplier
	; ToolTip % "The value is " . stickSpeed . "."


Sticks:
	; global stickSpeed
    Loop, 4 {
        if state := XInput_GetState(A_Index-1) {
			
			LSx := state.sThumbLX
			LSy := state.sThumbLY
			RSx := state.sThumbRX
			RSy := state.sThumbRY
			
			; if (abs(LSx) < XINPUT_GAMEPAD_LEFT_STICK_DEADZONE)
			; {
			; 	ReleasePressedDirectionalKey("WheelRight")
			; 	ReleasePressedDirectionalKey("WheelLeft")
			; 	LSx := 0
			; 	xDirection := ""
			; 	xDirectionLast := ""
			; }				
			; if (abs(LSy) < XINPUT_GAMEPAD_LEFT_STICK_DEADZONE)
			; {
			; 	ReleasePressedDirectionalKey("WheelUp")
			; 	ReleasePressedDirectionalKey("WheelDown")
			; 	LSy := 0
			; 	yDirection := ""
			; 	yDirectionLast := ""
			; }
			; if LSx
			; 	xDirection := LSx > 0 ? "WheelRight" : "WheelLeft"
			; if LSy
			; 	yDirection := LSy > 0 ? "WheelUp" : "WheelDown"
			; ;MsgBox % LSx . " / " . xDirection . " / " . xDirectionLast . " / " . LSy . " / " . yDirection . " / " . yDirectionLast
			; if (xDirection != "") ;&& xDirection != xDirectionLast)
			; {
			; 	ReleasePressedDirectionalKey(xDirectionLast)
			; 	Send {%xDirection%}
			; 	xDirectionLast := xDirection
			; }
			; if (yDirection != "") ; && yDirection != yDirectionLast)
			; {
			; 	ReleasePressedDirectionalKey(yDirectionLast)
			; 	Send {%yDirection%}
			; 	yDirectionLast := yDirection
			; }
			;8 689 = RS dead zone
			;24 078 = RS live zone
			;32 767	= radius
			RSHypotenuse := sqrt(RSx * RSx + RSy * RSy)
			if (RSHypotenuse > XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE) {
				RSValue := RSHypotenuse - XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE
				RSValueInProportion := RSValue / (32767 - XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE)
				;MsgBox % RSx . " - " . RSy . " - " . RSHypotenuse . " - " . RSValue . " - " . RSValueInProportion
				SetMouseDelay, -1 ; Makes movement smoother.
				if RSValueInProportion > 1
					RSValueInProportion := 1
				S := (1 - RSValueInProportion) * 100
				RSx *= RSValueInProportion * RSSensitivity				
				RSy *= RSValueInProportion * RSSensitivity				
				MouseMove, RSx, -RSy, S, R
			}


			LSHypotenuse := sqrt(LSx * LSx + LSy * LSy)
			if (LSHypotenuse > XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE) {
				LSValue := LSHypotenuse - XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE
				LSValueInProportion := LSValue / (32767 - XINPUT_GAMEPAD_RIGHT_STICK_DEADZONE)
				;MsgBox % LSx . " - " . LSy . " - " . LSHypotenuse . " - " . LSValue . " - " . LSValueInProportion
				SetMouseDelay, -1 ; Makes movement smoother.
				if LSValueInProportion > 1
					LSValueInProportion := 1
				S := (1 - LSValueInProportion) * 100
				LSx *= LSValueInProportion * LSSensitivity * stickSpeed
				LSy *= LSValueInProportion * LSSensitivity * stickSpeed
				MouseMove, LSx, -LSy, S, R
			}
        }
    }
return