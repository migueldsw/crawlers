#
#MAIN EXEC
#
from cluster import  calc_cluster, plot_dendrogram
from documents_evaluator import load_docs, compare_files, calc_dissimilarity_matrix
from subprocess import call
import numpy as np
import os
#call(['ls','-la'])

#-----------------------
DOCS_DIR = 'out/'
# UTILS------------------------------------------
#time cost evaluation
from datetime import datetime as dt
TIME = [] #[t_init,t_final]
def startCrono():
	TIME.append(dt.now())
def getCrono(): # returns delta t in seconds
	TIME.append(dt.now())
	deltat = TIME[-1]-TIME[-2]
	return deltat.seconds
plotdir = './plots'
if not os.path.isdir(plotdir):
	os.makedirs(plotdir)
matrixdir = './matrix'
if not os.path.isdir(matrixdir):
	os.makedirs(matrixdir)


def save_matrix(matrix):
	np.savetxt("matrix.csv", matrix, delimiter=",")



docs_lines, file_list = load_docs(DOCS_DIR)
startCrono()
D = calc_dissimilarity_matrix(docs_lines)
t = getCrono()
print ('Done in %d sec'%t)

C = calc_cluster(D)
plot_dendrogram(C)