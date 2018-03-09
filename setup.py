#!/usr/bin/env python
from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]
classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat'
]

setup(
    name='groupmebot',
    version='0.0.2',
    packages=['groupmebot'],
    url='https://github.com/clayscode/GroupMeBot',
    author='',
    author_email='',
    install_requires=reqs,
    classifiers=classifiers,
    description="Interactive client for GroupMe messaging system",
    keywords='groupme messaging client console interactive',
    entry_points={'console_scripts': ['groupmebot=groupmebot.__main__:main']}
)
