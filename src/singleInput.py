import copy


class SingleInput:
    def __init__(self, inputDict, extraVar=None, extraList=None):
        self.inputDict = inputDict
        self.extraVar = extraVar
        self.extraList = extraList

    def __eq__(self, other):
        if self.inputDict["type"] != other.inputDict["type"]:
            return False
        else:
            if self.inputDict["type"] in ['num', 'boolean']:
                if self.inputDict["python"] != other.inputDict["python"]:
                    return False
            elif self.inputDict["type"] == 'list_ht':
                if len(self.inputDict["vars"]) != len(other.inputDict["vars"]):
                    return False

        return True

    def __lt__(self, other):
        if self.inputDict["type"] == 'any' and other.inputDict["type"] != 'any':
            return True
        if self.inputDict["type"] == 'list_ht' and other.inputDict["type"] == 'list_ht':
            if len(self.inputDict["vars"]) < len(other.inputDict["vars"]):
                return True

        return False

    def __hash__(self):
        inputDict_copy = copy.deepcopy(self.inputDict)

        if 'lineno' in inputDict_copy:
            inputDict_copy.pop('lineno')

        if 'lexpos' in inputDict_copy:
            inputDict_copy.pop('lexpos')

        if 'lastpos' in inputDict_copy:
            inputDict_copy.pop('lastpos')

        if 'type' in inputDict_copy and inputDict_copy['type'] == 'any' and 'python' in inputDict_copy:
            inputDict_copy.pop('python')
            
        if 'type' in inputDict_copy and inputDict_copy['type'] == 'list_ht' and 'vars' in inputDict_copy:
                inputDict_copy['vars'] = len(inputDict_copy['vars'])

        return hash(tuple(sorted(inputDict_copy.items())))

    def __len__(self):
        return len(self.inputDict)

    def __str__(self):
        return str(self.inputDict)
