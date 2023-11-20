
import util_signals as us
from algo_dsp_filters import DcBlocker
from hope_dsp_filters import dc_blocker_exp

#####################################################
# Signals / Inputs
#####################################################
imp = us.impls()


#####################################################
# Tests
#####################################################
def test_dc_blocker():
    """ Test DC Blocker algorithm """
    exp = dc_blocker_exp
    dcb_test = DcBlocker()
    dcb_test.reset()
    res = dcb_test.process(imp)
    assert res == exp
