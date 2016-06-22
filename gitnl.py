import os
import sys
import subprocess

def parse_to_git(args):
    """
    returns a string with what should be passed to git.  E.g.,
    "push remotename branch"
    """
    #raise NotImplementedError
    return 'push eteq master'

if __name__ == '__main__':
    allargs = ' '.join(sys.argv[1:])
    gitcmds = readcmdline(allargs)

    res = input('Parsed command into "git {}". Enter to continue or anything '
                'else to quit.'.format(gitcmds))
    if res.strip() != '':
        sys.exit(1)

    gitpath = subprocess.check_output(['which', 'git'])
    os.system([gpath] + ' '.join(gitcmds))
