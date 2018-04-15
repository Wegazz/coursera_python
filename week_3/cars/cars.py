import csv
from enum import IntEnum, auto

import os


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        super().__init__(car_type, brand, photo_file_name, carrying)
        split_whl = body_whl.split('x') if body_whl != '' else [0, 0, 0]
        self.body_width = float(split_whl[0])
        self.body_height = float(split_whl[1])
        self.body_length = float(split_whl[2])

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


class CarSpec(IntEnum):
    car_type = 0
    brand = auto()
    passenger_seats_count = auto()
    photo_file_name = auto()
    body_whl = auto()
    carrying = auto()
    extra = auto()


def gen_object(row):
    car_type = row[CarSpec.car_type]

    if car_type == 'car':
        return Car(car_type,
                   row[CarSpec.brand],
                   row[CarSpec.photo_file_name],
                   row[CarSpec.carrying],
                   row[CarSpec.passenger_seats_count])

    if car_type == 'truck':
        return Truck(car_type,
                     row[CarSpec.brand],
                     row[CarSpec.photo_file_name],
                     row[CarSpec.carrying],
                     row[CarSpec.body_whl])

    if car_type == 'spec_machine':
        return SpecMachine(car_type,
                           row[CarSpec.brand],
                           row[CarSpec.photo_file_name],
                           row[CarSpec.carrying],
                           row[CarSpec.extra])

    raise ValueError(f"No such car_type: {car_type}")


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename, encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # Пропускаем заголовок
        for i, row in enumerate(reader):
            try:
                obj = gen_object(row)
            except (LookupError, ValueError) as e:
                print('Row #{} is bad, skipping. Error: {}'.format(i, e))
            else:
                car_list.append(obj)
    return car_list


if __name__ == '__main__':
    for x in get_car_list('coursera_week3_cars.csv'):
        print(x.__dict__, x.get_photo_file_ext(), x.get_body_volume() if isinstance(x, Truck) else '-', sep='; ')
