from hospital.element_hospital import ElementHospital


class DisposeHospital(ElementHospital):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.t_next = [float('inf')]

        self.time_finished_1 = 0
        self.time_finished_2 = 0
        self.time_finished_3 = 0

        self.type_1_amount = 0
        self.type_2_amount = 0
        self.type_3_amount = 0

    def in_act(self, next_element_type, t_start):
        if next_element_type == 1:
            self.time_finished_1 += self.t_curr - t_start
            self.type_1_amount += 1
        elif next_element_type == 2:
            self.time_finished_2 += self.t_curr - t_start
            self.type_2_amount += 1
        elif next_element_type == 3:
            self.time_finished_3 += self.t_curr - t_start
            self.type_3_amount += 1
        super().out_act()
