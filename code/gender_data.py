### GENDER ###
pairs = {
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
