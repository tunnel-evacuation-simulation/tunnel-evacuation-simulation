# tunnel-evacuation-simulation

This is a simulation of tunnel evacuation project for AGH class *Agent Systems*.

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

5. Run the project
```bash
python3 src/main.py
```


### Simulation parameters

For now, you can: 
- toggle the grid visibility by setting the `SHOW_GRID` variable in `src/settings.py` file.
- change number of agents by setting the `NUM_OF_AGENTS` variable in `src/settings.py` file
- change the grid layout by changing the `TILE_SIZE` variable in `src/settings.py` file

Also, for now, the agents move randomly.

