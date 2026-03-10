CD /d %~dp0
set _curloc=%~dp0
for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set _ParentFolderName=%%~dpnxJ
echo %_ParentFolderName%
echo %_curloc%

start playsound UpdateHighScoreStart.mp3

REM High scores leaderboard — reads from VPS high scores, saves to Other2
"%_curloc%vpc-get-high-scores-image.exe" "True" "" "CUSTOM3" "%_ParentFolderName%" "%_ParentFolderName%\POPMedia\Visual Pinball X\Other2" "20" "" "landscape"

start playsound UpdateHighScoreStop.mp3
