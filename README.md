# Elastic Optical Networks
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
import EONS

eon = EONS.EON()

#              ID       Lat     Lon     Type
eon.add_node('Paris', 48.8566, 2.3522, 'EOCC')
eon.add_node('Lyon', 45.7484, 4.8467, 'EOCC')

#            Source  Target  Length Capacity Cost
eon.add_link('Paris', 'Lyon', 465.6, 100, 329.90)
```
### Reading csv
```python
import EONS

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EONS.EON()
eon.load_csv(nodes_csv, links_csv)
```

## Getting reports
```python
eon.print_reports()
eon.save_reports()
# or
reports = eon.reports()
eon.print_reports(reports)
eon.save_reports(reports)
```

## Creating figures
```python
eon.show_figure()
# or
eon.save_figure()
```
### Result:
![Network figure](/results/network.png)
