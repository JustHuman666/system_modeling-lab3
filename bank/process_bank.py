import numpy as np

from base.element_base import ElementBase


class ProcessBank(ElementBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.t_next = [np.inf]*self.channels
        self.state = [0] * self.channels

        self.t_departure = 0
        self.previous_t_departure = 0
        self.t_in_system = 0
        self.previous_t_in_system = 0

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
        super().out_act()
        channels = self.get_current_channel()
        for channel in channels:
            self.t_next[channel] = float('inf')
            self.state[channel] = 0

            self.t_departure += self.t_curr - self.previous_t_departure
            self.previous_t_departure = self.t_curr
            self.t_in_system = + self.t_curr - self.previous_t_in_system

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
