import os.path
import requests
import json
from requests.auth import HTTPDigestAuth

class CloudApi(object):
    req = requests.Session()

    def __init__(self, username, password):
        self.req.auth = requests.auth.HTTPDigestAuth(username, password)
        self.req.headers.update({'Accept': 'application/json'})

    def requestAccount(self):
        r = self.req.get('https://my.cl.ly/account')
        print r.text
    
    def reuestItems(self):
        r = self.req.get('https://my.cl.ly/v3/items')
        print r.text        

    def getUploadParam(self, fileName):
        payload = {'name':fileName}
        r = self.req.post('https://my.cl.ly/v3/items', data=json.dumps(payload))
        res = json.loads(r.text)
        return res

    def uploadFile(self, filePath):
        fileName = os.path.basename(filePath)
        
        res = self.getUploadParam(fileName)

        data = res['s3']
        data['key'] = data['key'].replace('${filename}', fileName)

        files = {'file': open(filePath, 'rb')}
        r = requests.post(res['url'], data=data, files=files, allow_redirects=False)

        #get upload file url
        confirmUrl = r.headers['Location'] 
        r = self.req.get(confirmUrl)

        #file url
        r.text['share_url']

api = CloudApi('your_username', "your_password")
api.uploadFile('1.jpg')