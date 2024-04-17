::
:: Copy files from local windows system to remote raspberry pi
::

:: Pi
:: In batch text variables are defined with "set VARIABLE_NAME=VARIABLE_VALUE"
:: In batch these variables are referenced with %VAR_NAME%
:: Double quotes are not needed in general. But we do still do it. Explanation follows ...
set USER="jb"
set TARGET_IP="10.23.42.7"

:: Folders
:: Windows Paths
:: Here double Quotes are NEEDED for absolute windows path, if a ":" is contained.
:: With double quotes the scp command syntax is satisfied. So any absoluet path must be in double quotes.
:: Therefore we just simply define all text variables with double quotes.
set LOCAL_FOLDER="C:\Users\root\python_scmi"
set REMOTE_FOLDER="/home/jb/mps/scratch/python_scmi"

:: Quart app and status files in the remote raspberry pi directory
set EXECUTE_FILE="main.py"
set PID_FILE="current.pid"
set LOG_FILE="serverlog.log"


:: We define variables here in this batch-script, 
:: but we need the variables also within the envioronments of the ssh commands (We use bash there)
:: So we define a "batch" variable conatining all needed "bash" variables.
:: In each ssh call we can then export them with "export %ENV_VARS%".
:: On evaluation the "batch" variables with %VARIABLE% are evaluated and printed as "text" into the export command.
:: --> The export command takes this text and exports it into the current "bash" environment as environment variable. 
:: --> After doing that the variables can be reference with "bash" synatx:
:: --> For example: echo $EXECUTE_FILE
set ENV_VARS=REMOTE_FOLDER=%REMOTE_FOLDER% EXECUTE_FILE=%EXECUTE_FILE% PID_FILE=%PID_FILE% LOG_FILE=%LOG_FILE%

:: Create folder
:: make directory. "-p" enforces creation of subfolders if they are needed
:: mkdir /folderA/folderB fails if "/folderA" does not exist
:: mkdir -p /folderA/folderB succeeds as -p enforces the creation of "/folderA" BEFORE "/folderA/folderB". 
ssh %USER%@%TARGET_IP% export %ENV_VARS% ; "mkdir -p $REMOTE_FOLDER"

:: Copy files
:: Copy recursively with "-r"
:: --> scp -r SRC DST
:: Only copy files not the folder with "/*"
:: --> scp -r %LOCAL_FOLDER%/* ...
scp -r %LOCAL_FOLDER%/* %USER%@%TARGET_IP%:%REMOTE_FOLDER% 

:: Kill old, if exists
:: Change to project directory.
:: Check if file exists with "-f" in if-statement 
:: --> if [[ -f $PID_FILE ]] ; then ... 
:: kill process by using pidfile with "-F"
:: --> pkill -F $PID_FILE
:: Remove file afterwards with "rm"
ssh %USER%@%TARGET_IP% export %ENV_VARS% ; "cd $REMOTE_FOLDER ; if [[ -f $PID_FILE ]] ; then pkill -F $PID_FILE ; rm $PID_FILE ; fi"

:: Run process and store pid
:: Change to project directory.
:: Execute python file with "python3 $EXECUTE_FILE"
:: --> Log into logfile with " > $LOGFILE". ">" Redirects only stdout not stderr!
:: --> Redirect stderr to stdout with "2>&1". Otherwise only the regular output, but no errors would be logged
:: --> Run process in background with "&" such that the batch-script is not waiting for the return of that command.
:: This is needed as we start a web-service with "python3 $EXECUTE_FILE" which does not return until interrupted.
:: Finally write pid of started process into pidfile with "echo $! > $PID_FILE"
:: --> "$!" evaluates to the pid of the process being started last. with echo we print it to stdout. With "> $PID_FILE" we write stdout to the pidfile
ssh %USER%@%TARGET_IP% export %ENV_VARS% ; "cd $REMOTE_FOLDER ; python3 $EXECUTE_FILE > $LOG_FILE 2>&1 & echo $! > $PID_FILE"
