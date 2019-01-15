# Existential Graph Manipulation library (egml)
# 
# Written by:
#	Trevor Toryk (torykt@rpi.edu)
#	Mark Sgobba (sgobbm@rpi.edu)

# Exceptions (errors)
# EGDoublecutError: errors raised from attempts to add or remove doublecuts in illogical ways.
class EGDoublecutError(Exception):
	def __init__(self, str):
		self.string = str
	def __str__(self):
		return self.string
# EGRemovalError: errors raised from attempting to perform a removal on an odd level.
class EGRemovalError(Exception):
	def __init__(self, str):
		self.string = str
	def __str__(self):
		return self.string
# EGInsertionError: errors raised from attempting to perform an insertion on an even level.
class EGInsertionError(Exception):
	def __init__(self, str):
		self.string = str
	def __str__(self):
		return self.string
# EGIterationError: errors raised from attempting to perform an iteration illogically.
class EGIterationError(Exception):
	def __init__(self, str):
		self.string = str
	def __str__(self):
		return self.string
# EGCopyError: errors raised attempting to copy graphs.
class EGCopyError(Exception):
	def __init__(self, str):
		self.string = str
	def __str__(self):
		return self.string

# This is a function which makes a copy of any graph given it and returns the copy.
def copy_graph(sheet, graph):
	if type(graph) is Level:
		new_level = Level(None, sheet.get_next_id())
		for child in graph.children:
			new_child = copy_graph(sheet, child)
			new_level.children.append(new_child)
			new_child.parent = graph
		return new_level
	elif type(graph) is Sheet:
		raise EGCopyError("Cannot copy a sheet of assertion.")
	else:
		raise EGCopyError("Not a recognized type.")

