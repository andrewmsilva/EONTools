# EONTools, a tool library for Elastic Optical Networks
## Installing dependencies
```
pip3 install pandas
pip3 install matplotlib
pip3 install networkx
pip3 install haversine
```
## Creating network
### Manually
```python
from EONTools import EON

eon = EON()

#              ID       Lat     Lon     Type
eon.addNode('Paris', 48.8566, 2.3522, 'EOCC')
eon.addNode('Lyon', 45.7484, 4.8467, 'EOCC')

#            Source  Target  Length Capacity Cost
eon.addLink('Paris', 'Lyon', 393, 100, 329.90)
# Or auto-calculate length by itself
eon.addLink('Paris', 'Lyon', None, 100, 329.90)
```
### Reading csv
```python
from EONTools import EON, Report, Figure, Simulation

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EON()
eon.loadCSV(nodes_csv, links_csv)
```

## Getting reports
```python
Report.show(eon)
Report.save(eon)
# Or
report = Report.full(eon)
Report.show(eon, report)
Report.save(eon, report, 'results/')
```
### Results
```python
network report

degree : [('PortoAlegre', 2), ('Florianopolis', 2), ('SaoPaulo', 3), ('RioDeJaneiro', 3), ('Salvador', 2), ('Curitiba', 2), ('BeloHorizonte', 3), ('Brasilia', 3), ('Recife', 2), ('Fortaleza', 2)]
density : 0.26666666666666666
radius_by_leaps : 3
diameter_by_leaps : 5
center_by_leaps : ['SaoPaulo', 'RioDeJaneiro', 'BeloHorizonte', 'Brasilia']
periphery_by_leaps : ['Florianopolis', 'Recife']
eccentricity_by_leaps : {'PortoAlegre': 4, 'Florianopolis': 5, 'SaoPaulo': 3, 'RioDeJaneiro': 3, 'Salvador': 4, 'Curitiba': 4, 'BeloHorizonte': 3, 'Brasilia': 3, 'Recife': 5, 'Fortaleza': 4}
min_length : 239.290744722797
max_length : 1884.52283510062
radius_by_length : 2090.335242478452
diameter_by_length : 3489.524487669082
center_by_length : ['BeloHorizonte']
periphery_by_length : ['PortoAlegre', 'Fortaleza']
eccentricity_by_length : {'PortoAlegre': 3489.524487669082, 'Florianopolis': 3076.707818366016, 'SaoPaulo': 2540.529451176343, 'RioDeJaneiro': 2179.321857085925, 'Salvador': 2530.0510000154773, 'Curitiba': 2837.417073643219, 'BeloHorizonte': 2090.335242478452, 'Brasilia': 2702.349832434448, 'Recife': 3105.7388510763044, 'Fortaleza': 3489.524487669082}
min_capacity : 50
max_capacity : 50
radius_by_capacity : 150
diameter_by_capacity : 250
center_by_capacity : ['SaoPaulo', 'RioDeJaneiro', 'BeloHorizonte', 'Brasilia']
periphery_by_capacity : ['Florianopolis', 'Recife']
eccentricity_by_capacity : {'PortoAlegre': 200, 'Florianopolis': 250, 'SaoPaulo': 150, 'RioDeJaneiro': 150, 'Salvador': 200, 'Curitiba': 200, 'BeloHorizonte': 150, 'Brasilia': 150, 'Recife': 250, 'Fortaleza': 200}
min_cost : 1
max_cost : 1
radius_by_cost : 3
diameter_by_cost : 5
center_by_cost : ['SaoPaulo', 'RioDeJaneiro', 'BeloHorizonte', 'Brasilia']
periphery_by_cost : ['Florianopolis', 'Recife']
eccentricity_by_cost : {'PortoAlegre': 4, 'Florianopolis': 5, 'SaoPaulo': 3, 'RioDeJaneiro': 3, 'Salvador': 4, 'Curitiba': 4, 'BeloHorizonte': 3, 'Brasilia': 3, 'Recife': 5, 'Fortaleza': 4}
successes : 0
blocks : 0
blocks_by_modulation : 0
blocks_by_spectrum : 0
block_rate : None
success_rate : None
```
## Creating figures
```python
Figure.plot(eon)
# or
Figure.save(eon)
```
### Result:
![Network figure](/results/network.png)

# Simulating
```python
Simulation.simulateRandomDemands(eon, random_state=10)
# Demands is a list of dicts, each one with the data below
print(eon.demands[0])
# It's possible get some reports about the simulation
print(Report.fromDemands(eon))
```
## Result
```python
{'from': 'Recife', 'to': 'SaoPaulo', 'data_rate': 10, 'nodes_path': ['Recife', 'Salvador', 'RioDeJaneiro', 'SaoPaulo'], 'links_path': [('Salvador', 'Recife'), ('RioDeJaneiro', 'Salvador'), ('SaoPaulo', 'RioDeJaneiro')], 'path_length': 2156.743814583565, 'modulation_format': {'name': 'BPSK', 'data_rate': 12.5, 'power_consumption': 112, 'reach': 4000, 'spectral_efficiency': 1}, 'frequency_slots': 1, 'spectrum_path': [0], 'status': True}
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}
```

# Getting all possible networks with new links
```python
#                                                                Capacity Cost
possible_eons = Simulation.get_all_possible_eons_with_new_links_by_length(eon, 50, 1, n_links=1, max_length=reports['diameter_by_length'] / 2)
```

## Simulating them
```python
possible_eons = Simulation.get_all_possible_eons_with_new_links_by_length(eon, 50, 1, n_links=1, max_length=report['diameter_by_length'] / 2)
for i in range(len(possible_eons)):
    print('\nGraph %d simulation'%i)
    Simulation.simulateRandomDemands(possible_eons[i], random_state=10)
    print(Report.fromDemands(possible_eons[i])
```
### Results
```python
Graph 0 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 1 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 2 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 3 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 4 simulation
{'successes': 30, 'blocks': 15, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 15, 'block_rate': 0.3333333333333333, 'success_rate': 0.6666666666666666}

Graph 5 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 6 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

Graph 7 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 8 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 9 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

Graph 10 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 11 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 12 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

Graph 13 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 14 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 15 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 16 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 17 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

Graph 18 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

Graph 19 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}
```