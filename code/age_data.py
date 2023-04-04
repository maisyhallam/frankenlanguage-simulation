### AGE ###
pairs = {
'siblings': [('meB','myB'),('meZ','myZ')],
'm_siblings': [('mMeB','mMyB'),('mMeZ','mMyZ')],
'f_siblings': [('mFeB','mFyB'),('mFeZ','mFyZ')],
'mz_cousins': [('mMeZeS','mMeZyS'),('mMeZeD','mMeZyD'),('mMyZeS','mMyZyS'),('mMyZeD','mMyZyD'),('mMZeS','mMZyS'),('mMZeD','mMZyD')],
'mb_cousins': [('mMeBeS','mMeByS'),('mMeBeD','mMeByD'),('mMyBeS','mMyByS'),('mMyBeD','mMyByD'),('mMBeS','mMByS'),('mMBeD','mMByD')],
'fz_cousins': [('mFeZeS','mFeZyS'),('mFeZeD','mFeZyD'),('mFyZeS','mFyZyS'),('mFyZeD','mFyZyD'),('mFZeS','mFZyS'),('mFZeD','mFZyD')],
'fb_cousins': [('mFeBeS','mFeByS'),('mFeBeD','mFeByD'),('mFyBeS','mFyByS'),('mFyBeD','mFyByD'),('mFBeS','mFByS'),('mFBeD','mFByD')]
}

generation1_pairs = [('meB','myB'),('meZ','myZ'),
                         ('mMeZeS','mMeZyS'),('mMeZeD','mMeZyD'),('mMyZeS','mMyZyS'),('mMyZeD','mMyZyD'),('mMZeS','mMZyS'),('mMZeD','mMZyD'),
                         ('mMeBeS','mMeByS'),('mMeBeD','mMeByD'),('mMyBeS','mMyByS'),('mMyBeD','mMyByD'),('mMBeS','mMByS'),('mMBeD','mMByD'),
                         ('mFeZeS','mFeZyS'),('mFeZeD','mFeZyD'),('mFyZeS','mFyZyS'),('mFyZeD','mFyZyD'),('mFZeS','mFZyS'),('mFZeD','mFZyD'),
                         ('mFeBeS','mFeByS'),('mFeBeD','mFeByD'),('mFyBeS','mFyByS'),('mFyBeD','mFyByD'),('mFBeS','mFByS'),('mFBeD','mFByD')]

generation2_pairs = [('mMeB','mMyB'),('mMeZ','mMyZ'),('mFeB','mFyB'),('mFeZ','mFyZ')]

kin_types = ['siblings','m_siblings','f_siblings','mz_cousins','mb_cousins','fz_cousins','fb_cousins']

generation1 = ['siblings', 'mz_cousins','mb_cousins','fz_cousins','fb_cousins']
generation2 = ['m_siblings','f_siblings']
