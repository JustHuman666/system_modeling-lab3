import numpy as np

from hospital.element_hospital import ElementHospital


class CreateHospital(ElementHospital):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def out_act(self):
        super().out_act()

        self.t_next[0] = self.t_curr + self.get_delay()
        self.next_type_element = np.random.choice([1, 2, 3], p=[0.5, 0.1, 0.4])
        next_element = self.choose_next_element()
        next_element.in_act(self.next_type_element, self.t_curr)
