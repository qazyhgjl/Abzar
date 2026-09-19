# Offline Human Motion Simulator

A fully offline Python 3.9 desktop application for procedural human skeletal motion and Persian command control. The model is generated procedurally, so no model downloads, cloud APIs, CUDA, CDN, or telemetry are required.

## Run on Windows

```bat
py -3.9 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --no-index --find-links=vendor -r requirements.txt
python main.py
```

For an online setup once, replace the install command with `python -m pip install -r requirements.txt`; afterwards the application itself is offline. To create a wheelhouse for an air-gapped machine, run `pip download -r requirements.txt -d vendor` on a connected machine and copy `vendor/`.

## Features

- Procedural hierarchical humanoid skeleton with joint limits and forward kinematics.
- OpenGL viewport with orbit, zoom, grid, skeleton/body/x-ray/debug display modes.
- Offline Persian normalization, synonyms, Persian/English numbers, durations, repetitions, and chained commands.
- Smooth keyframe animation library: idle, walk, run, sit, lying, squat, push-up, sit-up, jump, stretch, arm raise, leg raise, turning and standing.
- Sequence queue with pause/resume/cancel, speed control, status and FPS.
- Manual joint controls for debugging.
- Automated parser, skeleton and animation tests.

## Tests

```bat
python -m unittest discover -s tests -v
```

## Limitations

This is an engineering simulator, not a medical model. Geometry is generated from primitives rather than a scanned anatomical mesh; muscle display is a stylized soft-tissue layer. Motion presets are kinematic and do not claim physiological accuracy. Add richer meshes under `assets/` only if licensing and offline distribution are acceptable.

## Adding a motion

Add a builder in `animation/motion_library.py` returning `MotionClip`, use joint names from `skeleton/skeleton.py`, and register its Persian aliases in `command/vocabulary.py`. Keep keyframes normalized to seconds and radians; the controller interpolates them smoothly.
