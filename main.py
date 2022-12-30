import random_generator as generator

from base.create_base import CreateBase
from base.process_base import ProcessBase
from base.model_base import ModelBase

from bank.create_bank import CreateBank
from bank.process_bank import ProcessBank
from bank.model_bank import ModelBank

from hospital.create_hospital import CreateHospital
from hospital.process_hospital import ProcessHospital
from hospital.model_hospital import ModelHospital
from hospital.dispose_hospital import DisposeHospital


def base_model(process: ProcessBase):
    print("Imitation of a base model. \n")
    creator = CreateBase(delay_mean=5, name='Creator', distribution='exponential')
    process_2 = ProcessBase(max_queue=3, name='Process 2', delay_mean=5, distribution='exponential')
    process_3 = ProcessBase(max_queue=3, name='Process 3', delay_mean=5, distribution='exponential')
    creator.next_element = [process]
    process.next_element = [process_2, process_3]
    elements = [creator, process, process_2, process_3]
    model = ModelBase(elements)
    model.simulate(1000)
    model.print_result()


def priority_model():
    print("Imitation of a base model with a priority. \n")
    process = ProcessBase(max_queue=3, name="Process 1", delay_mean=5, distribution='exponential')
    process.priority = [1, 2]
    base_model(process)


def probability_model():
    print("Imitation of a base model with a probability. \n")
    process = ProcessBase(max_queue=3, name="Process 1", delay_mean=5, distribution='exponential')
    process.probability = [0.5, 0.5]
    base_model(process)


def bank_model():
    print("Imitation of a bank model. \n")
    create = CreateBank(delay_mean=0.5, name='Creator', distribution='exponential')
    process_1 = ProcessBank(max_queue=3, delay_mean=0.3, name='Cashier 1', distribution='exponential')
    process_2 = ProcessBank(max_queue=3, delay_mean=0.3, name='Cashier 2', distribution='exponential')
    create.next_element = [process_1, process_2]
    process_1.state[0] = 1
    process_2.state[0] = 1
    process_1.t_next[0] = generator.normal(1, 0.3)
    process_2.t_next[0] = generator.normal(1, 0.3)
    create.t_next[0] = 0.1
    process_1.occupied_queue = 2
    process_2.occupied_queue = 2
    element_list = [create, process_1, process_2]
    bank_system = ModelBank(element_list, balancing=[process_1, process_2])
    bank_system.simulate(1000)
    bank_system.print_result()


def hospital_model():
    print("Imitation of a hospital model. \n")
    create = CreateHospital(delay_mean=15.0, name='creator', distribution='exponential')
    process_reception = ProcessHospital(max_queue=100, channels=2, name='reception', distribution='exponential')
    process_to_room = ProcessHospital(max_queue=100, delay_mean=3.0, delay_dev=8, channels=3,
                                      name='to the room', distribution='uniform')
    process_to_the_lab = ProcessHospital(max_queue=0, delay_mean=2.0, delay_dev=5, channels=10,
                                         name='to the lab', distribution='uniform')
    process_back_to_reception = ProcessHospital(max_queue=0, delay_mean=2.0, delay_dev=5, channels=10,
                                                name='to the reception', distribution='uniform')
    process_in_lab = ProcessHospital(max_queue=100, delay_mean=4.5, delay_dev=3, channels=2,
                                     name='register at lab', distribution='erlang')
    process_examination = ProcessHospital(max_queue=100, delay_mean=4.0, delay_dev=2, channels=2,
                                          name='examination', distribution='erlang')

    exit_1 = DisposeHospital(name='exit 1')
    exit_2 = DisposeHospital(name='exit 2')

    create.next_element = [process_reception]
    process_reception.next_element = [process_to_room, process_to_the_lab]
    process_to_room.next_element = [exit_1]
    process_to_the_lab.next_element = [process_in_lab]
    process_in_lab.next_element = [process_examination]
    process_examination.next_element = [exit_2, process_back_to_reception]
    process_back_to_reception.next_element = [process_reception]
    process_reception.priority = [1]

    process_reception.path = [[1], [2, 3]]
    process_examination.path = [[3], [2]]

    elements = [create,
                process_reception,
                process_to_room,
                process_to_the_lab,
                process_in_lab,
                process_examination,
                process_back_to_reception,
                exit_1, exit_2]

    hospital = ModelHospital(elements)
    hospital.simulate(1000)
    hospital.print_result()


if __name__ == "__main__":
    process = ProcessBase(max_queue=3, name='Process 1', delay_mean=5, distribution='exponential')
    base_model(process)
    # probability_model()
    # priority_model()
    # bank_model()
    # hospital_model()
