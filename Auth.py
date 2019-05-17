from idaapi import Form, warning
import requests
import jwt
BASE_URL = "https://our-amazon-web.com/"
LOGIN_PATH = "api/users/tokens"

class AuthForm(Form):
    def __init__(self):
        self.invert = False
        Form.__init__(self, r"""STARTITEM {id:iUserName}
BUTTON YES* Login
BUTTON CANCEL Cancel
Login form
{FormChangeCb}
<##Enter your username:{iUserName}>
<##Enter your password:{iPassword}>
{iResult}
""", {
            'FormChangeCb': Form.FormChangeCb(self.OnFormChange),
            'iUserName': Form.StringInput(tp=Form.FT_ASCII),
            'iPassword': Form.StringInput(tp=Form.FT_ASCII),
            "iResult": Form.StringLabel(tp=Form.FT_ASCII, value="", sz=1024)
        })
    def OnFormChange(self, fid):
        if fid == -2: # click on ok
            print "Clicked on login"
            user_token = try_to_log_in(self.GetControlValue(self.iUserName), self.GetControlValue(self.iPassword))
            if user_token == "-1":
                warning("Error, unvalid username and password")
            else:
                return 1
        else:
            return 1

def try_to_log_in(username,password):
    return "2"
    #return requests.post("{0}{1}".format(BASE_URL, LOGIN_PATH), data={"username":username, "password": password}).content
    
