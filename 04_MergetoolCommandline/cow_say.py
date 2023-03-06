import cmd
import shlex
import readline

from cowsay import cowsay, list_cows

class CowShell(cmd.Cmd):
    intro = 'This is cowsay shell. Moo all you like.\nType help or ? to list commands.\n'
    prompt = '(cowsay) '

    @staticmethod
    def __parse_arg(arg):
        params = {
            'message': None,
            'cow': 'default',
            'eyes': 'oo',
            'tongue': '  '
        }

        args = shlex.split(arg)
        for key, arg in zip(params, args):
            params[key] = arg

        return params


    def do_EOF(self, arg):
        """Exit the program"""
        return True

    def do_bye(self, arg):
        """Say goodbye to the cow (exits the program)"""
        return True

    def do_listcows(self, arg):
        """List available cows"""
        print(list_cows())

    def do_cowsay(self, arg):
        """Make cow says the message of your choice"""
        print(cowsay(**self.__parse_arg(arg)))

    def complete_cowsay(self, text, line, begidx, endidx):
        pass


if __name__ == '__main__':
    CowShell().cmdloop()
