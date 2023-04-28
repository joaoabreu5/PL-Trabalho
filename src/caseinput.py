class CaseInput:
    def __init__(self, inputCase):
        self.inputCase = inputCase
        
    def __eq__(self, other):
        i = 0
        
        while i < len(self):
            if self.inputCase[i]["type"] != other.inputCase[i]["type"]:
                return False
            else:
                if self.inputCase[i]["type"] in ['num','boolean']:
                    if self.inputCase[i]["python"] != other.inputCase[i]["python"]:
                        return False
                elif self.inputCase[i]["type"] == 'list_ht':
                    if len(self.inputCase[i]["vars"]) != len(other.inputCase[i]["vars"]):
                        return False
            i+=1
            
        return True
    
    def __hash__(self):
        return 0
    
    def __len__(self):
        return len(self.inputCase)