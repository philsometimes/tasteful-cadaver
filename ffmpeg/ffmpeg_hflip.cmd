:: ffmpeg_hflip.cmd 2018-03-22
:: batch file for horizontally flipping .avis
:: drag and drop valid files and folders onto this batch file to execute
:: requires ffmpeg in PATH/environmental variables

@echo off
:checkfileordir
if "%~x1" EQU ".avi" (goto iffile) else (goto ifdir)

:iffile
ffmpeg -i "%~1" -q:a 0 -q:v 0 -vf  hflip "%~dpn1HFLIP.avi" -y
goto end

:ifdir 
cd\
for /r %~1 %%f in (*.avi) do (
   ffmpeg -i "%%f" -q:a 0 -q:v 0 -vf  hflip "%%~dpnfHFLIP.avi" -y
   REM ~dpn expands loop variable %%f to drive letter, path and filename, removing extension
)
goto end
:end
PAUSE