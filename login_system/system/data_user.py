from dataclasses import dataclass


@dataclass
class User:
    """ A class representing each user """
    
    firstname: str
    lastname: str
    username: str
    age: int
    password: str
    email: str
    bio: str
    verified: str
    blockstatus: str


    def data_to_dict(self) -> dict:
        """ Returns a dictionary nicely formatted with the user's data

        :return: user data
        :rtype: dict
        """
        data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "age": self.age,
            #"password": self.password,
            "email": self.email,
            'bio': self.bio,
            'verified': self.verified,
            "blockstatus": self.blockstatus
        }
        return data

    
    @classmethod
    def from_dict(cls, **kwargs):
        """ Creates a user object from a dictionary

        :return: User object
        :rtype: User
        """
        return cls(**kwargs)
