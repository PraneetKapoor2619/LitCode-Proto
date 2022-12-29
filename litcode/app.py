#!/usr/bin/python3
import os
import subprocess as sbpr
import sys

# A bunch of important global variables
dir_sep = ""
directory_tree = []
code_snippet_ref = dict()
project_name = str()
doc_extension = str()
environment_lst = []
com_strt_delim_lst = []
com_end_delim_lst = []

# A lambda function for "prettyidenting" on the terminal
printspace = lambda : print("     ", end = "")

# Definition of functions
def printDirectoryTree():
	global directory_tree
	print("")
	print("*"*80)
	for parent_dir, subdirs, files in directory_tree:
		print("Parent directory:", parent_dir)
		print("Sub-directories:", subdirs)
		print("Files:", files)
		print("*"*80)
	print("")

def loadConfiguration():
	global project_name, doc_extension
	global environment_lst
	global com_strt_delim_lst, com_end_delim_lst
	fp = open("litconfig", "r")
	for line in fp:
		if line.startswith("project-name ="):
			project_name = line.lstrip("project-name =").strip()
		elif line.startswith("doc-extension ="):
			doc_extension = line.lstrip("doc-extension =").strip()
		elif line.startswith("environments ="):
			environment_lst += line.lstrip("environments =").strip().split()
		elif line.startswith("comment-start-delimiters ="):
			com_strt_delim_lst += line.lstrip("comment-start-delimiters =").strip().split()
		elif line.startswith("comment-end-delimiters ="):
			com_end_delim_lst += line.lstrip("comment-end-delimiters =").strip().split()

def printConfiguration():
	global project_name, doc_extension
	global environment_lst
	global com_strt_delim_lst, com_end_delim_lst
	print("")
	print("*"*80)
	print("Project name:", project_name)
	print("\ndoc-extension:", doc_extension)
	print("\nEnvironment list:", environment_lst)
	print("\nCommeent starting delimiters list:", com_strt_delim_lst)
	print("Comment ending delimeters list:", com_end_delim_lst)
	print("*"*80)
	print("")

def checkConfiguration():
	global project_name, doc_extension
	global environment_lst
	global com_strt_delim_lst, com_end_delim_lst
	pass

def writeCodeSnippetRef(fname):
	global code_snippet_ref
	global environment_list
	fp = open(fname, "r")
	env = ""
	endenv = ""
	caption = ""
	isCode = False
	for line in fp:
		orgline = line
		line = line.strip()
		if (line.startswith("\\begin{")) and ("[" in line and "]" in line):
			isCode = True
			env = line.strip("\\begin{")
			env = env[:env.find("}")].strip()
			endenv = "\\end{" + env + "}"
			caption = line[line.find("[") + 1:line.find("]")].strip()
			code_snippet_ref[caption] = ""
			continue
		elif line == endenv:
			isCode = False
			continue
		if isCode:
			code_snippet_ref[caption] += orgline

def printCodeSnippetRef():
	global code_snippet_ref
	print("")
	print("*"*80)
	for reference, string in code_snippet_ref.items():
		print("Reference:", reference)
		print("String:\n", string)
		print("*"*80)
	print("")

def mirrorScaffolding(dirname):
	dirname = dirname.replace("./Scaffolding", "./src")
	os.system("mkdir -p " + dirname)
	return dirname

def isLineSnippetRef(line):
	global com_strt_delim_lst, com_end_delim_lst
	line = line.strip()
	for sdelim in com_strt_delim_lst:
		if line.startswith(sdelim):
			reference = line.strip(sdelim)
			for edelim in com_end_delim_lst:
				if line.endswith(edelim):
					reference = reference.stip(edelim)
					# Because you cannot have more than one type
					# of delimiter for a comment
					break
			reference = reference.strip()
			return reference
	return False

def expandSnippetRef(fname):
	global code_snippet_ref
	fp = open(fname, "r")
	code = ""
	for line in fp:
		code += line
		line = line.strip()
		reference = isLineSnippetRef(line)
		if reference != False and reference in code_snippet_ref:
			code += code_snippet_ref[reference]
	return code

