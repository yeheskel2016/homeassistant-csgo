import json
import logging

from homeassistant.core import HomeAssistant   # <— new, replaces HomeAssistantType

_LOGGER = logging.getLogger(__name__)


class GameState:
    EVENT_ROUND_FREEZE = "csgo_round_freeze"
    EVENT_ROUND_STARTED = "csgo_round_started"
    EVENT_ROUND_ENDED = "csgo_round_ended"
    
    EVENT_ROUND_WIN_T = "csgo_round_win_t"
    EVENT_ROUND_WIN_CT = "csgo_round_win_ct"

    EVENT_BOMB_PLANTED = "csgo_bomb_planted"
    EVENT_BOMB_DEFUSED = "csgo_bomb_defused"
    EVENT_BOMB_EXPLODED = "csgo_bomb_exploded"

    EVENT_HEALTH_LOW = "csgo_health_low"
    EVENT_HEALTH_CRITICAL = "csgo_health_critical"

    EVENT_GAME_STOPPED = "csgo_game_stopped"

    EVENT_PLAYER_FLASHED = "csgo_player_flashed"

    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self._round_state = None
        self._bomb_state = None
        self._health_state = None
        self._flashed_state = None

    def load(self, data: str):
        obj = json.loads(data)
        self._round_state = obj["round_state"]
        self._bomb_state = obj["bomb_state"]
        self._health_state = obj["health_state"]
        self._flashed_state = obj["flashed_state"]

    def dump(self) -> str:
        return json.dumps({
            "round_state":   self._round_state,
            "bomb_state":    self._bomb_state,
            "health_state":  self._health_state,
            "flashed_state": self._flashed_state,
        })

    def update(self, data: dict):
        if "round" in data:
            if "phase" in data["round"] or "win_team" in data["round"]:
                self._check_round_state(value=data["round"])
            if "bomb" in data["round"]:
                self._check_bomb_state(value=data["round"]["bomb"])
        if "player" in data:
            self._check_health_state(value=data["player"]["state"]["health"])
            self._check_player_flashed(value=data["player"]["state"]["flashed"])
        else:
            self._reset()

    def _reset(self):
        if self._round_state or self._bomb_state:
            self._round_state = None
            self._bomb_state = None
            self._health_state = None
            self._flashed_state = None
            self._fire_event(event=self.EVENT_GAME_STOPPED)

    def _check_round_state(self, value: dict):
        # state hasn't changed
        if self._round_state == value:
            return

        # round status has changed so the bomb should reset
        self._bomb_state = None

        # check for phase data 
        if "phase" in value:
            if value["phase"] == "live":
                self._fire_event(event=self.EVENT_ROUND_STARTED)
            elif value["phase"] == "freezetime":
                self._fire_event(event=self.EVENT_ROUND_FREEZE)
            elif value["phase"] == "over":
                self._fire_event(event=self.EVENT_ROUND_ENDED)
        
        # check for winning team data
        if "win_team" in value:
            if value["win_team"] == "CT":
                self._fire_event(event=self.EVENT_ROUND_WIN_CT)
            elif value["win_team"] == "T":
                self._fire_event(event=self.EVENT_ROUND_WIN_T)

        # remember current state
        self._round_state = value
    
    def _check_health_state(self, value: int):
        # state hasn't changed
        if self._health_state == value:
            return

        # report new state
        if value <= 30 and value > 10:
            self._fire_event(event=self.EVENT_HEALTH_LOW)
        elif value <= 10:
            self._fire_event(event=self.EVENT_HEALTH_CRITICAL)

        # remember current state
        self._health_state = value

    def _check_player_flashed(self, value: int):
        # state hasen't changed
        if self._flashed_state == value:
            return

        # report new state
        if value > 0:
            # Add flashed_value to report in event
            data = {
                "flash_value": value
            }
            self._fire_event(event=self.EVENT_PLAYER_FLASHED, data=data)

        # remember current state
        self._flashed_state = value

    def _check_bomb_state(self, value: str):
        # state hasn't changed
        if self._bomb_state == value:
            return

        # report new state
        if value == "planted":
            self._fire_event(event=self.EVENT_BOMB_PLANTED)
        elif value == "defused":
            self._fire_event(event=self.EVENT_BOMB_DEFUSED)
        elif value == "exploded":
            self._fire_event(event=self.EVENT_BOMB_EXPLODED)

        # remember current state
        self._bomb_state = value

    def _fire_event(self, event: str, data: dict = None):
        _LOGGER.debug(f"csgo fired event: {event}")
        self._hass.bus.async_fire(event, data)
