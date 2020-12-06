import os
os.system("")
class log:
    red="\u001b[91m"
    yellow="\u001b[93m"
    green="\u001b[92m"
    white="\u001b[97m"
    cyan="\u001b[96m"
    def error(text):
        print(log.red+str(text))
    def warn(text):
        print(log.yellow+str(text))
    def notify(text):
        print(log.green+str(text))
    def say(text):
        print(log.white+str(text))
    def special(text):
        print(log.cyan+str(text))

