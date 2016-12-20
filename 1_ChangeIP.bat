@echo off
powershell -command "& {Set-ExecutionPolicy Bypass}"
color e
cls
echo                  _________-----_____
echo        ____------           __      ----__
echo  ___----             ___------              \
echo     ----________       ----  Paul Vu NGUYEN  \
echo                -----__    ^|             _____)
echo                     __-                /     \
echo         _______-----    ___--          \    /)\
echo   ------_______      ---____            \__/  /
echo                -----__    \ --    _          /\
echo                       --__--__     \_____/   \_/\
echo                               ---^|   /          ^|
echo                                  ^| ^|___________^|
echo                                  ^| ^| ((_(_)^| )_)
echo                                  ^|  \_((_(_)^|/(_)
echo                                   \             (
echo                                    \_____________)
@echo.
@echo.
@echo.
@set /p Name_Machine=Tien hanh FakeIP cho may so :: 
powershell -command .\changeIP %Name_Machine%
@echo.
@echo.

:END
