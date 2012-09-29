#! /usr/bin/env python

"""
gitbranchcommits.

Copyright 2012 Andy Hull 
andy@atomicrobotmonster.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import git
import pystache
import argparse

def read_commits(repo,base,branch):
    repo = git.Repo(repo)
    return repo.iter_commits(base + '..' + branch)

def make_markdown_renderer(template):
    return lambda context: pystache.render(template, context).encode('utf-8')

def generate(repo,base,branch,render):
    commits = read_commits(repo,base,branch)
    context = { 
        'repository': repo,
        'base': base,
        'target': branch, 
        'commits': list(commits)
    }
    return render(context)

def read_template(filename):
    return open(filename, 'r').read()

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Create release notes from all git commits made in branch "target" that are not in branch "base".',
    epilog="""The following variables are exposed to the mustache template:
    repository - the git repository directory as supplied on the command-line
    base       - the base branch as supplied on the command-line
    target     - the target branch as supplied on the command-line
    commits    - See http://packages.python.org/GitPython/0.3.2/tutorial.html#the-commit-object for more information""")
parser.add_argument('repository',help='git repository directory')
parser.add_argument('base',help='base branch')
parser.add_argument('target',help='target branch')
parser.add_argument('template',help='mustache template for rendering output. See http://http://mustache.github.com/ for more information')
args=parser.parse_args()

render = make_markdown_renderer(read_template(args.template))

print generate(
    args.repository, 
    args.base, 
    args.target, 
    render)
