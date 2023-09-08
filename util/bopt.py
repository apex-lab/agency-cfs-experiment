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

    def draw_from_post(self, lower_cutoff = None):
        '''
        Returns a draw from the posterior distribution. Using this method
        to pick your next sample is called "Thompson sampling," which has
        nicer convergence properties in some cases than e.g. just picking
        the mean.

        In the particular case of fitting a Weibull function, sampling values
        below the threshold may not provide as much new information about the
        threshold parameter, especially if you've picked a threshold criterion
        close to 50% accuracy (since everything below that will be practically
        chance accuracy). So you can use the `lower_cutoff` argument to truncate
        the posterior before drawing a sample. 
        '''
        if lower_cutoff:
            _x = self.tGuess + self.x
            above_bound = _x >= lower_cutoff
            pdf = self.pdf * above_bound # truncate the posterior
        p = pdf / pdf.sum()
        return self.tGuess + np.random.choice(self.x, p = p)
