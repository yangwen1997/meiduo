@echo
FOR  /L %%i IN (1, 1, 10) DO (
start cmd /k python main.py "%%i"
ping -n 10 127.0.01>null
)