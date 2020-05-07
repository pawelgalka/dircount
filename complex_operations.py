import commands
import error_factory
import settings
from directory_functions import Directory
from var_types import parse_value, Types, declare, let


def _if(directory):
    if not 3 >= directory.dirlen() >= 2:
        error_factory.ErrorFactory.invalid_command_dir_number([2,3], directory.path, directory.dirlen(), "IF")
    if parse_value(directory.navigate_to_nth_child(0), Types.boolean, 1):
        print("IF true execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("COMPLEX IF TRUE", directory.path)
            commands.expression(directory)

    elif directory.dirlen() == 3:
        print("IF false execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("COMPLEX IF FALSE", directory.path)
            commands.expression(directory)


def _while(directory):
    if directory.dirlen() != 2:  # logical condition, list of commands
        error_factory.ErrorFactory.invalid_command_dir_number([2], directory.path, directory.dirlen(), "WHILE")

    condition_dir = directory.navigate_to_nth_child(0)
    counter = 1
    while parse_value(condition_dir, Types.boolean, 1):
        print(f"WHILE executing {counter} times")
        root = Directory(directory.navigate_to_nth_child(1).path)
        execute_all_loop_commands(root)
        counter += 1


def _for(directory):
    # list of commands
    # var_declare, boolean_expression,  list of commands
    # var_declare, boolean_expression, let_expression, list of commands
    if directory.dirlen() not in for_arguments_dict.keys():
        error_factory.ErrorFactory.invalid_command_dir_number([1,3,4], directory.path, directory.dirlen(), "FOR")
    for_arguments_dict[directory.dirlen()](directory)


def _infinite_for(directory):
    print("Starting infinite for loop")
    while True:
        execute_all_loop_commands(directory.navigate_to_nth_child(0))


def _var_and_condition_for(directory):
    path, _, _ = declare(directory.navigate_to_nth_child(0))
    boolean_dir = directory.navigate_to_nth_child(1)
    commands_root = directory.navigate_to_nth_child(2)
    counter = 1
    while parse_value(boolean_dir, Types.boolean, 1):
        print(f"FOR executing {counter} times")
        execute_all_loop_commands(commands_root)
        counter += 1
    remove_var_from_scope(path)


def _full_for(directory):
    path, _, _ = declare(directory.navigate_to_nth_child(0))
    boolean_dir = directory.navigate_to_nth_child(1)
    let_dir = directory.navigate_to_nth_child(2)
    commands_root = directory.navigate_to_nth_child(3)
    counter = 1
    while parse_value(boolean_dir, Types.boolean, 1):
        print(f"FOR executing {counter} times")
        execute_all_loop_commands(commands_root)
        let(let_dir)
        counter += 1
    remove_var_from_scope(path)


def execute_all_loop_commands(root):
    for commands_dir in root.get_directory_children():
        print("COMPLEX WHEN command at", commands_dir.path)
        commands.expression(commands_dir)


def remove_var_from_scope(path):
    del settings.variables[path]


for_arguments_dict = {
    1: _infinite_for,
    3: _var_and_condition_for,
    4: _full_for,
}