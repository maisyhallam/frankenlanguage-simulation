import sys
import csv
import os
from collections import Counter

# pairs is a dictionary showing which kinbank shorthands represent which family relationships
# each tuple in pairs.values represents the pair of kin terms that will be compared for equality
gender_pairs = {'siblings': [('meB','meZ'),('myB','myZ')],
'm_siblings': [('mMeB','mMeZ'),('mMyB','mMyZ')],
'f_siblings': [('mFeB','mFeZ'),('mFyB','mFyZ')],
'mez_cousins': [('mMeZeS','mMeZeD'),('mMeZyS','mMeZyD'),('mMeZS','mMeZD')],
'meb_cousins': [('mMeBeS','mMeBeD'),('mMeByS','mMeByD'),('mMeBS','mMeBD')],
'fez_cousins': [('mFeZeS','mFeZeD'),('mFeZyS','mFeZyD'),('mFeZS','mFeZD')],
'feb_cousins': [('mFeBeS','mFeBeD'),('mFeByS','mFeByD'),('mFeBS','mFeBD')],
'myz_cousins': [('mMyZeS','mMyZeD'),('mMyZyS','mMyZyD'),('mMyZS','mMyZD')],
'myb_cousins': [('mMyBeS','mMyBeD'),('mMyByS','mMyByD'),('mMyBS','mMyBD')],
'fyz_cousins': [('mFyZeS','mFyZeD'),('mFyZyS','mFyZyD'),('mFyZS','mFyZD')],
'fyb_cousins': [('mFyBeS','mFyBeD'),('mFyByS','mFyByD'),('mFyBS','mFyBD')],
'mz_cousins': [('mMZeS','mMZeD'),('mMZyS','mMZyD'),('mMZS','mMZD')],
'mb_cousins': [('mMBeS','mMBeD'),('mMByS','mMByD'),('mMBS','mMBD')],
'fz_cousins': [('mFZeS','mFZeD'),('mFZyS','mFZyD'),('mFZS','mFZD')],
'fb_cousins': [('mFBeS','mFBeD'),('mFByS','mFByD'),('mFBS','mFBD')]
}

kin_types = ['siblings','m_siblings','f_siblings','mez_cousins','meb_cousins','fez_cousins','feb_cousins',
'myz_cousins','myb_cousins','fyz_cousins','fyb_cousins','mz_cousins','mb_cousins','fz_cousins','fb_cousins']

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

if __name__ == '__main__':
    main(sys.argv[1])
