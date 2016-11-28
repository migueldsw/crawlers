from levenshtein import levenshtein, rlevd
import os
import numpy as np

#-----------------------
DOCS_DIR = 'out/'

def load_docs(docs_dir):
	docs_lines = []
	file_list = os.listdir(docs_dir)
	for file in file_list:
		lines = [line.rstrip('\n') for line in open(docs_dir+file)]
		docs_lines.append(lines)
	return docs_lines, file_list

def compare_files(f1, f2):
	#returns a list of distances between of each line from each file
	out = []
	for l1 in f1:
		for l2 in f2:
			out.append(rlevd(l1,l2))
	return np.min(out)
	#return out

def calc_dissimilarity_matrix(docs_lines):
	n = len(docs_lines)
	out = np.zeros(n**2).reshape(n,n)
	for i in range(n):
		for j in range(n):
			out[i,j] = compare_files(docs_lines[i],docs_lines[j])
	print 'dissimilarity matrix:'
	print out
	return out


docs_lines, file_list = load_docs(DOCS_DIR)

print 'docs_lines | file_list'
print docs_lines
print file_list
D = calc_dissimilarity_matrix(docs_lines)