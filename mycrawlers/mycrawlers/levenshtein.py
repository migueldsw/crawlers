#Levenshtein distance
#ref.: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python

def levenshtein(s, t):
    '''Levenshtein dist'''
    if s == t: return 0
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
            
    return v1[len(t)]

def rlevd(s, t):
    '''Relative Levenshtein distance'''
    return float(levenshtein(s,t))/(max(len(s),len(t)))

# import numpy as np
# def levenshtein(source, target):
#     '''levenshtein dist 2'''
#     if (len(source) < len(target)):
#         return levenshtein(target, source)
#     # So now we have len(source) >= len(target).
#     if (len(target) == 0):
#         return len(source)
#     # We call tuple() to force strings to be used as sequences
#     # ('c', 'a', 't', 's') - numpy uses them as values by default.
#     source = np.array(tuple(source))
#     target = np.array(tuple(target))
#     # We use a dynamic programming algorithm, but with the
#     # added optimization that we only need the last two rows
#     # of the matrix.
#     previous_row = np.arange(target.size + 1)
#     for s in source:
#         # Insertion (target grows longer than source):
#         current_row = previous_row + 1
#         # Substitution or matching:
#         # Target and source items are aligned, and either
#         # are different (cost of 1), or are the same (cost of 0).
#         current_row[1:] = np.minimum(
#             current_row[1:],
#             np.add(previous_row[:-1], target != s))
#         # Deletion (target grows shorter than source):
#         current_row[1:] = np.minimum(
#                 current_row[1:],
#                 current_row[0:-1] + 1)
#         previous_row = current_row
#     return previous_row[-1]