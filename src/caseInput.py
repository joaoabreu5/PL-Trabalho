from singleInput import SingleInput
import copy


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
            i += 1

        return True

    def __lt__(self, other):
        for i in range(0, len(self)):
            i1 = SingleInput(self.inputCase[i])
            i2 = SingleInput(other.inputCase[i])
            if i1 < i2:
                return True

        return False

    def __hash__(self):
        inputCase_copy = []

        for d in self.inputCase:
            d_copy = copy.deepcopy(d)
            
            if 'lineno' in d_copy:
                d_copy.pop('lineno')

            if 'lexpos' in d_copy:
                d_copy.pop('lexpos')

            if 'lastpos' in d_copy:
                d_copy.pop('lastpos')

            if 'type' in d_copy and d_copy['type'] == 'any' and 'python' in d_copy:
                d_copy.pop('python')
                
            if 'type' in d_copy and d_copy['type'] == 'list_ht' and 'vars' in d_copy:
                d_copy['vars'] = len(d_copy['vars'])

            inputCase_copy.append(tuple(sorted(d_copy.items())))
            
        return hash(tuple(inputCase_copy))

    def __len__(self):
        return len(self.inputCase)

    def __str__(self):
        return str(self.inputCase)
