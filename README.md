# tunnel-evacuation-simulation

This is a simulation of tunnel evacuation project for AGH class _Agent Systems_.

### How to run

1. Clone the project

```bash
git clone https://github.com/tunnel-evacuation-simulation/tunnel-evacuation-simulation.git

```

2. Go to project root

```bash
cd tunnel-evacuation-simulation
```

3. Create a venv

```bash
python3 -m venv ~/.virtualenvs/tunnel-evacuation-simulation
```

4. Activate virtual environment and install dependencies

```bash
source ~/.virtualenvs/tunnel-evacuation-simulation/bin/activate
pip install --upgrade pip
pip install requirements.txt
```

5. To check available commands use --h flag

```bash
python src/main.py --h
```

6. Run the project

```bash
python3 src/main.py -f src/simulations/example_02.json -o agents_positions.csv
```
