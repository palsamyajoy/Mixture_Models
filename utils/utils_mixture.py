import numpy as np
from sklearn.metrics import confusion_matrix
import copy


def acc_check(tru, obs):
    lom = confusion_matrix(tru, obs).tolist()

    match = [max(lom[0])]
    max_prob_c = [lom[0].index(max(lom[0]))]
    for i in range(1, len(lom)):
        for j in max_prob_c:
            del lom[i][j]
        max_prob_c_temp = lom[i].index(max(lom[i]))
        max_prob_c.append(max_prob_c_temp)
        temp_match = max(lom[i])
        match.append(temp_match)

    match = np.sum([max(i) for i in lom])
    acc = match/len(tru)

    return acc


def prec_check(tru, obs):
    lom = confusion_matrix(tru, obs).tolist()
    lom_c = copy.deepcopy(lom)

    match = [max(lom_c[0])]
    max_prob_c = [lom[0].index(max(lom_c[0]))]
    for i in range(1, len(lom_c)):
        for j in sorted(max_prob_c, reverse=True):
            del lom_c[i][j]
        max_prob_c_temp = lom[i].index(max(lom_c[i]))
        max_prob_c.append(max_prob_c_temp)
        temp_match = max(lom_c[i])
        match.append(temp_match)
    lom = confusion_matrix(tru, obs).tolist()
    prec = []
    for k in range(len(match)):
        temp_prec = match[k]/np.sum(lom[k])
        prec.append(temp_prec)

    return np.mean(prec)


def rec_check(tru, obs):
    lom = confusion_matrix(tru, obs).tolist()
    lom_c = copy.deepcopy(lom)

    match = [max(lom_c[0])]
    max_prob_c = [lom_c[0].index(max(lom_c[0]))]
    for i in range(1, len(lom_c)):
        for j in sorted(max_prob_c, reverse=True):
            del lom_c[i][j]
        max_prob_c_temp = lom[i].index(max(lom_c[i]))
        max_prob_c.append(max_prob_c_temp)
        temp_match = max(lom_c[i])
        match.append(temp_match)

    lom = confusion_matrix(tru, obs).tolist()
    rec = []
    for k in range(len(match)):
        temp_rec = match[k]/np.sum([lom[l][max_prob_c[k]]
                                   for l in range(len(lom))])
        rec.append(temp_rec)

    return np.mean(rec)


def f_score(tru, obs):
    prec = prec_check(tru, obs)
    rec = rec_check(tru, obs)
    f_sc = 2/(prec**(-1)+rec**(-1))

    return f_sc


def mixture_clusters(gamma_matrix, data_lol):
    n = len(data_lol)
    k = len(gamma_matrix[0])
    cluster = []
    data_cwise = [[] for i in range(k)]
    for h in range(n):
        max_prob_c = gamma_matrix[h].index(max(gamma_matrix[h]))
        data_cwise[max_prob_c].append(data_lol[h])
        cluster.append(max_prob_c)

    return cluster, data_cwise
