import argparse
import numpy as np
from automate import post


def build_parser():

    parser = argparse.ArgumentParser(
        description="automate. This library is made for quick data manipulation from the command line"
    )
    sub_parsers = parser.add_subparsers(help="sub-commands help")

    d_categories = {
        "pre":{

        },
        "post": {
            "concat": post.Concatenator,
            "filter": post.Filterer,
            "resample":post.Resampler
        },
    }

    for category, actions in d_categories.items():
        group_parser = sub_parsers.add_parser(category)
        group_sub_parsers = group_parser.add_subparsers(
            help=f"{category} commands help"
        )

        for action, item in actions.items():
            action_parser = group_sub_parsers.add_parser(action)

            if item is not None:
                item(parser=action_parser).build_args()
                action_parser.set_defaults(func=item.do_actions)

    return parser


def main():
    import sys

    argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
