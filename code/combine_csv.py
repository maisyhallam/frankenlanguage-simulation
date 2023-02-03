import pandas as pd
import glob
import os


def merge_files(feature):
    files = os.path.join('../data/' + feature + '/*.csv')
    files_to_merge = glob.glob(files)
    merged_files = pd.concat(map(pd.read_csv,files_to_merge), ignore_index=True)
    merged_files.to_csv('../data/' + feature + '_merged_files.csv',index=False, encoding='utf-8-sig')

parameter = input('Which feature do you want to merge the data for? ')

merge_files(parameter)
