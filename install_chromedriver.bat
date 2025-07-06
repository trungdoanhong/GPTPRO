@echo off
echo Installing ChromeDriver manually...
echo.

:: Tao thu muc Downloads neu chua co
if not exist "%USERPROFILE%\Downloads" (
    mkdir "%USERPROFILE%\Downloads"
)

:: Tao thu muc chromedriver
if not exist "%USERPROFILE%\chromedriver" (
    mkdir "%USERPROFILE%\chromedriver"
)

echo Downloading ChromeDriver...
echo Please wait...

:: Tai xuong ChromeDriver (thay doi URL theo version Chrome hien tai)
powershell -Command "& {Invoke-WebRequest -Uri 'https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/win64/chromedriver-win64.zip' -OutFile '%USERPROFILE%\Downloads\chromedriver-win64.zip'}"

if exist "%USERPROFILE%\Downloads\chromedriver-win64.zip" (
    echo ChromeDriver downloaded successfully!
    echo.
    
    :: Giai nen file
    echo Extracting ChromeDriver...
    powershell -Command "& {Expand-Archive -Path '%USERPROFILE%\Downloads\chromedriver-win64.zip' -DestinationPath '%USERPROFILE%\chromedriver' -Force}"
    
    :: Copy chromedriver.exe ra thu muc chinh
    if exist "%USERPROFILE%\chromedriver\chromedriver-win64\chromedriver.exe" (
        copy "%USERPROFILE%\chromedriver\chromedriver-win64\chromedriver.exe" "%USERPROFILE%\chromedriver\chromedriver.exe"
        echo ChromeDriver installed successfully!
        echo Location: %USERPROFILE%\chromedriver\chromedriver.exe
        echo.
        
        :: Them vao PATH
        echo Adding ChromeDriver to PATH...
        setx PATH "%PATH%;%USERPROFILE%\chromedriver" /M
        
        echo.
        echo Installation completed!
        echo Please restart your command prompt and try running the Python script again.
        echo.
        
        :: Xoa file zip
        del "%USERPROFILE%\Downloads\chromedriver-win64.zip"
        
    ) else (
        echo Error: Could not extract ChromeDriver properly.
    )
) else (
    echo Error: Could not download ChromeDriver.
    echo Please check your internet connection and try again.
    echo.
    echo You can also download ChromeDriver manually from:
    echo https://chromedriver.chromium.org/downloads
)

pause 