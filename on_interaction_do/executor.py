#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import math
import re
import time
from typing import Union

import services
import sims4
import sims4.commands
import sims4.hash_util
from objects.game_object import GameObject
from on_interaction_do.cache.dc_cache import DcCache
from on_interaction_do.executors.dc_command import DcCommand
from on_interaction_do.executors.vanilla_command import VanillaCommand
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils

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
from interactions.utils import routing
from on_interaction_do.cache.data_store import DataStore
from on_interaction_do.enums.generic_function import GenericFunction
from on_interaction_do.enums.oid_constants import OidConstants

from on_interaction_do.executors.generic_command import GenericCommand
from on_interaction_do.modinfo import ModInfo
from sims.sim import Sim
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_cas_utils import SimInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.commands.run_commands import RunCommands

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class Executor:
    # noinspection PyTypeChecker
    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(),
        OidConstants.COMMAND,  # o19.oid.do_command
        "Run a command",
        command_arguments=(
                CommonConsoleCommandArgument('funcs_with_params', 'text', ''),
                CommonConsoleCommandArgument('sim_id_str', 'text', ''),
                CommonConsoleCommandArgument('target_sim_or_obj_id_str', 'text', '', is_optional=True, default_value=''),
        )
    )
    def o19_do_command(output: CommonConsoleCommandOutput, funcs_with_params: str, sim_id_str: str, target_sim_or_obj_id_str: str = ''):
        # TODO fully support target_object / target_sim_or_obj_id_str
        """
        Called from the basic_extras.do_command section with 'o19.oid.do_command param sim_id (sim_id)'.
        @param output:
        @param funcs_with_params:
        @param sim_id_str:
        @param target_sim_or_obj_id_str:
        @return:
        """
        log.debug(f'{OidConstants.COMMAND} "{funcs_with_params}" (sim={sim_id_str}, target={target_sim_or_obj_id_str})')
        interaction_id: int = 0
        sim_id: int = 0
        sim_info: Union[SimInfo, None] = None
        target_id: int = 0
        target_sim_info: Union[SimInfo, None] = None
        target_object: Union[GameObject, None] = None
        try:
            sim_id = int(sim_id_str)
            sim_info: SimInfo = CommonSimUtils.get_sim_info(sim_id)
            interaction_str = re.sub(r'^id\(([0-9]+)\).*', r'\g<1>', funcs_with_params)
            interaction_id = int(interaction_str)
            if target_sim_or_obj_id_str:
                target_id = int(target_sim_or_obj_id_str)
                target_sim_info: Union[SimInfo, None] = CommonSimUtils.get_sim_info(target_id)
                if target_sim_info:
                    log.info(f"{OidConstants.COMMAND}('{sim_info}' ({sim_id}): '{funcs_with_params}' on '{target_sim_info}' ({target_id})")
                else:
                    target_object = CommonObjectUtils.get_game_object(target_id)
                    if target_object:
                        log.info(f"{OidConstants.COMMAND}('{sim_info}' ({sim_id}): '{funcs_with_params}' on '{target_sim_info}' ({target_id})")
                    else:
                        log.info(f"{OidConstants.COMMAND}('{sim_info}' ({sim_id}): '{funcs_with_params}' on '???' ({target_id})")
            else:
                log.info(f"{OidConstants.COMMAND}('{sim_info}' ({sim_id}): {funcs_with_params}')")
        except Exception as e:
            log.error(f"{OidConstants.COMMAND}('{funcs_with_params}') >> Failed to extract data: '{e}'", throw=False)
            return

        for function in funcs_with_params.split('+'):
            # support for sim names. strip all parameters after RegEx and keep spaces
            f, _p = re.sub(r'^([^(]*)(?:\(([a-zA-Z0-9,.+ ]*)\)|(.*))$', r'\g<1> \g<2>', function).split(' ', 1)
            p = [s.strip() for s in _p.split(',')]
            function_type = f.split('_', 1)[0]
            if function_type == GenericFunction.ID or function_type == GenericFunction.NOP:
                continue
            if function_type == OidConstants.PREFIX_GENERIC[:-1]:
                rv = GenericCommand().process(f, p, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)

            elif function_type == OidConstants.PREFIX_DC_OR_VANILLA[:-1]:
                if DcCache().failure:
                    f = re.sub(r"^.", r"bg", f)
                    rv = VanillaCommand().process(f, p, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
                else:
                    f = re.sub(r"^.", r"dc", f)
                    rv = DcCommand().process(f, p, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
            elif function_type == OidConstants.PREFIX_VANILLA[:-1]:
                rv = VanillaCommand().process(f, p, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
            elif function_type == OidConstants.PREFIX_DC[:-1]:
                rv = DcCommand().process(f, p, interaction_id, sim_id, sim_info, target_id, target_sim_info, target_object, funcs_with_params)
            else:
                log.warn(f"Executor.dc: Skipping unknown function '{f}' in '{funcs_with_params}'")
                rv = True
            if rv is False:
                log.warn(f"Executor.dc: exiting as function '{function}' returned 'False'.")
                break

    @staticmethod
    @CommonIntervalEventRegistry.run_every(ModInfo.get_identity(), milliseconds=1000)
    def o19_timer_1000ms():
        if CommonTimeUtils.game_is_paused():
            return
        Executor._rotate_sim()
        Executor._run_undo_commands()
        Executor._run_repeat_commands()

    @staticmethod
    def _run_repeat_commands():
        def cleanup():
            try:
                del cs[sim_id]
            except:
                pass

        cs = DataStore().repeat_commands
        if not cs:
            return
        log.debug(f"_run_repeat_commands({cs}")

        for sim_id, _data in cs.items():
            end_time, cmd, param, tuning_ref, next_runs, sim = _data
            if end_time < time.time():
                # Remove the sim and process the next command in 1000ms & avoid dict-modified-error
                cleanup()
                return
            try:
                next_run = next_runs[0]
                if next_run < time.time():
                    log.debug(f"next_run {tuning_ref}: {type(tuning_ref)} ... {DataStore().interaction_ids}")
                    process_sim = False
                    if tuning_ref != 0:
                        tuning_ids = DataStore().get_interaction_ids(tuning_ref)
                        log.debug(f"tuning_ids {tuning_ids}")
                        for interaction in tuple(sim.si_state):
                            sim_interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
                            log.debug(f"sim_interaction_id {sim_interaction_id}")
                            if sim_interaction_id in tuning_ids:
                                process_sim = True
                                break
                    log.debug(f"next_run {process_sim}")
                    if process_sim:
                        RunCommands().run_command(f"{cmd} {param} {sim_id}")
                    else:
                        # Interaction is no longer running, never ever repeat
                        cleanup()
                        return
            except Exception as e:
                log.warn(f"Running '{cmd}' failed: '{e}'.")
                cleanup()
                return

    @staticmethod
    def _run_undo_commands():
        cs = DataStore().undo_commands
        if not cs:
            return
        log.debug(f"_run_undo_commands({cs})")

        process_sim = False
        for sim_id, _data in cs.items():
            end_time, cmd, param, interaction_id, post_delay, sim = _data
            if end_time < time.time():
                # Max time reached, execute the command no matter what
                process_sim = True
            elif interaction_id != 0:
                # Check whether the interaction is still running, if so do nothing
                process_sim = True
                for interaction in tuple(sim.si_state):
                    sim_interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
                    if sim_interaction_id == interaction_id:
                        process_sim = False
                        break

            if process_sim:
                if post_delay > 0:
                    # Run the command in post_delay seconds (no check for interaction_id)
                    DataStore().add_undo_command(cmd, param, sim_id, t_max=post_delay)
                else:
                    try:
                        RunCommands().run_command(f"{cmd} {param} {sim_id}")
                    except Exception as e:
                        log.warn(f"Running '{cmd}' failed: '{e}'.")
                    try:
                        del cs[sim_id]
                    except:
                        pass
                # Process the next command in 1000ms & avoid dict-modified-error
                return

    @staticmethod
    def _rotate_sim():
        if not DataStore().sim_angle:
            return

        sim = None
        try:
            remove_sims = set()
            for sim, angles in DataStore().sim_angle.items():
                target_angle, step, current_angle = angles
                current_angle += step
                if target_angle == current_angle:
                    remove_sims.add(sim)
                else:
                    DataStore().sim_angle.update({sim: (target_angle, step, current_angle)})
                Executor.__rotate_sim(sim, step)
            for sim in remove_sims:
                try:
                    del DataStore().sim_angle[sim]
                except:
                    pass
        except:
            try:
                # If something fails: cleanup
                del DataStore().sim_angle[sim]
            except:
                pass

    @staticmethod
    def __rotate_sim(sim: Sim, angle_deg: int):
        (position, orientation, level, surface_id) = sim.get_location_for_save()
        angle_rad = sims4.math.yaw_quaternion_to_angle(orientation)
        log.debug(f"angle {angle_rad} | q={orientation} | {angle_deg}°")
        angle_rad += angle_deg * math.pi / 180
        q = sims4.math.angle_to_yaw_quaternion(angle_rad)
        log.debug(f"====> {angle_rad} | q={orientation}")
        zone_id = services.current_zone_id()
        routing_surface = routing.SurfaceIdentifier(zone_id, level, routing.SurfaceType.SURFACETYPE_WORLD)
        # noinspection PyUnresolvedReferences
        location = sims4.math.Location(sims4.math.Transform(position, q), routing_surface)
        sim.location = location

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
