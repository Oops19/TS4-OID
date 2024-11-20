#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
from on_interaction_do.enums.dc_function import DcFunction
from on_interaction_do.enums.generic_function import GenericFunction
from on_interaction_do.enums.oid_constants import OidConstants
from on_interaction_do.enums.vanilla_function import VanillaFunction
from on_interaction_do.modinfo import ModInfo

# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.basic_extras import BasicExtras
from ts4lib.utils.tuning_helper import TuningHelper

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)


class TuneKritical:
    """
    To gather the interaction IDs with S4CL:
    Pause the game and click on object X and select the interaction. It will be queued in the interaction Q.
    Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
    Un-pause the game and wait until the sim is using the object.
    Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
    The 'interact' and the 'interacting' interactions may be two different ones.
    """
    tuning_helper: TuningHelper = None
    basic_extras: BasicExtras = None

    # inspect - Kritical:PracticalSexArcade-CUSTOMER-constraintToTeleport basic_extras._tuned_values
    # inspect - Kritical:Urinal2UseConstraint1 basic_extras._tuned_values
    # o19.critical.start
    # inspect - Kritical:Urinal2UseConstraint1 basic_extras._tuned_values
    # o19.tuning.commands id(123)+strip_bottom+raise_genital+undo(30,6) 141601745642262288
    # inspect - Kritical:Celadon:Constraint:WillingUse1 basic_extras._tuned_values

    @staticmethod
    def tune_styx_urinal():  # [Kritical]StyxUrinal.package 1h
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        # StyxUrinal1: "Kritical:Urinal2UseConstraint1" = 17192679856254027866
        # 16440018589410761277, no longer used in 1h (bug in XML)
        tuning_list = ["Kritical:Urinal2UseConstraint1", "16440018589410761277", ]  #
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_RAISE_GENITAL}+{DcFunction.F_UNDO_OUTFIT}(30,2)"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=False)
        # no proper exit call -> undo

    @staticmethod
    def tune_celadon_urinal():  # [Kritical]CeladonUrinal.package 1a
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        tuning_list = ["Kritical:Celadon:Constraint:WillingUse1", "Kritical:Celadon:Constraint:UnwillingUse1",
                       "Kritical:Celadon:Constraint:WillingUseFemale1", "Kritical:Celadon:Constraint:UnwillingUseFemale1", ]
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_RAISE_GENITAL}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=False)

        tuning_list = ["Kritical:Celadon:Super:WillingUse1", "Kritical:Celadon:Super:UnwillingUse1",
                       "Kritical:Celadon:Super:WillingUseFemale1", "Kritical:Celadon:Super:UnwillingUseFemale1", ]
        param = f"{DcFunction.F_EQUIP_BOTTOM}+{DcFunction.F_LOWER_GENITAL}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, include_target_sim=False)

    @staticmethod
    def tune_lethe_urinal():  # [Kritical]LetheUrinal.package 1a
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        tuning_list = ["Kritical:StandingUseMod", ]  # 17990069473521690511
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_RAISE_GENITAL}+{DcFunction.F_UNDO_OUTFIT}(10000,1)"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=False)
        # no proper exit call -> undo

        tuning_dict = TuneKritical.tuning_helper.get_tuning_dict(manager, tuning_list)
        TuneKritical.tuning_helper.remove_privacy(tuning_dict)

    @staticmethod
    def tune_exercise_bike():  # [Kritical]ExerciseBike.package 1b
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        tuning_list = ["Kritical:fuckbikeInteraction1", ]  # 10887928206835823379
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_UNDO_OUTFIT}(10000,5)"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=False)

        param = f"{DcFunction.F_RAISE_GENITAL}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', offset_time=5, include_target_sim=False)

    @staticmethod
    def tune_sensory_deprivation_chamber():  # [Kritical]SensoryDeprivationChamber.package 1a
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        tuning_list = ["Kritical:SensoryDeprivationChamberTuning-EnterConstraint1", ]  # 10207621747435304214
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_UNDRESS_TOP}+{DcFunction.F_UNDO_OUTFIT}(10000,3)"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=False)

    @staticmethod
    def tune_thigh_master():  # `[Kritical]Thighmaster.package` 1
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        # 10256348970374828421, 18032649320114211498, 17984596482812320431
        tuning_list = ["Kritical:Thighmaster_Constraint_Light1", "Kritical:Thighmaster_Constraint_Med1", "Kritical:Thighmaster_Constraint_Heavy1", ]
        param = f"{GenericFunction.NOP}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning', drop_basic_extras=['TunableDoCommandWrapper.DoCommand', 'TunableSetVisibilityStateElementWrapper.SetVisibilityStateElement', ],
                                                 include_target_sim=False)

        tuning_list = ["Kritical:Thighmaster_Interaction_Light1", "Kritical:Thighmaster_Interaction_Med1", "Kritical:Thighmaster_Interaction_Heavy1",
                       "Kritcal:Thighmaster_Interaction_Light1", "Kritcal:Thighmaster_Interaction_Med1", "Kritcal:Thighmaster_Interaction_Heavy1", ]  # type on name (v1)
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_UNDO_OUTFIT}(600,3)"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, timing='at_beginning',
                                                 drop_basic_extras=['TunableDoCommandWrapper.DoCommand', 'TunableSetVisibilityStateElementWrapper.SetVisibilityStateElement', 'TunableChangeOutfitElementWrapper.ChangeOutfitElement', ],
                                                 include_target_sim=False)

    @staticmethod
    def allow_feeding_from_feed_machine_v2():  # `Kritical:FeedMachineObject1.package` 1d
        manager = "TRAIT"
        tuning_list = ["GEN_DeviousDesires_Fetishes_Trait_SimPreference_LIKE_Fetish_CUM_CONSUMPTION_AsFeeder", ]
        dd_tunings = TuneKritical.tuning_helper.get_tunings(manager, tuning_list)

        manager = "INTERACTION"
        tuning_list = ['Kritical:FeedMachine1InteractionConstraint1', ]
        tuning_dict = TuneKritical.tuning_helper.get_tuning_dict(manager, tuning_list)
        TuneKritical.tuning_helper.modify_test_globals(tuning_dict, add_whitelist_traits=dd_tunings)

    @staticmethod
    def tune_arcade():
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND
        tuning_list = ["Kritical:PracticalSexArcade-CUSTOMER-constraintToTeleport", "Kritical:PracticalSexArcade-CUSTOMER-constraintToTeleportUnprotected1",
                       "Kritical:BJArcadeTuning-ConstraintCustomer1", "Kritical:BJArcadeTuning-ConstraintCustomerEvil1", ]
        param = f"{DcFunction.F_UNDRESS_BOTTOM}+{DcFunction.F_RAISE_GENITAL}+{DcFunction.F_EQUIP_STRAP_ON}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=True)

        param = f"{GenericFunction.F_RANDOM}(3)+{VanillaFunction.F_IMPREGNATE}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, offset_time=30.0, include_target_sim=True)

        tuning_list = ["Kritical:BJArcadeTuning-IdleCustomer1", "Kritical:PracticalSexArcade-UsageInteraction1(2)", "Kritical:PracticalSexArcade-UsageInteraction1(2)Unprotected1", ]
        param = f"{DcFunction.F_EQUIP_BOTTOM}+{DcFunction.F_PENIS_MILKED}+{DcFunction.F_LOWER_GENITAL}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param, drop_basic_extras=['TunableDoCommandWrapper.DoCommand', ], include_target_sim=True)

    @staticmethod
    def tune_arcade_remove_gender_check():
        manager = "INTERACTION"
        tuning_list = ["Kritical:PracticalSexArcade-CUSTOMER-constraintToTeleport", "Kritical:BJArcadeTuning-ConstraintCustomerEvil1", "Kritical:BJArcadeTuning-ConstraintCustomer1", ]
        tuning_dict = TuneKritical.tuning_helper.get_tuning_dict(manager, tuning_list)
        TuneKritical.tuning_helper.modify_test_globals(tuning_dict, no_gender_check=True)

    @staticmethod
    def tune_milking_machine():
        manager = "INTERACTION"
        cmd = OidConstants.COMMAND

        tuning_list = ["Kritical:MM_MilkCowSmallAssetsConstraint1", "Kritical:MM_MilkCowMediumAssetsConstraint1", "Kritical:MM_MilkCowBigAssetsConstraint1",
                       "Kritical:MilkingUpgrade:InteractionTuning:Constaint:SmallAssetsMilking1", "Kritical:MilkingUpgrade:InteractionTuning:Constaint:MedAssetsMilking1", "Kritical:MilkingUpgrade:InteractionTuning:Constaint:LargeAssetsMilking1", ]
        param = f"{DcFunction.F_UNDRESS_TOP}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param,
                                                 drop_basic_extras=['TunableDoCommandWrapper.DoCommand', 'TunableSetVisibilityStateElementWrapper.SetVisibilityStateElement', 'TunableChangeOutfitElementWrapper.ChangeOutfitElement', ],
                                                 include_target_sim=False)

        tuning_list = ["Kritical:MM_MilkCowSmallAssetsInteraction1", "Kritical:MM_MilkCowMediumAssetsInteraction1", "Kritical:MM_MilkCowBigAssetsInteraction1",
                       "Kritical:MilkingUpgrade:InteractionTuning:Interaction:LargeAssetsMilking1", "Kritical:MilkingUpgrade:InteractionTuning:Interaction:MedAssetsMilking1",
                       "Kritical:MilkingUpgrade:InteractionTuning:Interaction:SmallAssetsMilking1", ]
        param = f"{DcFunction.F_EQUIP_TOP}+{DcFunction.F_BREASTS_MILKED}"
        TuneKritical.basic_extras.add_do_command(manager, tuning_list, cmd, param,
                                                 drop_basic_extras=['TunableDoCommandWrapper.DoCommand', 'TunableSetVisibilityStateElementWrapper.SetVisibilityStateElement', 'TunableChangeOutfitElementWrapper.ChangeOutfitElement', ],
                                                 include_target_sim=False)

    @staticmethod
    def allow_milking_for_dd_v2():
        manager = "TRAIT"
        tuning_list = ["GEN_DeviousDesires_Fetishes_Trait_SimPreference_LIKE_Fetish_BREAST_MILKING_AsSource",
                       "DeviousDesires_MilkFarm_Deviant_Sim_Trait", "DeviousDesires_MilkFarm_Trait_Breast_Milk_Producer_*", ]
        dd_tunings = TuneKritical.tuning_helper.get_tunings(manager, tuning_list)

        manager = "INTERACTION"
        tuning_list = ["Kritical:MM_MilkCowSmallAssetsConstraint1", "Kritical:MM_MilkCowMediumAssetsConstraint1", "Kritical:MM_MilkCowBigAssetsConstraint1",
                       "Kritical:MilkingUpgrade:InteractionTuning:Constaint:SmallAssetsMilking1", "Kritical:MilkingUpgrade:InteractionTuning:Constaint:MedAssetsMilking1", "Kritical:MilkingUpgrade:InteractionTuning:Constaint:LargeAssetsMilking1", ]
        tuning_dict = TuneKritical.tuning_helper.get_tuning_dict(manager, tuning_list)

        TuneKritical.tuning_helper.modify_test_globals(tuning_dict, add_whitelist_traits=dd_tunings, remove_blacklist_buffs=True)

        manager = "SNIPPET"
        tuning_list = ["Kritical:MM_LactatesTestSet1", ]
        tuning_dict = TuneKritical.tuning_helper.get_tuning_dict(manager, tuning_list)

        TuneKritical.tuning_helper.modify_test_globals(tuning_dict, add_whitelist_traits=dd_tunings, remove_blacklist_buffs=True)

    @staticmethod
    def start():
        log.debug(f'# Kritical will no longer be used!')
        return

        log.debug("# Kritical")
        TuneKritical.tuning_helper = TuningHelper()
        TuneKritical.basic_extras = BasicExtras()

        log.debug('# Styx Urinal ...')
        TuneKritical.tune_styx_urinal()
        log.debug('# Celadon Urinal ...')
        TuneKritical.tune_celadon_urinal()
        log.debug('# Lethe Urinal ...')
        TuneKritical.tune_lethe_urinal()
        log.debug('# Lethe Exercise Bike ...')
        TuneKritical.tune_exercise_bike()
        log.debug('# Lethe Sensory Deprivation Chamber ...')
        TuneKritical.tune_sensory_deprivation_chamber()
        log.debug('# Thigh Master ...')
        TuneKritical.tune_thigh_master()
        log.debug('# Feed From Feeding Machine (Cum/Milk addicted) ...')
        TuneKritical.allow_feeding_from_feed_machine_v2()

        log.debug('# Arcade ...')
        TuneKritical.tune_arcade()
        log.debug('Arcade - Gender Check ...')
        TuneKritical.tune_arcade_remove_gender_check()

        log.debug('Milking Machine ...')
        TuneKritical.tune_milking_machine()
        log.debug('Milking Machine - Allow DD ...')
        TuneKritical.allow_milking_for_dd_v2()

        log.debug("# That's all.")

