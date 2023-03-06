import cmd
import shlex
import readline

from cowsay import THOUGHT_OPTIONS, cowsay, cowthink, list_cows, make_bubble

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

    @staticmethod
    def __complete_arg(text, line, begidx, endidx):
        defaults = {
            'cow': list_cows(),
            'eyes': ['==', 'XX', '$$', '@@', '**', '--', 'OO', '..'],
            'tongue': ['U ', 'WW', '__', 'ZZ']
        }

        args = shlex.split(line)
        if len(args) <= 2 and begidx != endidx:
            return None
        else:
            idx = len(args) - 3
            if begidx == endidx:
                idx += 1

            key = ['cow', 'eyes', 'tongue'][idx]
            options = defaults[key]
            return [opt for opt in options if opt.startswith(text)]


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
        """Make cow say the message of your choice"""
        print(cowsay(**self.__parse_arg(arg)))

    def do_cowthink(self, arg):
        """Make cow think the message of your choice"""
        print(cowthink(**self.__parse_arg(arg)))

    def complete_cowsay(self, text, line, begidx, endidx):
        return self.__complete_arg(text, line, begidx, endidx)

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.__complete_arg(text, line, begidx, endidx)

    def do_make_bubble(self, arg):
        """Generate bubble with text"""
        params = {
            'text': None,
            'wrap_text': True,
            'width': 40
        }

        args = shlex.split(arg)
        for key, arg, func in zip(params, args, [lambda x: x, eval, int]):
            params[key] = func(arg)

        params.update({
            'brackets': THOUGHT_OPTIONS['cowsay']
        })

        print(make_bubble(**params))

    def complete_make_bubble(self, text, line, begidx, endidx):
        args = shlex.split(line)
        if len(args) <= 2 and begidx != endidx:
            return None
        else :
            idx = len(args) - 2
            if begidx == endidx:
                idx += 1
            if idx == 1:
                return [opt for opt in ['True', 'False'] if opt.startswith(text)]


if __name__ == '__main__':
    CowShell().cmdloop()
