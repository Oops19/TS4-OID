#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from on_interaction_do.cheats.do_ww_command import DoWwCommand
from on_interaction_do.modinfo import ModInfo
from on_interaction_do.tune_game import TuneGame
from on_interaction_do.user_config import UserConfig
from sims.sim_info import SimInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.tuning_helper import TuningHelper


class TuneCheats:

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

    @staticmethod
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

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.oid.info_am_bottom', "")
    def o19_cheat_print_outfit_modifiers(output: CommonConsoleCommandOutput):
        try:
            from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
            from deviousdesires.nudity_system.enums.part_handle_type import DDPartHandleType
            from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
            sim_info = CommonSimUtils.get_active_sim_info()
            is_nude = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.NUDE).result
            is_under = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_BOTTOM, DCPartLayer.UNDERWEAR).result
            is_strap = DDNuditySystemUtils().is_equipment_set_to_layer_by_type(sim_info, DDPartHandleType.EQUIPMENT_STRAPON, DCPartLayer.NUDE).result
            is_out = not (is_nude or is_under or is_strap)
            output(f"{sim_info} o={is_out} u={is_under} n={is_nude} d={is_strap}")
        except Exception as e:
            output(f"Error: {e}")