# Pychemkit
---
### A python package for chemistry calculations (Work-in-progress)

## Elements

### Initialize an element instance
```python
from pychemkit.foundations.element import Element

hydrogen = Element('H')
print(hydrogen.atomic_mass) # 1.001
print(hydrogen.electrons) # 1
```


### Initialize compounds
```python
from pychemkit.foundations.compound import Compound

acetic_acid = Compound('CH3COOH')
print(acetic_acid.composition) # {Element('C'): 2, Element('H'): 4, Element('O'): 2}
print(acetic_acid.get_element_percentage('C')) # 20.000
```

### Some Basic stoichiometric calculations
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