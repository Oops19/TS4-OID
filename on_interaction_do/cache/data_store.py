#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import time
from typing import Tuple, Union, Dict, List, Set

from on_interaction_do.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)


class DataStore(object, metaclass=Singleton):
    def __init__(self):
        self.sim_angle: Dict[Sim, Tuple[int, int, int]] = {}  # {sim: (target_angle, step, current_angle), ...}

        self.undo_commands: Dict[int, Tuple[float, str, str, int, float, Union[Sim, None]]] = {}  # {sim_id: command, ...}
        self.repeat_commands: Dict[int, Tuple[float, str, str, int, List[float], Union[Sim, None]]] = {}  # {sim_id: command, ...}

        self.interaction_ids: Dict[int, Set[int]] = {}

        self.repeat_commands_v2: Dict[int, Tuple[str, str, int, int, int, Union[Sim, None], float, List[float]]] = {}
        """
        {sim_id: (command, parameter, sim_id, target_sim_id, tuning_ref, sim: Sim, end_time: float, run_at: List[float]), ...}
        """

    def add_undo_command(self, command: str, parameter, sim_id: int, t_max: float, interaction_id: int = 0, post_delay: float = 0):
        log.debug(f"Store: {command} {parameter} {sim_id} while id:{interaction_id} runs for max {t_max}s with post_delay {post_delay}s.")
        if interaction_id > 0:
            sim = CommonSimUtils.get_sim_instance(sim_id)
        else:
            sim = None
        self.undo_commands.update({sim_id: (time.time() + t_max, command, parameter, interaction_id, post_delay, sim)})

    def add_repeat_command(self, command: str, parameter, sim_id: int, t_max: float, tuning_ref: int = 0, delay: float = 60):
        try:
            log.debug(f"Repeat: {command} {parameter} {sim_id} while ref:{tuning_ref} runs every {delay}s, for max {t_max}s.")
            if tuning_ref != 0:
                sim = CommonSimUtils.get_sim_instance(sim_id)
            else:
                sim = None
            _start_time = time.time()
            end_time = _start_time + t_max
            run_at: List[float] = []
            _i = 0
            while True:
                _next_time = _start_time + _i * delay
                if _next_time > end_time:
                    break
                run_at.append(_next_time)
                _i += 1
            self.repeat_commands.update({sim_id: (end_time, command, parameter, tuning_ref, run_at, sim)})
        except Exception as e:
            log.error(f"{e}")

    def store_interaction_ids(self, interaction_ids: Set[int]) -> int:
        i_id = len(self.interaction_ids) + 1
        self.interaction_ids.update({i_id: interaction_ids})
        return i_id

    def get_interaction_ids(self, tuning_ref: int) -> Set[int]:
        ii = self.interaction_ids
        return ii.get(tuning_ref, set())

    def add_repeat_command_v2(self, command: str, parameter, sim_id: int, target_sim_id: int, tuning_ref: int, t_max: float, t_delay: float):
        try:
            log.debug(f"Repeat: {command} {parameter} {sim_id} while ref:{tuning_ref} runs every {t_delay}s, for max {t_max}s.")
            if tuning_ref != 0:
                sim = CommonSimUtils.get_sim_instance(sim_id)
            else:
                sim = None
            _start_time = time.time()
            end_time = _start_time + t_max
            run_at: List[float] = []
            _i = 0
            while True:
                _next_time = _start_time + _i * t_delay
                if _next_time > end_time:
                    break
                run_at.append(_next_time)
                _i += 1
            self.repeat_commands_v2.update({sim_id: (command, parameter, sim_id, target_sim_id, tuning_ref, sim, end_time, run_at)})
        except Exception as e:
            log.error(f"{e}")


DataStore()
