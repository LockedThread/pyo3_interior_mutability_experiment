from typing import List

class PyOtherStruct:
    """Python-visible wrapper with interior mutability."""
    
    def __init__(self, x: int) -> None: ...
    
    x: int  # Attribute access in Python
    
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    
class PyMyStruct:
    """A container of PyOtherStruct wrappers."""
    items_py: List[PyOtherStruct]  # Returns the same wrapper instances each time

    def __init__(self, wrappers: List[PyOtherStruct]) -> None: ...
    
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...