
.PHONY: default start stop restart clean

default: restart

start:
	python3 main.py & 

stop:
	-pkill -f "python3 main.py"

restart: | stop start 

