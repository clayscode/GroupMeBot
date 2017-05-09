import json
import sys
class settings:
    def __init__(self):
        try:
                json_data = open("config.json").read()
                data = json.loads(json_data)
                self.accessToken = data['accessToken']
                self.botId = data['botId']
                self.groupId = data['groupId']
                self.userId = data['userId']
                self.idNum = 0
        except IOError:
                print("config.json not found! Please run setup.py.")
                sys.exit(1)
