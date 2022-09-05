#!/usr/bin/python3

""" import modules for set id and datetime """
import uuid
from datetime import datetime
import models


class BaseModel():
    """ BaseModel Class """

    def __init__(self, *args, **kwargs):

        if bool(kwargs):
            for name_attr, value in kwargs.items():
                if name_attr in ["created_at", "updated_at"]:
                    setattr(self,
                            name_attr,
                            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif name_attr != "__class__":
                    setattr(self, name_attr, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def save(self):
        """ save method """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ to_dict method """
        dic = dict(self.__dict__)
        dic['__class__'] = self.__class__.__name__
        dic['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        dic['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return dic

    def __str__(self):
        """ __str__ method """
        msg = "[{}] ({}) {}"
        return msg.format(self.__class__.__name__, self.id, self.__dict__)
