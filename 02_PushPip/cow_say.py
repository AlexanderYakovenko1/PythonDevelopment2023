import sys
from argparse import ArgumentParser

from cowsay import cowsay, list_cows, read_dot_cow


PRESETS = {
    'b': 'Borg mode',
    'd': 'Dead mode',
    'g': 'Greedy mode',
    'p': 'Paranoia mode',
    's': 'Stoned mode',
    't': 'Tired mode',
    'w': 'Wired mode',
    'y': 'Youthful mode'
}


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('message', nargs='?', help='The message for cow to say.')
    parser.add_argument('-e', type=str, default='oo', metavar='eye_string', help='String to use for cow\'s eyes. Only first two characters are used.')
    parser.add_argument('-f', type=str, default='default', metavar='cowfile', help='Specify cow\'s appearance.')
    parser.add_argument('-l', action='store_true', help='List available cows.')
    parser.add_argument('-n', action='store_false', help='Text wrap switch')
    parser.add_argument('-T', type=str, default='  ', metavar='tongue_string', help='String to use for cow\'s tongue. Must be two characters in lenght.')
    parser.add_argument('-W', type=int, default=40, metavar='column', help='Word wrap width.')

    for preset, desc in PRESETS.items():
        parser.add_argument(f"-{preset}", action='store_true', help=desc)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.l:
        print(*list_cows())
    else:
        if args.message is None:
            message = sys.stdin.read()
        else:
            message = args.message

        cow = args.f
        eyes = args.e[:2]
        tongue = args.T[:2]
        width = args.W
        wrap_text = args.n

        if '/' in args.f:
            with open(args.f) as f:
                cowfile = read_dot_cow(f)
        else:
            cowfile = None

        preset = [p for p in PRESETS if getattr(args, p)]
        preset = preset[0] if preset else None
        print(cowsay(message, cow, preset, eyes, tongue, width, wrap_text, cowfile))


if __name__ == '__main__':
    main()
