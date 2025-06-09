from typing import List
from smolagents import Tool
from legacy.utils import ContextManager

from .create import CreateTool
from .edit import EditTool
from .find import FindTool
from .insert import InsertTool
from .open import OpenTool
from .run import RunTool
from .search import SearchTool
from .show import ShowTool


# Provide the function calls to EventHandler
def init_toolset(context_hander: ContextManager) -> List[Tool]:
    toolset = [
        CreateTool(context_hander),
        EditTool(context_hander),
        FindTool(context_hander),
        InsertTool(context_hander),
        OpenTool(context_hander),
        RunTool(context_hander),
        SearchTool(context_hander),
        ShowTool(context_hander),
    ]
    return toolset

