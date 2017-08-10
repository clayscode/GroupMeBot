from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='groupme',
    version='0.0.2',
    packages=['groupmebot'],
    url='https://github.com/clayscode/GroupMeBot',
    license='',
    author='',
    author_email='',
    description='GroupMe API',
    install_requires=reqs
)
