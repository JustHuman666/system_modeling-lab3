import numpy as np

from hospital.element_hospital import ElementHospital


class ProcessHospital(ElementHospital):
    def __init__(self, path=None, **kwargs):
        super().__init__(**kwargs)

        self.start_time = [-1] * self.channels
        self.start_queue = []
        self.types = [-1] * self.channels
        self.queue_types = []
        self.priority_types = []
        self.path = path
        self.time_going_to_lab = 0
        self.previous_time_going_to_lab = 0

        self.time_of_finishing_type_2 = 0
        self.amount_of_type_2 = 0

    def in_act(self, next_element_type, t_start):
        self.next_element_type = next_element_type

        if self.name == 'to the lab':
            self.time_going_to_lab += self.t_curr - self.previous_time_going_to_lab
            self.previous_time_going_to_lab = self.t_curr

        if self.name == 'to the reception' and next_element_type == 2:
            self.time_of_finishing_type_2 += self.t_curr - t_start
            self.amount_of_type_2 += 1

        channels = self.get_channels()
        if len(channels) > 0:
            for channel in channels:
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()
                self.types[channel] = self.next_element_type
                self.start_time[channel] = t_start
                break
        else:
            if self.occupied_queue < self.max_queue:
                self.occupied_queue = self.occupied_queue + 1
                self.queue_types.append(self.next_element_type)
                self.start_queue.append(t_start)
                if self.occupied_queue > self.max_found_queue:
                    self.max_found_queue = self.occupied_queue
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()
        channels = self.get_current_channel()
        for channel in channels:
            self.t_next[0] = float('inf')
            self.state[0] = 0

            previous_next_element_type = self.types[channel]
            previous_t_start = self.start_time[channel]
            self.types[channel] = -1
            self.start_time[channel] = -1

            if self.occupied_queue > 0:
                self.occupied_queue -= 1
                priority_index = self.get_prior_index()
                self.next_element_type = self.queue_types.pop(priority_index)
                self.state[0] = 1
                self.t_next[0] = self.t_curr + super().get_delay()
                self.types[channel] = self.next_element_type
                self.start_time[channel] = self.start_queue.pop(priority_index)

            if self.next_element is not None:
                if self.name == "to the reception":
                    self.next_element_type = 1
                else:
                    self.next_element_type = previous_next_element_type

                if self.path is None:
                    next_element = np.random.choice(self.next_element, p=self.probability)
                    next_element.in_act(self.next_element_type, previous_t_start)
                else:
                    for index, path in enumerate(self.path):
                        if self.next_element_type in path:
                            next_element = self.next_element[index]
                            next_element.in_act(self.next_element_type, previous_t_start)
                            break

    def get_prior_index(self):
        for prior_types_index in self.priority_types:
            for type_index in np.unique(self.queue_types):
                if type_index == prior_types_index:
                    return self.queue_types.index(type_index)
        else:
            return 0

    def print_info(self):
        super().print_info()
        print(f"queue: {self.occupied_queue}, failure: {self.failure}")
