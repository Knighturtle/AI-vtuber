#Requires AutoHotkey v2.0
#SingleInstance Force

; VSeeFace をアクティブにする（タイトルに VSeeFace が含まれるウィンドウ）
if WinExist("VSeeFace")
{
    WinActivate("VSeeFace")
    Sleep 600
}
else
{
    MsgBox "VSeeFace window not found. Open VSeeFace first."
    ExitApp
}

; あなたの割り当てに合わせる（画像より）
Send "^+{F2}"   ; Fun
Sleep 1200
Send "^+{F3}"   ; Angry
Sleep 1200
Send "^+{F1}"   ; Neutral（ある場合）

ExitApp

