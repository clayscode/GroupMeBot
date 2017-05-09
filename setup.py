from setuptools import setup
from pip.req import parse_requirements
import sys

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

accessToken = str(raw_input("Enter your accessToken: "))
botId = str(raw_input("Enter your botID: "))
groupId = str(raw_input("Enter your groupId: "))
userId = str(raw_input("Enter your userId: "))

try:
    with open('Config.json','w+') as f:
        f.write('{{\n "accessToken":"{}",\n "botId":"{}",\n "groupId":"{}",\n "userId":"{}"\n}}'.format(accessToken,botId,groupId,userId))
    except:
        print "Unexpected Error. Closing"
        sys.exit(1)
        
setup(
    name='gmbot',
    version='0.0.1',
    packages=['connect','Settings','googlespell'],
    url='https://github.com/clayscode/GroupMeGrammarBot',
    license='',
    author='',
    author_email='',
    description='GroupMe Bot',
    install_requires=reqs
)
