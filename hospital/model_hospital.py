import numpy as np

from base.model_base import ModelBase
from hospital.dispose_hospital import DisposeHospital
from hospital.process_hospital import ProcessHospital


class ModelHospital(ModelBase):
    def __init__(self, elements: list):
        super().__init__(elements)
        self.event = elements[0]

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')
            for e in self.list:
                if np.min(e.t_next) < self.t_next and not isinstance(e, DisposeHospital):
                    self.t_next = np.min(e.t_next)
                    self.event = e.id

            delta = self.t_next - self.t_curr
            for e in self.list:
                e.do_statistics(delta)

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

    def print_result(self):
        super().print_result()
        mean_time_arriving_to_lab = 0
        time_of_finishing_counter = 0
        processors_amount = 0
        finished_clients_amount = 0

        for e in self.list:
            if isinstance(e, ProcessHospital):
                processors_amount += 1
                if e.name == "to the lab":
                    mean_time_arriving_to_lab = e.time_going_to_lab / e.quantity
                if e.name == "to the reception":
                    time_finished_type_2 = float('inf')
                    if e.amount_of_type_2 != 0:
                        time_finished_type_2_extra = e.time_of_finishing_type_2 / e.amount_of_type_2
                    print(f"mean time of finishing for clients of type 2: {time_finished_type_2_extra}\n")

            elif isinstance(e, DisposeHospital):
                time_of_finishing_counter += e.time_finished_1 + e.time_finished_2 + e.time_finished_3
                finished_clients_amount += e.quantity
                time_finished_type_1 = float('inf')
                time_finished_type_2 = float('inf')
                time_finished_type_3 = float('inf')

                if e.type_1_amount != 0:
                    time_finished_type_1 = e.time_finished_1 / e.type_1_amount
                if e.type_2_amount != 0:
                    time_finished_type_2 = e.time_finished_2 / e.type_2_amount
                if e.type_3_amount != 0:
                    time_finished_type_3 = e.time_finished_3 / e.type_3_amount
                print(f"mean time of finishing for clients of type 1: {time_finished_type_1} \n"
                      f"mean time of finishing for clients of type 2: {time_finished_type_2} \n"
                      f"mean time of finishing for clients of type 3: {time_finished_type_3} \n")

        time_of_finishing_average = time_of_finishing_counter / finished_clients_amount

        print(f"mean time gap for arriving to the lab: {mean_time_arriving_to_lab} \n"
              f"mean time of finishing for clients average: {time_of_finishing_average} \n")
