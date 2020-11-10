# from typing import Union
import typing


# Exercise 1 - Room Class


class Room(object):
    """Room class
        Takes 2 inputs: name as a string and size as an integer (in meters)"""

    def __init__(self, name: str, size: typing.Union[int, float]) -> None:
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return f'{self.name}, {self.size}m'


# Exercise 2 and 3 - House Class and NotEnoughSpace exception


class NotEnoughSpaceError(Exception):

    def __init__(self, size: typing.Union[int, float], max_size: typing.Union[int, float]) -> None:
        self.size = size
        self.max_size = max_size

    def __str__(self) -> str:
        return f'{self.size}m is greater than available space of {self.max_size}m'


class House(object):
    """House class
        House class always starts empty and can contain any number of Rooms
        Max_size attribute is defined upon initializing the House object"""

    def __init__(self, available_space: typing.Union[int, float] = 100):
        self.rooms: typing.List[Room] = []
        self.available_space = available_space

    def add_rooms(self, *new_rooms: Room) -> None:
        for room in new_rooms:
            if self.size() + room.size <= self.available_space:
                self.rooms.append(room)
            else:
                raise NotEnoughSpaceError(self.size() + room.size, self.available_space)

    def size(self) -> typing.Union[int, float]:
        return sum([room.size
                    for room in self.rooms])

    def calculate_tax(self) -> typing.Union[int, float]:
        house_size = self.size()
        return 100 * house_size

    def __add__(self, new_room: Room) -> "House":
        if self.size() + new_room.size > self.available_space:
            raise NotEnoughSpaceError(self.size() + new_room.size, self.available_space)
        else:
            output = House(self.available_space)
            output.rooms = self.rooms
            output.rooms.append(new_room)
            return output

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        for room in self.rooms:
            output += f'{room}\n'
        return output[:-1]


# Exercise 4 - Neighborhood class


class Neighborhood(object):
    total_size = 0

    def __init__(self, name: str = '') -> None:
        self.name = name
        self.houses: typing.List[House] = []

    def add_houses(self, *new_houses: House) -> None:
        self.houses += new_houses
        Neighborhood.total_size += sum([house.size()
                                        for house in new_houses])

    def size(self) -> typing.Union[int, float]:
        return sum([house.size()
                    for house in self.houses])

    def house_types(self) -> typing.Dict[str, int]:
        diff_houses: typing.Dict[str, int] = {}
        for one_house in self.houses:
            diff_houses[one_house.__class__.__name__] = diff_houses.get(one_house.__class__.__name__, 0) + 1
        return diff_houses

    def calculate_tax(self) -> typing.Union[int, float]:
        return sum([house.calculate_tax()
                    for house in self.houses])

    def find_with_room(self, **kwargs) -> set:
        output = set()
        for house in self.houses:
            for room in house.rooms:
                if room.name == kwargs['name'] and room.size == kwargs['size']:
                    output.add(house)

        return output

    def __add__(self, new_house: House) -> "Neighborhood":
        output = Neighborhood()
        output.houses = self.houses
        output.houses.append(new_house)
        Neighborhood.total_size += new_house.size()
        return output


# Exercise 5 and 7 - SingleFamilyHouse, TownHouse, Apartment classes


class SingleFamilyHouse(House):
    def __init__(self, available_space: typing.Union[int, float] = 200) -> None:
        super().__init__(available_space)

    def calculate_tax(self) -> typing.Union[int, float]:
        house_size = self.size()
        if house_size <= 150:
            return 1.2 * (100 * house_size)
        else:
            return 1.2 * (100 * 150) + 1.5 * (100 * (house_size - 150))


class TownHouse(House):
    def __init__(self, available_space: typing.Union[int, float] = 100) -> None:
        super().__init__(available_space)

    def calculate_tax(self) -> typing.Union[int, float]:
        house_size = self.size()
        return 100 * house_size


class Apartment(House):
    def __init__(self, available_space: typing.Union[int, float] = 80) -> None:
        super().__init__(available_space)

    def calculate_tax(self) -> typing.Union[int, float]:
        house_size = self.size()
        return 0.75 * (100 * house_size)