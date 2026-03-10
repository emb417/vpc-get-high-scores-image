CD /d %~dp0
set _curloc=%~dp0
for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set _ParentFolderName=%%~dpnxJ
echo %_ParentFolderName%
echo %_curloc%

REM Weekly leaderboard — reads from current week, saves to BackGlass
"%_curloc%vpc-get-high-scores-image.exe" "weekly" "%_ParentFolderName%\POPMedia\Default\BackGlass" "pl_TOTW" "" "20" "landscape"
