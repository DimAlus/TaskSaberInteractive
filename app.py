"""Task builder

Usage:
    app.py [-s scheme] [-t taskpath] [-b buildpath] [-c] [-h] [<command>] [<args> ...]

Options:
    -h --help                               Show this screen.
    -c --colored                            Use colored output 
                                                (recommended if not used cmd.exe)
    -t taskpath --tasks=taskpath            Select path to tasks  list file
    -b buildpath --builds=buildpath         Select path to builds list file
    -s scheme --settings-scheme=scheme      Select settings scheme at settings.toml

Commands:
"""

# """Task builder

# Usage:
#     app.py [(-s <scheme>)] [(-t <taskpath>)] [(-b <buildpath>)] [-h] [<command>] [<args> ...]

# Options:
#     -h --help               Show this screen.
#     -t --tasks              Select path to tasks  list file
#     -b --builds             Select path to builds list file
#     -s --settings-scheme    Select settings scheme at settings.toml

# Commands:
# """
# Comminds are all modules into directory modules
import modules

__tabsize, __to_desc = 4, len("-h --help                               ")

for module in dir(modules):
    if not module.startswith("__"):
        # Adding to __doc__ command description
        desc = getattr(getattr(modules, module), "description", "")
        __doc__ += f"{' ' * __tabsize}{module}{' ' * (__to_desc - len(module))}{desc}"


from docopt import docopt, DocoptExit
from modules.lib import to_color

if __name__ == "__main__":
    args = docopt(__doc__, help=False)
    # print(args)

    ###
    ### Get implemetable module
    ###
    mod = getattr(
        modules,
        ""
        if args["<command>"] is None or args["<command>"].startswith("__")
        else args["<command>"],
        None,
    )

    if args["--help"]:
        docopt(__doc__ if mod is None else mod.__doc__)

    if mod is None:
        raise DocoptExit(f"Wrong command selected: <{args['<command>']}>!")

    ###
    ### Get settings
    ###
    from settings import settings, settings_file

    scheme = args["--settings-scheme"] if args["--settings-scheme"] else "standard"
    if not scheme in settings:
        raise DocoptExit(
            f"Wrong scheme selected: <{scheme}>! \n"
            + f"Settings file: <{settings_file}>\n"
        )

    mod.run(
        **args,
        scheme=settings[scheme],
        to_color=(to_color if "--colored" in args else lambda x, y: x),
    )
