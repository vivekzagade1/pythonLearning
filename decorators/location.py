import inspect

from decorators.position import *
from dataclasses import dataclass


def auto_repr(cls):
    members = vars(cls)

    if "__repr__" in members:
        raise TypeError(f"{cls.__name__} already defines __repr__")

    if "__init__" not in members:
        raise TypeError(f"{cls.__name__} does not override __init__")

    sig = inspect.signature(cls.__init__)
    parameter_names = list(sig.parameters)[1:]

    if not all(
        isinstance(members.get(name, None), property)
        for name in parameter_names
    ):
        raise TypeError(
            f"Cannot apply auto_repr to {cls.__name__} because not all "
            "__init__ parameters have matching properties"
        )

    def synthesized_repr(self):
        return "{typename}({args})".format(
            typename=typename(self),
            args=", ".join(
                "{name}={value!r}".format(
                    name=name,
                    value=getattr(self, name)
                ) for name in parameter_names
            )
        )

    setattr(cls, "__repr__", synthesized_repr)

    return cls


# @auto_repr
@dataclass(eq=True, frozen=True)
class Location:
    name: str
    position: Position

    def __post_init__(self):
        if self.name == "":
            raise ValueError("Location name can't be empty")


"""
    def __init__(self, name, position):
        self._name = name
        self._position = position

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

#    def __repr__(self):
#        return f"{typename(self)}(name={self.name}, position={self.position})"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.position == other.position

    def __hash__(self):
        return hash((self.name, self.position))
"""

hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(22.29, 114.16))
cape_town = Location("Cape Town", EarthPosition(22.29, 114.16))
rotterdam = Location("Rotterdam", EarthPosition(22.29, 114.16))
maracaibo = Location("Maracaibo", EarthPosition(22.29, 114.16))
