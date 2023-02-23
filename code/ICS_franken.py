import sys
import csv
import os
from collections import Counter

# pairs is a dictionary showing which kinbank shorthands represent which family relationships
# each tuple in pairs.values represents the pair of kin terms that will be compared for equality
gen2 = [['mMB','mMeB','mMyB'],['mMZ','mMeZ','mMyZ'],['mFB','mFeB','mFyB'],['mFZ','mFeZ','mFyZ']]
gen1 = [['mMBS'],['mMZS'],['mFBS'],['mFZS']] # just one child to keep things simple

# {'siblings': [('meB','meZ'),('myB','myZ')],
# 'm_siblings': [('mMeB','mMeZ'),('mMyB','mMyZ')],
# 'f_siblings': [('mFeB','mFeZ'),('mFyB','mFyZ')],
# 'mez_cousins': [('mMeZeS','mMeZeD'),('mMeZyS','mMeZyD'),('mMeZS','mMeZD')],
# 'meb_cousins': [('mMeBeS','mMeBeD'),('mMeByS','mMeByD'),('mMeBS','mMeBD')],
# 'fez_cousins': [('mFeZeS','mFeZeD'),('mFeZyS','mFeZyD'),('mFeZS','mFeZD')],
# 'feb_cousins': [('mFeBeS','mFeBeD'),('mFeByS','mFeByD'),('mFeBS','mFeBD')],
# 'myz_cousins': [('mMyZeS','mMyZeD'),('mMyZyS','mMyZyD'),('mMyZS','mMyZD')],
# 'myb_cousins': [('mMyBeS','mMyBeD'),('mMyByS','mMyByD'),('mMyBS','mMyBD')],
# 'fyz_cousins': [('mFyZeS','mFyZeD'),('mFyZyS','mFyZyD'),('mFyZS','mFyZD')],
# 'fyb_cousins': [('mFyBeS','mFyBeD'),('mFyByS','mFyByD'),('mFyBS','mFyBD')],
# 'mz_cousins': [('mMZeS','mMZeD'),('mMZyS','mMZyD'),('mMZS','mMZD')],
# 'mb_cousins': [('mMBeS','mMBeD'),('mMByS','mMByD'),('mMBS','mMBD')],
# 'fz_cousins': [('mFZeS','mFZeD'),('mFZyS','mFZyD'),('mFZS','mFZD')],
# 'fb_cousins': [('mFBeS','mFBeD'),('mFByS','mFByD'),('mFBS','mFBD')]
# }

def get_kin(file,directory):
    """Loads in a frankenlanguage csv file, populates a dictionary with the kin terms."""
    # file_path = '../frankenlanguages/' + directory + '/' + file
    file_path = '../kinbank/raw/' + directory + '/' + file
    kin_terms = {}
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            parameter = line['parameter'] # kin type
            word = line['word'] # kin term
            kin_terms[parameter] = word
    return kin_terms

# def has_duplicates(seq):
#     if any(seq.count(x) > 1 for x in seq):
#

def list_generations(ks):
    generation1 = {}
    generation2 = {}
    for kin in gen2:
        if kin[0] in ks.keys():
            generation2[kin[0]] = ks[kin[0]]
        else:
            generation2[kin[0]] = 'na'
    for pair1,pair2 in gen1:
        if pair1 in ks.keys():
            generation1[pair1] = ks[pair1]
        else:
            generation1[pair1] = ('na')
        if pair1 in ks.keys():
            generation1[pair2] = ks[pair2]
        else:
            generation1[pair2] = ('na')

    return generation1,generation2

def find_relevant_kin():
    for kin_types in gen:
        for type in kin_types:

# def find_duplicates(gen):
#     seen = set()
#     dupes = []
#     print(gen)
#
#     for term in gen.values():
#         if term in seen:
#             dupes.append(term)
#         else:
#             seen.add(term)
#     return dupes

def enumerate_generation2(gen):
    """Turn lists of Gen2 kin terms into lists of numbers. Each number indicates a unique kin term."""
    gen_pattern = list(gen.values())
    code = 0

    # for each unique item in gen_pattern
    for item in set(gen_pattern):
        code += 1
        # for as many times as that item appears in gen pattern
        while item in gen_pattern:
            index = gen_pattern.index(item)
            # label it 0 if na
            if item == 'na':
                gen_pattern[index] = 0
            # give it a unique number if anything else
            else:
                gen_pattern[index] = code

    return gen_pattern

