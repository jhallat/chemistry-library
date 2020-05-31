import unittest
from decimal import Decimal

from formula.parser import parse_formula, FormulaRoot, FormulaNode, FormulaNodeType, parse_ion_equation
from periodictable import Ion
from scinotation import Count


def test_parse_formula_HCl():
    actual = parse_formula('HCl')
    #expected = [(Decimal('1.000'), 'H'), (Decimal('1.000'), 'Cl')]
    expected = FormulaRoot('HCl', [])
    expected.children.append(FormulaNode(Count(1), 'HCl', FormulaNodeType.COMPOUND, [
        FormulaNode(Count(1), 'H', FormulaNodeType.ATOM, []),
        FormulaNode(Count(1), 'Cl', FormulaNodeType.ATOM, [])
        ]))

    assert actual == expected

def test_parse_formula_Fe2O3_combined_with_H2O():
    actual = parse_formula('Fe2O3*[3/2]H2O')
    expected = FormulaRoot('Fe2O3*[3/2]H2O', [])
    expected.children.append(FormulaNode(Count(1), 'Fe2O3', FormulaNodeType.COMPOUND, [
            FormulaNode(Count(2), 'Fe', FormulaNodeType.ATOM, []),
            FormulaNode(Count(3), 'O', FormulaNodeType.ATOM, [])]))
    expected.children.append(FormulaNode(Count('1.5'), 'H2O', FormulaNodeType.COMPOUND, [
            FormulaNode(Count(2), 'H', FormulaNodeType.ATOM, []),
            FormulaNode(Count(1), 'O', FormulaNodeType.ATOM, [])]))

    assert actual == expected

def test_flatten_formula_Fe2O3_combined_with_H2O():
    actual = parse_formula('Fe2O3*[3/2]H2O').flatten()
    expected = [(Count(2), 'Fe'), (Count('9/2'), 'O'), (Count(3), 'H')]
    assert actual == expected

def test_parse_formula_BaOH2():
    actual = parse_formula('Ba(OH)2')
    expected = FormulaRoot('Ba(OH)2', [])
    expected.children.append(FormulaNode(Count(1), 'Ba(OH)2', FormulaNodeType.COMPOUND, [
        FormulaNode(Count(1), 'Ba', FormulaNodeType.ATOM, []),
        FormulaNode(Count(2), 'OH', FormulaNodeType.POLYATOMIC_ION, [
            FormulaNode(Count(1), 'O', FormulaNodeType.ATOM, []),
            FormulaNode(Count(1), 'H', FormulaNodeType.ATOM, [])
        ])
    ]))
    assert actual == expected

def test_parse_equation_Li_and_O():
    actual = parse_ion_equation('Li + O')
    expected = [Ion('Li', 1), Ion('O', -2)]
    assert actual == expected