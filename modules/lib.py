import os, yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from docopt import DocoptExit


def get_yaml(path: str | None, name: str, scheme: dict) -> dict | None:
    if not path:
        path = scheme.get(name, None)
    if not path or not type(path) is dict:
        return None
    path = path.get("path", None)
    if not path or not type(path) is str or not os.path.exists(path):
        return None
    with open(path, "r") as f:
        try:
            yml = yaml.load(f, Loader=Loader)
        except:
            return None
    return yml


def to_color(mess: str, color: str):
    clrs = ["gray", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    if not color.lower() in clrs:
        color = "white"
    color = clrs.index(color.lower())

    return f"\u001b[3{color}m" + mess + "\u001b[0m"


# Parse tasks on correct data
def get_tasks(
    path: str | None,
    scheme: dict,
    to_color=lambda x, y: x,
) -> dict[str:set]:
    yml = get_yaml(path=path, name="tasks", scheme=scheme)

    if yml is None:
        raise DocoptExit("Wrong load yaml: <tasks> not loaded!")
    if not "tasks" in yml:
        raise DocoptExit("Wrong read yaml: object <tasks> not found!")
    if not type(yml["tasks"]) is list:
        raise DocoptExit("Wrong read yaml: object <tasks> must be list!")
    tasks = {}
    for tsk in yml["tasks"]:
        if task_is_correct(tsk):
            tasks[tsk["name"]] = tasks.get(tsk["name"], set()) | set(
                tsk["dependencies"]
            )
        else:
            print(to_color("Warning!", "yellow"), f"task <{tsk}> not correct!")
    return tasks


# Parse builds on correct data
def get_builds(
    path: str | None,
    scheme: dict,
    to_color=lambda x, y: x,
) -> dict[str:set]:
    yml = get_yaml(path=path, name="builds", scheme=scheme)
    if yml is None:
        raise DocoptExit("Wrong load yaml: <builds> not loaded!")
    if not "builds" in yml:
        raise DocoptExit("Wrong read yaml: object <builds> not found!")
    if not type(yml["builds"]) is list:
        raise DocoptExit("Wrong read yaml: object <builds> must be list!")
    builds = {}
    for bld in yml["builds"]:
        if build_is_correct(bld):
            builds[bld["name"]] = builds.get(bld["name"], set()) | set(bld["tasks"])
        else:
            print(to_color("Warning!", "yellow"), f"task <{bld}> not correct!")
    return builds


def task_have_cycle(name: str, tasks: dict) -> bool:
    return False
    pass


def task_is_correct(task: dict) -> bool:
    return type(task) is dict and "name" in task and "dependencies" in task


def build_is_correct(build: dict) -> bool:
    return type(build) is dict and "name" in build and "tasks" in build
