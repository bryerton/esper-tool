.. image:: https://travis-ci.org/bryerton/esper-tool.svg?branch=master
    :target: https://travis-ci.org/bryerton/esper-tool

==========
ESPER TOOL
==========

Overview
--------
A python-based command line utility for accessing a device running the ESPER web service. Works with Python 2 and 3. 

The tool allows for the reading and writing of ESPER variables via the command line.

The available subcommands are:

- `interactive`_
- `read`_
- `write`_
- `upload`_
- `download`_

For a list of interactive shell commands type `help` in the interactive shell prompt

Installation
------------
The recommended installation method is via pip

  To install:
    `pip install esper-tool`
  To upgrade:
    `pip install -U esper-tool`
  To run it locally from the github source:
    `python -m esper_tool`

Interactive
-----------
 Command:
  `esper-tool interactive [-h] [-u USER] [-p PASS] <url> [mid]`

 Purpose:
  Connects to an esper service located at `url` and opens an interactive shell 
 
 Options:
  `-h`
  
  `--help`
   Print out help for this subcommand 
 
  `-u USER`
  
  `--user USER`
   User to use for HTTP basic authentication
 
  `-p PASS`
  
  `--password PASS`
   Password to use for HTTP basic authentication. If `-u` is specified, but `-p` is not, the user will be prompted for a password

  `url`
   Location of ESPER web service given in standard web URL format. If the port is excluded, it defaults to 80

  `mid`
   Module ID or MID to start in. May be given as numerical value, or module key. 

Read
----
 Command:
  `esper-tool read [-h] [-u USER] [-p PASS] [-o OFFSET] [-l LEN] <url> <mid> <vid>`
 
 Purpose:
  Read an ESPER variable's data, located at URL. Return value is JSON data type
 
 Options:
  `-h`
  
  `--help`
   Print out help for this subcommand

  `-u USER`
  
  `--user USER`
   User to use for HTTP basic authentication
 
  `-p PASS`
  
  `--password PASS`
   Password to use for HTTP basic authentication. If `-u` is specified, but `-p` is not, the user will be prompted for a password

  `-o OFFSET`

  `--offset OFFSET`
   Element to start read at within ESPER variable. Defaults to first element (0)

  `-l LEN`

  `--len LEN`
   Number of elements to read

  `url`
   Location of ESPER web service given in standard web URL format. If the port is excluded, it defaults to 80

  `mid`
   Module ID or MID. May be given as numerical value, or module key. 

  `vid`
   Variable ID or VID. May be given as numerical value, or variable key. 

 Examples:
  `esper-tool read -o 1 -l 32 localhost:8080 0 0`
   Reads `32` elements of variable `0` starting at offset `1`, at` localhost:8080` module `0`, variable `0`

Write
-----
 Command:
  `esper-tool write [-h] [-u USER] [-p PASS] [-d DATA] [-f FILE] [-o OFFSET] <url> <mid> <vid>`
 
 Purpose:
  Writes JSON data to an ESPER variable. May write the full array or a slice. Data can be specified on the command line or by a file
 
 Options:
  `-h`
  
  `--help`
   Print out help for this subcommand 

  `-u USER`
  
  `--user USER`
   User to use for HTTP basic authentication
 
  `-p PASS`
  
  `--password PASS`
   Password to use for HTTP basic authentication. If `-u` is specified, but `-p` is not, the user will be prompted for a password

  `-d DATA`

  `--data DATA`
   JSON data to write. May take the form of any standard JSON datatype. Datatype must be compatible with ESPER datatype of variable

  `-f FILE`

  `--file FILE`
   File containing JSON data to be written to variable. Same as `-d` but data is written in FILE 

  `-o OFFSET`

  `--offset OFFSET`
   Element to start read at within ESPER variable. Defaults to first element (0)

  `url`
   Location of ESPER web service given in standard web URL format. If the port is excluded, it defaults to 80

  `mid`
   Module ID or MID. May be given as numerical value, or module key. 

  `vid`
   Variable ID or VID. May be given as numerical value, or variable key. 

 Examples:
  `esper-tool write -d 255 localhost 1 2`
   Writes the value `255` to module `1`, variable `2` at `localhost`

  `esper-tool write -d [0,2] -o 1 http://localhost:8080 mymodule myvar`
   Writes the array `[0,2]` to the variable `myvar` starting at the second element. The variable is located in the module `mymodule` on host `localhost:8080` 

Upload
------

 Command:
  `esper-tool upload [-h] [-u USER] [-p PASS] -f FILE [-r RETRY] <url> <mid> <vid>`
 
 Purpose:
  Upload a binary file to an ESPER variable. Particularly useful for updates to large variable arrays, binary data must match binary format of ESPER variable, or data loaded will be erroneous. 
 
 Options:
  `-h`
  
  `--help`
   Print out help for this subcommand 

  `-u USER`
  
  `--user USER`
   User to use for HTTP basic authentication
 
  `-p PASS`
  
  `--password PASS`
   Password to use for HTTP basic authentication. If `-u` is specified, but `-p` is not, the user will be prompted for a password

  `-f FILE`

  `--file FILE`
   File containing binary data to be written to variable

  `-r RETRY`

  `--retry RETRY`
   Number of times to retry if timeout occurs, can be useful if ESPER service connected to is slow to write to disk/flash
  
  `url`
   Location of ESPER web service given in standard web URL format. If the port is excluded, it defaults to 80

  `mid`
   Module ID or MID. May be given as numerical value, or module key. 

  `vid`
   Variable ID or VID. May be given as numerical value, or variable key. 

 Examples:
  `esper-tool upload -v --file ~/waveform.bin -r 3 http://localhost:80/ 5 waveform_replay`
   Uploads the contents of file `waveform.bin` to `localhost` module `5`, variable `waveform_replay`. It will retry `3` times in the event of failure

Download
--------
 Command:
  `esper-tool download [-h] [-u USER] [-p PASS] -f FILE [-r RETRY] <url> <mid> <vid>`
 
 Purpose:
  Downloads variable data to a binary file.
 
 Options:
  `-h`
  
  `--help`
   Print out help for this subcommand 

  `-u USER`
  
  `--user USER`
   User to use for HTTP basic authentication
 
  `-p PASS`
  
  `--password PASS`
   Password to use for HTTP basic authentication. If `-u` is specified, but `-p` is not, the user will be prompted for a password

  `-f FILE`

  `--file FILE`
   Location of file to write variable data to

  `-r RETRY`

  `--retry RETRY`
   Number of times to retry if timeout occurs, can be useful if ESPER service connected to is slow to write to disk/flash
  
  `url`
   Location of ESPER web service given in standard web URL format. If the port is excluded, it defaults to 80

  `mid`
   Module ID or MID. May be given as numerical value, or module key. 

  `vid`
   Variable ID or VID. May be given as numerical value, or variable key. 

 Examples:
  `esper-tool download -v --file ~/waveform.bin -r 3 http://localhost:80/ 5 waveform_replay`
   Download the contents of file `localhost` module `5`, variable `waveform_replay` to `waveform.bin`. It will retry `3` times in the event of failure
