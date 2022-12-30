import numpy as np
from copy import deepcopy

import random_generator as generator


class ElementBase:
    next_id = 0

    def __init__(self,  delay_mean=None, name="", distribution="", channels=1, max_queue=float('inf'), delay_dev=0.0, probability=1):
        self.name = name
        self.t_next = [0]
        self.delay_mean = delay_mean
        self.delay_dev = delay_dev
        self.distribution = distribution
        self.quantity = 0
        self.t_curr = self.t_next
        self.state = [0]
        self.next_element = None
        self.id = ElementBase.next_id
        ElementBase.next_id += 1

        self.channels = channels
        self.max_queue = max_queue
        self.occupied_queue = 0
        self.probability = [probability]
        self.priority = [1]

        self.mean_queue_length = 0
        self.mean_load = 0
        self.failure = 0
        self.max_found_queue = 0

    def get_delay(self):
        if self.distribution == "exponential":
            return generator.exponential(self.delay_mean)
        elif self.distribution == "normal":
            return generator.normal(self.delay_mean, self.delay_dev)
        elif self.distribution == "uniform":
            return generator.uniform(self.delay_mean, self.delay_dev)
        elif self.distribution == "erlang":
            return generator.erlang(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def get_channels(self):
        channels = []
        for index in range(self.channels):
            if self.state[0] == 0:
                channels.append(index)
        return channels

    def get_current_channel(self):
        channels = []
        for index in range(self.channels):
            if self.t_next[0] == self.t_curr:
                channels.append(index)
        return channels

    def in_act(self):
        pass

    def out_act(self):
        self.quantity += 1

    def next_by_priority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        min_queue_index = 0

        for index in range(len(priorities)):
            if min(priorities) == 100000:
                break
            max_priority_index = priorities.index(min(priorities))
            if 0 in self.next_element[max_priority_index].state:
                return self.next_element[max_priority_index]
            else:
                if self.next_element[max_priority_index].occupied_queue < min_queue:
                    min_queue = self.next_element[max_priority_index].occupied_queue
                    min_queue_index = self.next_element.index(self.next_element[max_priority_index])
            priorities[max_priority_index] = 100000

        return self.next_element[min_queue_index]

    def choose_next_element(self):
        if self.probability != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probability)
            return next_element
        elif self.priority != [1]:
            next_element = self.next_by_priority()
            return next_element
        elif self.probability == [1] and self.priority == [1]:
            return self.next_element[0]
        elif self.probability != [1] and self.priority != [1]:
            print("There cannot be chosen both of the options.")
            SystemExit()

    def do_statistics(self, delta):
        self.mean_queue_length += self.occupied_queue * delta
        for index in range(self.channels):
            self.mean_load += self.state[0] * delta
        self.mean_load = self.mean_load / self.channels
        if self.occupied_queue > self.max_found_queue:
            self.max_found_queue = self.occupied_queue

    def print_info(self):
        print(f"\n{self.name} state: {self.state}, quantity: {self.quantity}, t_next: {self.t_next}")
