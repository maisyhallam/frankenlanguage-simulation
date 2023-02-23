# This script takes the raw csv files from KinBank and for each language checks if the same
# feature distinctions are made anywhere in G0 and G+1. It populates a new csv file with this information.
# The goal is to see whether feature symmetry is universal (or near-universal) in kinship systems cross-linguistically.

import csv
import os

#load in a language csv file, populate a dictionary with the kin terms
def get_kin(family,file):
    file_path = 'raw/' + family + '/' + file
    kin_terms = {}
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        next(csv_reader) #skip the header
        for line in csv_reader:
            parameter = line['parameter'] #relationship
            word = line['word'] #kin term
            kin_terms[parameter] = word
    return kin_terms

# check if a pair of kin terms are identical or not
def check_equality(pair1,pair2):
    if pair1[0] == pair1[1] and pair2[0] == pair2[1]:
        return '0'
    else:
        return '1'

#a function to evaluate whether siblings, cousins, and parents' siblings are distinguished by gender or age
def check_feature_symmetry(family,file):
    kt = get_kin(family,file)

    kin_types = ['siblings','m siblings','f siblings','mz cousins','mb cousins','fz cousins','fb cousins']
    generations = ['G0','G+1','G+1','G0','G0','G0','G0']

    gender_pairs = [[('meB','meZ'),('myB','myZ')], #siblings
    [('mMeB','mMeZ'),('mMyB','mMyZ')], #m siblings
    [('mFeB','mFeZ'),('mFyB','mFyZ')], #f siblings
    [('mMeZS','mMeZD'),('mMyZS','mMyZD')], #mz cousins
    [('mMeBS','mMeBD'),('mMyBS','mMyBD')], #mb cousins
    [('mFeZS','mFeZD'),('mFyZS','mFyZD')], #fz cousins
    [('mFeBS','mFeBD'),('mFyBS','mFyBD')]] #fb cousins


    age_pairs = [[('meB','myB'),('meZ','myZ')],
    [('mMZeS','mMZyS'),('mMZeD','mMZyD')],
    [('mMBeS','mMByS'),('mMBeD','mMByD')],
    [('mFZeS','mFZyS'),('mFZeD','mFZyD')],
    [('mFBeS','mFByS'),('mFBeD','mFByD')],
    [('mMeB','mMyB'),('mMeZ','mMyZ')],
    [('mFeB','mFyB'),('mFeZ','mFyZ')]]

    results = []

    for i in range(len(kin_types)):
        gender = pair_kin_terms(kt,gender_pairs)
        # age = pair_kin_terms(kt,age_pairs)
        print(gender[i])
        for pair in gender[i]:
            if pair[0] not in kt.keys() or pair[1] not in kt.keys():
                continue
            else:
                gender_result = check_equality(gender[i][0],gender[i][1])
                results.append((kin_types[i],generations[i],gender_result))

    return results

# a function to match kin codes to actual kin terms in a particular language,
# so we can evaluate whether two kin terms are the same
def pair_kin_terms(kin_system,pairs):
    list = []
    for kin_type in pairs:
        x = kin_type[0][0]
        y = kin_type[0][1]
        a = kin_type[1][0]
        b = kin_type[1][1]
        # try:
        #list.append([(kin_system[x],kin_system[y]),(kin_system[a],kin_system[b])])
        # except:
        #     # add another try to just add mother's brother's daughter etc if relative age is not included in the language file
        #     continue
        if x not in kin_system.keys() or y not in kin_system.keys() or a not in kin_system.keys() or b not in kin_system.keys():
            continue
        else:
            list.append([(kin_system[x],kin_system[y]),(kin_system[a],kin_system[b])])
    return list

# a function to extract the language name from the filename
def get_language_name(string):
    language_name = ''
    for i in range(len(string)-13):
        language_name += string[i]
    return language_name

# a function to write the results to a csv file
def write_to_csv(filename,family,file):
    language = get_language_name(file)
    line = check_feature_symmetry(family,file)
    with open(filename, 'a', encoding="utf8") as csv_file:
        csvwriter = csv.writer(csv_file)
        for kin_type,generation,gender in line:
            csvwriter.writerow([language,kin_type,generation,gender])

def get_csv_files(path):
    directory = os.scandir(path)
    files = []
    for file in directory:
        files.append(file.name)
    return files

families = ['Austroasiatic', 'Sino-Tibetan', 'Afro-Asiatic',
'Indo-European', 'Pano-Tacanan', 'Nuclear Trans New Guinea',
'Pama-Nyungan', 'Tai-Kadai', 'Other', 'Arawakan', 'Austronesian', 'Algic',
'Cariban', 'Nakh-Daghestanian', 'Turkic', 'Dravidian', 'Uto-Aztecan',
'Atlantic-Congo', 'Uralic', 'Tupian']

with open('feature_symmetry.csv', 'a') as csv_file:
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(['LANGUAGE','KIN TYPE','GENERATION','GENDER DISTINGUISHED'])

for family in families:
    files = get_csv_files(r'raw/' + family)
    for file in files:
        write_to_csv('feature_symmetry.csv',family,file)
