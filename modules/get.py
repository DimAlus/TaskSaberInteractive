"""Task builder

Usage:
    app.py get [(<tasks> | <builds>) [<name> ...]]

Description:
    Show a datails of tasks and builds.

Commands:
    task        Show a details of tasks.
    builds      Show a details of builds.
    name        Name of task ot build for details.


"""
description = "Show a datails of tasks and builds."


from docopt import DocoptExit
from .lib import get_tasks, get_builds, task_have_cycle


def __get_dependencies(
    name: str,
    tasks: dict[str:set],
    loaded: set[str],
    path: set[str],
) -> list[tuple[str, int]]:
    if name in loaded:
        return []
    if name in path:
        return [(name, 1)]
    if not name in tasks:
        return [(name, 2)]
    lt = []
    for dep in tasks[name]:
        res = __get_dependencies(dep, tasks, loaded, path | {name})
        lt += res
        loaded |= {r[0] for r in res}
    return lt + [(name, 0)]


def __get_tasks(**kwargs):
    tasks = get_tasks(
        kwargs["--tasks"],
        kwargs["scheme"],
        kwargs["to_color"],
    )
    names = kwargs["<args>"]
    task_names = set(tasks)
    if len(names) > 1:
        names = names[1:]
    else:
        names = list(task_names)
    for name in names:
        if name in task_names:
            print("Task info:", f"Name: {name}", "Dependencies: ", sep="\n\t", end="")
            print(
                *[
                    kwargs["to_color"](t[0], {1: "yellow", 2: "red"}.get(t[1], "white"))
                    for t in __get_dependencies(name, tasks, set(), set())
                ],
                sep=", ",
            )
        else:
            print(kwargs["to_color"]("Warning!", "yellow"), f"task <{name}> not exist!")


def __get_builds(**kwargs):
    builds = get_builds(
        kwargs["--builds"],
        kwargs["scheme"],
        kwargs["to_color"],
    )
    tasks = get_tasks(
        kwargs["--tasks"],
        kwargs["scheme"],
        kwargs["to_color"],
    )
    names = kwargs["<args>"]
    build_names = set(builds)
    if len(names) > 1:
        names = names[1:]
    else:
        names = list(builds)
    for name in names:
        if name in builds:
            loaded = set()
            deps = []
            for tsk in builds[name]:
                deps += __get_dependencies(tsk, tasks, loaded, set())
                loaded |= {d[0] for d in deps}
            print("Build info:", f"Name: {name}", "Dependencies: ", sep="\n\t", end="")
            print(
                *[
                    kwargs["to_color"](t[0], {1: "yellow", 2: "red"}.get(t[1], "white"))
                    for t in deps
                ],
                sep=", ",
            )
        else:
            print(
                kwargs["to_color"]("Warning!", "yellow"), f"build <{name}> not exist!"
            )


def run(**kwargs):
    if "builds" in kwargs["<args>"] or "build" in kwargs["<args>"]:
        __get_builds(**kwargs)
    elif "tasks" in kwargs["<args>"] or "task" in kwargs["<args>"]:
        __get_tasks(**kwargs)
    else:
        __get_tasks(**kwargs)
        __get_builds(**kwargs)
