#!/usr/bin/python3

import cmd
import json
import re

from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB."""

    prompt = "(hbnb) "

    def default(self, line):
        """Handle unknown commands."""
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts and processes commands."""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line

        classname, method, args = match.groups()
        uid, attr_or_dict = self._parse_args(args)

        if method == "update" and attr_or_dict:
            self._handle_update(classname, uid, attr_or_dict)
            return ""

        command = f"{method} {classname} {uid} {attr_or_dict}"
        self.onecmd(command)
        return command

    def _parse_args(self, args):
        """Parses arguments for class.method() calls."""
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False
        return uid, attr_or_dict

    def _handle_update(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)

        if not classname:
            print("** class name missing **")
            return

        if classname not in storage.classes():
            print("** class doesn't exist **")
            return

        if uid is None:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return

        attributes = storage.attributes().get(classname, {})
        instance = storage.all()[key]

        for attribute, value in d.items():
            if attribute in attributes:
                value = attributes[attribute](value)
            setattr(instance, attribute, value)
        instance.save()

    def do_EOF(self, line):
        """Handle End Of File character."""
        print()
        return True

    def do_quit(self, line):
        """Exit the program."""
        return True

    def emptyline(self):
        """Do nothing on ENTER."""
        pass

    def do_create(self, line):
        """Create an instance."""
        if not line:
            print("** class name missing **")
            return

        classname = line.split()[0]
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return

        new_instance = storage.classes()[classname]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Print the string representation of an instance."""
        if not line:
            print("** class name missing **")
            return

        words = line.split(' ')
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return

        if len(words) < 2:
            print("** instance id missing **")
            return

        key = f"{words[0]}.{words[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destroy(self, line):
        """Delete an instance based on the class name and id."""
        if not line:
            print("** class name missing **")
            return

        words = line.split(' ')
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return

        if len(words) < 2:
            print("** instance id missing **")
            return

        key = f"{words[0]}.{words[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Print all string representations of all instances."""
        if line:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
                return

            instances = [str(obj) for key, obj in storage.all().items()
                    if type(obj).__name__ == words[0]]
            print(instances)
        else:
            all_instances = [str(obj) for key, obj in storage.all().items()]
            print(all_instances)

    def do_count(self, line):
        """Count the instances of a class."""
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
            return

        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return

        matches = [k for k in storage.all() if k.startswith(words[0] + '.')]
        print(len(matches))

    def do_update(self, line):
        """Update an instance by adding or updating attribute."""
        if not line:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        if not match:
            print("** class name missing **")
            return

        classname, uid, attribute, value = match.groups()
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return

        if uid is None:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if not attribute:
            print("** attribute name missing **")
            return

        if not value:
            print("** value missing **")
            return

        cast = None
        if not re.search('^".*"$', value):
            if '.' in value:
                cast = float
            else:
                cast = int
        else:
            value = value.replace('"', '')

        attributes = storage.attributes().get(classname, {})
        instance = storage.all()[key]

        if attribute in attributes:
            value = attributes[attribute](value)
        elif cast:
            try:
                value = cast(value)
            except ValueError:
                pass  # fine, stay a string then

        setattr(instance, attribute, value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

