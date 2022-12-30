import numpy as np

from base.element_base import ElementBase


class ProcessBase(ElementBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = [0] * self.channels
        self.t_next = [np.inf] * self.channels

    def in_act(self):
        channels = self.get_channels()
        if len(channels) > 0:
            for channel in channels:
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()
                break
        else:
            if self.occupied_queue < self.max_queue:
                self.occupied_queue = self.occupied_queue + 1
            else:
                self.failure += 1

    def out_act(self):
        channels = self.get_current_channel()
        for channel in channels:
            super().out_act()
            self.t_next[channel] = float('inf')
            self.state[channel] = 0

            if self.occupied_queue > 0:
                self.occupied_queue -= 1
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()

            if self.next_element is not None:
                next_element = self.choose_next_element()
                next_element.in_act()

    def print_info(self):
        super().print_info()
        print(f"failure: {self.failure}")
