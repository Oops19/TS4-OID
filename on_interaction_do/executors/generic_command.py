#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import random
import re
from typing import List

from objects.game_object import GameObject
from on_interaction_do.cache.data_store import DataStore
from on_interaction_do.cache.dc_cache import DcCache
from on_interaction_do.enums.generic_function import GenericFunction
from on_interaction_do.enums.oid_constants import OidConstants
from on_interaction_do.executors.dc_command import DcCommand
from on_interaction_do.executors.vanilla_command import VanillaCommand
from on_interaction_do.modinfo import ModInfo


from sims.sim_info import SimInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.opacity.opacity_manager import OpacityManager
from ts4lib.utils.simple_ui_notification import SimpleUINotification
from ts4lib.utils.singleton import Singleton
from ui.ui_dialog_notification import UiDialogNotification

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'GenericCommand')
log.enable()


class GenericCommand(metaclass=Singleton):

    def process(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        log.debug(f"GenericCommand.process({function}, {parameters}, {interaction_id}, {sim_info}, {target_sim_info})")

        if function == GenericFunction.F_REPEAT:
            return self._repeat(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function == GenericFunction.F_RANDOM:
            return self._random(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function == GenericFunction.F_ROTATE_ABS:
            return self._rotate_abs(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function == GenericFunction.F_ROTATE_RND:
            return self._rotate_rnd(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function == GenericFunction.F_ROTATE_END:
            return self._rotate_end(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function == GenericFunction.F_OPACITY:
            return self._opacity(function, parameters, interaction_id, sim_id, target_id, funcs_with_params)
        elif function[:2] == OidConstants.PREFIX_DC_OR_VANILLA:  # TODO remove this code ... moved to Executor
            if DcCache().failure:
                function = re.sub(r"^.", r"bg", function)
                return VanillaCommand().process(function, parameters, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
            else:
                function = re.sub(r"^.", r"dc", function)
                return DcCommand().process(function, parameters, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
        elif function == GenericFunction.F_DEBUG_INFO:
            SimpleUINotification().show('OID DEBUG', f'{function}({parameters}) interaction_id={interaction_id}, sim={sim_info}, participant={target_sim_info}, obj={target_object}')
        elif function == GenericFunction.F_DEBUG_ALERT:
            SimpleUINotification().show('OID DEBUG', f'{function}({parameters}) interaction_id={interaction_id}, sim={sim_info}, participant={target_sim_info}, obj={target_object}', UiDialogNotification.UiDialogNotificationUrgency.URGENT)
        else:
            log.debug(f"GC.process: Unknown function {function}")
        return True

    def _repeat(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_sim_id: int, funcs_with_params: str) -> bool:
        try:
            tuning_reference: int = 0
            t_max: float = GenericFunction.REPEAT_DEFAULT_VALUE_T_MAX
            t_delay: float = GenericFunction.REPEAT_DEFAULT_VALUE_T_DELAY
            if len(parameters) >= 1:
                tuning_reference = int(parameters[0])
                if len(parameters) >= 2:
                    t_max = int(parameters[1])
                    if len(parameters) >= 3:
                        t_delay = int(parameters[2])
        except:
            log.warn(f"Could not parse parameter ({function}({parameters})), using default values.")
            return False

        _, _, remaining = funcs_with_params.partition(GenericFunction.F_REPEAT)  # everything after '^...+repeat(123)+'
        _, _, remaining_funcs_with_params = funcs_with_params.partition(GenericFunction.JOIN)

        DataStore().add_repeat_command_v2(OidConstants.COMMAND, remaining_funcs_with_params, sim_id, target_sim_id, tuning_reference, t_max, t_delay)
        return True

    def _random(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_sim_id: int, funcs_with_params: str) -> bool:
        rnd_value = GenericFunction.RANDOM_DEFAULT_VALUE
        try:
            if parameters:
                rnd_value = int(parameters[0])
        except:
            log.warn(f"Could not parse parameter ({function}({parameters})), using default values.")
            return False

        i = random.randint(0, 100)
        if i > rnd_value:
            log.debug(f"Random ({i} > {rnd_value}) --> Skipping further functions")
            return False
        log.debug(f"Random ({i} <= {rnd_value}) --> Execute further functions")
        return True

    def _rotate_abs(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_sim_id: int, funcs_with_params: str) -> bool:
        try:
            angle = int(parameters[0])
            self._rotate_sim(angle, sim_id)
        except:
            pass
        return True

    def _rotate_rnd(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_sim_id: int, funcs_with_params: str) -> bool:
        try:
            angle = int(parameters[0])
            _rnd_angle = int(parameters[1])
            rnd_angle = random.randint(-_rnd_angle, _rnd_angle)
            angle += rnd_angle
            self._rotate_sim(angle, sim_id)
        except:
            pass
        return True

    def _rotate_sim(self, angle: int, sim_id: int):
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360
        log.debug(f"Rotating sim {angle}°")
        sim = CommonSimUtils.get_sim_instance(sim_id)
        step = 3 if angle < 180 else -3
        angle = int(angle / 3) * step
        DataStore().sim_angle.update({sim: (angle, step, 0)})

    def _rotate_end(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_sim_id: int, funcs_with_params: str) -> bool:
        try:
            sim = CommonSimUtils.get_sim_instance(sim_id)
            del DataStore().sim_angle[sim]
        except:
            pass
        return True

    def _opacity(self, function: str, parameters: List[str], interaction_id: int, sim_id: int, target_id: int, funcs_with_params: str) -> bool:
        try:
            om = OpacityManager()
            sim = CommonSimUtils.get_sim_instance(sim_id)
            opacity = float(parameters[0])
            fade_duration = float(parameters[1])
            om.fade_to(sim, opacity, fade_duration)
        except:
            pass
        return True