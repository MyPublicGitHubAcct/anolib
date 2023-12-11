import numpy as np

#####################################################
#
# Wave-table oscillators
#
#####################################################


# class DcBlocker:
#     """
#     DC blocking filter from https://ccrma.stanford.edu/~jos/filters/DC_Blocker.html
#     Defaults to pole = 0.995 - see website for rationale.
#     """
    # def __init__(self):
    #     self.pole = 0.995
    #     self.x1 = 0
    #     self.y1 = 0
    #     self.output_signal = []
    #
    # def __str__(self):
    #     return f"pole = {self.pole}, x1 = {self.x1}, y1 = {self.y1}, out = {self.output_signal}"
    #
    # def reset(self):
    #     self.pole = 0.995
    #     self.x1 = 0
    #     self.y1 = 0
    #     self.output_signal = []
    #
    # def set_pole(self, pole):
    #     self.pole = pole
    #
    # def process(self, input_signal):
    #     for x in input_signal:
    #         y = x - self.x1 + self.pole * self.y1
    #         self.output_signal.append(y)
    #         self.x1 = x
    #         self.y1 = y
    #
    #     return self.output_signal

