from app.utils.settings import cnf
from app.config.database import Client
from app.services.google import ServiceManager

import json

class UserService():
    
    def __init__(self):
        self.client = Client().get_connection('user_information')

        
    def get_user(self):
        user_data = []
        scopes = ['https://www.googleapis.com/auth/documents.readonly']

        service = ServiceManager().get_service('docs','v1',scopes)
        document = service.documents().get(documentId='').execute()
        
        content = document.get('body').get('content')
        total = 0
        for node_content in content:
            total+=1
            if total == 1:
                continue
            for node_paragraph in node_content.get('paragraph').get('elements'):
                content = {
                    node_content.get('paragraph').get('paragraphStyle').get('namedStyleType')\
                    : node_paragraph.get('textRun').get('content').strip().replace('\t', '')}
                user_data.append(content)
        print(total)
        """with open(cnf.BASE_PATH +'\\app\\resources\\document.json', 'w') as f: 
            json.dump(content, f)
            f.close()
        """
        #user_data = ' '.join(user_data).split()
 

        return user_data
          