#!/usr/bin/python3
"""Class Review that inherits from BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class Review"""
    place_id = ""
    user_id = ""
    text = ""
