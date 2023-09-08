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
        provably nicer convergence properties than e.g. just picking the mean.
        '''
        p = self.pdf / self.pdf.sum()
        return self.tGuess + np.random.choice(self.x, p = p)

    def mean_exp(self, base = 10):
        '''
        Returns the posterior expectation of the exponentiated distribution.

        This is handy when converting back from log10 scale, since
        10**mean(x) != mean(10**x) in general.
        '''
        _x = self.tGuess + self.x
        exp_x = base**_x
        return np.sum(self.pdf * exp_x) / np.sum(self.pdf)
