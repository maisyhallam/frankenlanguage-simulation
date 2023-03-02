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

generation1_pairs = [('meB','meZ'),('myB','myZ'),('mMeZeS','mMeZeD'),('mMeZyS','mMeZyD'),('mMeZS','mMeZD'),
('mMyZeS','mMyZeD'),('mMyZyS','mMyZyD'),('mMyZS','mMyZD'),('mMZeS','mMZeD'),('mMZyS','mMZyD'),('mMZS','mMZD'),
('mMeBeS','mMeBeD'),('mMeByS','mMeByD'),('mMeBS','mMeBD'),('mMyBeS','mMyBeD'),('mMyByS','mMyByD'),('mMyBS','mMyBD'),
('mMBeS','mMBeD'),('mMByS','mMByD'),('mMBS','mMBD'),('mFeZeS','mFeZeD'),('mFeZyS','mFeZyD'),('mFeZS','mFeZD'),
('mFyZeS','mFyZeD'),('mFyZyS','mFyZyD'),('mFyZS','mFyZD'),('mFZeS','mFZeD'),('mFZyS','mFZyD'),('mFZS','mFZD'),
('mFeBeS','mFeBeD'),('mFeByS','mFeByD'),('mFeBS','mFeBD'),('mFyBeS','mFyBeD'),('mFyByS','mFyByD'),('mFyBS','mFyBD'),
('mFBeS','mFBeD'),('mFByS','mFByD'),('mFBS','mFBD')]

generation2_pairs = [('mMeB','mMeZ'),('mMyB','mMyZ'),('mFeB','mFeZ'),('mFyB','mFyZ')]

kin_types = ['siblings','m_siblings','f_siblings','mz_cousins','mb_cousins','fz_cousins','fb_cousins']

generation1 = ['siblings', 'mz_cousins','mb_cousins','fz_cousins','fb_cousins']
generation2 = ['m_siblings','f_siblings']

# list of language families, ie directory names that the kinbank data is divided into
families = ['Austroasiatic', 'Sino-Tibetan', 'Afro-Asiatic',
'Indo-European', 'Pano-Tacanan', 'Nuclear Trans New Guinea',
'Pama-Nyungan', 'Tai-Kadai', 'Other', 'Arawakan', 'Austronesian', 'Algic',
'Cariban', 'Nakh-Daghestanian', 'Turkic', 'Dravidian', 'Uto-Aztecan',
'Atlantic-Congo', 'Uralic', 'Tupian']

def get_kin(file_path,type,term):
    """Loads in a frankenlanguage csv file, populates a dictionary with the kin terms."""
    kin_terms = {}
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            parameter = line[type] # kin type
            word = line[term] # kin term
            kin_terms[parameter] = word
    return kin_terms

def denominator(generation_list,number):
    """Returns the number of possible relationships that could have this distinction."""
    denominator = 0
    for kin_type in generation_list:
        for pair in gender_pairs[kin_type]:
            denominator += 1
    denominator -= number
    return denominator

def check_feature_symmetry(ks):
    """Checks whether the terms used in the language for each pair of kin terms match."""
    results = {}

    for kin in kin_types:
        count = 0
        for pair in gender_pairs[kin]:
            if pair[0] in ks.keys() and pair[1] in ks.keys():
                if ks[pair[0]] == ks[pair[1]]:
                    results[pair] = 0
                else:
                    results[pair] = 1
            else:
                results[pair] = 'null'

    print(results)
    return results

def get_csv_files(path):
    """Fetches a list of files from the directory located by the given filepath."""
    directory = os.scandir(path)
    files = []
    for file in directory:
        files.append(file.name)
    return files

def get_language_name(string):
    """Extract the language name from the filename of kinbank data."""
    language_name = ''
    if string.startswith('Morgan1871_'):
        string = string[len('Morgan1871_'):]
    for i in range(len(string)-13):
        language_name += string[i]
    return language_name


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
        if i in generation1_pairs:
            gen1_values.append(feature_symmetry_results[i])
        else:
            gen2_values.append(feature_symmetry_results[i])

    gen1_nulls = gen1_values.count('null')
    gen2_nulls = gen2_values.count('null')

    # unsure whether to keep this or not - seems unfair either way to count or not count where there isn't enough data to know for sure if a distinction is made
    gen1_values = [x for x in gen1_values if x != 'null']
    gen2_values = [x for x in gen2_values if x != 'null']

    gen1_denominator = denominator(generation1,gen1_nulls)
    gen2_denominator = denominator(generation2,gen2_nulls)

    if gen1_denominator == 0:
        results['generation1'] = 'null'
    else:
        results['generation1'] = sum(gen1_values)/gen1_denominator

    if gen2_denominator == 0:
        results['generation2'] = 'null'
    else:
        results['generation2'] = sum(gen2_values)/gen2_denominator

    return results



def write_full_csv(filename,language,generation_results,set):
    """Creates a list of a languages two generation scores, and writes the language name + score to a csv file if the score is not 'null'."""
    generation1 = generation_results['generation1']
    generation2 = generation_results['generation2']
    if generation1 == 'null' or generation2 == 'null':
        pass
    else:
        with open(filename, 'a', encoding='utf8') as csv_file:
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow([language,generation1,generation2,set])

def write_headers(filename):
    with open(filename, 'a', encoding='utf8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['LANGUAGE','GEN_0','GEN_1','SET'])

def main(data_type,count):
    if data_type == 'kinbank':
        filename = '../data/gender/prop/kinbank.csv'
        write_headers(filename)

        for family in families:
            files = get_csv_files('../kinbank/raw/' + family)

            for file in files:
                ks = get_kin('../kinbank/raw/' + family + '/' + file,'parameter','word')
                language = get_language_name(file)
                feature_symmetry_results = check_feature_symmetry(ks)
                gen_results = generation_results(feature_symmetry_results)

                write_full_csv(filename,language,gen_results,'kinbank')

    if data_type == 'frankenlanguage':
        file_path = '../frankenlanguages/'
        directory_counter = 0

        for i in range(int(count)):
            directory_counter += 1
            filename = '../data/gender/prop/prop_set' + str(directory_counter) + '.csv'
            files = get_csv_files(file_path + str(directory_counter))
            write_headers(filename)


            for file in files:
                ks = get_kin(file_path + str(directory_counter) + '/' + file,'TYPE','TERM')
                feature_symmetry_results = check_feature_symmetry(ks)
                gen_results = generation_results(feature_symmetry_results)
                language = file + '_' + str(directory_counter)

                write_full_csv(filename,language,gen_results,str(directory_counter))

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
