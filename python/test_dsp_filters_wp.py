import inpt_wp_inputs as ins
import algo_dsp_filters

"""
Compares the output of each filter based on 5 test inputs against
an expected result.

To run all test, type pytest at top level like:
    (venv) ➜  anolib git:(main) ✗ pytest

To run only the tests in this file, do this:
    (venv) ➜  anolib git:(main) ✗ pytest -q python/test_dsp_filters_wp.py
"""


class TestFirstOrderFeedForwardFilter:

    def test_ff_dc(self):
        res = algo_dsp_filters.one_zero_filter(ins.dc, 0.5, 0.5)
        assert res == [0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    def test_ff_nyquist(self):
        res = algo_dsp_filters.one_zero_filter(ins.nyquist, 0.5, 0.5)
        assert res == [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def test_ff_half_nyquist(self):
        res = algo_dsp_filters.one_zero_filter(ins.halfNyquist, 0.5, 0.5)
        assert res == [0.0, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5]

    def test_ff_quarter_nyquist(self):
        res = algo_dsp_filters.one_zero_filter(ins.quarterNyquist, 0.5, 0.5)
        assert res == [0.0, 0.3535, 0.8534999999999999, 0.8534999999999999, 0.3535, -0.3535,
                       -0.8534999999999999, -0.8534999999999999]

    def test_ff_impulse(self):
        res = algo_dsp_filters.one_zero_filter(ins.impulse, 0.5, 0.5)
        assert res == [0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0]


class TestFirstOrderFeedBackFilter:

    def test_fb_dc(self):
        res = algo_dsp_filters.one_pole_filter(ins.dc, 0.5, 0.5)
        assert res == [0.0, 0.5, 0.25, 0.375, 0.3125, 0.34375, 0.328125, 0.3359375]

    def test_fb_nyquist(self):
        res = algo_dsp_filters.one_pole_filter(ins.nyquist, 0.5, 0.5)
        assert res == [-0.5, 0.75, -0.875, 0.9375, -0.96875, 0.984375, -0.9921875, 0.99609375]

    def test_fb_half_nyquist(self):
        res = algo_dsp_filters.one_pole_filter(ins.halfNyquist, 0.5, 0.5)
        assert res == [0.0, 0.5, -0.25, -0.375, 0.1875, 0.40625, -0.203125, -0.3984375]

    def test_fb_quarter_nyquist(self):
        res = algo_dsp_filters.one_pole_filter(ins.quarterNyquist, 0.5, 0.5)
        assert res == [0.0, 0.3535, 0.32325000000000004, 0.19187499999999996, -0.09593749999999998,
                       -0.30553125, -0.347234375, -0.1798828125]

    def test_fb_impulse(self):
        res = algo_dsp_filters.one_pole_filter(ins.impulse, 0.5, 0.5)
        assert res == [0.0, 0.5, -0.25, 0.125, -0.0625, 0.03125, -0.015625, 0.0078125]
