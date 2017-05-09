from setuptools import setup
from pip.req import parse_requirements
import sys

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]
 
setup(
    name='groupmebot',
    version='0.0.1',
    packages=['groupmebot'],
    url='https://github.com/clayscode/GroupMeBot',
    license='',
    author='',
    author_email='',
    description='GroupMe Bot',
    install_requires=reqs
)
