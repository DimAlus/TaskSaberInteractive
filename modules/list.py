"""Task builder

Usage:
    app.py <list> [<tasks> | <builds>]

Description:
    Show a list of tasks and builds.

Commands:
    task        Show a list of tasks.
    builds      Show a list of builds.


"""
description = "Show a list of tasks and builds."
from docopt import DocoptExit
from .lib import get_tasks, get_builds, task_have_cycle


def __show_tasks(**kwargs):
    tasks = get_tasks(
        kwargs["--tasks"],
        "tasks",
        kwargs["scheme"],
        kwargs["to_color"],
    )
    print(
        "List of available tasks:",
        *[
            kwargs["to_color"](
                name,
                "red" if task_have_cycle(name, tasks) else "white",
            )
            for name in tasks
        ],
        sep="\n * ",
        end="\n\n",
    )
    pass


def __show_builds(**kwargs):
    builds = get_builds(
        kwargs["--builds"],
        "builds",
        kwargs["scheme"],
        kwargs["to_color"],
    )
    print(
        "List of available builds:",
        *[name for name in builds],
        sep="\n * ",
        end="\n\n",
    )


def run(**kwargs):
    if "builds" in kwargs["<args>"]:
        __show_builds(**kwargs)
    elif "tasks" in kwargs["<args>"]:
        __show_tasks(**kwargs)
    else:
        __show_tasks(**kwargs)
        __show_builds(**kwargs)
