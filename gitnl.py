from __future__ import print_function, division, absolute_import

import os
import sys
from subprocess import Popen, PIPE, STDOUT, check_output
import pandas as pd


def parse_to_git(args):
    """
    returns a string with what should be passed to git.  E.g.,
    "push remotename branchname"
    """
    print(args)
    inds_prep = np.where(hier['pos'] in ['PRT'])[0]
    if len(inds_prep) == 0:
        print('No preposition found')
    elif len(inds_prep) > 1:
        print('Multiple prepositions found')
    action = args[args['group'] == 'ROOT']['word'].ix[0]
    others = args[args['NOUN'] == 'NOUN']]
    others2 = others[others['parent'] < inds_prep[0]]
        
    kwargs = dict(action=action)
    cmd = 'git {action}'.format(**kwargs)
    # raise NotImplementedError
    # return 'push eteq master'
    

demo_file = '/Users/andrews/software/python/models/syntaxnet/syntaxnet/demo.sh'
phrase = 'push branch test_branch to remote github_repo.'
bash_cmd = 'echo {0} | {1}'.format(phrase, demo_file)
pp = Popen(bash_cmd, shell=True, stdout=PIPE, stderr=STDOUT)
out = pp.communicate()[0]
out_split = out.split('\n')
for i, it in enumerate(out_split):
    if it[0] == '1':
        ind = i
        break

colln_tabbed = out_split[ind:-3]  # need better way to cut off trailing useless rows 
colln = [it.split('\t') for it in colln_tabbed]
columns = ['level', 'word', 'ig1','pos', 'fine', 'ig2', 'parent', 'group', 'ig3', 'ig4']

raw = pd.DataFrame(colln, columns=columns)
useful_cols = ['level', 'word', 'pos', 'fine', 'parent', 'group']
hier = raw[useful_cols]
hier = pd.to_numeric(hier['level'])
hier = pd.to_numeric(hier['parent'])


#  level         word   pos fine parent  group
#      1         push  VERB   VB      0   ROOT
#      2       branch  NOUN   NN      3     nn
#      3  test_branch  NOUN   NN      1   dobj
#      4           to   PRT   TO      5    aux
#      5       remote  VERB   VB      1  xcomp
#      6  github_repo  NOUN   NN      5   dobj

# ['push VB ROOT',
#  ' +-- test_branch NN dobj',
#  ' |   +-- branch NN nn',
#  ' +-- remote VB xcomp',
#  ' |   +-- to TO aux',
#  ' |   +-- github_repo NN dobj']

if __name__ == '__main__':
    # allargs = ' '.join(sys.argv[1:])
    gitcmds = parse_to_git(hier)

    res = input('Parsed command into "git {}". Enter to continue or anything '
                'else to quit.'.format(gitcmds))
    if res.strip() != '':
        sys.exit(1)

    gitpath = check_output(['which', 'git']).decode()
    command = gitpath.strip() + ' ' + gitcmds.strip()
    print('Doing this command: "{}"'.format(command))
    sys.exit(os.system(command))
