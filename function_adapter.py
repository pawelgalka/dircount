import commands
from directory_functions import Directory
from variable_holder import VariableStack


class Function:
    function_stack = []

    # 1 folder - list of commands, 2 folder - name, 3 folder - args no (if empty 0 arg fun),
    # 4 folder return value name (if empty void func)
    def __init__(self, pointer, name, args_no, return_val_id):
        self.variable_stack = VariableStack()
        self.root = Directory(pointer)
        self.name = name
        self.args_no = args_no
        self.return_val_id = return_val_id

    def perform_function_code(self):
        print("PERFORMING FUNCTION", self.name)
        for directory in self.root.get_directory_children():
            print(self.name, directory.path)
            commands.expression(directory)
        if self.return_val_id is not None:
            return self.find_var_by_name(self.return_val_id)[1]

    def find_var_by_name(self, var_name):
        return self.variable_stack.get_var_by_name(var_name)

    def find_var_by_path(self, var_pointer):
        return self.variable_stack.get_var_by_path(var_pointer)

    def clear_var_stack(self):
        self.variable_stack.clear()

    def __str__(self):
        return ",".join([str(s) for s in [self.root.path, self.name, self.return_val_id]])

    def __eq__(self, other):
        isinstance(other, Function.__class__) and self.root == other.root
