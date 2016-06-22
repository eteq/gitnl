from __future__ import print_function, division, absolute_import

import unittest
import gitnl


class GitnlTestCase(unittest.TestCase):
    """Tests from 'gitnl.py'."""

    def test_push_remotename_branchfrom(self):
        desired = 'push remotename branchfrom'
        actual = gitnl.parse_to_git('push my branch branchfrom to a remote called remotename')
        self.assertEqual(actual, desired)

    def test_rename_branch_locally(self):
        desired = 'branch -m old_branch new_branch'
        actual = gitnl.parse_to_git('branch rename branch old_branch to new_branch')
        self.assertEqual(actual, desired)

if __name__ == '__main__':
    unittest.main()
