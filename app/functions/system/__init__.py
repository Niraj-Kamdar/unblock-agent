from .askQuestion import function as system_askQuestion
from .supportedFunctions import function as system_supportedFunctions
from .taskCompleted import function as system_taskCompleted

system = [
    system_askQuestion,
    system_supportedFunctions,
    system_taskCompleted,
]

__all__ = [
  "system"
]