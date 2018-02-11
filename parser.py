from collections import defaultdict


def read_data(path):
    lst = []
    with open(path, 'r', encoding='latin1', errors='ignore') as f:
        for i in range(14):
            f.readline()
        for line in f:
            lst.append(remover(line).strip().split("\t"))
    return lst


def remover(s):
    lst = ["'", '"', ">", "<"]
    new_s = ""
    for i in range(len(s)):
        if s[i] not in lst:
            new_s += s[i]
    return new_s


def dict_cr(lst, year):
    dictionary = defaultdict(list)
    for line in lst:
        if "({}".format(year) in line[0]:
            if line[-1][0] == "(":
                dictionary[line[-2]].append(line[0][0:line[0].index("(")])
            else:
                dictionary[line[-1]].append(line[0][0:line[0].index("(")])
    return dictionary


def main(path, year):
    lst = read_data(path)
    dictionary = dict_cr(lst, year)
    return dictionary
