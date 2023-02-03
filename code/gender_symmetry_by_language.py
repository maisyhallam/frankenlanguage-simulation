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

age_pairs = {'siblings': [('meB','myB'),('meZ','myZ')],
'm_siblings': [('mMeB','mMyB'),('mMeZ','mMyZ')],
'f_siblings': [('mFeB','mFyB'),('mFeZ','mFyZ')],
'mez_cousins': [('mMeZeS','mMeZyS'),('mMeZeD','mMeZyD')],
'meb_cousins': [('mMeBeS','mMeByS'),('mMeBeD','mMeByD')],
'fez_cousins': [('mFeZeS','mFeZyS'),('mFeZeD','mFeZyD')],
'feb_cousins': [('mFeBeS','mFeByS'),('mFeBeD','mFeByD')],
'myz_cousins': [('mMyZeS','mMyZyS'),('mMyZeD','mMyZyD')],
'myb_cousins': [('mMyBeS','mMyByS'),('mMyBeD','mMyByD')],
'fyz_cousins': [('mFyZeS','mFyZyS'),('mFyZeD','mFyZyD')],
'fyb_cousins': [('mFyBeS','mFyByS'),('mFyBeD','mFyByD')],
'mz_cousins': [('mMZeS','mMZyS'),('mMZeD','mMZyD')],
'mb_cousins': [('mMBeS','mMByS'),('mMBeD','mMByD')],
'fz_cousins': [('mFZeS','mFZyS'),('mFZeD','mFZyD')],
'fb_cousins': [('mFBeS','mFByS'),('mFBeD','mFByD')]
}

lineage_pairs = {'p_siblings': [('mMeB','mFeB'),('mMeZ','mFeZ'),('mMyB','mFyB'),('mMyZ','mFyZ')],
'pez_cousins': [('mMeZeS','mFeZeS'),('mMeZeD','mFeZeD'),('mMeZyS','mFeZyS'),('mMeZyD','mFeZyD')],
'peb_cousins': [('mMeBeS','mFeBeS'),('mMeBeD','mFeBeD'),('mMeByS','mFeByS'),('mMeByD','mFeByD')],
'pyz_cousins': [('mMyZeS','mFyZeS'),('mMyZeD','mMyFeD'),('mMyZyS','mFyZyS'),('mMyZyD','mFyZyD')],
'pyb_cousins': [('mMyBeS','mFyBeS'),('mMyBeD','mFyBeD'),('mMyByS','mFyByS'),('mMyByD','mFyByD')],
'pz_cousins': [('mMZeS','mFZyS'),('mMZeD','mFZyD')],
'pb_cousins': [('mMBeS','mFByS'),('mMBeD','mFByD')]
}

kin_types = ['siblings','m_siblings','f_siblings','mez_cousins','meb_cousins','fez_cousins','feb_cousins',
'myz_cousins','myb_cousins','fyz_cousins','fyb_cousins','mz_cousins','mb_cousins','fz_cousins','fb_cousins']

lineage_kin_types = ['p_siblings','pez_cousins','peb_cousins','pyz_cousins','pyb_cousins','pz_cousins','pb_cousins']

generation1 = ['siblings', 'mz_cousins','mb_cousins','fz_cousins','fb_cousins']
generation2 = ['m_siblings','f_siblings']
# ['G0','G+1','G+1','G0','G0','G0','G0']

lineage_generation1 = ['pez_cousins','peb_cousins','pyz_cousins','pyb_cousins','pz_cousins','pb_cousins']
lineage_generation2 = ['p_siblings']

features = ['gender','age','lineage']

# load in a language csv file, populate a dictionary with the kin terms
def get_kin(family,file):
    # print(file)
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

# do the actual terms used in a language for the pairs of kin terms for each relationship match?
def check_feature_symmetry(ks,feature):
    results = {}

    if feature == 'age':

        for kin in kin_types:
            for pair in age_pairs[kin]:
                if pair[0] in ks.keys() and pair[1] in ks.keys():
                    if ks[pair[0]] == ks[pair[1]]:
                        results[kin] = 0
                    else:
                        results[kin] = 1
                else:
                    continue
            if kin not in results:
                results[kin] = 'null'


    elif feature == 'gender':

            for kin in kin_types:
                # print(kin)
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

    elif feature == 'lineage':

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

