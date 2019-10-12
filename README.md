# EONTools, a tool library for Elastic Optical Networks

## Installing

### OMNet++

1. > \$ sudo apt-get update
2. > \$ sudo apt-get install build-essential gcc g++ bison flex perl \python python3 qt5-default libqt5opengl5-dev tcl-dev tk-dev \libxml2-dev zlib1g-dev default-jre doxygen graphviz libwebkitgtk-1.0 openscenegraph-plugin-osgearth libosgearth-dev openmpi-bin libopenmpi-dev libpcap-dev gnome-color-chooser nemiver
3. Download OMNet++ from [here](https://omnetpp.org/download/)
4. > \$ cd Downloads
5. > \$ tar xvfz omnetpp-5.5.1-src-linux.tgz
6. Move the folder somewhere you choose
7. > \$ cd omnetpp-5.5.1
8. > \$ . setenv
9. > \$ sudo gedit ~/.bashrc
10. Add the following line at the end of the file, then save it: `export PATH=$PATH:/home/YOUR_USER/FOLDER_YOU_CHOOSE/omnetpp-5.5.1/bin`
11. > \$ ./configure
12. > \$ make
13. > \$ omnetpp

### Python libraries

> \$ pip install pandas

> \$ pip install matplotlib

> \$ pip install networkx

> \$ pip install haversine

## Developing

### Creating network

#### Manually

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

#### Reading csv

```python
from EONTools import EON, Report, Figure, Simulation

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EON()
eon.loadCSV(nodes_csv, links_csv)
```

### Getting reports

```python
Report.show(eon)
Report.save(eon)
# Or
report = Report.full(eon)
Report.show(report)
Report.save(report, 'results/')
```

#### Results

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

### Creating figures

```python
Figure.plot(eon)
# or
Figure.save(eon)
```

#### Result:

![Network figure](/results/network.png)

### Simulating

```python
print('\nOriginal EON simulation')
eon.resetSpectrum()
demands = Simulation.createRandomDemands(eon, random_state=10)
demands = Simulation.simulateDemands(eon, demands)
print(Report.fromDemands(demands))
```

#### Result

```python
Original EON simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}
```

### Getting all possible networks with new links

```python
#                                                                Capacity Cost
possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, n_links=1, max_length=report['diameter_by_length'] / 2)
```

### Simulating them

```python
i = 0
for possible_eon in possible_eons:
    print('\nEON', i, 'simulation')
    i += 1
    possible_eon.resetSpectrum()
    demands = Simulation.createRandomDemands(possible_eon, random_state=10)
    demands = Simulation.simulateDemands(possible_eon, demands)
    print(Report.fromDemands(demands))
```

#### Results

```python
EON 0 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 1 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 2 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 3 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 4 simulation
{'successes': 30, 'blocks': 15, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 15, 'block_rate': 0.3333333333333333, 'success_rate': 0.6666666666666666}

EON 5 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 6 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

EON 7 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 8 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 9 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

EON 10 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 11 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 12 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

EON 13 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 14 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 15 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 16 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 17 simulation
{'successes': 29, 'blocks': 16, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 16, 'block_rate': 0.35555555555555557, 'success_rate': 0.6444444444444445}

EON 18 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}

EON 19 simulation
{'successes': 28, 'blocks': 17, 'blocks_by_modulation': 0, 'blocks_by_spectrum': 17, 'block_rate': 0.37777777777777777, 'success_rate': 0.6222222222222222}
```
