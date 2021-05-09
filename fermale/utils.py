from typing import Union

from fermale.FermionOperator import FermionOperator


def describe_result(lhs: FermionOperator, rhs: Union[FermionOperator, float], action: callable, action_symbol: str):
    return f'{lhs} {action_symbol} {rhs} = {action(lhs, rhs)}'
