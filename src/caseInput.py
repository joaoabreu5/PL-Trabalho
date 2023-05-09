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
        inputCase_copy = copy.deepcopy(self.inputCase)

        for d in inputCase_copy:
            if 'lineno' in d:
                d.pop('lineno')

            if 'lexpos' in d:
                d.pop('lexpos')

            if 'lastpos' in d:
                d.pop('lastpos')

        return hash(str(inputCase_copy))

    def __len__(self):
        return len(self.inputCase)

    def __str__(self):
        return str(self.inputCase)
