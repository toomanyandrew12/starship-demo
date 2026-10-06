"""A small command-line starship exploration game."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from importlib.metadata import entry_points
import random


@dataclass(frozen=True)
class AuthConfig:
    """Authentication configuration returned by a provider plugin."""

    token: str
    enabled: bool = True


def load_auth_config() -> AuthConfig:
    """Load the first installed mission-control authentication provider."""
    providers = list(entry_points(group="starship.auth"))
    if not providers:
        raise RuntimeError("AuthConfig not found.")

    values = providers[0].load()(application="starship")
    if not isinstance(values, Mapping):
        raise RuntimeError("AuthConfig not found.")

    token = values.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("AuthConfig not found.")
    return AuthConfig(token=token, enabled=bool(values.get("enabled", True)))


class ShipStatus(Enum):
    DOCKED = "docked"
    IN_TRANSIT = "in_transit"
    IN_ORBIT = "in_orbit"


@dataclass
class CrewMember:
    name: str
    role: str
    health: int = 100


@dataclass
class Planet:
    name: str
    distance: float
    resources: list[str] = field(default_factory=list)


@dataclass
class Starship:
    name: str
    fuel: float = 1000.0
    status: ShipStatus = ShipStatus.DOCKED
    location: str = "Earth Spacedock"
    crew: list[CrewMember] = field(default_factory=list)
    cargo: dict[str, int] = field(default_factory=dict)

    def travel_to(self, planet: Planet) -> bool:
        fuel_cost = planet.distance * 20
        if fuel_cost > self.fuel:
            print(f"Insufficient fuel for {planet.name}.")
            return False

        self.status = ShipStatus.IN_TRANSIT
        self.fuel -= fuel_cost
        print(f"Travelling to {planet.name}...")

        if planet.resources:
            resource = random.choice(planet.resources)
            self.cargo[resource] = self.cargo.get(resource, 0) + 1
            print(f"Collected: {resource}")

        self.location = planet.name
        self.status = ShipStatus.IN_ORBIT
        return True

    def status_report(self) -> str:
        return (
            f"=== {self.name} Status Report ===\n"
            f"Location: {self.location}\n"
            f"Status: {self.status.value}\n"
            f"Fuel: {self.fuel:.1f}\n"
            f"Crew: {len(self.crew)}\n"
            f"Cargo: {self.cargo}"
        )


ROUTE = [
    Planet("Mars", 0.0001, ["iron", "ice"]),
    Planet("Proxima b", 4.24, ["minerals"]),
    Planet("Gliese 667Cc", 23.6, ["water", "food"]),
]


def main() -> None:
    auth = load_auth_config()
    if not auth.enabled:
        raise RuntimeError("Mission-control authentication is disabled.")

    ship = Starship(
        name="USS Horizon",
        crew=[
            CrewMember("Captain Park", "captain"),
            CrewMember("Jax", "pilot"),
            CrewMember("Torres", "engineer"),
        ],
    )

    print(ship.status_report())
    for planet in ROUTE:
        if not ship.travel_to(planet):
            break
        print(ship.status_report())

    print(f"Mission complete. Final location: {ship.location}")


if __name__ == "__main__":
    main()
