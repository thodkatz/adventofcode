from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional, Union


class FileNode:
    def __init__(self, name: str, size: int = 0, parent: Optional[FileNode] = None):
        self.file = name
        self.size = size
        self.parent: Optional[FileNode] = parent
        self._subfiles: Dict[str, FileNode] = {}

    def is_file(self):
        return len(self._subfiles) == 0

    def add(self, node: Union[FileNode, str]):
        if isinstance(node, str):
            self._add_dir(node)
        else:
            self._add_file(node)

    def _add_dir(self, name: str):
        self._subfiles[name] = FileNode(name, parent=self)

    def _add_file(self, node: FileNode):
        assert node.is_file()
        self._subfiles[node.file] = node

    @classmethod
    def file(cls, filename: str, size: int, parent: FileNode):
        return cls(filename, size=size, parent=parent)

    @property
    def subfiles(self) -> Dict[str, FileNode]:
        return self._subfiles

    def __repr__(self):
        return repr(f"{self.file}, {self.size}")


class FileSystem:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.root = FileNode("")
        self.root.add("/")
        self.curr = self.root
        self._parse()

    def _parse(self):
        with open(self.filepath, "r") as file:
            for line in file:
                self._parse_command(line.strip())
        self._update_size(self.root)

    def _parse_command(self, line: str):
        if line.startswith("$ cd"):
            dirname = line.split("$ cd ")[1]
            if dirname == "..":
                self.curr = self.curr.parent
            else:
                self.curr = self.curr.subfiles[dirname]
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir"):
            dirname = line.split("dir ")[1]
            self.curr.add(dirname)
        else:
            size, filename = line.split(" ")
            self.curr.add(FileNode.file(filename, int(size), parent=self.curr))

    def _update_size(self, node: FileNode) -> int:
        for sub_node in node.subfiles.values():
            node.size += self._update_size(sub_node)
        return node.size

    def total_size_under_size(self, target: int):
        return sum(node.size for node in self.nodes_by_size(target, is_greater=False))

    def nodes_by_size(self, target: int, is_greater: bool) -> List[FileNode]:
        def dfs(node: FileNode, res):
            cond = node.size > target if is_greater else node.size <= target
            if not node.is_file() and cond:
                res.append(node)
            for sub_node in node.subfiles.values():
                dfs(sub_node, res)

        res = []
        dfs(self.root, res)
        return res

    def node_to_delete(self, target: int) -> int:
        return min([node.size for node in self.nodes_by_size(target, is_greater=True)])

def main():
    filesystem = FileSystem(Path("input.txt"))
    print(filesystem.total_size_under_size(100_000))
    total_space = 70_000_000
    need = 30_000_000
    current_free_space = total_space - filesystem.root.size
    to_delete = need - current_free_space
    print(filesystem.node_to_delete(to_delete))



if __name__ == "__main__":
    main()
