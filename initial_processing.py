import itertools
import json
import pandas as pd
import os

IN_A_ROW_MIN = 30
MERGE_IF_CLOSER_THAN = 10
LOOK_FOR_ABOVE = 0.5

ALPHABET = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
ILV = ['I', 'L', 'V']
ILVM = ['I', 'L', 'V', 'M']
ILVMF = ['I', 'L', 'V', 'M', 'F']
DE = ['D', 'E']
VI = ['V', 'I']
PLVIMFY = ['P', 'L', 'V', 'I', 'M', 'F', 'Y']
PLVIM = ['P', 'L', 'V', 'I', 'M']
DES = ['D', 'E', 'S']
EDSTP = ['E', 'D', 'S', 'T', 'P']

type_1 = list(itertools.product(
    ILV, ILV, ALPHABET, ILV
))
type_2 = list(itertools.product(
    ILV, ALPHABET, ILV, ILV
))
type_3 = list(itertools.product(
    ILV, ILV, ILV, ILV
))
type_4 = list(itertools.product(
    ALPHABET, ILV, ILV, ILV
))
type_5 = list(itertools.product(
    ILV, DE, ILV, DE, ILV
))
type_alpha = list(itertools.product(
    VI, ALPHABET, VI, VI
))
type_beta = list(itertools.product(
    VI, ALPHABET, VI, ILV
))
type_a = list(itertools.product(
    PLVIM, ILVM, ALPHABET, DES, DES, DES
))
type_b = list(itertools.product(
    PLVIMFY, ILVM, "D", "L", "T"
))
type_r = list(itertools.product(
    DES, DES, DES, ILVM, ALPHABET, ILVMF, ILVMF
))
combined_list = type_1 + type_2 + type_3 + type_4 + type_5 + type_alpha + type_beta + type_a + type_b + type_r
complete_sim_list = []
for sim in combined_list:
    str_ = ''
    for item in sim:
        str_ = str_ + item
    complete_sim_list.append(str_)



counter = 0
with open("uploads/iupred.txt") as raw_data:


    iupred_number = 0
    for line in raw_data:
        if "################" in line:
            iupred_number += 1

with open("uploads/iupred.txt") as raw_data:
    for line in raw_data:
        if line.startswith("################"):

            file_number = f"{counter:04d}"
            with open(f"raw_results_folder/results{file_number}.txt", mode="a") as file, open("dump_file.txt", mode="r") as dump:
                for line2 in dump:
                    file.write(line2)

            print(f"IUPred file read progress: {counter}/{iupred_number}")
            counter += 1
            os.remove("dump_file.txt")

        elif not line.startswith("#"):
            with open("dump_file.txt", mode="a") as dump:
                dump.write(line)

