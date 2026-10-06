# Starship

Starship is a small command-line space exploration game. Assemble a crew,
scan planets, manage fuel, and keep the ship operational through a short
mission.

## Requirements

- Python 3.9 or newer
- A deployment-specific authentication provider implementing the `starship.auth` entry-point group

Authentication providers are installed separately by each deployment. Set
`STARSHIP_API_KEY` (and, when required, `STARSHIP_CLIENT_ID`) before starting
the application. A provider may validate the configured credential with its
service before enabling the application.

## Running the game

```bash
git clone https://github.com/toomanyandrew12/starship-demo.git
cd starship-demo
python app.py
```

The game prints a status report as the ship visits each planet on its route.

## License

MIT
