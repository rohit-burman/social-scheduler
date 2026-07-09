from __future__ import annotations

import time


def main() -> None:
    print("worker started: waiting for jobs")
    while True:
        # Placeholder loop. Replace with Redis consumer implementation from docs.
        time.sleep(5)


if __name__ == "__main__":
    main()
