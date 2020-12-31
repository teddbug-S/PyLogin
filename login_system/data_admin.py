from dataclasses import dataclass
from sys import path

from admintype import AdminType


@dataclass
class Admin:
    """ A class representing an admin """
    
    firstname: str
    lastname: str
    username: str
    age: str
    password: str
    type: AdminType


    def data_to_dict(self) -> dict:
        """ Returns a dictionary nicely formatted with the admin's data

        :return: admin data
        :rtype: dict
        """
        data = {
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "age": self.age,
            "password": self.password,
            "type": self.type
        }
        return data

    
    @classmethod
    def from_dict(cls, **kwargs):
        """ Creates an admin object from a dictionary

        :return: Admin object
        :rtype: Admin
        """
        return cls(**kwargs)
