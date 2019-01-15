# EGML
## Authors
2014:
Mark Sgobba 
Trever Toryk 

## LICENSE

This software is to be considered free and open-source, though attempts to sell this software or any modified copies of this software are hereby PROHIBITED.

## PREREQUISITES

This version was developed and tested on Python 3.4.0 (the original CPython variant).  While it will likely work with versions of CPython in the v3 family, we haven't tested this and so it is not supported.  The same goes for the other variants of Python (Jython, IPython, PyPI).  Due to syntactical differences, Python 2.X will definitely NOT work with this library.

Other than what is included in the default Python installation, no other libraries are needed.

## INSTRUCTIONS

From the command line:

python3 reason.py

From any Python application (incl. Python IDLE):

import reason

(Note that this will put you directly in EGML manipulation mode, where it accepts commands.)

If you just want to use the objects and functionality of EGML and not the command line application:

import egml

### egml.py

This file contains:

*The existential graph error library (all exceptions starting with "EG")
*The copy_graph() function (which clones graphs or portions of graphs)
*The Level object class (in existential graph-speak, a "cut" or "sublevel")
*The Sheet object class (again, in e.g.-speak, the "sheet of assertion", a derivation of the Level object)

The way this program works is by creating a tree which is representative of an existential graph:

				____________________________
			   |							|
			   |	(A)						|
			   |			( (B) (C) )		|
			   |							|
			   |____________________________|
			   
							 ^
							 |
							 |
							 |
							 v
							 
							[ ]
							/ \
						   /   \
						 (A)   ( )
							   / \
							  /   \
							(B)   (C)
							
...internally, of course.  There are functions that you can use to do this (and they are all well-notated inside the file).

### reason.py

reason.py provides the user frontend to the EGML objects and functions.  It specifies a command-line application that can be used to string together objects and create trees easily and quickly.

The item between the square brackets ([ ]) is the item you are currently running commands on.  We call it the "context".  To change objects, use the "select" command.

To find a list of available commands, type "help" or "?" into the command line and press enter.

To work this program, first create the tree you want to operate on.  Start with "new sheet" and then use "create" statements to create new levels and atoms.  (If you make a mistake, there are "delete" commands as well.)  We call this stage "setup mode".  In setup mode, strict enforcement of the EG rules is disabled.

To switch to the strict rule-checking mode (and to thereby solve the EG), use the "mode solve" command.  Note that when you do this, there's no going back.

After going into solve mode, you can only use EG rules (insert/remove doublecut, insert, remove, (de)iterate).

To create the graphs to insert or iterate, use the "create level", which will create a new disconnected level to run commands on.  You can break the canonical rules, but only on this level!  Once you place it in the graph, it starts being rule-checked like everything else.

To view the current state of the tree/graph, use the print command (in either setup or solve mode).  It will print the state of the tree FROM THE CURRENT NODE.  To get the whole tree, call print from the sheet of assertion ("select 0" then "print").

## FUTURE IDEAS

*Logging to a file - make a graph "save-able" and "load-able" by simply logging the actions to a text file.  A submission to a "Grade Grinder"-like server could determine the authenticity of the text log.
*On that note, a Python server-esque application that determines whether or not a logged graph was created validly and follows all the rules.
*A GUI component that displays the actual existential graph instead of the tree notation that we use.
*A GUI that uses reason.py to create, display, and manipulate existential graphs.
