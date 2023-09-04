from psychopy.contrib.quest import QuestObject as _QuestObject

class QuestObject(_QuestObject):

    def pdf_at(self, t):
        '''
        override QuestObject.pdf_at for an ad hoc bug fix
        '''
        i = int(round((t - self.tGuess) / self.grain)) + 1 + self.dim/2
        i = min(len(self.pdf), max(1,i)) - 1
        p = self.pdf[int(i)]
        return p
