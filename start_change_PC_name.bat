@set /p Name_Machine= Please put your machine name : 
wmic computersystem where name="%COMPUTERNAME%" call rename name="%Name_Machine%"
shutdown.exe /r /t 00