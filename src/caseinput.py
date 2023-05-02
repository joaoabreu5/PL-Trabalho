from singleinput import SingleInput
class CaseInput:
    def __init__(self, inputCase):
        self.inputCase = inputCase
        
    def __eq__(self, other):
        i = 0
        
        while i < len(self):
            i1 = SingleInput(self.inputCase[i])
            i2 = SingleInput(other.inputCase[i])
            if i1 != i2:
                return False
            i+=1
            
        return True

    def __lt__(self, other):
        i = 0
        
        while i < len(self):
            i1 = SingleInput(self.inputCase[i])
            i2 = SingleInput(other.inputCase[i])
            if i1 < i2:
                return True
            i+=1
            
        return False
    
    def __hash__(self):
        return str(self.inputCase)
    
    def __len__(self):
        return len(self.inputCase)

    def __str__(self):
        return str(self.inputCase)