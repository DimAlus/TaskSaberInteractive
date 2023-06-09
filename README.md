# Немного о разработчике
https://docs.google.com/document/d/1aYIyPKLziVc0T9I9Mlo1tynArC-v9PuheCDBeTLT-Lo/edit#heading=h.61qt5j2cwjev
# Описание
Для разработки игр требуется билд-система, которая автоматизирует и ускоряет рутинные процессы.

Система оперирует понятиями `задача` и `билд`. 

### `Задача` – это то, что нужно сделать.

Например:
* Собрать ресурсы игры
* Скомпилировать .exe
* Запаковать игру

Задача описывается уникальным именем (`name`) и ее зависимостями (`dependencies`) от других задач. Задача не может быть выполнена раньше, чем ее зависимости. 

Описания задач задаются в .yaml-файле `tasks.yaml`.

### `Билд` – это группа задач, объединенных функционально.

Например:
* **Собрать игру**
    * собрать ресурсы игры 
    * скомпилировать .exe 
    * запаковать игру
* **Запустить тесты** 
    * собрать ресурсы игры
    * скомпилировать .exe

Билд описывается уникальным именем (`name`) и списком задач (`tasks`).
Описания билдов задаются в yaml-файле `builds.yaml`.

# CLI
Программу можно вызывать с помощью комманной строки.
### Progam CLI
```bash
Usage:
    app.py  [-s scheme] [-t taskpath] [-b buildpath] [-c] [-h] 
            [<command>] [<args> ...]

Options:
    -h --help                               
                Show this screen.
    -c --colored                            
                Use colored output 
                (recommended if not used cmd.exe)
    -t taskpath --tasks=taskpath            
                Select path to tasks  list file
    -b buildpath --builds=buildpath         
                Select path to builds list file
    -s scheme --settings-scheme=scheme      
                Select settings scheme at settings.toml

Commands:
    list        Show a list of tasks and builds.
    get         Show a datails of tasks and builds.
```
Для каждой из команд используются разные списки аргументов
### List CLI
```bash
Usage:
    app.py <list> [<tasks> | <builds>] [<name> ...]

Description:
    Show a list of tasks and builds.

Commands:
    task        Show a list of tasks.
    builds      Show a list of builds.

```
### Get CLI
```bash
Usage:
    app.py <get> [(<tasks> | <builds>) [<name> ...]]

Description:
    Show a datails of tasks and builds.

Commands:
    task        Show a details of tasks.
    builds      Show a details of builds.
    name        Name of task ot build for details.

```
# Зависимости
* Python 3.10
```bash
pip install docopt, pyyaml
```
# Выбор файлов для сборки
Выбрать необходимые файлы для сборки (`tasks.yaml`, `builds.yaml`) можно двумя способами:
1. Явно указать их с помощью аргументов командной строки.
1. Задать через *файл конфигурации*.

## С помощью командной строки
Для явного указания файлов исходников можно воспользоваться ключами:
```bash
-t taskpath --tasks=taskpath            
            Select path to tasks  list file
-b buildpath --builds=buildpath         
            Select path to builds list file
```

Например:
```bash
app.py -b C:/builds.yaml list builds
app.py --builds=C:/builds.yaml -t ./tasks.yaml get builds
```

В случае, если какой-либо файл не указан явно, он берется из файла конфикурации.

## С помощью *файла конфигурации*
В файле `settings.toml` определены параметры по умолчанию для программы.

В случае, если их необходимо перезаписать, рекоммендуется создать файл `settings.overload.toml`, в котором будут изменяться параметры, зависящие от конкретного устройства.

Например:

`settings.toml`
```toml
[standard]
[standard.tasks]
path = "./data/tasks.yaml"

[standard.builds]
path = "./data/builds.yaml"


[other]
[other.tasks]
path = "./data/tasks_other.yaml"

[other.builds]
path = "./data/builds_other.yaml"
```
`settings.overload.toml`
```toml
[standard]
[standard.tasks]
path = "C:/tasks.yaml"

[standard.builds]
path = "C:/builds.yaml"


[other]
[other.tasks]
path = "./data/tasks_other.yaml"

[other.builds]
path = "./data/builds_other.yaml"
```

Пояснение:

Файл `overload` включен в `.gitignore` и подходит для локальной конфигурации на конкретном устройстве.

### Схемы конфигурации
Также, для удобства предоставлена возможность выбора схемы конфигурации.

По умолчанию берется схема `standard`.

Схему можно переопределить параметром коммандной строки:
```bash
app.py -s other list
```

# Инструкция по запуску
С выбором файлов `tasks.yaml` и `builds.yaml` мы разобрались в прошлой главе.

## Справка
Чтобы получить справку по программе, необходимо использовать ключ `-h`.

Чтобы получить детальную информацию по определенной команде, необходимо также написать ее имя.

Например:
```bash
app.py -h
app.py list -h
```

## App List
```bash
Usage:
    app.py <list> [<tasks> | <builds>]

Description:
    Show a list of tasks and builds.

Commands:
    task        Show a list of tasks.
    builds      Show a list of builds.

```
В случае, если не указаны подкоманды (`tasks`, `builds`), программа выведет сперва список задач, затем список сборок. 

Если заданы обе подкоманды, будет выведен только список сборок.

Например:
```bash
rem Вывод списка сборок и задач
app.py list

rem Вывод списка задач
app.py list tasks
```

## App Get
```bash
Usage:
    app.py <get> [(<tasks> | <builds>) [<name> ...]]

Description:
    Show a datails of tasks and builds.

Commands:
    task        Show a details of tasks.
    builds      Show a details of builds.
    name        Name of task ot build for details.

```
Подкоманды `task` и `tasks`, `build` и `builds` равнозначны соответственно.

В случае, если не указаны подкоманды (`tasks`, `builds`), программа выведет сперва детальную информацию по всем задачам, затем по сборкам. 

Если заданы обе подкоманды, вторая будет расцениваться как параметр `<name>`.

Если `<name>` не задан, будет выведена информация по всем элементам.

`<name>` можно передавать списком, через пробел.

Например:
```bash
rem Вывод информации по задачам t1 и t2
app.py -c get task t1 t2

rem Вывод информации по сборке task
app.py -c get build task
```

## Примечание
Если используется терминал, поддерживающий ANSI последовательности (не cmd.exe), рекомендуется использовать флаг -с, выделяющий проблемные места цветом.

Таким образом при ошибке чтения задач или сборок будут выводиться цветные предупреждения, а команда `get` будет выделять **красным** не найденные задачи, а **желтым** найденные циклы при анализе зависимостей.