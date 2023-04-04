### LINEAGE ###
pairs = {
'p_siblings': [('mMeB','mFeB'),('mMeZ','mFeZ'),('mMyB','mFyB'),('mMyZ','mFyZ')],
'pz_cousins': [('mMeZeS','mFeZeS'),('mMeZeD','mFeZeD'),('mMeZyS','mFeZyS'),('mMeZyD','mFeZyD'),
               ('mMyZeS','mFyZeS'),('mMyZeD','mMyFeD'),('mMyZyS','mFyZyS'),('mMyZyD','mFyZyD'),
               ('mMZeS','mFZyS'),('mMZeD','mFZyD')],
'pb_cousins': [('mMeBeS','mFeBeS'),('mMeBeD','mFeBeD'),('mMeByS','mFeByS'),('mMeByD','mFeByD'),
                ('mMyBeS','mFyBeS'),('mMyBeD','mFyBeD'),('mMyByS','mFyByS'),('mMyByD','mFyByD'),
                ('mMBeS','mFByS'),('mMBeD','mFByD')]
}

generation1_pairs = [('mMeZeS','mFeZeS'),('mMeZeD','mFeZeD'),('mMeZyS','mFeZyS'),('mMeZyD','mFeZyD'),
               ('mMyZeS','mFyZeS'),('mMyZeD','mMyFeD'),('mMyZyS','mFyZyS'),('mMyZyD','mFyZyD'),
               ('mMZeS','mFZyS'),('mMZeD','mFZyD'),('mMeBeS','mFeBeS'),('mMeBeD','mFeBeD'),('mMeByS','mFeByS'),('mMeByD','mFeByD'),
               ('mMyBeS','mFyBeS'),('mMyBeD','mFyBeD'),('mMyByS','mFyByS'),('mMyByD','mFyByD'),
               ('mMBeS','mFByS'),('mMBeD','mFByD')]

generation2_pairs = [('mMeB','mFeB'),('mMeZ','mFeZ'),('mMyB','mFyB'),('mMyZ','mFyZ')]

kin_types = ['p_siblings','pz_cousins','pb_cousins']

generation1 = ['pz_cousins','pb_cousins']
generation2 = ['p_siblings']
