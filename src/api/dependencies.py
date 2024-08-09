from typing import Annotated

from fastapi import Depends

from src.utils.transaction import (
    BaseManager,
    TransactionManager,
)

TransactionDep = Annotated[BaseManager, Depends(TransactionManager)]
