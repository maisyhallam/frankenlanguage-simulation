import sys
import csv
import os
from collections import Counter

# pairs is a dictionary showing which kinbank shorthands represent which family relationships
# each tuple in pairs.values represents the pair of kin terms that will be compared for equality
gen2 = ['mMB','mMeB','mMyB','mMZ','mMeZ','mMyZ','mFB','mFeB','mFyB','mFZ','mFeZ','mFyZ']
gen1 = ['mMBS', 'mMBeS', 'mMByS','mMZS','mMZeS','mMZyS','mFBS','mFBeS','mFByS','mFZS','mFZeS','mFByS'] # just one child to keep things simple

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

# def find_relevant_kin(generation):
#     relevant_kin = []
#     for kin_types in generation:
#         # for j in i:
#         #     index = generation2.index(j)
#         #     if j == 'na'
#         #     generation2.remove(j)
#         #     generation1.remove(generation1[i][j])
#         if len(set(kin_types)) == 1:
#             relevant_kin.append([x for x in kin_types if x == kin_types[0]])
#         elif len(set(kin_types)) == 2:
#             relevant_kin.append(list(dict.fromkeys(kin_types)))
#         else:
#             continue
#
#     return relevant_kin

def list_generations(ks,gen):
    """Returns a list of the kin terms for each kin type in gen, na if not available in the data."""
    generation = []
    for kin_type in gen:
        placeholder = []
        if kin_type in ks.keys():
            placeholder.append(ks[kin_type])
        else:
            placeholder.append('na')
        generation += placeholder
    # generation = list(generation[i:i+3] for i in range(0,len(list(generation)),3)) # because there are 3 terms for each kin type right now
    # relevant_kin = find_relevant_kin(generation)
    # print(relevant_kin)
    print(generation)
    return generation




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

def flatten(l):
    return [item for sublist in l for item in sublist]

def code_kin_types(gen):
    codes = {}
    placeholder = []
    code = 0

    # code each unique item in gen_pattern
    for kin_type in gen:
        if kin_type in placeholder:
            continue
        elif kin_type == 'na':
            placeholder.append(0)
        else:
            placeholder.append(kin_type)
            code += 1
            codes[kin_type] = code

    return codes

def enumerate_generation(gen):
    """Turn lists of kin terms into lists of numbers. Each number indicates a unique kin term."""
    codes = code_kin_types(gen)
    code = 0

    for kin_type in set(gen):

        while kin_type in gen:
            index = gen.index(kin_type)

            # label it 0 if na
            if kin_type == 'na':
                gen[index] = 0
            # give it a unique number if anything else
            else:
                gen[index] = codes[kin_type]

    # gen_pattern = list(gen_pattern[i:i+length] for i in range(0,len(list(gen)),length))
    print(gen)
    return gen

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
#
#
#     gen_pattern = [list(gen.values())[i:i+2] for i in range(0,len(list(gen.values())),2)]
#
#     print(gen_pattern)
#     return gen_pattern


def check_pattern(pattern1,pattern2):
    """Checks whether the categories of kin are the same in gen2 as gen1."""
    ICS_score = 0
    denominator = 4

    # for each type of kin
    for i in range(4):
        if pattern2[i] == pattern1[2]: # order of the list matters: so same index of both lists will be the parent/child pair
            if pattern1[i] == 0 or pattern2[i] == 0:
                continue
            else:
                ICS_score += 1
        else:
            continue
    print(ICS_score/denominator)

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
        write_headers('../data/frankenlanguages_ICS.csv')

        for file in files:
            kin_terms = get_kin(file,str(directory_counter))
            feature_symmetry_results = check_feature_symmetry(kin_terms)
            gen_results = generation_results(feature_symmetry_results)

            write_full_csv('../data/frankenlanguages_ICS.csv',file + '_' + str(directory_counter),gen_results)

# if __name__ == '__main__':
#     main(sys.argv[1])

ks = get_kin('English_stan1293.csv','Indo-European')
generation1 = list_generations(ks,gen1)
generation2 = list_generations(ks,gen2)
gen1_pattern = enumerate_generation(generation1)
gen2_pattern = enumerate_generation(generation2)

# print(gen1_pattern,gen2_pattern)
check_pattern(gen1_pattern,gen2_pattern)
