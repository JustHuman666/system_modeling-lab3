from base.element_base import ElementBase


class ElementHospital(ElementBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_element_type = None

    def get_delay(self):
        if self.name == 'reception':
            if self.next_element_type == 1:
                self.delay_mean = 15
            elif self.next_element_type == 2:
                self.delay_mean = 40
            elif self.next_element_type == 3:
                self.delay_mean = 30
        return super().get_delay()