# def enumerate_generation1(gen):
#     """Turn lists of Gen1 kin terms into lists of numbers. Each number indicates a unique kin term."""
#     gen = list(gen.values())
#     gen_pattern = [1,2,3,4] # placeholder list to maintain index range
#     code = 0
#
#     for item in set(gen): # for each unique item in gen
#         code += 1
#         index = gen.index(item)
#         index += 1
#         if (index % 2) == 0: # check if index + 1 is even
#             continue # do nothing if so
#         else:
#             while item in gen:
#                 index = gen.index(item)
#                 if item == 'na':
#                     gen_pattern[index] = 0
#                 else:
#                     gen_pattern[index] = code
#                 gen.remove(item)
#     return gen_pattern


    gen_pattern = [list(gen.values())[i:i+2] for i in range(0,len(list(gen.values())),2)]

    print(gen_pattern)
    return gen_pattern


def check_pattern(pattern1,pattern2):
    """Checks whether the categories of kin are the same in gen2 as gen1."""
    ICS_score = 0
    denominator = 4

    # for each type of kin
    for i in range(4):
        if pattern2 == pattern1: # order of the list matters: so same index of both lists will be the parent/child pair
            print(pattern2[i],pattern1[i])
            if pattern1[i] == 0 or pattern2[i] == 0:
                continue
            else:
                ICS_score += 1
        else:
            continue
    print(ICS_score/denominator)


def check_feature_symmetry(ks):
    """Checks whether the terms used in the language for each pair of kin terms match."""
    results = {}

    for kin in kin_types:
        for pair in gender_pairs[kin]:
            if pair[0] in ks.keys() and pair[1] in ks.keys():
                if ks[pair[0]] == ks[pair[1]]:
                    results[kin] = 0
                else:
                    results[kin] = 1
            else:
                continue
        if kin not in results:
            results[kin] = 'null'

    return results

def get_csv_files(path):
    """Fetches a list of files from the directory located by the given filepath."""
    directory = os.scandir(path)
    files = []
    for file in directory:
        files.append(file.name)
    return files

def write_symmetry_csv(filename,file,symmetries):
    """Writes a csv file with the name of each frankenlanguage file plus its symmetry score."""
    with open(filename, 'a', encoding="utf8") as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([file] + symmetries)

def generation_results(feature_symmetry_results):
    """Gives each generation of a kinship system a score of 1 or 0 for whether or not it uses a gender distinction. A score is null if there wasn't enough information to tell."""
    results = {}
    gen1_values = []
    gen2_values = []
    for i in feature_symmetry_results:
        if i in generation1:
            gen1_values.append(feature_symmetry_results[i])
        else:
            gen2_values.append(feature_symmetry_results[i])

    if 1 in gen1_values:
        results['generation1'] = 1
    elif 0 in gen1_values:
        results['generation1'] = 0
    elif 'null' in gen1_values:
        results['generation1'] = 'null'

    if 1 in gen2_values:
        results['generation2'] = 1
    elif 0 in gen2_values:
        results['generation2'] = 0
    elif 'null' in gen2_values:
        results['generation2'] = 'null'

    return results



def write_full_csv(filename,language,generation_results):
    """Creates a list of a languages two generation scores, and writes the language name + score to a csv file if the score is not 'null'."""

    result = []
    for i in generation_results:
        result.append(generation_results[i])


    if 'null' in result:
        pass
    else:
        with open(filename, 'a', encoding='utf8') as csv_file:
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow([language,result])

def write_headers(filename):
    with open(filename, 'a', encoding='utf8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['LANGUAGE','GENDER'])

def main(argv):
    directory_counter = 0

    for i in range(int(argv)):
        directory_counter += 1
        files = get_csv_files('../frankenlanguages/' + str(directory_counter))
        write_headers('../data/frankenlanguages_gender.csv')

        for file in files:
            kin_terms = get_kin(file,str(directory_counter))
            feature_symmetry_results = check_feature_symmetry(kin_terms)
            gen_results = generation_results(feature_symmetry_results)

            write_full_csv('../data/frankenlanguages_gender.csv',file + '_' + str(directory_counter),gen_results)

# if __name__ == '__main__':
#     main(sys.argv[1])

ks = get_kin('English_stan1293.csv','Indo-European')
generation1,generation2 = list_generations(ks)
gen1_pattern = enumerate_generation1(generation1)
gen2_pattern = enumerate_generation(generation2)

print(gen1_pattern,gen2_pattern)
check_pattern(gen1_pattern,gen2_pattern)
