@echo on
title Worldquant Collect Theme
cd %~dp0src
javac GUI_Main.java
java GUI_Main
del *.class
exit
