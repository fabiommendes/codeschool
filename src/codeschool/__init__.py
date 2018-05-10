"""
Overview of codeschool codebase:

Sub-Packages

- cli: command line scripts that helps managing codeschool
- config: django settings, templates and project files
- hyper: jinja2/hyperpython components
- fixes: monkey-patch 3rd party libs


Django apps and app groups

- cs_accounts: user authentication, login and signup (uses userena)
- cs_extra: optional codeschool activities
- cs_gamification: points, badges and stars
- cs_lms: learning management system, control courses, grades, etc
- cs_questions: implement different question types
- cs_social: social network capabilities


Tests

- /tests/: global tests
- /tests/<app>/: separated by group of app
"""

from codeschool import fixes as _fixes
_fixes.apply()
