import time

from src.plant import Plant

TICK_SECONDS = 0.5
PRINT_EVERY_N_TICKS = 4


def main() -> None:
    plant = Plant()
    tick = 0

    print("plant-sim: running standalone tick loop (Ctrl+C to stop)")

    try:
        while True:
            plant.step(TICK_SECONDS)
            tick += 1

            if tick % PRINT_EVERY_N_TICKS == 0:
                print(plant.read_all())

            time.sleep(TICK_SECONDS)
    except KeyboardInterrupt:
        print("\nplant-sim: stopped")


if __name__ == "__main__":
    main()
