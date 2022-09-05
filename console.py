#!/usr/bin/python3
""" import cmd module, BaseModel and storage """
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models import storage
import sys
import json

list_classes = ["BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Review",
                "Place"]


class HBNBCommand(cmd.Cmd):
    def do_update(self, arg):
        """Updates an instance based on the class
        name and id by adding or updating attribute"""
        objs = storage.all()
        args = arg.split(" ")
        if len(arg) == 0:
            print("** class name missing **")
        elif args[0] in list_classes:
            if len(args) < 2:
                print("** instance id missing **")
            elif args[1] in [name_id.split(".")[1] for name_id in objs.keys()]:
                name_id = args[0] + "." + args[1]
                obj = objs[name_id]
                if len(args) < 3:
                    print("** attribute name missing **")
                else:
                    if len(args) < 4:
                        print("** value missing **")
                    else:
                        try:
                            setattr(obj, args[2], eval(args[3].strip('"')))
                        except:
                            setattr(obj, args[2], args[3].strip('"'))
                        storage.save()
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation
        of all instances based or not on the class name."""
        objs = storage.all()
        args = arg.split(" ")
        list_out = []
        if len(arg) == 0:
            for obj in objs.values():
                list_out.append(str(obj))
            print(list_out)
        elif args[0] in list_classes:
            for name_id in objs.keys():
                if name_id.split(".")[0] == args[0]:
                    list_out.append(str(objs[name_id]))
            print(list_out)
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split(" ")
        if len(arg) == 0:
            print("** class name missing **")
        elif args[0] in list_classes:
            if len(args) == 2:
                name_id = args[0] + "." + str(args[1])
                objs = storage.all()
                if name_id in objs.keys():
                    del(objs[name_id])
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_create(self, arg):
        """Creates a new instance of BaseModel
        and prints the id. Example:(hbnb) create BaseModel\n """
        args = arg.split(" ")
        if len(arg) == 0:
            print("** class name missing **")
        elif args[0] in list_classes:
            obj = eval(args[0] + "()")
            id = getattr(obj, 'id')
            storage.save()
            print(id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg=""):
        """Prints the string representation
        of an instance based on the class name and id"""
        args = arg.split(" ")
        if len(arg) == 0:
            print("** class name missing **")
        elif args[0] in list_classes:
            if len(args) >= 2:
                name_id = args[0] + "." + str(args[1])
                objs = storage.all()
                if name_id in objs.keys():
                    obj = objs[name_id]
                    print(obj)
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_quit(self, arg):
        """Quit command to exit the program \n"""
        sys.exit(1)

    def do_EOF(self, arg):
        """ EOF SystemExiit """
        print("")
        return True

    def emptyline(self):
        pass

    def default(self, line):
        words = line.split(".")
        class_name = words[0]
        if class_name in list_classes and len(words) > 1:
            command = words[1]
            if command in ['all()', 'count()']:
                if command == "all()":
                    self.do_all(class_name)
                elif command == "count()":
                    self.count(class_name)
            else:
                if "show" in command:
                    my_id = command.split("(")[1].strip(")")
                    concat = class_name + " " + my_id
                    self.do_show(concat)
                elif "destroy" in command:
                    my_id = command.split("(")[1].strip(')"')
                    concat = class_name + " " + my_id
                    self.do_destroy(concat)
                elif "update" in command:
                    cn = class_name
                    if "{" not in command.split("(")[1]:
                        myd = command.split("(")[1].split(", ")[0].strip(')"')
                        n_at = command.split("(")[1].split(", ")[1].strip(')"')
                        v_at = command.split("(")[1].split(", ")[2].strip(')"')
                        concat = cn + " " + myd + " " + n_at + " " + v_at
                        self.do_update(concat)
                    elif len(command.split("(")[1].split(", {")) == 2:
                        md = command.split("(")[1].split(", {")[0].strip(')"')
                        s = command.split("(")[1].split(", {")[1].strip(")")
                        dic = eval("{" + s)
                        for atr, val in dic.items():
                            concat = cn + " " + md + " " + atr + " " + str(val)
                            self.do_update(concat)

    def count(self, class_name):
        objs = storage.all()
        num_objs = 0
        for name_id in objs.keys():
            if name_id.split(".")[0] == class_name:
                num_objs += 1
        print(num_objs)

if __name__ == '__main__':
    prompt = HBNBCommand()
    prompt.prompt = '(hbnb) '
    prompt.cmdloop()
