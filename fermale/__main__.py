import click
from openfermion import FermionOperator as FermionOperator_, jordan_wigner, eigenspectrum, bravyi_kitaev, reverse_jordan_wigner
from openfermion import count_qubits, commutator, hermitian_conjugated

from fermale.FermionOperator import FermionOperator, QubitOperator
from fermale.utils import describe_result


@click.group()
def main():
    pass


@main.command()
@click.option('-c', '--coefficient', type=float, default=1.0)
def test_operators_initialization(coefficient: float):
    # 1. Let's create some basic operator

    operator = FermionOperator('2^ 1 3 7^', coefficient)
    alternative_operator = coefficient * FermionOperator(((2, 1), (1, 0), (3, 0), (6, 1)))

    sum_of_operators = operator + alternative_operator

    identity = FermionOperator('')
    zero = FermionOperator()

    # print(f'Fermion operator: {operator}; the terms are {list(operator.terms.keys())[0]}')
    print(f'Fermion operator: {operator}; the flattened terms are {operator.flattened_terms}')
    print(f'Alternative fermion operator: {alternative_operator}')
    print(f'Sum fermion operator: {sum_of_operators}; the terms are {sum_of_operators.terms}')
    # print(operator == alternative_operator)
    print(f'Identity operator: {identity}')
    print(f'Zero operator: {zero}')

    # 2. Checking operator combinations

    lhs_operator = FermionOperator('17^')
    rhs_operator = FermionOperator('19^')

    print(describe_result(lhs_operator, rhs_operator, lambda lhs, rhs: lhs * rhs, '*'))
    print(describe_result(lhs_operator, lhs_operator, lambda lhs, rhs: lhs * rhs, '*'))

    print(describe_result(lhs_operator, rhs_operator, lambda lhs, rhs: lhs + rhs, '+'))
    print(describe_result(lhs_operator, 5, lambda lhs, rhs: lhs ** rhs, '^'))

    # print(describe_result(lhs_operator * rhs_operator, lhs_operator, lambda lhs, rhs: lhs / rhs, '/')) # Throws an exception

    # 3. Use some auxiliary functions

    print(f'Operator {lhs_operator ** 5} occupies {count_qubits(lhs_operator)} qubits')
    print(f'Operator {rhs_operator ** 2} occupies {count_qubits(rhs_operator)} qubits')
    print(f'Operator {operator} occupies {count_qubits(operator)} qubits')

    print(f'Operator {operator} is {"not " if not operator.is_normal_ordered() else ""}normal ordered')
    print(f'Operator {(lhs_operator + rhs_operator)} is {"not " if not (lhs_operator + rhs_operator).is_normal_ordered() else ""}normal ordered')
    print(f'Operator {(lhs_operator * rhs_operator)} is {"not " if not (lhs_operator * rhs_operator).is_normal_ordered() else ""}normal ordered')
    print(f'Operator {(rhs_operator * lhs_operator)} is {"not " if not (rhs_operator * lhs_operator).is_normal_ordered() else ""}normal ordered')

    print(f'Commutator of {lhs_operator} and {rhs_operator} is {commutator(lhs_operator, rhs_operator)}')

    # 4. See qubit operators

    operator = QubitOperator('X1 Z3', coefficient) + QubitOperator('X20', coefficient - 1)
    print(f'Operator {operator} occupies {count_qubits(operator)} qubits')

    # 4. Perform transformations from fermion to qubit operators

    fermion_operator = FermionOperator_('5^', 0.1 + 0.2j)
    fermion_operator += hermitian_conjugated(fermion_operator)
    jw_operator = jordan_wigner(fermion_operator)
    bk_operator = bravyi_kitaev(fermion_operator)

    print()
    print('Source fermion operator:')
    print(fermion_operator)
    print()
    print('Source fermion operator with conjugate:')
    print(fermion_operator)
    print()
    print('Source fermion operator with conjugate passed through Jordan-Wigner transformation:')
    print(jw_operator)
    print()
    print('Eigenspectrum of the obtained operator:')
    print(eigenspectrum(jw_operator))
    print()
    print('Reversed:')
    print(reverse_jordan_wigner(jw_operator))
    print()
    print('Source fermion operator with conjugate passed through Bravyi-Kitaev transformation:')
    print(bk_operator)
    print()
    print('Eigenspectrum of the obtained operator:')
    print(eigenspectrum(bk_operator))
    print()


if __name__ == '__main__':
    main()
