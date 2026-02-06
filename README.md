# Phoenix

**Version: Pre-Alpha**

Phoenix is an open-world action RPG inspired by the classic top-down style of GTA 2. Built with Python and Raylib, it features a dynamic city environment, vehicle systems, character switching, and a metro transit system.

## 🎮 Features

-   **Open World**: Explore a city with diverse locations.
-   **Character Switching**: Instantly switch between multiple characters (`1`, `2`, `3`).
-   **Vehicle System**: Drive cars, enter/exit vehicles.
-   **Metro System**: Fast travel between city districts using the metro.
-   **Save/Load System**: Persistence for player positions and states.
-   **Debug Console**: Built-in cheat console for testing and fun.

## 🕹️ Controls

| Action | Key(s) |
| :--- | :--- |
| **Movement** | `W`, `A`, `S`, `D` |
| **Enter/Exit Vehicle** | `E` |
| **Switch Character** | `1`, `2`, `3` |
| **Use Metro** | `M` (when near a station) |
| **Pause Menu** | `ESC` |
| **Cheat Console** | `~` (Grave / Tilde) |
| **Console Submit** | `Enter` |

## �️ Cheat Codes

Access the console by pressing `~` (Grave/Tilde).

| Command | Description | Example |
| :--- | :--- | :--- |
| `KIG_ME_OUT x y z` | Teleport to coordinates | `KIG_ME_OUT 0 5 0` |
| `GIVE_CAR` | Spawn a vehicle near you | `GIVE_CAR` |
| `GOD_MODE` | Toggle invincibility | `GOD_MODE` |
| `HELP` | List available commands | `HELP` |

## �🚀 Installation & Usage

### Prerequisites

-   **OS**: Linux or Windows
-   **Python**: Version 3.10 or higher

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/klein-moretti67/redemption.git
    cd redemption
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Linux/Mac
    source .venv/bin/activate
    # Windows
    .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r phoenix/requirements.txt
    ```

### Running the Game

To start the game, run the main script from the project root:

```bash
python phoenix/main.py
```

## 🛠️ Developer Guide

### Project Structure

```
redemption/
├── phoenix/               # Main source code
│   ├── assets/            # Game assets (images, sounds, etc.)
│   ├── core/              # Core systems (Camera, SaveSystem)
│   ├── entities/          # Game entities (Character, Vehicle)
│   ├── ui/                # UI components (Console, PauseMenu)
│   ├── world/             # World generation and Scene management
│   ├── src/               # Source modules
│   ├── main.py            # Entry point
│   └── requirements.txt   # Python dependencies
├── .github/workflows/     # CI/CD configurations
├── test.c                 # C-level sanity check for Raylib
└── README.md              # Project documentation
```

### Build Process

The project uses **Nuitka** to compile the Python code into a standalone executable. This is handled automatically via GitHub Actions in `.github/workflows/engine.yml`.

To build locally (requires Nuitka):

```bash
pip install nuitka
python -m nuitka --onefile --include-data-dir=phoenix/assets=assets --output-dir=build phoenix/main.py
```

### CI/CD Pipeline

The project features a GitHub Actions pipeline that:
1.  Triggers on push to `main` or manual dispatch.
2.  Builds the game for **Linux** and **Windows**.
3.  Creates a GitHub Release with the compiled executables (`phoenix-linux` and `phoenix-windows.exe`).

### Debugging Notes

-   **God Mode**: Enable via the console (`~`) with command `toggle_god_mode` (implied, check `GameCommands`).
-   **Teleport**: Console command support for teleporting players.
-   **C Sanity Check**: `test.c` is provided to verify Raylib functionality on the host system if needed.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---
*Remade by klein-moretti67 with help from Antigravity*