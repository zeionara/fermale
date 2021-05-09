from abc import ABC

from openfermion import SymbolicOperator as SymbolicOperator_, FermionOperator as FermionOperator_, QubitOperator as QubitOperator_


class SymbolicOperator(SymbolicOperator_, ABC):
    def __str__(self):
        string_representation = super().__str__()
        return string_representation.replace('\n', ' ')

    @property
    def flattened_terms(self):
        terms = []
        for operator_set, _ in self.terms.items():
            terms.extend(operator_set)
        return terms


class FermionOperator(SymbolicOperator, FermionOperator_):
    pass


class QubitOperator(SymbolicOperator, QubitOperator_):
    pass
