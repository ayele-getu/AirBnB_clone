#!/usr/bin/python3
'''Tests for FileStorage class'''
import models
from models.engine.file_storage import FileStorage
import os
import unittest


class TestFile_Storage(unittest.TestCase):
    '''start tests'''

    def test_docstring(self):
        '''test if funcions, methods, classes
        and modules have docstring'''
        msj = "Module doesnt have docstring"
        obj = models.engine.file_storage.__doc__
        self.assertIsNotNone(obj, msj)  # Modules
        msj = "Classes doesnt have docstring"
        self.assertIsNotNone(obj, msj)  # Classes

    def test_executable_file(self):
        '''test if file has permissions u+x to execute'''
        # Check for read access
        is_read_true = os.access('models/engine/file_storage.py', os.R_OK)
        self.assertTrue(is_read_true)
        # Check for write access
        is_write_true = os.access('models/engine/file_storage.py', os.W_OK)
        self.assertTrue(is_write_true)
        # Check for execution access
        is_exec_true = os.access('models/engine/file_storage.py', os.X_OK)
        self.assertTrue(is_exec_true)

    def test_is_an_instance(self):
        '''check if my_model is an instance of BaseModel'''
        my_model = FileStorage()
        self.assertIsInstance(my_model, FileStorage)
