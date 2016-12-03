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
	f1.sort(key=len)
	f2.sort(key=len)
	str1 = ''.join(f1)
	str2 = ''.join(f2)
	return rlevd(str1,str2)

def calc_dissimilarity_matrix(docs_lines):
	n = len(docs_lines)
	print ('Calculating dissimilarity matrix for %d documents...'%n)
	out = np.zeros(n**2).reshape(n,n)
	for i in range(n):
		print ('...%d/%d...'%(i+1,n))
		for j in range(n):
			if (i>j):
				out[i,j] = compare_files(docs_lines[i],docs_lines[j])
				out[j, i] = out[i,j]
	print 'dissimilarity matrix:'
	print out
	return out


#docs_lines, file_list = load_docs(DOCS_DIR)
# print 'docs_lines | file_list'
# print docs_lines
# print file_list
#D = calc_dissimilarity_matrix(docs_lines)