# A level is a sublevel, also known as a "cut".  Its id is used internally.
class Level:	
	# The following variables are defined:
	#	parent - the Level containing this Level
	#	id - the (internal) ID of the level (used mainly for searching)
	#	depth - the level of this level (parent depth +1 in this instance)
	#	children - the Levels which are a part of this Level
	#	atoms - the atoms which are in this level (represented as letters)
	
	################ Solve Mode Functions ################
	
	### DOUBLECUT INSERTION
	def ins_doublecut(self, atoms = None):
		if not atoms:
			# Create 2 new levels and link them to each other and to this level's parent level
			first_new_level = Level(self.parent)
			second_new_level = Level(first_new_level)
			# Set this level's parent to the second new level
			self.parent = second_new_level
			# Modify the depth of this level and its children
			self.set_depth(self.depth + 2)
			# Remove this level from the children of its original parent
			first_new_level.parent.children.remove(self)
			# Add the first new level to the same original parent
			first_new_level.parent.children.append(first_new_level)
			# Make the second new level a child of the first new level
			first_new_level.children.append(second_new_level)
			# Make this level a child of the second new level
			second_new_level.children.append(self)
		elif type(atoms) is str:
			if atoms in self.atoms:
				first_new_level = Level(self)
				second_new_level = Level(first_new_level)
				self.children.append(first_new_level)
				first_new_level.children.append(second_new_level)
				second_new_level.atoms.append(atoms)
				self.atoms.remove(atoms)
			else:
				raise EGDoublecutError("One of the passed atoms is not in the list of atoms.")
		elif type(atoms) is list:
			for atom in atoms:
				if atom not in self.atoms:
					raise EGDoublecutError("One of the passed atoms is not in the list of atoms.")
			first_new_level = Level(self)
			second_new_level = Level(first_new_level)
			self.children.append(first_new_level)
			first_new_level.children.append(second_new_level)
			for atom in atoms:
				second_new_level.atoms.append(atom)
				self.atoms.remove(atom)
		else:
			return TypeError("atoms can only be an alphabetic string of length 1 or a list of such strings.")
	
	### DOUBLECUT REMOVAL
	def rem_doublecut(self):
		# This one is a bit of an oddity.  Why?  Because we can remove this level and the one above it, or this and the one below it.
		# Note that the default behavior will be to remove the one above.  If it can't do that it will remove the level below.
		if type(self.parent) is Level and len(self.parent.children) == 1 and len(self.parent.atoms) == 0:
			for child in self.children:
				child.set_depth(child.depth - 2)
				child.parent = self.parent.parent
				self.parent.parent.children.append(child)
			for atom in self.atoms:
				self.parent.parent.atoms.append(atom)
			self.parent.parent.children.remove(self.parent)
			self.children = []
			new_context = self.parent.parent
			self.parent.parent = None
			return new_context
		elif len(self.children) == 1 and len(self.atoms) == 0 and type(self.children[0]) is Level:
			for child in self.children[0].children:
				child.parent = self.parent
				child.set_depth(child.depth - 2)
				self.parent.children.append(child)
			for atom in self.children[0].atoms:
				self.parent.atoms.append(atom)
			self.parent.children.remove(self)
			self.children[0].children = []
			new_context = self.parent
			self.parent = None
			return new_context
		else:
			raise EGDoublecutError("This Level is not eligible for the doublecut rule.")
	
	### INSERTION OF ANY GRAPH
	def insert(self, atom = None, level = None):
		if type(self.depth) is int and not self.depth % 2 == 1:
			raise EGInsertionError("To use insertion, level must be odd.")
			
		if atom and level:
			raise EGInsertionError("Only pass EITHER a new atom OR a new level to insert at this point.")

		if atom and type(atom) is str and atom.isalpha() and len(atom) == 1:
			self.atoms.append(atom)
		elif atom and type(atom) is str:
			raise ValueError("Atom name must be exactly one letter in length.")
		elif atom:
			raise TypeError("Atom must be a string of length 1.")
		elif level and type(level) is Level and level.parent == None:	# That last condition is to ensure that this isn't a different part of the tree we're taking!
			self.children.append(level)
			level.parent = self
			level.set_depth(self.depth + 1)
		elif level and type(level) is Level:
			raise EGInsertionError("The level to be inserted must not already have a parent somewhere in the tree.")
		elif level:
			raise TypeError("Level must be an instance of the Level object.")
		else:
			raise ValueError("Either the atom or the level must be set.")
	
	### REMOVAL OF ANY GRAPH
	# When called without arguments, removes this sublevel.
	# When called with the single argument atom, removes the atom from this sublevel.
	def remove(self, atom = None, level = None):
		if type(self.depth) is int and not self.depth % 2 == 0:
			raise EGRemovalError("You attempted to make a removal on an odd level.")
			
		if atom and level:
			raise EGRemovalError("Only set either atom OR level.")
		
		if atom and type(atom) is str:
			self.atoms.remove(atom)
			print(self.context_repr + " updated: removed " + atom)
		elif atom:
			raise TypeError("atom must be a single-character alphabetic string.")
		elif level and type(level) is Level:
			if level in self.children:
				self.children.remove(level)
				print(self.context_repr + " updated: removed " + str(level))
				level.parent = None
			else:
				raise EGRemovalError("level is not a child of this sublevel.")
		elif level:
			raise TypeError("level must be a Level object that is the child of this Level object.")
		else:
			raise ValueError("Either the atom or the level must be set.")
		#else:
		#	#for child in self.children:
		#	#	child.set_depth(child.depth - 1)
		#	#	child.parent = self.parent
		#	#	self.parent.children.append(child)
		#	self.parent.children.remove(self)
		#	self.children = []
		#	new_context = self.parent
		#	self.parent = None
		#	print(self.context_repr + " deleted self")
		#	return new_context		# Done only so reason() can set the new context
			
	### ITERATION RULE
	def iterate(self, level = None, atom = None):
		if level and atom:
			raise EGIterationError("Only specify either the Level (subgraph) OR atom to iterate.")
		
		if atom:
			if type(atom) is str and atom.isalpha() and len(atom) == 1:
				context = self.parent
				found = False
				while context:
					if atom in context.atoms:
						found = True
						break
					context = context.parent
				if found:
					self.atoms.append(atom)
					print(self.context_repr + " updated: added atom " + atom)
				else:
					raise EGIterationError("atom not found in any of the containing Levels.")
			else:
				raise ValueError("atom must be set to a one-character alphabetic string.")
				
		elif level:
			if type(level) is Level and level.parent == None:		# Again, last condition ensures that we're not borrowing a level from somewhere else in the graph
				context = self.parent
				found = False
				while context:
					for child in context.children:
						if level.equal(child):
							found = True
							break
					if found:
						break
				if found:
					self.children.append(level)
					level.parent = self
					level.set_depth(self.depth + 1)
					print(self.context_repr + " updated: added " + level.context_repr + " to level's children[]")
				else:
					raise EGIterationError("level not found in any of the levels above this one.")
			elif type(level) is Level:
				raise EGIterationError("level must not already have a parent somewhere in this tree.")
			else:
				raise TypeError("level must be set to an instance of a Level object.")
		else:
			raise ValueError("Either the atom or the level must be set.")
		
	### DEITERATION RULE
	def deiterate(self, level = None, atom = None):
		if level and atom:
			raise EGIterationError("Only specify either the Level (subgraph) OR atom to iterate.")
		
		if atom:
			if type(atom) is str and atom.isalpha() and len(atom) == 1:
				context = self.parent
				found = False
				while context:
					if atom in context.atoms:
						found = True
						break
					context = context.parent
				if found:
					self.atoms.remove(atom)
					print(self.context_repr + " updated: removed " + atom + " from level's atoms[]")
				else:
					raise EGIterationError("atom not found in any of the containing Levels.")
			else:
				raise ValueError("atom must be set to a one-character alphabetic string.")
				
		elif level:
			if type(level) is Level:
				context = self.parent
				found = False
				while context:
					for child in context.children:
						if level.equal(child):
							found = True
							break
					if found:
						break
				if found:
					try:
						self.children.remove(level)
					except:
						raise EGIterationError("level not found in this level's children.")
						
					level.parent = None
					print(self.context_repr + " updated: removed child level " + level.context_repr)
				else:
					raise EGIterationError("level not found in any of the levels above this one.")
			else:
				raise TypeError("level must be set to an instance of a Level object.")
		else:
			raise ValueError("Either the atom or the level must be set.")
	
	############## Setup Mode Functions #################
	
	def create(self, atom = None):
		if not atom:
			new_level = Level(self)
			self.children.append(new_level)
		elif type(atom) is str and len(atom) == 1 and atom.isalpha():
			self.atoms.append(atom)
			print(self.context_repr + " updated: added atom " + atom)
		else:
			raise ValueError("atom must be set to a one-character alphabetic string.")
	
	def delete(self, atom = None):
		if not atom:
			self.parent.children.remove(self)
			new_context = self.parent
			self.parent = None
			print(self.context_repr + " and all atoms and children deleted")
			return new_context
		elif type(atom) is str and len(atom) == 1 and atom.isalpha() and atom in self.atoms:
			self.atoms.remove(atom)
			print(self.context_repr + " updated: deleted atom " + atom)
		elif not atom in self.atoms:
			raise NameError("atom not in this level's atoms.")
		else:
			raise ValueError("atom must be set to a one-character alphabetic string.")
	
	############ Internal Class Functions ###############
	
	def get_sheet(self):
		if self.parent:
			return self.parent.get_sheet()
		else:
			return None
	
	def set_depth(self, new_depth):
		if not (type(new_depth) is int):
			raise TypeError("'new_depth' must be an integer.")
		self.depth = new_depth
		print(self.context_repr + " updated: new depth is " + str(self.depth))
		for item in self.children:
			item.set_depth(new_depth + 1)
	
	def equal(self, other_level):
		# Check atoms:
		if not len(self.atoms) == len(other_level.atoms):
			return False
		for atom in self.atoms:
			if not atom in other_level.atoms:
				return False
		# Check levels:
		if not len(self.children) == len(other_level.children):
			return False
		for child in self.children:
			are_equal = False
			for other_child in other_level.children:
				if child.equal(other_child):
					are_equal = True
			if not are_equal:
				return False
		return True
	
	######### Recursive Item Finding Function ###########
	
	def find(self, id):
		retval = False
		if self.id == id:
			return self
		for item in self.children:
			if item.id == id and not retval:
				return item
			elif not retval:
				retval = item.find(id)
		return retval
	
	################### Initialization ###################
	
	def __init__(self, new_parent, new_id = None):
		if new_id:
			self.id = new_id
		else:
			try:
				self.id = new_parent.get_sheet().get_next_id()
			except:
				raise EGInitializationException("To initialize a Level you need either a parent node or an ID from the sheet of assertion.")
		
		self.parent = new_parent
		if new_parent and type(new_parent.depth) is int:
			self.depth = self.parent.depth + 1
		else:
			self.depth = "?"
			
		self.atoms = []
		self.children = []
		
		self.context_repr = 'Level id %d' % self.id 
		
		print("Level id " + str(self.id) + " depth " + str(self.depth) + " created")
		
	################## String Representation ###############
	
	def __repr__(self):
		ret = "\t"*self.depth+'['+str(self.id)+']'+repr(self.atoms)+"\n"
		for child in self.children:
			ret += child.__repr__()
		return ret

