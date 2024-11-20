#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Union, Any

import services
import sims4
import sims4.resources
from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils

from native.animation import NativeAsm
from on_interaction_do.cheats.do_ww_command import DoWwCommand
from on_interaction_do.modinfo import ModInfo
from on_interaction_do.tune_game import TuneGame
from on_interaction_do.tune_kritical import TuneKritical
from on_interaction_do.user_config import UserConfig
from sims.sim import Sim
from sims4.hash_util import hash64
from sims.sim_info import SimInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.tuning_helper import TuningHelper

class TuneCheats:

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.xxx', "")
    def o19_cheat_xxxxload_conf(output: CommonConsoleCommandOutput):
        sim_info = CommonSimUtils.get_active_sim_info()
        is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE).result
        is_under = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR).result
        is_strap = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.NUDE).result
        is_out = not (is_nude or is_under or is_strap)
        output(f"{sim_info} o={is_out} u={is_under} n={is_nude} d={is_strap}")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.patch', "Apply the loaded configuration again.'")
    def o19_cheat_load_conf(output: CommonConsoleCommandOutput):
        parse_error = UserConfig().update_configuration_files()
        if parse_error:
            output(f"Error in configuration (see log file)")
        else:
            output(f"Configuration loaded.")
        uc = UserConfig()
        user_data = uc.configuration_data
        TuneGame(user_data).start()
        output(f"Configuration applied.")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.patch_verbose', "Apply the loaded configuration again (verbose mode).'")
    def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
        parse_error = UserConfig().update_configuration_files()
        if parse_error:
            output(f"Error in configuration (see log file)")
        else:
            output(f"Configuration loaded.")
        th = TuningHelper()
        th.verbose = True
        uc = UserConfig()
        user_data = uc.configuration_data
        TuneGame(user_data).start()
        th.verbose = False
        output(f"Configuration applied.")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.debug.refresh_cheat', "...'")
    def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
        dwc = DoWwCommand()
        output(f"s={dwc.supported_interactions}")
        output(f"u={dwc.unsupported_interactions}")

        output(f"Updating ...")
        th = TuningHelper()
        th.verbose = True
        manager = "INTERACTION"
        tunings = ['HIU:*', 'PR:*', ]
        th.get_tuning_ids(manager, tunings)

        manager = "INTERACTION"
        tunings = ['Kritical:*', ]
        th.get_tuning_ids(manager, tunings)
        th.verbose = False

        output(f"s={dwc.supported_interactions}")
        output(f"u={dwc.unsupported_interactions}")

    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.debug.info_am', 'Print appearance modifiers.')
    def cmd_o19_layer_info(output: CommonConsoleCommandOutput):
        try:
            from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
            from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
            from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
            sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
            parts = (DDPartHandleType.EQUIPMENT_TOP, DDPartHandleType.EQUIPMENT_BOTTOM, DDPartHandleType.EQUIPMENT_SOCKS, DDPartHandleType.EQUIPMENT_FEET,
                     DDPartHandleType.EQUIPMENT_FULL_BODY, DDPartHandleType.EQUIPMENT_CUMMERBUND,)
            for undress_part in parts:
                is_outerwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.OUTERWEAR).result
                is_underwear = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.UNDERWEAR).result
                is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, undress_part, DCPartLayer.NUDE).result
                output(f"{undress_part}: {is_outerwear}|{is_underwear}|{is_nude}")

            output(f"OK")
        except Exception as e:
            output(f"Oops: {e}")

    # deprecated
    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.deprecated.run_kritical', "Re-run 'Kritical'")
    def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
        th = TuningHelper()
        th.verbose = True
        TuneKritical.start()
        th.verbose = False
        output(f"Done")

    # deprecated
    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.deprecated.run_vanilla', "Re-run 'Vanilla'")
    def o19_cheat_log_all_interactions(output: CommonConsoleCommandOutput):
        th = TuningHelper()
        th.verbose = True
        uc = UserConfig()
        user_data = uc.configuration_data
        TuneGame(user_data).start()
        th.verbose = False
        output(f"Done")

# deprecated
@CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.deprecated.feet', 'Undress shoes.')
def cmd_o19_kri_feet(output: CommonConsoleCommandOutput):
    def _setup_asm_default(self, interaction_sim: Sim, interaction_target: Any, interaction_asm: NativeAsm, *args, **kwargs) -> Union[bool, None]:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
        equipment_part_handle = DDNuditySystemUtils().get_equipment_part_handle_from_handle_type(self.part_handle)
        current_layer = equipment_part_handle.get_current_layer(target_sim_info)
        interaction_asm.set_parameter('current_undress_layer', current_layer.name.lower())
        interaction_asm.set_parameter('to_undress_layer', self.to_layer.name.lower())
        # We return None here to indicate that we do not want to replace the original asm.
        return None

    try:
        sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
        sim: Sim = CommonSimUtils.get_sim_instance(sim_info)
        # interaction_asm: NativeAsm = None
        # _setup_asm_default(sim, sim, interaction_asm)

        anim_prefix = 'GEN_DeviousDesires_Nudity_Interaction_ModifyEquipment_ByPartHandleAnimated'
        undress_anim = 'NUDE_EQUIPMENT_FEET'
        interaction_id = hash64(f"{anim_prefix}_{undress_anim}")
        high_value = 1 << (64 - 1)
        interaction_id = interaction_id | high_value
        output(f"{sim_info}: {interaction_id}")
        result = CommonSimInteractionUtils.queue_interaction(sim_info, interaction_id, target=sim)
        output(f"OK {result}")
    except Exception as e:
        output(f"Oops: {e}")

# deprecated
@CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.print_gender', 'Whatever.')
def cmd_o19_gender_info(output: CommonConsoleCommandOutput):
    try:
        sim_info: SimInfo = CommonSimUtils.get_active_sim_info()
        output(f"M={CommonGenderUtils.is_male(sim_info)} F={CommonGenderUtils.is_female(sim_info)}")
    except Exception as e:
        output(f"Oops: {e}")



