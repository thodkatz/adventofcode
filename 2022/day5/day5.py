"""
Sorry for the python usage. We were supposed to use julia, but I am not thinking in julia and it is frustrating. Switched to my friend python
"""

from __future__ import annotations
from typing import List, TextIO
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Instructions:
    count: int
    start: int
    dest: int

    @classmethod
    def create(cls, line: str) -> Instructions:
        parts = line.split(" ")
        assert len(parts) == 6
        zero_index_offset = 1
        return Instructions(int(parts[1]), int(parts[3]) - zero_index_offset, int(parts[5]) - zero_index_offset)


class Tasks:
    STACK_OFFSET = 4

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._stacks: List[List[str]] = []
        self._gold_stacks: List[List[str]] = []
        self._silver_stacks: List[List[str]] = []
        self._parse()

    def _parse(self):
        with open(self._filepath, "r") as file:
            line = self._readline(file)
            while not self._is_end_of_base_stack(line):
                self._parse_stacks(line)
                line = self._readline(file)

            self._reverse_stacks()
            line = self._move_to_instructions(file)

            self._gold_stacks = deepcopy(self._stacks)
            self._silver_stacks = deepcopy(self._stacks)
            while line:
                instruction = Instructions.create(line)
                self._apply_silver_instruction(instruction)
                self._apply_gold_instruction(instruction)
                line = self._readline(file)

    def _parse_stacks(self, line: str):
        for count, i in enumerate(range(0, len(line), self.STACK_OFFSET)):
            if len(self._stacks) == count:
                self._stacks.append([])
            if not line[i] == " ":
                self._stacks[count].append(line[i + 1])

    def _is_end_of_base_stack(self, line: str):
        return len(line) >= 2 and line[0] == " " and line[1].isnumeric()

    def _readline(self, file: TextIO):
        return file.readline().strip("\n")

    def _reverse_stacks(self):
        assert len(self._stacks) != 0
        # improving performance when it comes to applying instructions
        for stack in self._stacks:
            stack.reverse()
            
    def _move_to_instructions(self, file: TextIO) -> str:
        line = self._readline(file)
        while not line.startswith("move"):
            line = self._readline(file)
        return line

    def _apply_silver_instruction(self, instruction: Instructions):
        from_stack = self._silver_stacks[instruction.start]
        to_stack = self._silver_stacks[instruction.dest]
        for _ in range(instruction.count):
            to_stack.append(from_stack.pop())

    def _apply_gold_instruction(self, instruction: Instructions):
        from_stack = self._gold_stacks[instruction.start]
        to_stack = self._gold_stacks[instruction.dest]
        crates = []
        for _ in range(instruction.count):
            crates.append(from_stack.pop())
        for crate in reversed(crates):
            to_stack.append(crate)

    @property
    def silver_solution(self) -> str:
        return "".join([stack[-1] for stack in self._silver_stacks])

    @property
    def gold_solution(self) -> str:
        return "".join([stack[-1] for stack in self._gold_stacks])


def main():
    task = Tasks("input.txt")
    print(task.silver_solution)
    print(task.gold_solution)


if __name__ == "__main__":
    main()
