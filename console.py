#!/usr/bin/python3
import cmd
import shlex
from shlex import split
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """hbnb command interpreter class"""

    prompt = '(hbnb) '

    __myClasses = [
        "BaseModel", "User", "State",
        "City", "Place", "Amenity", "Review"]

    def do_EOF(self, line):
        """End of file function """
        return True

    def do_quit(self, line):
        """Command that quit"""
        return True

    def do_create(self, args):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id"""
        args = shlex.split(args)
        if args == []:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        else:
            models.storage.reload()
            instance = eval(args[0])()
            instance.save()
            print(instance.id)

    def do_show(self, args):
        """Prints the string representation of an
        instance based on the class name and id"""
        args = shlex.split(args)
        if args == []:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            models.storage.reload()
            for key, obj in models.storage.all().items():
                if obj.id == args[1] and obj.__class__.__name__ == args[0]:
                    print(obj.__str__())
                    return
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        args = shlex.split(args)
        if args == []:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            models.storage.reload()
            my_objs = models.storage.all()
            for k, obj in my_objs.items():
                if obj.id == args[1] and obj.__class__.__name__ == args[0]:
                    del(my_objs[k])
                    models.storage.save()
                    return
            print("** no instance found **")

    def do_all(self, args):
        """ Prints all string representation of all
        instances based or not on the class name."""
        args = shlex.split(args)
        if len(args) == 0:
            models.storage.reload()
            my_list = []
            for i, obj in models.storage.all().items():
                my_list.append(obj.__str__())
            print(my_list)
        elif args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        else:
            models.storage.reload()
            my_list = []
            for i, obj in models.storage.all().items():
                if obj.__class__.__name__ == args[0]:
                    my_list.append(obj.__str__())
            print(my_list)

    def do_update(self, args):
        """Updates an instance based on the class name
        and id by adding or updating attribute """
        args = shlex.split(args)
        if args == []:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            models.storage.reload()
            my_objs = models.storage.all()
            for i, obj in my_objs.items():
                if obj.id == args[1] and obj.__class__.__name__ == args[0]:
                    if len(args) == 2:
                        print("** attribute name missing **")
                        return
                    elif len(args) == 3:
                        print("** value missing **")
                        return
                    else:
                        new_att = args[3]
                        if hasattr(obj, str(args[2])):
                            new_att = (type(getattr(obj, args[2])))(args[3])
                        obj.__dict__[args[2]] = new_att
                        models.storage.save()
                        return
            print("** no instance found **")

    def parse(self, args):
        """strtok"""
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def emptyline(self):
        """print a new empty line"""
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_count(self, args):
        """count"""
        counter = 0
        args = split(args, " ")
        if args[0] not in HBNBCommand.__myClasses:
            print("** class doesn't exist **")
        else:
            things = models.storage.all()
            for key in things:
                name = key.split('.')
            if name[0] == args[0]:
                counter += 1
            print(counter)

    def default(self, args):
        """do the default """
        sargs = args.split('.')
        if len(sargs) >= 2:
            if sargs[1] == "all()":
                self.do_all(sargs[0])
            elif sargs[1] == "count()":
                self.do_count(sargs[0])
            elif sargs[1][:4] == "show":
                self.do_show(self.parse(sargs))
            elif sargs[1][:7] == "destroy":
                self.do_destroy(self.parse(sargs))
            elif sargs[1][:6] == "update":
                args = self.parse(sargs)
                if isinstance(args, list):
                    obj = models.storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, args)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
