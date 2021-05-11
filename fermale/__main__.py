import os

import click
import numpy as np
from openfermion import FermionOperator as FermionOperator_, jordan_wigner, eigenspectrum, bravyi_kitaev, reverse_jordan_wigner, fermi_hubbard, get_sparse_operator, get_ground_state
from openfermion import count_qubits, commutator, hermitian_conjugated

from fermale.FermionOperator import FermionOperator, QubitOperator
from fermale.plots import draw_plot
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


@main.command()
@click.option('-x', '--abscissa', type=int, default=2)
@click.option('-y', '--ordinate', type=int, default=2)
@click.option('-t', '--tunneling', type=float, default=2.)
@click.option('-c', '--coulomb', type=float, default=1.)
@click.option('-m', '--magnetic-field', type=float, default=0.5)
@click.option('-p', '--chemical-potential', type=float, default=0.25)
@click.option('-l', '--periodic', is_flag=True)
@click.option('-s', '--spinless', is_flag=True)
@click.option('-m', '--symmetry', is_flag=True)
def test_hubbard_model(abscissa: int, ordinate: int, tunneling: float, coulomb: float, magnetic_field: float, chemical_potential: float, periodic: bool, spinless: bool, symmetry: bool):
    hubbard_operator = fermi_hubbard(
        x_dimension=abscissa,
        y_dimension=ordinate,
        tunneling=tunneling,
        coulomb=coulomb,
        chemical_potential=chemical_potential,
        magnetic_field=magnetic_field,
        periodic=periodic,
        spinless=spinless,
        particle_hole_symmetry=symmetry
    )
    # print(hubbard_operator)
    jw_hamiltonian = jordan_wigner(hubbard_operator)
    print('Jordan-Wigner hamiltonian without compression: ')
    print(jw_hamiltonian)
    print()
    jw_hamiltonian.compress()
    print('Jordan-Wigner hamiltonian with compression: ')
    print(jw_hamiltonian)
    print()
    sparse_operator = get_sparse_operator(hubbard_operator)
    print('Sparse operator')
    print(sparse_operator)
    print()
    print(f'Energy of the model is {get_ground_state(sparse_operator)[0]} in units of T and J')

    # xs = range(1, 9)
    # energy_levels = [
    #     get_ground_state(
    #         get_sparse_operator(
    #             fermi_hubbard(
    #                 x_dimension=x,
    #                 y_dimension=ordinate,
    #                 tunneling=tunneling,
    #                 coulomb=coulomb,
    #                 chemical_potential=chemical_potential,
    #                 magnetic_field=magnetic_field,
    #                 periodic=periodic,
    #                 spinless=spinless,
    #                 particle_hole_symmetry=symmetry
    #             )
    #         )
    #     )[0]
    #     for x in xs
    # ]
    #
    # os.makedirs('assets/hubbard', exist_ok=True)
    #
    # draw_plot(
    #     xs, energy_levels,
    #     x_label='X coordinate',
    #     y_label='Ground state energy in units of T and J',
    #     title='Ground state energy of the Hubbard model',
    #     path='assets/hubbard/x.jpeg'
    # )
    #
    # energy_levels = [
    #     get_ground_state(
    #         get_sparse_operator(
    #             fermi_hubbard(
    #                 x_dimension=abscissa,
    #                 y_dimension=x,
    #                 tunneling=tunneling,
    #                 coulomb=coulomb,
    #                 chemical_potential=chemical_potential,
    #                 magnetic_field=magnetic_field,
    #                 periodic=periodic,
    #                 spinless=spinless,
    #                 particle_hole_symmetry=symmetry
    #             )
    #         )
    #     )[0]
    #     for x in xs
    # ]
    # draw_plot(
    #     xs, energy_levels,
    #     x_label='Y coordinate',
    #     y_label='Ground state energy in units of T and J',
    #     title='Ground state energy of the Hubbard model',
    #     path='assets/hubbard/y.jpeg'
    # )

    ts = np.arange(0, 4, 0.2)
    energy_levels = [
        get_ground_state(
            get_sparse_operator(
                fermi_hubbard(
                    x_dimension=abscissa,
                    y_dimension=ordinate,
                    tunneling=t,
                    coulomb=coulomb,
                    chemical_potential=chemical_potential,
                    magnetic_field=magnetic_field,
                    periodic=periodic,
                    spinless=spinless,
                    particle_hole_symmetry=symmetry
                )
            )
        )[0]
        for t in ts
    ]
    draw_plot(
        ts, energy_levels,
        x_label='Tunneling coefficient',
        y_label='Ground state energy in units of T and J',
        title='Ground state energy of the Hubbard model',
        path='assets/hubbard/t.jpeg'
    )


if __name__ == '__main__':
    main()
