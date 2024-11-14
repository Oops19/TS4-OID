#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


class DcFunction:

    F_RAISE_GENITAL = 'dc_raise_genital'  # this includes penis and strapon
    F_LOWER_GENITAL = 'dc_raise_genital'

    F_EQUIP_STRAP_ON = 'dc_equip_strap_on'
    F_REMOVE_STRAP_ON = 'dc_remove_strap_on'

    F_ERECT_PENIS = 'dc_erect_penis'  # Undo: dc_lower_penis
    F_LOWER_PENIS = 'dc_flaccid_penis'

    # Milk Farm DLC settings
    F_BREASTS_MILKED = 'dc_breasts_milked'  # optionally append (1.0) to specify a multiplier for milk reduction of the sim
    F_PENIS_MILKED = 'dc_penis_milked'  # optionally append (3.0) to specify a multiplier for milk reduction of the sim
    r''' Everything else might be added later
    F_BREAST_FEEDING = 'dc_breast_feeding'
    F_PENIS_FEEDING = 'dc_penis_feeding'

    F_BREASTS_MILKING = 'dc_breasts_milking'
    F_PENIS_MILKING = 'dc_penis_milking'
    '''

    # Outfit related functions - DC
    F_UNDO_OUTFIT = 'dc_undo_outfit'

    F_UNDRESS_PREFIX = 'dc_undress_'
    F_EQUIP_PREFIX = 'dc_equip_'
    F_UNDRESS_CAS_PARTS = 'dc_undress_cas_parts'  # append (1-3,8-10) - the body parts to remove, (1-200) to remove everything incl. tattoos, scars, makeup, rings, ...
    F_EQUIP_CAS_PARTS = 'dc_equip_cas_parts'  # append (1-3, 8-10, HAT) - these body parts will be to added

    F_EQUIP_ALL = 'dc_equip_all'
    F_EQUIP_FULL = 'dc_equip_full'
    F_EQUIP_TOP = 'dc_equip_top'
    F_EQUIP_BOTTOM = 'dc_equip_bottom'
    # F_EQUIP_SHOES = 'dc_equip_shoes'
    # F_EQUIP_NEXT = 'dc_equip_next'  # add 1 cas part in a pre-defined order (... SHOE, HAT)

    F_UNDRESS_ALL = 'dc_undress_all'  # Undo: 'undress_bottom' - all outfit/garment odyParts will be added by p_equip_all
    F_UNDRESS_FULL = 'dc_undress_full'
    F_UNDRESS_TOP = 'dc_undress_top'  # Undo: p_wear_top
    F_UNDRESS_BOTTOM = 'dc_undress_bottom'  # Undo: p_wear_bottom
    F_UNDRESS_SHOES = 'dc_undress_shoes'
    F_UNDRESS_NEXT = 'dc_undress_next'  # remove 1 cas part in a pre-defined order (HAT, SHOE, ...)