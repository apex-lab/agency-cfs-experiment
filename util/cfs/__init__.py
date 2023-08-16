from psychopy import visual
from .cfs import CFSMask

def init_window(**kwargs):
    '''
    Initializes a psychopy window with some settings that are
    suitable for presentation of anaglyph stereo images.

    Arguments
    ---------
    **kwargs :
        You can input any arguments to psychopy.visual.Window that aren't
        already specified within this function.
    '''
    win = visual.Window(
        allowStencil = False,
        color = [0, 0, 0],
        colorSpace = 'rgb',
        blendMode = 'add', # MUST BE 'add' to superimpose red+blue/green images
        useFBO = True,
        **kwargs
        )
    # psychopy's default shader will replace pixel values that are
    # "out of bounds" following additive blending (say a white fixation cross
    # is superimposed over an image) with random noise to let
    # the user know this has occured. We don't want that, so we recompile
    # the shader to clip
    fragFBOtoFrame = '''
        uniform sampler2D texture;

        void main() {
            vec4 textureFrag = texture2D(texture,gl_TexCoord[0].st);
            gl_FragColor.rgb = textureFrag.rgb;
        }
        '''
    win._progFBOtoFrame = visual.shaders.compileProgram(
        visual.shaders.vertSimple,
        fragFBOtoFrame
        )
    return win