# if symmetry = 0, there is no feature symmetry. if > 0, there is symmetry.
def symmetry_or_not(feature_symmetry_results, feature):
    # print(feature_symmetry_results)
    sum_gen_1 = []
    sum_gen_2 = []

    if feature == 'lineage':
        for kin in lineage_generation1:
            sum_gen_1.append(feature_symmetry_results[kin])
        for kin in lineage_generation2:
            sum_gen_2.append(feature_symmetry_results[kin])

    else:
        for kin in generation1:
            sum_gen_1.append(feature_symmetry_results[kin])
        for kin in generation2:
            sum_gen_2.append(feature_symmetry_results[kin])

    if gen1_counts['yes'] > 0 and gen2_counts['yes'] > 0:
        symmetry = (1,1)
    elif gen1_counts['yes'] == 0 and gen2_counts['yes'] > 0:
        symmetry = (0,1)
    elif gen1_counts['yes'] > 0 and gen2_counts['yes'] == 0:
        symmetry = (1,0)
    elif gen1_counts['yes'] == 0 and gen2_counts['yes'] == 0:
        symmetry = (0,0)

    # print(symmetry)
    return symmetry

def get_language_name(string):
    language_name = ''
    if string.startswith('Morgan1871_'):
        string = string[len('Morgan1871_'):]
    for i in range(len(string)-13):
        language_name += string[i]
    return language_name

# get a list of the kinbank csv files
def get_csv_files(path):
    directory = os.scandir(path)
    files = []
    for file in directory:
        files.append(file.name)
    return files

# write the csv file with our results
def write_symmetry_csv(filename,file,symmetries):
    language = get_language_name(file)
    with open(filename, 'a', encoding="utf8") as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([language] + symmetries)

def generation_results(feature_symmetry_results):
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



def write_full_csv(filename,file,generation_results):
    result = []
    for i in generation_results:
        result.append(generation_results[i])
    # if feature == 'lineage':
    #     for i in full_results:
    #         result = i[0]
    #         if i in lineage_generation1:
    #             generation = 'n'
    #         else:
    #             generation = 'n+1'
    # else:
    #     for i in full_results:
    #         result = i[0]
    #         if i in generation1:
    #             generation = 'n'
    #         else:
    #             generation = 'n+1'
    if 'null' in result:
        pass
    else:
        with open(filename, 'a', encoding='utf8') as csv_file:
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow([language,result])

families = ['Austroasiatic', 'Sino-Tibetan', 'Afro-Asiatic',
'Indo-European', 'Pano-Tacanan', 'Nuclear Trans New Guinea',
'Pama-Nyungan', 'Tai-Kadai', 'Other', 'Arawakan', 'Austronesian', 'Algic',
'Cariban', 'Nakh-Daghestanian', 'Turkic', 'Dravidian', 'Uto-Aztecan',
'Atlantic-Congo', 'Uralic', 'Tupian']

with open('gender_distinction_pruned.csv', 'a') as csv_file:
    csvwriter = csv.writer(csv_file)
    # csvwriter.writerow(['LANGUAGE','GENDER SYMMETRY','AGE SYMMETRY','LINEAGE SYMMETRY'])
    csvwriter.writerow(['LANGUAGE','GENDER'])


full_results = {}

for family in families:
    files = get_csv_files(r'raw/' + family)

    for file in files:
        kin_terms = get_kin(family,file)
        language = get_language_name(file)
        # symmetries = []
        feature_symmetry_results = check_feature_symmetry(kin_terms,'gender')
        gen_results = generation_results(feature_symmetry_results)

        write_full_csv('gender_distinction_pruned.csv',file,gen_results)


        # for feature in features:
        #     feature_symmetry_results = check_feature_symmetry(kin_terms,feature)
        #     write_full_csv('feature_distinction.csv',file,feature_symmetry_results,feature,breaks)
        #     symmetries.append(symmetry_or_not(feature_symmetry_results,feature))
        #
        # write_symmetry_csv('feature_symmetry.csv',file,symmetries)
