#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import List, Set

from objects.game_object import GameObject
from on_interaction_do.enums.vanilla_function import VanillaFunction
from on_interaction_do.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from ts4lib.common_enums.body_type import BodyType
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'VanillaCommand')
log.enable()


class VanillaCommand(metaclass=Singleton):

    def process(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        log.debug(f"VanillaCommand.process({function}, {parameters}, {interaction_id}, {sim_info} ({sim_id}), {target_sim_info}/{target_object} ({target_id}))")

        if function == VanillaFunction.F_UNDRESS_ALL:
            self._undress(self._get_body_types(parameters))
        elif function == VanillaFunction.F_EQUIP_ALL:
            self._equip(self._get_body_types(parameters))
        elif function == VanillaFunction.F_IMPREGNATE:
            self._impregnate(sim_info, target_sim_info)
        else:
            log.debug(f"VC.process: Unknown function {function}")
        return True

    def _get_body_types(self, parameters) -> Set[int]:
        body_types: Set[int] = set()
        for parameter in parameters:
            if isinstance(parameter, int):
                body_types.add(parameter)
            elif isinstance(parameter, str) and parameter:
                body_types.add(BodyType[parameter].value)
        return body_types

    def _undress(self, body_types: Set[int]):
        log.debug(f"Not implemented: undressing {body_types}")  # TODO
        pass

    def _equip(self, body_types: Set[int]):
        log.debug(f"Not implemented: equipping {body_types}")  # TODO
        pass

    def _impregnate(self, sim_info, target_sim_info):
        if sim_info and target_sim_info and CommonSimPregnancyUtils.can_be_impregnated(target_sim_info) and CommonSimPregnancyUtils.can_impregnate(sim_info):
            CommonSimPregnancyUtils.start_pregnancy(target_sim_info, sim_info)