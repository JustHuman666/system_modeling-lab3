import numpy as np

from base.element_base import ElementBase
from base.process_base import ProcessBase

from bank.process_bank import ProcessBank
from hospital.process_hospital import ProcessHospital


class ModelBase:
    def __init__(self, elements: list[ElementBase]):
        self.list = elements
        self.t_next = 0.0
        self.event = 0
        self.t_curr = self.t_next

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')
            for e in self.list:
                if np.min(e.t_next) < self.t_next:
                    self.t_next = np.min(e.t_next)
                    self.event = e.id
            for e in self.list:
                e.do_statistics(self.t_next - self.t_curr)
            self.t_curr = self.t_next
            for e in self.list:
                e.t_curr = self.t_curr
            if len(self.list) > self.event:
                self.list[self.event].out_act()
            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()

        return self.print_result()

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self) -> dict:
        print("\n-------------RESULTS-------------")
        mean_length_of_queue_counter = 0
        failure_probability_counter = 0
        mean_load_counter = 0
        max_found_queue_length = 0
        processors_amount = 0

        for e in self.list:
            e.print_info()
            if isinstance(e, ProcessBase) or isinstance(e, ProcessBank) or isinstance(e, ProcessHospital):
                processors_amount += 1
                mean_length_of_queue = e.mean_queue_length / self.t_curr
                failure_probality = 0
                if e.quantity != 0:
                    failure_probality = e.failure / e.quantity
                mean_load = e.mean_load / self.t_curr
                print(f"mean length of queue = {mean_length_of_queue} \nfailure probability  = {failure_probality}"
                      f"\nmean_load = {mean_load}")
                mean_length_of_queue_counter += mean_length_of_queue
                failure_probability_counter += failure_probality
                mean_load_counter += mean_load

                if e.max_found_queue > max_found_queue_length:
                    max_found_queue_length = e.max_found_queue

        mean_load_average = mean_load_counter / processors_amount
        failure_probability_average = failure_probability_counter / processors_amount
        mean_length_of_queue_average = mean_length_of_queue_counter / processors_amount

        print(f'mean load average: {mean_load_average} \n'
              f'failure probability average: {failure_probability_average} \n'
              f'mean length of queue average: {mean_length_of_queue_average} \n'
              f'max found queue length: {max_found_queue_length} \n')
