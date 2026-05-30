@echo off
cd /d "C:\Users\jia'yue\WorkBuddy\Claw\geo-repo"
"C:\Users\jia'yue\.workbuddy\binaries\python\versions\3.13.12\python.exe" auto_geo_v3.py
echo Exit code: %ERRORLEVEL%
exit /b %ERRORLEVEL%
