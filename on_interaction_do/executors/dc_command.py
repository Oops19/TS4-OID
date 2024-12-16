#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
import re
from typing import List

from objects.game_object import GameObject
from on_interaction_do.cache.data_store import DataStore
from on_interaction_do.cache.dc_cache import DcCache
from on_interaction_do.cache.outfit_cache import OutfitCache
from on_interaction_do.enums.dc_function import DcFunction
from on_interaction_do.enums.generic_function import GenericFunction
from on_interaction_do.enums.oid_constants import OidConstants
from on_interaction_do.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.common_enums.body_type import BodyType
from ts4lib.utils.singleton import Singleton
try:
    from deviantcore.cas_part_system.enums.body_location import DCBodyLocation
    from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
    from deviantcore.utils.sexual_organ_utils import DCSexualOrganUtils
    from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
    from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
    from deviousdesires.nudity_system.utils.penis_state_utils import DDPenisStateUtils
    from deviousdesires.sex.enums.string_ids import DDSexSystemStringId
except:
    pass

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'DcCommand')
log.enable()


class DcCommand:  # TODO support reload .... (metaclass=Singleton):
    def __init__(self):
        pass

    def process(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        log.debug(f"DC.process({function}, {parameters}, {interaction_id}, {sim_info}, {target_sim_info})")
        if DcCache().failure:
            return True

        if function == DcFunction.F_RAISE_GENITAL:
            self._raise_genital(sim_info)
        elif function == DcFunction.F_EQUIP_STRAP_ON:
            self._equip_strap_on(sim_info)
        elif function == DcFunction.F_ERECT_PENIS:
            self._erect_penis(sim_info)
        elif function == DcFunction.F_LOWER_GENITAL:
            self._lower_genital(sim_info)
        elif function == DcFunction.F_REMOVE_STRAP_ON:
            self._remove_strap_on(sim_info)
        elif function == DcFunction.F_LOWER_PENIS:
            self._flaccid_penis(sim_info)
        elif function == DcFunction.F_PENIS_ORGASM:
            self._penis_orgasm(parameters, sim_info)

        elif function == DcFunction.F_PENIS_MILKED:
            self._penis_milked(function, parameters, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
        elif function == DcFunction.F_BREASTS_MILKED:
            self._breast_milked(function, parameters, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)

        elif function == DcFunction.F_UNDO_OUTFIT:
            self._undo_outfit(function, parameters, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)

        elif function.startswith(DcFunction.F_UNDRESS_PREFIX):
            if function.startswith(DcFunction.F_UNDRESS_CAS_PARTS):
                self._equip_or_undress_body_part(function, parameters, sim_info)
            elif function == DcFunction.F_UNDRESS_ALL:
                self._undress_all(sim_info)
            elif function == DcFunction.F_UNDRESS_FULL:
                self._undress_full(sim_info)
            elif function == DcFunction.F_UNDRESS_TOP:
                self._undress_top(sim_info)
            elif function == DcFunction.F_UNDRESS_BOTTOM:
                self._undress_bottom(sim_info)
            elif function == DcFunction.F_UNDRESS_SHOES:
                self._undress_shoes(sim_info)
            elif function == DcFunction.F_UNDRESS_NEXT:
                self._undress_next(sim_info, parameters)
            else:
                log.debug(f"DC.process: Unknown undress function {function}")
        elif function.startswith(DcFunction.F_EQUIP_PREFIX):
            if function.startswith(DcFunction.F_UNDRESS_CAS_PARTS):
                self._equip_or_undress_body_part(function, parameters, sim_info)
            elif function == DcFunction.F_EQUIP_ALL:
                self._equip_all(sim_info)
            elif function == DcFunction.F_EQUIP_FULL:
                self._equip_full(sim_info)
            elif function == DcFunction.F_EQUIP_TOP:
                self._equip_top(sim_info)
            elif function == DcFunction.F_EQUIP_BOTTOM:
                self._equip_bottom(sim_info)
            else:
                log.debug(f"DC.process: Unknown equip function {function}")
        else:
            log.debug(f"DC.process: Unknown function {function}")
        return True

    def _raise_genital(self, sim_info: SimInfo) -> bool:
        self._erect_penis(sim_info)
        self._equip_strap_on(sim_info)
        return True

    def _lower_genital(self, sim_info: SimInfo) -> bool:
        self._flaccid_penis(sim_info)
        self._remove_strap_on(sim_info)
        return True

    def _equip_strap_on(self, sim_info: SimInfo) -> bool:
        try:
            if not DCSexualOrganUtils().has_penis(sim_info):
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.NUDE)
        except:
            pass
        return True

    def _remove_strap_on(self, sim_info: SimInfo) -> bool:
        try:
            if not DCSexualOrganUtils().has_penis(sim_info):
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.OUTERWEAR)
        except:
            pass
        return True

    def _erect_penis(self, sim_info: SimInfo) -> bool:
        try:
            if DCSexualOrganUtils().has_penis(sim_info):
                DDPenisStateUtils().set_erect(sim_info, DDSexSystemStringId.BUFF_REASON_FROM_ENGAGING_IN_SEXY_TIME, update_outfit=True)
        except:
            pass
        return True

    def _flaccid_penis(self, sim_info: SimInfo) -> bool:
        try:
            if DCSexualOrganUtils().has_penis(sim_info):
                DDPenisStateUtils().set_flaccid(sim_info, update_outfit=True)
        except:
            pass
        return True

    def _penis_orgasm(self, parameters: List, sim_info: SimInfo) -> bool:
        if DcCache().failure:
            return True
        if DCSexualOrganUtils().has_penis(sim_info):
            try:
                multiplier = abs(float(parameters[0]))
            except:
                multiplier = 1
            try:
                from deviousdesires_milk_farm.utils.sim_milk_utils import DDMFSimMilkUtils
                from deviousdesires_milk_farm.settings.setting_utils import DDMilkFarmSettingUtils
                if DDMFSimMilkUtils().has_required_cum_level_for_orgasm(sim_info):
                    amount = DDMilkFarmSettingUtils.CumProduction.get_cum_lost_per_orgasm() * multiplier
                    DDMFSimMilkUtils().change_cum_level(sim_info, -amount)
                    log.debug(f"Sprayed {amount:.2f} ({multiplier:.2f} orgasms with {DDMilkFarmSettingUtils.CumProduction.get_cum_lost_per_orgasm():.2f})")
            except:
                log.warn(f"Milk Farm DLC not found!")
        return True

    def _penis_milked(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        if DcCache().failure:
            return True
        if DCSexualOrganUtils().has_penis(sim_info):
            try:
                multiplier = abs(float(parameters[0]))
            except:
                multiplier = 1
            try:
                from deviousdesires_milk_farm.utils.sim_milk_utils import DDMFSimMilkUtils
                from deviousdesires_milk_farm.settings.setting_utils import DDMilkFarmSettingUtils
                if DDMFSimMilkUtils().has_required_cum_level_for_orgasm(sim_info):
                    amount = DDMilkFarmSettingUtils.get_milk_or_cum_amount_per_bottle() * multiplier
                    DDMFSimMilkUtils().change_cum_level(sim_info, -amount)
                    log.debug(f"Milked {amount:.2f} ({multiplier:.2f} bottles with {DDMilkFarmSettingUtils.get_milk_or_cum_amount_per_bottle():.2f})")
            except:
                log.warn(f"Milk Farm DLC not found!")
        return True

    def _breast_milked(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        if DcCache().failure:
            return True
        if DCSexualOrganUtils().has_breasts(sim_info):
            try:
                multiplier = abs(float(parameters[0]))
            except:
                multiplier = 3
            try:
                # optionally: multiplier = ... based on buff / production levels
                from deviousdesires_milk_farm.settings.setting_utils import DDMilkFarmSettingUtils
                from deviousdesires_milk_farm.utils.sim_milk_utils import DDMFSimMilkUtils
                from deviousdesires_milk_farm.mobile_milking.components.sim_milking_component import DDSimMilkingComponent
                body_location = DCBodyLocation.CHEST  # DDMFBodyLocation.BREASTS
                milking_component: DDSimMilkingComponent = DDSimMilkingComponent(sim_info, (body_location,))
                amount = DDMilkFarmSettingUtils.get_milk_or_cum_amount_per_bottle() * multiplier
                milking_component._sim_milk_utils.change_milk_level(milking_component._sim_info, body_location, -amount)
                log.debug(f"Milked {amount:.2f} ({multiplier:.2f} bottles with {DDMilkFarmSettingUtils.get_milk_or_cum_amount_per_bottle():.2f})")
            except:
                log.warn(f"Milk Farm DLC not found!")
        return True

    def _undo_outfit(self, function: str, parameters: List, interaction_id: int, sim_id: int, sim_info: SimInfo, target_id: int, target_sim_info: SimInfo, target_object: GameObject, funcs_with_params: str = None) -> bool:
        t_max_str = parameters[0]
        t_max = float(t_max_str)
        if len(parameters) == 2:
            post_delay_str = parameters[0]
            post_delay = float(post_delay_str)
        else:
            post_delay = 0
        new_parameter = f'id({interaction_id})'

        # Parameters with (...)
        for undos in [
            (GenericFunction.F_UNDRESS_CAS_PARTS, GenericFunction.F_EQUIP_CAS_PARTS),
        ]:
            undo_1, undo_2 = undos
            if undo_1 in funcs_with_params:
                _undo = re.sub(r'.*\+' + undo_1 + r'\(([^)]*)\).*$', undo_2 + r'(\g<1>)', funcs_with_params)
                new_parameter = f"{new_parameter}{GenericFunction.JOIN}{_undo}"
            elif undo_2 in funcs_with_params:
                _undo = re.sub(r'.*\+' + undo_2 + r'\(([^)]*)\).*$', undo_1 + r'(\g<1>)', funcs_with_params)
                new_parameter = f"{new_parameter}{GenericFunction.JOIN}{_undo}"

        # Parameters without (...), simple swap
        for undos in [
            (DcFunction.F_RAISE_GENITAL, DcFunction.F_LOWER_GENITAL),
            (DcFunction.F_EQUIP_STRAP_ON, DcFunction.F_REMOVE_STRAP_ON),
            (DcFunction.F_ERECT_PENIS, DcFunction.F_LOWER_PENIS),
            (DcFunction.F_EQUIP_ALL, DcFunction.F_UNDRESS_ALL),
            (DcFunction.F_EQUIP_TOP, DcFunction.F_UNDRESS_TOP),
            (DcFunction.F_EQUIP_FULL, DcFunction.F_UNDRESS_FULL),
            (DcFunction.F_EQUIP_BOTTOM, DcFunction.F_UNDRESS_BOTTOM),
        ]:
            undo_1, undo_2 = undos
            if undo_1 in funcs_with_params:
                new_parameter = f"{new_parameter}{GenericFunction.JOIN}{undo_2}"
            elif undo_2 in funcs_with_params:
                new_parameter = f"{new_parameter}{GenericFunction.JOIN}{undo_1}"

        DataStore().add_undo_command(OidConstants.COMMAND, new_parameter, sim_id=sim_id, t_max=t_max, interaction_id=interaction_id, post_delay=post_delay)
        return True

    def _equip_or_undress_body_part(self, function: str, parameters: List[str], sim_info: SimInfo):
        for body_part_str in parameters:
            if body_part_str.isdigit():
                body_part_int = int(body_part_str)
                body_part: BodyType = BodyType(body_part_int)
            else:
                body_part: BodyType = BodyType(BodyType[body_part_str])
            dd_part_handle_type = None
            if body_part == BodyType.UPPER_BODY:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_TOP  # 6
            elif body_part == BodyType.LOWER_BODY:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_BOTTOM  # 7
            elif body_part == BodyType.CUMMERBUND:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_CUMMERBUND  # 9
            elif body_part == BodyType.FULL_BODY:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_FULL_BODY  # 5
            elif body_part == BodyType.TIGHTS:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_TIGHTS  # 42
            elif body_part == BodyType.SOCKS:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_SOCKS  # 36
            elif body_part == BodyType.SHOES:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_FEET  # 8
            elif body_part == BodyType.GLASSES:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_GLASSES  # 11
            elif body_part == BodyType.EARRINGS:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_EARRINGS  # 10
            elif body_part == BodyType.NECKLACE:
                dd_part_handle_type = DDPartHandleType.EQUIPMENT_NECKLACE  # 12
            if dd_part_handle_type is None:
                log.warn(f"Not supported: '{body_part}'")
                continue
            else:
                log.debug(f"Mapped {body_part} to {dd_part_handle_type}")

            if function == DcFunction.F_EQUIP_CAS_PARTS:
                self._equip_body_part(sim_info, body_part, dd_part_handle_type)
            else:  # undress
                self._undress_body_part(sim_info, body_part, dd_part_handle_type)
        return True

    def _undress_all(self, sim_info):
        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.ALL, DCPartLayer.NUDE)

    def _equip_all(self, sim_info):
        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.ALL, DCPartLayer.OUTERWEAR)

    r"""
    Fixme, check whether sim has TOP & BOTTOM or FULL and apply modifiers accordingly.
    Check back with 
    """
    def _undress_full(self, sim_info):
        self._undress_top(sim_info)
        self._undress_bottom(sim_info)

    def _equip_full(self, sim_info):
        self._equip_top(sim_info)
        self._equip_bottom(sim_info)

    def _undress_top(self, sim_info):
        is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.NUDE).result
        is_under = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.UNDERWEAR).result
        is_strap = None
        data = [is_nude, is_under, is_strap]
        OutfitCache.outfit_top.update({sim_info.sim_id: data})
        log.debug(f"OutfitCache: {OutfitCache.outfit_top}")
        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.NUDE)

    def _equip_top(self, sim_info):
        data = OutfitCache.outfit_top.pop(sim_info.sim_id, None)
        if data:
            is_nude, is_under, _ = data
            is_outer = not (is_nude or is_under)
            if is_outer:
                log.debug("OutfitTools: Adding outerwear")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.OUTERWEAR)
            else:
                if is_nude:
                    log.debug("OutfitTools: Removing everything")
                    DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.NUDE)
                if is_under:
                    log.debug("OutfitTools: Adding underwear")
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.UNDERWEAR)
        else:
            log.debug('OutfitTools: NoChange')

    def _undress_bottom(self, sim_info):
        is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE).result
        is_under = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR).result
        is_strap = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.NUDE).result
        # EQUIPMENT_STRAPON + NUDE ... add/has strapon
        # EQUIPMENT_STRAPON + OUTERWEAR ... remove/no strapon
        data = [is_nude, is_under, is_strap]
        OutfitCache.outfit_bottom.update({sim_info.sim_id: data})
        log.debug(f"OutfitCache: {OutfitCache.outfit_bottom}")
        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)

    def _equip_bottom(self, sim_info):
        data = OutfitCache.outfit_bottom.pop(sim_info.sim_id, None)
        if data:
            log.debug(f"{data}")
            is_nude, is_under, is_strap = data
            is_outer = not (is_nude or is_under or is_strap)
            if is_outer:
                log.debug("OutfitTools: Adding outerwear")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.OUTERWEAR)
            else:
                if is_nude:
                    log.debug("OutfitTools: Removing everything")
                    DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)
                if is_under:
                    log.debug("OutfitTools: Adding underwear")
                    DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR)
                if is_strap:
                    log.debug("OutfitTools: Adding strap-on")
                    DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.NUDE)
        else:
            log.debug("OutfitTools: No change, Sim not found")

    def _undress_shoes(self, sim_info):
        undress_part = DDPartHandleType.EQUIPMENT_FEET
        _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
        if _is_nude:
            undress_part = DDPartHandleType.EQUIPMENT_SOCKS
            _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
            if not _is_nude:
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE)
        else:
            DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE)

    def _underss_next_custom(self, sim_info: SimInfo, parameters: List) -> bool:
        _map = {
            1: DDPartHandleType.EQUIPMENT_HAT,
            3: DDPartHandleType.EQUIPMENT_HEAD,
            5: DDPartHandleType.EQUIPMENT_FULL_BODY,
            6: DDPartHandleType.EQUIPMENT_TOP,
            7: DDPartHandleType.EQUIPMENT_BOTTOM,
            8: DDPartHandleType.EQUIPMENT_FEET,  # SHOES
            9: DDPartHandleType.EQUIPMENT_CUMMERBUND,
            10: DDPartHandleType.EQUIPMENT_EARRINGS,
            11: DDPartHandleType.EQUIPMENT_GLASSES,
            12: DDPartHandleType.EQUIPMENT_NECKLACE,
            13: DDPartHandleType.EQUIPMENT_HANDS,  # GLOVES
            14: DDPartHandleType.EQUIPMENT_WRIST_LEFT,
            15: DDPartHandleType.EQUIPMENT_WRIST_RIGHT,
            36: DDPartHandleType.EQUIPMENT_SOCKS,
            42: DDPartHandleType.EQUIPMENT_TIGHTS,
        }
        for _body_type in parameters:
            body_type = int(_body_type)
            if body_type not in _map.keys():
                continue
            undress_part = _map.get(body_type)

            _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
            _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
            _is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
            if undress_part in [DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM]:
                _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
            else:
                _is_underwear = None
            log.debug(f"{sim_info}: {undress_part}: outer={_is_outerwear}, nude={_is_nude}, under={_is_underwear}")

            if _is_nude:
                continue
            if undress_part in [DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM]:
                if _is_outerwear:
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR)
                    break
                if _is_underwear:
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE)
                    break
            if _is_outerwear:
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE)
                break

            _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
            _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
            _is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
            if undress_part in [DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM]:
                _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
            else:
                _is_underwear = None
            log.debug(f"{sim_info}: {undress_part}: outer={_is_outerwear}, nude={_is_nude}, under={_is_underwear} <<<< Now")
        return True

    def _undress_next(self, sim_info: SimInfo, parameters: List) -> bool:
        if parameters:
            return self._underss_next_custom(sim_info, parameters)
        # HAT, SHOES, SOCKS, TOP, BOTTOM, FULL, CUMMERBUND, TIGHTS
        return self._underss_next_custom(sim_info, [1, 8, 36, 6, 7, 5, 9, 42, ])

        undress_parts_1 = (
            [DDPartHandleType.EQUIPMENT_FEET, DDPartHandleType.EQUIPMENT_SOCKS, ],
        )
        undress_parts_2 = (
            [DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM, DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_CUMMERBUND, ],
        )

        undress_parts_1_complete = True
        notification = None
        for undress_parts in undress_parts_1:
            is_nude = False
            is_underwear = False
            is_outerwear = False
            for undress_part in undress_parts:
                _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
                _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
                _is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
                log.debug(f"{sim_info}: {undress_part}: outer={is_outerwear}, under={is_underwear}, nude={is_nude}")
                is_nude |= _is_nude
                is_underwear |= _is_underwear
                is_outerwear |= _is_outerwear
            if not is_nude:
                undress_parts_1_complete = False
                for undress_part in undress_parts:
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE)
                break

        if undress_parts_1_complete:
            for undress_parts in undress_parts_2:
                is_nude = False
                is_underwear = False
                is_outerwear = False
                for undress_part in undress_parts:
                    _is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
                    _is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
                    _is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
                    log.debug(f"{sim_info}: {undress_part}: outer={is_outerwear}, under={is_underwear}, nude={is_nude}")
                    is_nude |= _is_nude
                    is_underwear |= _is_underwear
                    is_outerwear |= _is_outerwear

                if is_outerwear:
                    for undress_part in undress_parts:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_FULL_BODY, DCPartLayer.NUDE)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_CUMMERBUND, DCPartLayer.NUDE)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR)
                    break
                elif is_underwear:
                    if DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.UNDERWEAR).result:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.NUDE)
                        break
                    else:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_FULL_BODY, DCPartLayer.NUDE)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_CUMMERBUND, DCPartLayer.NUDE)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)
                        break
                else:
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_FULL_BODY, DCPartLayer.NUDE)
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_CUMMERBUND, DCPartLayer.NUDE)
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_TOP, DCPartLayer.NUDE)
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE)
                    break

        # sim_info.resend_outfits()

    @staticmethod
    def _equip_body_part(sim_info: SimInfo, body_part, dd_part_handle_type) -> bool:
        """
        return False if no change is possible
        """
        if DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.NUDE).result:
            if DDNuditySystemUtils().is_body_slot_set_to_layer_by_type(sim_info, body_part, DCPartLayer.UNDERWEAR):
                log.debug(f"Nude -> Underwear")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.UNDERWEAR)
            else:
                log.debug(f"Nude -> Outerwear")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.OUTERWEAR)
        elif DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.UNDERWEAR).result:
            log.debug(f"Underwear -> Outerwear")
            DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.OUTERWEAR)
        else:
            log.debug(f"Outerwear -> Outerwear")
            return False
        return True

    @staticmethod
    def _undress_body_part(sim_info: SimInfo, body_part, dd_part_handle_type) -> bool:
        """
        return False if no change is possible
        """
        if DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.OUTERWEAR).result:
            if DDNuditySystemUtils().is_body_slot_set_to_layer_by_type(sim_info, body_part, DCPartLayer.UNDERWEAR):
                log.debug(f"Outerwear -> Underwear")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.UNDERWEAR)
            else:
                log.debug(f"Outerwear -> Nude")
                DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.NUDE)
        elif DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.UNDERWEAR).result:
            log.debug(f"Underwear -> Nude")
            DDNuditySystemUtils().set_equipment_part_to_layer_by_type(sim_info, dd_part_handle_type, DCPartLayer.UNDERWEAR)
        else:
            log.debug(f"Nude -> Nude")
            return False
        return True
