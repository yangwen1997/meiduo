@echo
FOR  /L %%i IN (26, 1, 29) DO (
start cmd /k python main.py "%%i"
ping -n 10 127.0.01>null
)