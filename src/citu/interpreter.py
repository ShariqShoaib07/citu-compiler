"""TAC interpreter scaffold for doc/design.md sections 3.4 and 4.5."""

from .tac import TAC


class TACInterpreter:
    """Execute a TAC program in the selected backend, a TAC interpreter."""

    def run(self, program: list[TAC]) -> None:
        """Input: TAC instructions. Output: program output on stdout; implements sections 3.4 and 4.5."""
        raise NotImplementedError("TODO")
