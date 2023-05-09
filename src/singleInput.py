import copy


class SingleInput:
    def __init__(self, inputDict):
        self.inputDict = inputDict

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
        inputDict_copy = copy.copy(self.inputDict)

        if 'lineno' in inputDict_copy:
            inputDict_copy.pop('lineno')

        if 'lexpos' in inputDict_copy:
            inputDict_copy.pop('lexpos')

        if 'lastpos' in inputDict_copy:
            inputDict_copy.pop('lastpos')

        return hash(str(inputDict_copy))

    def __len__(self):
        return len(self.inputDict)

    def __str__(self):
        return str(self.inputDict)
