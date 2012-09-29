relnotes
========

Quick and easy tools for building release notes.

gitcommits.py
-------------------

Render git commits using a user-supplied mustache template. 

To see all commits made to branch bar that are not present on branch foo in "myrepo" and render using the sample mustache template:

gitcommits.py myrepo foo..bar template/gitcommits.py