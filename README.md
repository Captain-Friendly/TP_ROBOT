[README.md](https://github.com/user-attachments/files/34607119/README.md)
# TP_ROBOT: Autonomous Robot

A two-wheeled robot, driven by a Raspberry Pi, that navigates to a series of waypoints on its own. It locates itself with radio positioning beacons, turns to the right heading using a gyroscope, stops for obstacles seen by a lidar, and watches for movement with a camera once it reaches each destination.

This was the final integrative project (PFI, "Le robot autonome") for a college robotics course. The code and comments are written in French.

## Features

- **Waypoint navigation**: turns toward a target point, then drives to it while tracking its position.
- **Positioning**: reads `POS,x,y` messages from a radio beacon system over a serial port.
- **Heading control**: integrates the IMU's gyroscope to turn the robot to a desired angle, recalibrating the gyro drift whenever the robot is not turning.
- **Obstacle detection**: scans with a YDLIDAR X4 and brakes when something is inside a rectangular zone in front of the robot.
- **Motion detection**: after each leg, uses the camera (frame differencing with OpenCV) to show moving objects in a live window.
- **Hardware abstraction**: motors and the IMU have fake counterparts (`FauxMoteur`, `FauxModuleInertiel`) so the logic can be tested without a robot.

## Hardware

| Component | Used for | Connection |
|---|---|---|
| Raspberry Pi | Runs everything | n/a |
| 2 DC motors with an H-bridge driver | Drive and steering (differential drive) | GPIO: left motor `in1=6, in2=5, en=13`; right motor `in1=15, in2=14, en=18` (`en` is PWM) |
| ICM-20948 IMU | Gyroscope for heading | I²C |
| Radio positioning beacons | Position (x, y) | Serial `/dev/ttyACM0`, 115200 baud |
| YDLIDAR X4 | Obstacle detection | Serial `/dev/ttyUSB0` (via `PyLidar3`) |
| USB camera | Motion detection | `/dev/video0` |

Device paths and GPIO pins are hard-coded; see [Configuration](#configuration) if your wiring differs.

## Requirements

- Python 3 on Linux (the code targets a Raspberry Pi)
- Python packages:

```bash
pip install pyserial gpiozero icm20948 PyLidar3 opencv-python numpy
```

Depending on your setup, `gpiozero` may also need a pin factory such as `lgpio` or `RPi.GPIO`, and I²C must be enabled on the Pi.

## Usage

1. Power the beacons and place the robot in the area they cover.
2. Make sure the lidar, positioning receiver and camera are plugged in at the paths listed above.
3. Run:

```bash
python main.py
```

What happens:

1. The robot waits for its first GPS fix and records it as the starting point.
2. It builds a route relative to that point. `main.py` currently uses an **L-shaped route** on a 2 × 2 grid (assuming the beacons report metres): `(0,2) → (2,2) → (0,2) → (0,0)`.
3. For each destination, the robot turns toward it, drives there, and stops. It then opens a camera window with motion detection. Press **x** in that window to continue to the next waypoint.
4. When the route is done, everything shuts down and the motors are set to neutral.

`main.py` also defines `obtenir_points_carre` (square) and `obtenir_points_X` (X pattern). To use one, change the function called in `main()`.

## How it works

```
main.py
  └── DirecteurIA              drives the robot to a destination
        ├── GPS                 serial thread → latest (x, y) Point
        ├── DirecteurRotation   turns the robot to a target angle
        │     └── Gyrometre     integrates gyro readings → current angle
        │           └── ModuleInertiel (ICM-20948)
        ├── Lidar               thread → objet_present flag
        └── Robot               high-level motion (avancer, tourner_g/d, freiner)
              └── Moteur ×2     H-bridge control via gpiozero
```

When asked to go to a destination, `DirecteurIA`:

1. Reads the current position and computes the bearing and distance to the target.
2. Asks `DirecteurRotation` to turn to that bearing (within a 5° tolerance).
3. Drives forward at reduced speed, checking position every 0.1 s. It brakes while the lidar reports an obstacle or no GPS fix is available, and stops about 0.25 m short of the target.
4. Gives up and shuts down if the GPS position stops changing for more than 5 consecutive readings.

Long-running parts (GPS, gyro, lidar, motion detection) run in their own threads and share a `JetonAnnulation`, a simple cancellation token that stops all of them when `terminer()` is called.

## Project structure

| File | Role |
|---|---|
| `main.py` | Entry point; builds the route and runs it |
| `DirecteurIA.py` | Navigation to a destination (turn, drive, obstacle and GPS checks) |
| `DirecteurRotation.py` | Turns the robot to a desired angle using the gyro |
| `Gyrometre.py` | Tracks heading from gyro readings, with drift calibration |
| `ModuleInertiel.py` | Wrapper around the ICM-20948, plus `FauxModuleInertiel` for tests |
| `GPS.py` | Reads positions from the beacon receiver over serial |
| `lidar.py` | Obstacle detection with the YDLIDAR X4 |
| `DetecteurMouvement.py` | Camera-based motion detection (OpenCV) |
| `Camera.py` | Thin wrapper around `cv2.VideoCapture` |
| `Robot.py` | Robot-level movement and speed control, with a state-change subscription |
| `Moteur.py` | Single motor control, plus `FauxMoteur` for tests |
| `EtatRobot.py`, `Mode.py` | Enums for robot state and motor mode |
| `Point.py` | 2D point with angle, distance and norm helpers |
| `Algos.py` | Utility functions (approximate equality, polar-to-Cartesian, rectangle test) |
| `CollectionCirculaire.py` | Fixed-size circular buffer |
| `JetonAnnulation.py` | Cancellation token for threads |

## Configuration

Values live as constants near the top of each file.

| Setting | Where | Default |
|---|---|---|
| Motor GPIO pins | `Robot.construire()` | see [Hardware](#hardware) |
| Default / max motor speed | `Robot.py` | 0.8 / 1.0 |
| Travel speed, distance tolerance | `DirecteurIA.py` | 0.4, 0.2 |
| Turn speed, angle tolerance | `DirecteurRotation.py` | 0.6, 5° |
| Gyro scale correction | `Gyrometre.CORRECTION_ANGLE` | 360 / 345 (found experimentally) |
| GPS serial port and baud rate | `GPS.py` | `/dev/ttyACM0`, 115200 |
| Lidar serial port | `lidar.py` | `/dev/ttyUSB0` |
| Lidar detection zone (mm) | `lidar.py` | x from −500 to −176.78, y ±176.78, angles 135°–225° |
| Camera device and size | `Camera.py` | `/dev/video0`, 320 × 240 |
| Motion sensitivity | `DetecteurMouvement.py` | threshold 70, minimum area 500 px |

## Testing

Several modules have a small self-check or demo that runs when the file is executed directly, for example:

```bash
python Point.py
python CollectionCirculaire.py
python Robot.py        # uses FauxMoteur, no hardware needed (see Known issues)
```

`GPS.py`, `lidar.py`, `Gyrometre.py`, `Camera.py` and `DetecteurMouvement.py` also have a `main()` for trying a single component on real hardware.

## Known issues

- `main.py` calls `lancer_detection_mouvement(jeton)`, but that method takes no argument, so the motion-detection step fails with a `TypeError` as written.
- `DirecteurIA.py` imports `from Lidar import Lidar`, but the file is named `lidar.py`. This works on case-insensitive filesystems (Windows, macOS) but fails on Linux, including a Raspberry Pi, unless the file is renamed to `Lidar.py` or the import is changed.
- Some of the standalone `main()` / `test()` helpers are out of date with the classes they call (for instance `Robot.py` still tests `tourner_avancer_g`, which was removed).

## Authors

Pascal Arès, Philippe C. Léger and Julian Angel Murillo, December 2022.
