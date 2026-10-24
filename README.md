# plant-sim

Physical process simulation for the AquaFlow Systems treatment plant. Models the 5
treatment stages as a continuous simulation loop, exposing current process values
and accepting actuator commands through an internal API.

## Stages

| Stage | Depth |
|---|---|
| Raw water intake | simplified — tank level, intake flow |
| Dosage chimique | detailed — pH and chemical dosing dynamics |
| Filtration | simplified — turbidity reduction as a function of flow |
| Désinfection | simplified — chlorine dose affects pathogen index, depends on upstream pH |
| Distribution | simplified — aggregates final water-quality indicators |

See `AquaFlow-Systems/plant-spec/register-map.md` for the values each stage exposes
to its PLC.

## Running standalone

```bash
pip install -r requirements.txt
python -m src.main
```

Serves the simulation loop plus a small live view at http://localhost:8000 — an SVG
diagram of the 5 stages updating over a WebSocket.

## Interface for plc-fleet

`plc-fleet` reads and writes simulated values through `src/api.py`'s internal HTTP
endpoints (`GET /state/<stage>`, `POST /actuate/<stage>`), one process per stage.

## Tests

```bash
pytest
```