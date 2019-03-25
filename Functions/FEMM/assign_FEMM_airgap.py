# -*- coding: utf-8 -*-
"""@package assign_FEMM_airgap
@date Created on août 20 15:08 2018
@author franco_i
"""
import femm

from pyleecan.Functions.FEMM import GROUP_AG


def assign_FEMM_airgap(surf, prop, FEMM_dict):
    """Assign properties of the Airgap surface between the stator and the rotor

    Parameters
    ----------
    surf : Surface
        the surface to assign
    prop : str
        the property to assign
    FEMM_dict : dict
        Dictionnary containing the main parameters of FEMM

    Returns
    -------
    None
    
    """
    point_ref = surf.point_ref
    femm.mi_addblocklabel(point_ref.real, point_ref.imag)
    femm.mi_selectlabel(point_ref.real, point_ref.imag)
    femm.mi_setblockprop(
        prop,
        FEMM_dict["automesh_airgap"],
        FEMM_dict["meshsize_airgap"],
        0,
        0,
        GROUP_AG,
        0,
    )
    femm.mi_clearselected()