# The sheet of assertion is just a specific "Level", namely level 0.  Right now it also has an id of 0 for sake of ease of identification.
class Sheet(Level):
	############## Object Identity Tracking ##############
	
	next_id = 1
	
	def get_next_id(self):
		ret = self.next_id
		self.next_id += 1
		return ret
		
	################ Solve Mode Functions ################
	
	### DOUBLECUT INSERTION
	def ins_doublecut(self, atoms = None):
		if not atoms:
			# On the sheet of assertion, we just create 2 new Levels and make the necessary links.
			first_new_level = Level(self)
			second_new_level = Level(first_new_level)
			self.children.append(first_new_level)
			first_new_level.children.append(second_new_level)
		# In other cases, its just like it is in the Level class.
		elif type(atoms) is str:
			if atoms in self.atoms:
				first_new_level = Level(self)
				second_new_level = Level(first_new_level)
				self.children.append(first_new_level)
				first_new_level.children.append(second_new_level)
				second_new_level.atoms.append(atoms)
				self.atoms.remove(atoms)
			else:
				raise EGDoublecutError("One of the passed atoms is not in the list of atoms.")
		elif type(atoms) is list:
			for atom in atoms:
				if atom not in self.atoms:
					raise EGDoublecutError("One of the passed atoms is not in the list of atoms.")
			first_new_level = Level(self)
			second_new_level = Level(first_new_level)
			self.children.append(first_new_level)
			first_new_level.children.append(second_new_level)
			for atom in atoms:
				second_new_level.atoms.append(atom)
				self.atoms.remove(atom)
		else:
			raise TypeError("atoms can only be an alphabetic string of length 1 or a list of such strings.")
	
	### DOUBLECUT REMOVAL
	#def rem_doublecut(self)
	#	This function should *not* be called here, because there can be multiple doublecuts on the Sheet.
	#	Instead, call it from one of the Levels of the doublecut you want to remove.
	def rem_doublecut(self):
		raise EGDoublecutError("Do not call rem_doublecut from the Sheet of Assertion.")
	
	### INSERTION OF ANY GRAPH
	#def insert(self, item)
	#	The default behavior of insert() in the parent class Level causes it to fail instantaneously if the Level is not odd.
	#	So, while you might think we want to override this for the Sheet, we don't need to.
	
	### REMOVAL OF ANY GRAPH
	#def remove(self, item)
	#	The new definition of remove makes it compatible with the sheet of assertion.
	
	### ITERATION RULE
	def iterate(self, level = None, atom = None):
		raise EGIterationError("Unable to iterate to the sheet of assertion.")
	
	### DEITERATION RULE
	def deiterate(self, level = None, atom = None):
		raise EGIterationError("Unable to deiterate from the sheet of assertion.")
		
	############## Setup Mode Functions #################
	
	#def create(self, atom = None):
	#	This function works just fine as imported.
	
	def delete(self, atom = None):
		#	This function works just fine as imported...except that it doesn't if the user attempts to delete the Sheet.
		if not atom:
			raise EGRemovalError("Cannot remove the Sheet of Assertion.")
		elif type(atom) is str and len(atom) == 1 and atom.isalpha() and atom in self.atoms:
			self.atoms.remove(atom)
			print(self.context_repr + " updated: deleted atom " + atom)
		elif not atom in self.atoms:
			raise NameError("atom not in this level's atoms.")
		else:
			raise ValueError("atom must be set to a one-character alphabetic string.")
		
	############ Internal Class Functions ###############
	
	def get_sheet(self):
		#	This function is slightly different:
		return self
	
	def set_depth(self, new_depth):
		#	This function won't be used on the Sheet of Assertion.  Just in case...
		raise ValueError("Why are you attempting to change the depth of the Sheet of Assertion?")
	
	#def equal(self, other_level):
	#	This function works just fine as imported.
	
	######### Recursive Item Finding Function ###########
	
	#def find(self, id):
	#	This function works just fine as imported.
	
	################### Initialization ###################
	
	def __init__(self):
		self.parent = None
		self.depth = 0
		self.children = []
		self.atoms = []
		self.id = 0
		
		self.context_repr = 'Sheet id 0'
		
		print('Sheet id 0 created')
		
	################## String Representation ###############
	
	#def __repr__(self):
	#	This function works just fine as imported.