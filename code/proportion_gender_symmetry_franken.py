import sys
import csv
import os
from collections import Counter

# pairs is a dictionary showing which kinbank shorthands represent which family relationships
# each tuple in pairs.values represents the pair of kin terms that will be compared for equality
gender_pairs = {
'siblings': [('meB','meZ'),('myB','myZ')],
'm_siblings': [('mMeB','mMeZ'),('mMyB','mMyZ')],
'f_siblings': [('mFeB','mFeZ'),('mFyB','mFyZ')],
'mz_cousins': [('mMeZeS','mMeZeD'),('mMeZyS','mMeZyD'),('mMeZS','mMeZD'),
               ('mMyZeS','mMyZeD'),('mMyZyS','mMyZyD'),('mMyZS','mMyZD'),
               ('mMZeS','mMZeD'),('mMZyS','mMZyD'),('mMZS','mMZD')],
'mb_cousins': [('mMeBeS','mMeBeD'),('mMeByS','mMeByD'),('mMeBS','mMeBD'),
               ('mMyBeS','mMyBeD'),('mMyByS','mMyByD'),('mMyBS','mMyBD'),
               ('mMBeS','mMBeD'),('mMByS','mMByD'),('mMBS','mMBD')],
'fz_cousins': [('mFeZeS','mFeZeD'),('mFeZyS','mFeZyD'),('mFeZS','mFeZD'),
               ('mFyZeS','mFyZeD'),('mFyZyS','mFyZyD'),('mFyZS','mFyZD'),
               ('mFZeS','mFZeD'),('mFZyS','mFZyD'),('mFZS','mFZD')],
'fb_cousins': [('mFeBeS','mFeBeD'),('mFeByS','mFeByD'),('mFeBS','mFeBD'),
               ('mFyBeS','mFyBeD'),('mFyByS','mFyByD'),('mFyBS','mFyBD'),
               ('mFBeS','mFBeD'),('mFByS','mFByD'),('mFBS','mFBD')]
}

kin_types = ['siblings','m_siblings','f_siblings','mz_cousins','mb_cousins','fz_cousins','fb_cousins']

generation1 = ['siblings', 'mz_cousins','mb_cousins','fz_cousins','fb_cousins']
generation2 = ['m_siblings','f_siblings']

def get_kin(file,directory):
    """Loads in a frankenlanguage csv file, populates a dictionary with the kin terms."""
    file_path = '../frankenlanguages/' + directory + '/' + file
    kin_terms = {}
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            parameter = line['TYPE'] # kin type
            word = line['TERM'] # kin term
            kin_terms[parameter] = word
    return kin_terms

# def denominator(generation_list):
#     """Returns the number of possible relationships that could have this distinction."""
#     denominator = 0
#     for kin_type in generation_list:
#         for pair in gender_pairs[kin_type]:
#             denominator += 1
#     return denominator

def check_feature_symmetry(ks):
    """Checks whether the terms used in the language for each pair of kin terms match."""
    results = {}

    for kin in kin_types:
        results[kin] = 0
        for pair in gender_pairs[kin]:
            if pair[0] in ks.keys() and pair[1] in ks.keys():
                if ks[pair[0]] == ks[pair[1]]:
                    continue
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
    """Returns the proportion of symmetrical relationships for each generation. A score is null if there wasn't enough information to tell."""
    results = {}
    gen1_values = []
    gen2_values = []
    for i in feature_symmetry_results:
        if i in generation1:
            gen1_values.append(feature_symmetry_results[i])
        else:
            gen2_values.append(feature_symmetry_results[i])

# unsure whether to keep this or not - seems unfair either way to count or not
# count where there isn't enough data to know for sure if a distinction is made
    for j in gen1_values:
        if j == 'null':
            gen1_values.remove(j)
            gen1_denominator -= 1

    for k in gen2_values:
        if k == 'null':
            gen2_values.remove(k)
            gen2_denominator -= 1

    results['generation1'] = sum(gen1_values)/len(generation1)
    results['generation2'] = sum(gen2_values)/len(generation2)

    return results



def write_full_csv(filename,language,generation_results,set):
    """Creates a list of a languages two generation scores, and writes the language name + score to a csv file if the score is not 'null'."""
    generation1 = generation_results['generation1']
    generation2 = generation_results['generation2']
    with open(filename, 'a', encoding='utf8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([language,generation1,generation2,set])

def write_headers(filename):
    with open(filename, 'a', encoding='utf8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['LANGUAGE','GEN_0','GEN_1','SET'])

def main(argv):
    directory_counter = 0

    for i in range(int(argv)):
        directory_counter += 1
        filename = '../data/gender/prop/prop_set' + str(directory_counter) + '.csv'
        files = get_csv_files('../frankenlanguages/' + str(directory_counter))
        write_headers(filename)

        for file in files:
            kin_terms = get_kin(file,str(directory_counter))
            feature_symmetry_results = check_feature_symmetry(kin_terms)
            gen_results = generation_results(feature_symmetry_results)
            language = file + '_' + str(directory_counter)

            write_full_csv(filename,language,gen_results,str(directory_counter))

if __name__ == '__main__':
    main(sys.argv[1])
