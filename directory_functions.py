import os

import error_factory


class Directory:
    path_separator = '/'

    def __init__(self, path, parent_path=None):
        self.parent_path = parent_path
        self.path = path
        children = os.listdir(path)

        children = list(filter(lambda x: os.path.isdir(self.get_child_path(x)), children))
        children.sort(key=lambda x: (len(x), x))
        self.children_paths = [self.get_child_path(child) for child in children]

    def get_path(self):
        return self.path

    def get_nth_child_path(self, n):
        return self.children_paths[n]

    def get_child_path(self, child_name):
        return os.path.abspath(self.path + self.path_separator + child_name)
        # return self.path + self.path_separator + child_name

    def navigate_to_nth_child(self, n):
        return Directory(self.get_nth_child_path(n), parent_path=self)

    def get_children_paths(self):
        return self.children_paths

    def get_directory_children(self):
        return [Directory(child, parent_path=self.path) for child in self.children_paths]

    def dirlen(self):
        return len(self.children_paths)

    def get_dir_type(self):
        print("DIR FUNC ", self.navigate_to_nth_child(0).path)
        return self.navigate_to_nth_child(0).dirlen()

    def get_link_path(self):
        return (os.readlink(self.path), os.readlink(self.path)[:-1])[os.readlink(self.path).endswith('/')]

    def is_var_linked(self):
        # done for handling both path reference and name reference
        # TODO: in var_types create parser for reference type if dirlen = 1 -> pointer if dirlen = 3 -> by name (one folder must be link to anything eq. parent folder and 2 other typical string
        return any(os.path.islink(path) for path in
                   self.get_children_paths()) and \
               self.dirlen() in [1, 3]  # is link or string name of var

    @staticmethod
    def directory_to_bit(directory_path):
        n_subdirs = Directory(directory_path).dirlen()
        if n_subdirs > 1:
            error_factory.ErrorFactory.bit_directory_error(directory_path, n_subdirs)
        else:
            return n_subdirs
