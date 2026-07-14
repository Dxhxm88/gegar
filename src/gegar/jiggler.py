"""Mouse jiggling logic for gegar."""

import math
import random
import time

from pynput.mouse import Controller


class Jiggler:
    """Handles mouse movement patterns."""

    def __init__(self, distance: int = 5, pattern: str = "circle"):
        self.mouse = Controller()
        self.distance = distance
        self.pattern = pattern
        self._step = 0

    def jiggle(self) -> None:
        """Perform one jiggle movement based on the configured pattern."""
        if self.pattern == "circle":
            self._move_circle()
        elif self.pattern == "random":
            self._move_random()
        elif self.pattern == "square":
            self._move_square()
        else:
            self._move_circle()

    def _move_circle(self) -> None:
        """Move in a small circle (returns to original position)."""
        steps = 8
        angle_step = 2 * math.pi / steps
        for i in range(steps):
            angle = i * angle_step
            dx = int(self.distance * math.cos(angle))
            dy = int(self.distance * math.sin(angle))
            self.mouse.move(dx, dy)
            time.sleep(0.02)
        # Return to approximate original position
        self.mouse.move(0, 0)

    def _move_random(self) -> None:
        """Move to a random offset and back."""
        dx = random.randint(-self.distance, self.distance)
        dy = random.randint(-self.distance, self.distance)
        self.mouse.move(dx, dy)
        time.sleep(0.05)
        self.mouse.move(-dx, -dy)

    def _move_square(self) -> None:
        """Move in a square pattern (returns to original position)."""
        d = self.distance
        movements = [(d, 0), (0, d), (-d, 0), (0, -d)]
        for dx, dy in movements:
            self.mouse.move(dx, dy)
            time.sleep(0.03)


def run_jiggler(interval: int, distance: int, pattern: str, duration: int, stop_event) -> None:
    """
    Main jiggler loop.

    Args:
        interval: Seconds between jiggles.
        distance: Pixels to move.
        pattern: Movement pattern name.
        duration: Total seconds to run (0 = forever).
        stop_event: threading.Event to signal stop.
    """
    jiggler = Jiggler(distance=distance, pattern=pattern)
    start_time = time.time()

    while not stop_event.is_set():
        if duration > 0 and (time.time() - start_time) >= duration:
            break

        jiggler.jiggle()

        # Wait in small increments so we can respond to stop_event quickly
        for _ in range(interval * 10):
            if stop_event.is_set():
                return
            time.sleep(0.1)
