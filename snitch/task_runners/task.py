from __future__ import annotations
from enum import Enum
from collections import deque
from typing import Callable, Tuple, Awaitable, Any
from dataclasses import dataclass


class TaskType(Enum):
    HEALTH_CHECK = 'hc'
    IDEMPOTENCY_CHECK = 'id'


class TaskQueue:
    def __init__(self) -> None:
        self.__queue = deque([])

    def add_task(self, task: Task) -> None:
        self.__queue.append(task)

    def pop_task(self) -> Task:
        return self.__queue.popleft()

    def __len__(self) -> int:
        return len(self.__queue)


@dataclass
class Task:
    task: Callable[[Tuple], Awaitable[Any]]
    args: Tuple
