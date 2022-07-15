# Pychemkit

---

### A simple python package for general chemistry calculations and modeling

---

## Foundations

### Elements

```python
from pychemkit.foundations.element import Element

hydrogen = Element('H')
print(hydrogen.atomic_mass) # 1.001
print(hydrogen.electrons) # 1
```

### Compounds

```python
from pychemkit.foundations.compound import Compound

acetic_acid = Compound('CH3COOH')
print(acetic_acid.composition) # {Element('C'): 2, Element('H'): 4, Element('O'): 2}
print(acetic_acid.get_element_percentage('C')) # 20.000
```

### Basic stoichiometric calculations

```python
from pychemkit.foundations.compound import Compound

#Initialize
glucose = Compound('C6H12O6')

# Calculate moles of glucose given the mass in grams
grams_glucose = 200.0
moles_glucose = glucose.mass_to_moles(grams_glucose)
print(moles_glucose) # 1.1101489819933834

# Calculate the number of mass in grams of glucose given the number of moles
moles_glucose = 2.5
grams_glucose = glucose.moles_to_mass(moles_glucose)
print(grams_glucose) # 450.39
```

### Calculating Empirical and Molecular Formulas

```python
from pychemkit.stoich.experimental import EmpiricalFormula, MolecularFormula

elems = 'CHONNa'
percentages = [35.51, 4.77, 37.85, 8.29, 13.60]
msg = MolecularFormula(elements=elems, percentages=percentages, mass=169)
print(msg.em_formula)
```

### Balancing Chemical Equation

```python
from pychemkit.stoich.reaction import SimpleChemicalReaction

water_formation = SimpleChemicalReaction(
    reactants=['H2', 'O2'],
    products=['H2O']
)

print(water_formation.balance()) # [1, 2, 2]
```

---

## Installation

### Mac/Linux

```commandline
$ mkdir dirname
$ cd dirname
$ python3 -m venv env
$ source env/bin/activate
$ git clone https://github.com/glaciapag/pychemkit.git .
$ pip install -e .
```

### Windows

```powershell
$ mkdir dirname
$ cd dirname
$ python -m venv env
$ env\Scripts\activate.bat
$ git clone https://github.com/glaciapag/pychemkit.git .
$ pip install -e .
```

## Testing

```commandline
$ cd test
$ python -m unittest
```