def init():
	global dir_sep, doc_extension
	full_path = os.getcwd()
	index1 = full_path.rfind(dir_sep) + 1
	parent_name = full_path[index1:]
	os.system("mkdir -p Documentation/ Scaffolding/")
	os.system("touch Documentation/" + parent_name + doc_extension)
	os.system("touch litconfig")
	os.system()

def tangle():
	global dir_sep, directory_tree, code_snippet_ref
	global doc_extension, environment_lst
	global com_strt_delim_lst, com_end_delim_lst
	# Now create a list of references
	print("\n[2]: Creating dictionary of code snippet references...")
	for (parent, subdirs, files) in directory_tree:
		if parent.startswith("./Documentation") and len(files) > 0:
			for f in files:
				if f.endswith(doc_extension):
					fname = parent + dir_sep + f
					writeCodeSnippetRef(fname)
	printspace()
	print("Dictionary created.")
	#printCodeSnippetRef()

	print("\n[3]: Creating ./src...")
	os.system("mkdir src")
	printspace()
	print("./src created.")

	# Now read the Scaffolding directory...
	# Mirror it in src and write the files in scaffolding, adding
	# code after references
	print("\n[4]: Starting tangling...")
	for (parent, subdirs, files) in directory_tree:
		if parent.startswith("./Scaffolding") and len(files) > 0:
			printspace()
			print("Mirroring:", parent)
			target_dirname = mirrorScaffolding(parent)
			for f in files:
				fname = parent + dir_sep + f
				code = expandSnippetRef(fname)
				fname = target_dirname + dir_sep + f
				fp = open(fname, "w")
				fp.write(code)
				fp.close()
	printspace()
	print("Tangling complete.")

def weave():
	global project_name, doc_extension
	print("Here")
	com1 = "texliveonfly -c pdflatex Documentation/" +\
	 project_name + doc_extension
	com2 = "bibtex " + project_name + ".aux"
	os.system(com1)
	os.system(com2)
	os.system(com1)
	os.system(com1)

def test():
	global typical
	print(typical)

def main():
	# Set directory separator
	if sys.platform == "linux" or sys.platform == "linux2":
		dir_sep = "/"
	elif sys.platform == "darwin":
		dir_sep = "/"
	elif sys.platform == "win32":
		dir_sep = "\\"

	# Read directory tree and check if its a valid one
	check_flag = False
	for parent_dir, subdirs, files in os.walk(".", topdown = True):
		if (parent_dir == "." and check_flag == False):
			if ("Documentation" in subdirs) and \
			("Scaffolding" in subdirs) and ("litconfig" in files):
				check_flag = True
		directory_tree.append((parent_dir, subdirs, files))
	directory_tree.sort(key = lambda x:x[0])
	
	test()
	# It may be possible that the directory is not yet a litcode repository,
	# and the programmer wants to set it up as one. In which case they will use
	# "init" argument	
	sys.argv.append("")
	if sys.argv[1] == "init":
		if check_flag == False:
			init()
			print("Exiting...")
			exit(0)
		elif check_flag == True:
			print("This is already a LitCode repository.")
			print("Exiting...")
			exit(1)
	else:
		if check_flag == False:
			print("Directory not properly set up.")
			exit(1)
		elif check_flag == True:
			print("Directory verified.")
	
	# You have come this far because the argument passed was not init...		
	# Now load configuration file
	print("\n[1]: Loading configuration...")
	loadConfiguration()
	printspace()
	print("Configuration loaded.")
	checkConfiguration()

	# Now perform some operations based on the command line argument
	if sys.argv[1] == "":
		print("Running everything")
		tangle()
		weave()
	elif sys.argv[1] == "tangle":
		tangle()
	elif sys.argv[1] == "weave":
		weave()
	else:
		print("Invalid command:", sys.argv[1])