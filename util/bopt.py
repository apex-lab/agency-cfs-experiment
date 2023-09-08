from psychopy.contrib.quest import QuestObject as _QuestObject
import numpy as np

class QuestObject(_QuestObject):

    def pdf_at(self, t):
        '''
        override QuestObject.pdf_at for an ad hoc bug fix
        '''
        i = int(round((t - self.tGuess) / self.grain)) + 1 + self.dim/2
        i = min(len(self.pdf), max(1,i)) - 1
        p = self.pdf[int(i)]
        return p

    def draw_from_post(self):
        '''
        Returns a draw from the posterior distribution. Using this method
        to pick your next sample is called "Thompson sampling," which has
        nicer convergence properties in some case than e.g. just picking
        the mean.
        '''
        p = self.pdf / self.pdf.sum()
        return self.tGuess + np.random.choice(self.x, p = p)
