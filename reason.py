#	Existential Graph Manipulation Library
#	
#	reason.py
#
#	The user interface to the EGML objects.

from egml import Sheet, Level, copy_graph
import sys
import traceback

def EG_reason():
	context = None	# The item commands are being run on
	all_items = {}	# All items not otherwise connected (the sheet of assertion plus any other disconnected graph portions.
					# NOTE: the sheet of assertion will always be all_items[0].  Any other disconnected graph pieces (like pieces created using "create") are stored in here by ID.
	mode = "setup"	# "setup" means that any action is allowed.  "solve" means that only logical EG actions can be performed on the tree.
	
	while True:
		command = None
		if mode == "setup" and context:
			context_representation = context.context_repr + "*"
		elif mode == "setup":
			context_representation = "*"
		elif mode == "solve" and context:
			context_representation = context.context_repr
		elif mode == "solve" and not context:
			context_representation = ""
			
		command = input('[' + context_representation + '] ')
		
		command_args = command.split(' ')
		recognized = True
		
		if mode == "solve":
			if len(command_args) == 1:
				if command_args[0] == 'help' or command_args[0] == '?':
					print("Here are a list of possible commands to run:")
					print("\thelp                         Shows this dialog.")
					print("\tversion                      Shows the version number.")
					print("\tspam                         Does nothing.  (No really.  This is not a Monty Python joke.)")
					print("\tselect <id>                  Changes the selected Level (what is in between the [ and ]) to the object")
					print("\t                             with id <id>.")
					print("\tinsert doublecut [atoms]     Inserts 2 Levels (around the selected Level or, if supplied, around [atoms]")
					print("\t                             (comma-separated) in this level.")
					print("\tremove doublecut             Intelligently removes 2 Levels, either the selected Level and the one above, or")
					print("\t                             the Level and the one below.")
					print("\tinsert <atom>                Inserts <atom> at the Level selected.")
					print("\tinsert <id>                  Inserts the graph with the id of <id> at the selected Level.")
					print("\tremove <atom>                Removes <atom> from the selected Level.")
					print("\tremove <id>                  Removes the graph with the id of <id> from the selected Level.")
					print("\titerate <atom>               Inserts <atom> at the selected Level using a Level above as the logical")
					print("\t                             justification.")
					print("\titerate <id>                 Inserts Level with id <id> at the selected Level, finding the justification")
					print("\t                             automagically.")
					print("\tdeiterate <atom>             Removes <atom> from the selected Level using a Level above as the logical")
					print("\t                             justification.")
					print("\tdeiterate <id>               Removes Level with id <id> from the selected Level, finding the justification")
					print("\t                             automagically.")
					print("\tcreate level                 Creates a new, nonconnected Level.  You can add things to that Level freely.  This")
					print("\t                             Level can only be used for iteration or insertion.")
					print("\tprint                        Prints the current state of the EG at the selected Level.  Go to level id 0")
					print("\t                             (sheet) to print the whole EG.")
					print("\tinfo                         Prints information about the selected level.")
					print("\tquit                         Quits the reason() loop.")
					
				elif command_args[0] == 'version':
					print("\tEGML version 0.1a4140")
					print("\tThis version does not include spam.")
					
				elif command_args[0] == 'spam':
					# Background: it's necessary in every Python program to make a reference to Monty Python.  Here's mine.  ~Trevor
					print("\tMenu:")
					print("\tEgg and spam")
					print("\tEgg, bacon, and spam")
					print("\tEgg, bacon, sausage, and spam")
					print("\tSpam, bacon, sausage, and spam")
					print("\tSpam, egg, spam, spam, bacon, and spam")
					print("\tSpam, spam, spam, egg, and spam")
					print("\tSpam, spam, spam, spam, spam, spam, baked beans, spam, spam, spam, and spam")
					
				elif command_args[0] == 'print':
					try:
						print(context)
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
						
				elif command_args[0] == 'info':
					print("\t" + context.context_repr + ":")
					print("\tid: " + str(context.id))
					if type(context) is Level:
						print("\tparent: " + str(context.parent.context_repr))
					elif type(context) is Sheet:
						print("\tparent: " + str(context.parent))
					print("\tdepth: " + str(context.depth))
					print("\tatoms: " + str(context.atoms))
					print("\tchildren: ")
					for child in context.children:
						print("\t\t" + child.context_repr)
						
				elif command_args[0] == 'quit':
					break
					
				elif command_args[0] == '':
					pass
					
				else:
					recognized = False
					
			elif len(command_args) == 2:
				if command_args[0] == 'insert' and command_args[1] == 'doublecut':
					try:
						context.ins_doublecut()
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
						
				elif command_args[0] == 'remove' and command_args[1] == 'doublecut':
					try:
						new_context = context.rem_doublecut()
						context = new_context
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
						
				elif command_args[0] == 'select':
					if command_args[1].isdigit():
						new_context = all_items[0].find(int(command_args[1]))
						if not new_context:
							try:
								new_context = all_items[int(command_args[1])]
							except:
								new_context = context
								print("ERROR: id not found")
						context = new_context
					else:
						print("ERROR: that's no id!")
						
				elif command_args[0] == 'insert':
					if command_args[1].isalpha():
						try:
							context.insert(atom = command_args[1])
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
					elif command_args[1].isdigit():
						# NOTE: you can only do this if you use "create level" to create a new, disconnected level and then add things to it.  Then pass that level as the id in insert.
						#try:
							context.insert(level = all_items[int(command_args[1])])
							del all_items[int(command_args[1])]					# Removes the disconnected level from all_items
						#except:
							#type_, value_, tb_ = sys.exc_info()
							#print(value_)
						
				elif command_args[0] == 'remove':
					if command_args[1].isalpha():
						try:
							context.remove(atom = command_args[1])
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
							
					elif command_args[1].isdigit():
						found_item = all_items[0].find(int(command_args[1]))
						if found_item:
							try:
								context.remove(level = found_item)
							except:
								type_, value_, tb_ = sys.exc_info()
								print(value_)
						else:
							print("ERROR: given id not found.")
					else:
						print("ERROR: that's not an atom or id!")

				elif command_args[0] == 'iterate':
					if command_args[1].isalpha():
						try:
							context.iterate(atom = command_args[1])
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
							
					elif command_args[1].isdigit():
						found_item = all_items[0].find(int(command_args[1]))
						if found_item:
							try:
								# This extra step makes a copy of the subgraph to iterate...that way we don't make pointer mistakes in the graph.
								copy_found_item = copy_graph(all_items[0], found_item)
								context.iterate(level = copy_found_item)
							except:
								type_, value_, tb_ = sys.exc_info()
								print(value_)
						
				elif command_args[0] == 'deiterate':
					if command_args[1].isalpha():
						try:
							context.deiterate(atom = command_args[1])
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
							
					elif command_args[1].isdigit():
						found_item = all_items[0].find(int(command_args[1]))
						if found_item:
							try:
								context.deiterate(level = found_item)
							except:
								type_, value_, tb_ = sys.exc_info()
								print(value_)
					
				elif command_args[0] == 'create' and command_args[1] == 'level':
					try:
						new_level = Level(None, new_id = all_items[0].get_next_id())
						all_items[new_level.id] = new_level
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
					
				else:
					recognized = False
					
			elif len(command_args) == 3:
				if command_args[0] == 'insert' and command_args[1] == 'doublecut':
					if command_args[2].isalpha():
						try:
							context.ins_doublecut(command_args[2])
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
							
					else:
						try:
							context.ins_doublecut(command_args[2].split(','))
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
							
				else:
					recognized = False
					
			else:
				recognized = False
		elif mode == "setup":
			if len(command_args) == 1:
				if command_args[0] == "help" or command_args[0] == '?':
					print("Here are a list of possible commands to run:")
					print("\thelp                         Shows this dialog.")
					print("\tversion                      Shows the version number.")
					print("\tspam                         Does nothing.  (No really.  This is not a Monty Python joke.)")
					print("\tnew sheet                    Creates a new sheet of assertion (only if one doesn't already exist).")
					print("\tselect <id>                  Changes the selected Level (what is in between the [ and ]) to the object")
					print("\t                             with id <id>.")
					print("\tmode solve                   Switch to problem solving mode.")
					print("\tcreate atom <atom>           Creates a new atom in the selected level.")
					print("\tcreate level                 Creates a new level and makes it a child of the selected level.")
					print("\tdelete atom <atom>           Deletes atom <atom> from the selected level.")
					print("\tdelete level                 Deletes the selected level.")
					print("\tprint                        Prints the current state of the EG at the selected Level.  Go to level id 0")
					print("\t                             (sheet) to print the whole EG.")
					print("\tinfo                         Prints information about the selected level.")
					print("\tquit                         Quits the reason() loop.")
					
				elif command_args[0] == "info":
					print("\t" + context.context_repr + ":")
					print("\tid: " + str(context.id))
					if type(context) is Level:
						print("\tparent: " + str(context.parent.context_repr))
					elif type(context) is Sheet:
						print("\tparent: " + str(context.parent))
					print("\tdepth: " + str(context.depth))
					print("\tatoms: " + str(context.atoms))
					print("\tchildren: ")
					for child in context.children:
						print("\t\t" + child.context_repr)
						
				elif command_args[0] == "spam":
					# Background: it's necessary in every Python program to make a reference to Monty Python.  Here's mine.  ~Trevor
					print("\tMenu:")
					print("\tEgg and spam")
					print("\tEgg, bacon, and spam")
					print("\tEgg, bacon, sausage, and spam")
					print("\tSpam, bacon, sausage, and spam")
					print("\tSpam, egg, spam, spam, bacon, and spam")
					print("\tSpam, spam, spam, egg, and spam")
					print("\tSpam, spam, spam, spam, spam, spam, baked beans, spam, spam, spam, and spam")
					
				elif command_args[0] == 'print':
					try:
						print(context)
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
					
				elif command_args[0] == 'version':
					print("\tEGML version 0.1a4140")
					print("\tThis version does not include spam.")
				
				elif command_args[0] == 'quit':
					break
					
				elif command_args[0] == '':
					pass
				
				else:
					recognized = False
					
			elif len(command_args) == 2:
				if command_args[0] == 'new' and command_args[1] == 'sheet':
					if not context:
						try:
							context = Sheet()
							all_items[0] = context
						except:
							type_, value_, tb_ = sys.exc_info()
							print(value_)
					else:
						print("ERROR: you already have a sheet of assertion.")
				
				elif command_args[0] == "mode" and command_args[1] == "solve":
					print("NOTE: once you enter solve mode, you cannot re-enter setup mode.")
					inp = input("Are you sure you want to continue? [yes/no] ")
					if inp == 'yes':
						mode = "solve"
						
				elif command_args[0] == "create" and command_args[1] == "level":
					try:
						context.create()
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
				
				elif command_args[0] == "delete" and command_args[1] == "level":
					try:
						new_context = context.delete()
						context = new_context
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
				
				elif command_args[0] == 'select':
					if command_args[1].isdigit():
						new_context = all_items[0].find(int(command_args[1]))
						if not new_context:
							try:
								new_context = all_items[int(command_args[1])]
							except:
								new_context = context
								print("ERROR: id not found")
						context = new_context
					else:
						print("ERROR: that's no id!")
				
				else:
					recognized = False
						
			elif len(command_args) == 3:
				if command_args[0] == "create" and command_args[1] == "atom":
					try:
						context.create(atom = command_args[2])
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
						
				elif command_args[0] == "delete" and command_args[1] == "atom":
					try:
						context.delete(atom = command_args[2])
					except:
						type_, value_, tb_ = sys.exc_info()
						print(value_)
				
				else:
					recognized = False
				
		if not recognized:
			print("ERROR: command not recognized.")

EG_reason()