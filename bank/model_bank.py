import numpy as np

from bank.process_bank import ProcessBank
from base.model_base import ModelBase


class ModelBank(ModelBase):
    def __init__(self, elements: list, balancing=None):
        super().__init__(elements)
        self.changes_of_queue = 0
        self.balancing = balancing
        self.processed_clients = 0
        self.clients_left = 0
        self.clients_amount_in_bank = 0

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')
            for e in self.list:
                if np.min(e.t_next) < self.t_next:
                    self.t_next = np.min(e.t_next)
                    self.event = e.id

            delta = self.t_next - self.t_curr
            for e in self.list:
                e.do_statistics(delta)
            self.clients_amount_in_bank += (self.balancing[0].occupied_queue +
                                            self.balancing[1].occupied_queue +
                                            self.balancing[0].state[0] +
                                            self.balancing[1].state[0]) * delta

            self.t_curr = self.t_next
            for e in self.list:
                e.t_curr = self.t_curr
            if len(self.list) > self.event:
                self.list[self.event].out_act()
            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()
            self.choose_a_queue()
        return self.print_result()

    def choose_a_queue(self):
        elements_in_queues = []
        for element in self.list:
            if isinstance(element, ProcessBank):
                elements_in_queues.append(element.occupied_queue)

        queue_1 = elements_in_queues[0] - elements_in_queues[1]
        queue_2 = elements_in_queues[1] - elements_in_queues[0]

        if queue_1 >= 2:
            self.list[1].occupied_queue -= 1
            self.list[2].occupied_queue += 1
            print(f"Element left the {self.list[1].name} to {self.list[2].name}")
            self.changes_of_queue += 1
        elif queue_2 >= 2:
            self.list[2].occupied_queue -= 1
            self.list[1].occupied_queue += 1
            print(f"Element left the {self.list[2].name} to {self.list[1].name}")
            self.changes_of_queue += 1

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self) -> dict:
        super().print_result()
        departure_mean_time_counter = 0
        time_in_system_counter = 0
        processors_amount = 0

        for e in self.list:
            if isinstance(e, ProcessBank):
                processors_amount += 1
                mean_departure_time = e.t_departure / e.quantity
                print(f"mean depature time to {e.name} = {mean_departure_time}\n")
                departure_mean_time_counter += mean_departure_time
                time_in_system_counter += e.t_departure / e.quantity

        departure_mean_time_average = departure_mean_time_counter / processors_amount
        time_in_system_average = time_in_system_counter / processors_amount
        clients_amount_in_bank_average = self.clients_amount_in_bank / self.t_curr

        print(f'mean time of departure average: {departure_mean_time_average} \n'
              f'mean time in system average: {time_in_system_average} \n'
              f'amount of clients in a system average: {clients_amount_in_bank_average} \n'
              f'amount of times of changing some queues: {self.changes_of_queue} \n')
