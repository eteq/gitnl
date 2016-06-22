import os
import sys
import subprocess
from astropy.io import ascii


def parse_to_git(args):
    """
    returns a string with what should be passed to git.  E.g.,
    "push remotename branchname"
    """

    #os.chdir('/Users/Brian/Work/github_projects/google_models/syntaxnet/')
    cmd = "echo '{0}' | /Users/Brian/Work/github_projects/google_models/syntaxnet/syntaxnet/demo.sh".format(args)

    # send the command thru Parsy McParseface and grab the output
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = p.communicate()
    outlist = out.split('\n')

# 'push my branch myname to a remote nameB'
#
# ['Parse:',
#  'push VB ROOT',
#  ' +-- myname NN dobj',
#  ' |   +-- my PRP$ poss',
#  ' |   +-- branch NN nn',
#  ' +-- to IN prep',
#  ' |   +-- nameB NN pobj',
#  ' |       +-- a DT det',
#  ' |       +-- remote JJ amod',
#  ' +-- . . punct',
#  '']

# <Table length=9>
#  col1  col2  col3 col4 col5 col6  col7  col8 col9 col10
# int64  str6  str1 str4 str4 str1 int64  str5 str1  str1
# ----- ------ ---- ---- ---- ---- ----- ----- ---- -----
#     1   push    _ VERB   VB    _     0  ROOT    _     _
#     2     my    _ PRON PRP$    _     4  poss    _     _
#     3 branch    _ NOUN   NN    _     4    nn    _     _
#     4 myname    _ NOUN   NN    _     1  dobj    _     _
#     5     to    _  ADP   IN    _     1  prep    _     _
#     6      a    _  DET   DT    _     8   det    _     _
#     7 remote    _  ADJ   JJ    _     8  amod    _     _
#     8  nameB    _ NOUN   NN    _     5  pobj    _     _
#     9      .    _    .    .    _     1 punct    _     _


    fulllist = [{'group': 'ROOT', 'fine': 'VRB', 'value': 'push'},
                {'group': 'prep', 'fine': 'in', 'value': 'to'},
                {'group': 'ROOT', 'fine': 'VRB', 'value': 'push'}
                ]

    ind = [i for i, line in enumerate(outlist) if ':Seconds elapsed' in line]
    if not ind:
        raise Exception('No lines found in output from command')
    else:
        ind = ind[-1]

    chunk = outlist[ind+1:]
    t = ascii.read(chunk, names=['level', 'word', 'b1', 'coarse', 'fine', 'b2', 'parent', 'group', 'b3', 'b4'])

    t.sort('parent')
    if t[0]['coarse'] != 'VERB':
        raise Exception('Parent 0 root is not a VERB')
    else:
        gitcmd = t[0]['word']

    parent1 = t['parent'] == 1
    input1 = (t[parent1]['coarse'] == 'NOUN') & (t[parent1]['group'] == 'dobj')

    # before the preposition
    if sum(input1) <= 0:
        raise Exception('No NOUN object in rank 1')
    else:
        input_name = t[parent1][input1]['word'][0]

    preplevel = t[parent1][t[parent1]['group'] == 'prep']['level']
    prepword = t[parent1][t[parent1]['group'] == 'prep']['word'][0]

    # after the preposition
    postprep = t['level'] > preplevel
    input2 = (t[postprep]['coarse'] == 'NOUN') & (t[postprep]['fine'] == 'NN')
    output_name = t[postprep][input2]['word'][0]

    # git syntax VRB
    if prepword == 'to':
        build_git = '{0} {1} {2}'.format(gitcmd, output_name, input_name)
    elif prepword == 'from':
        build_git = '{0} {1} {2}'.format(gitcmd, input_name, output_name)

    return build_git
    #raise NotImplementedError
    #return 'push eteq master'

if __name__ == '__main__':
    allargs = ' '.join(sys.argv[1:])
    gitcmds = parse_to_git(allargs)
    print('my git comamd', gitcmds)

    print('Parsed command into "git {}". Enter to continue or e to quit.'.format(gitcmds))
    #res = input('Parsed command into "git {}". Enter to continue or e to quit.'.format(gitcmds))
    #print(res)
    # if res.strip() == 'e':
    #     sys.exit(1)

    gitpath = subprocess.check_output(['which', 'git']).decode()
    command = gitpath.strip() + ' ' + gitcmds.strip()
    print('Doing this command: "{}"'.format(command))
    sys.exit(os.system(command))
