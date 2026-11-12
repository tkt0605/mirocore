import pytest

from mirocore.terminal_robot.normalized import (
    delete_memory,
    extract_delete_target,
    extract_query,
)
from mirocore.terminal_robot.reply import search_memory

# @pytetst.mark.parametrize(
#     ("utterance", "expected"),
#     [
#         ("犬")

#     ]
# )