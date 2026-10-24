import asyncio
import contextlib
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.plant import Plant

TICK_SECONDS = 0.5
STATIC_DIR = Path(__file__).parent / "static"

plant = Plant()
connected_clients: set[WebSocket] = set()

STAGE_READERS = {
    "raw_water": lambda: plant.raw_water.read(),
    "dosing": lambda: plant.dosing.read(),
    "filtration": lambda: plant.filtration.read(),
    "disinfection": lambda: plant.disinfection.read(),
    "distribution": lambda: plant.distribution.read(),
}

STAGE_SETTERS = {
    "raw_water": {
        "intake_pump_speed": lambda v: plant.raw_water.set_intake_pump_speed(v),
    },
    "dosing": {
        "pump_speed": lambda v: plant.dosing.set_pump_speed(v),
        "ph_setpoint": lambda v: plant.dosing.set_ph_setpoint(v),
        "pump_state": lambda v: plant.dosing.set_pump_state(bool(v)),
    },
    "disinfection": {
        "chlorine_dose": lambda v: plant.disinfection.set_chlorine_dose(v),
    },
}


class ActuateRequest(BaseModel):
    values: dict[str, float | bool]


async def broadcast_state() -> None:
    if not connected_clients:
        return
    state = plant.read_all()
    dead = []
    for ws in connected_clients:
        try:
            await ws.send_json(state)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connected_clients.discard(ws)


async def tick_loop() -> None:
    while True:
        plant.step(TICK_SECONDS)
        await broadcast_state()
        await asyncio.sleep(TICK_SECONDS)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(tick_loop())
    yield
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


app = FastAPI(title="plant-sim", lifespan=lifespan)


@app.get("/state")
def get_all_state() -> dict:
    return plant.read_all()


@app.get("/state/{stage}")
def get_stage_state(stage: str) -> dict:
    if stage not in STAGE_READERS:
        raise HTTPException(status_code=404, detail=f"unknown stage '{stage}'")
    return STAGE_READERS[stage]()


@app.post("/actuate/{stage}")
def actuate_stage(stage: str, request: ActuateRequest) -> dict:
    if stage not in STAGE_SETTERS:
        raise HTTPException(status_code=404, detail=f"unknown or non-actuable stage '{stage}'")

    setters = STAGE_SETTERS[stage]
    for key, value in request.values.items():
        if key not in setters:
            raise HTTPException(
                status_code=400,
                detail=f"'{key}' is not an actuator on stage '{stage}'",
            )
        setters[key](value)

    return STAGE_READERS[stage]()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        await websocket.send_json(plant.read_all())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        connected_clients.discard(websocket)


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
