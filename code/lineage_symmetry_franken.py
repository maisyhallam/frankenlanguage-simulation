import sys
import csv
import os
from collections import Counter

# pairs is a dictionary showing which kinbank shorthands represent which family relationships
# each tuple in pairs.values represents the pair of kin terms that will be compared for equality
lineage_pairs = {'p_siblings': [('mMeB','mFeB'),('mMeZ','mFeZ'),('mMyB','mFyB'),('mMyZ','mFyZ')],
'pez_cousins': [('mMeZeS','mFeZeS'),('mMeZeD','mFeZeD'),('mMeZyS','mFeZyS'),('mMeZyD','mFeZyD')],
'peb_cousins': [('mMeBeS','mFeBeS'),('mMeBeD','mFeBeD'),('mMeByS','mFeByS'),('mMeByD','mFeByD')],
'pyz_cousins': [('mMyZeS','mFyZeS'),('mMyZeD','mMyFeD'),('mMyZyS','mFyZyS'),('mMyZyD','mFyZyD')],
'pyb_cousins': [('mMyBeS','mFyBeS'),('mMyBeD','mFyBeD'),('mMyByS','mFyByS'),('mMyByD','mFyByD')],
'pz_cousins': [('mMZeS','mFZyS'),('mMZeD','mFZyD')],
'pb_cousins': [('mMBeS','mFByS'),('mMBeD','mFByD')]
}

lineage_kin_types = ['p_siblings','pez_cousins','peb_cousins','pyz_cousins','pyb_cousins','pz_cousins','pb_cousins']

lineage_generation1 = ['pez_cousins','peb_cousins','pyz_cousins','pyb_cousins','pz_cousins','pb_cousins']
lineage_generation2 = ['p_siblings']

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

    for kin in lineage_kin_types:
        for pair in lineage_pairs[kin]:
            if pair[0] in ks.keys() and pair[1] in ks.keys():
                if ks[pair[0]] == ks[pair[1]]:
                    results[kin] = 0
                else:
                    results[kin] = 1
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
    """Gives each generation of a kinship system a score of 1 or 0 for whether or not it uses a side of the family distinction. A score is null if there wasn't enough information to tell."""
    results = {}
    gen1_values = []
    gen2_values = []
    for i in feature_symmetry_results:
        if i in lineage_generation1:
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
        csvwriter.writerow(['LANGUAGE','LINEAGE'])

def main(argv):
"""For however many frankenlanguages there are (specified by an argument given on the command line), 
    directory_counter = 0

    for i in range(int(argv)):
        directory_counter += 1
        files = get_csv_files('../frankenlanguages/' + str(directory_counter))
        write_headers('../data/frankenlanguages_lineage.csv')

        for file in files:
            kin_terms = get_kin(file,str(directory_counter))
            feature_symmetry_results = check_feature_symmetry(kin_terms)
            gen_results = generation_results(feature_symmetry_results)

            write_full_csv('../data/frankenlanguages_lineage.csv',file + '_' + str(directory_counter),gen_results)

if __name__ == '__main__':
    main(sys.argv[1])
