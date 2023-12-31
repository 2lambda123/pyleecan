from numpy import exp, sqrt

from ....Classes.Arc1 import Arc1
from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine
from ....Functions.labels import HOLEV_LAB, HOLEM_LAB


def build_geometry(self, alpha=0, delta=0, is_simplified=False):
    """Compute the curve (Segment) needed to plot the Slot.
    The ending point of a curve is the starting point of the next curve in
    the list

    Parameters
    ----------
    self : HoleM58
        A HoleM58 object
    alpha : float
        Angle to rotate the slot (Default value = 0) [rad]
    delta : complex
        Complex to translate the slot (Default value = 0)
    is_simplified : bool
       True to avoid line superposition

    Returns
    -------
    surf_list: list
        List of SurfLine needed to draw the HoleM58

    """

    # Get correct label for surfaces
    lam_label = self.parent.get_label()
    R_id, surf_type = self.get_R_id()
    vent_label = lam_label + "_" + surf_type + "_R" + str(R_id) + "-"
    mag_label = lam_label + "_" + HOLEM_LAB + "_R" + str(R_id) + "-"

    Rext = self.get_Rext()
    R0 = self.R0

    # Get all the points
    point_dict = self._comp_point_coordinate()
    Z1 = point_dict["Z1"]
    Z2 = point_dict["Z2"]
    Z3 = point_dict["Z3"]
    Z4 = point_dict["Z4"]
    Z5 = point_dict["Z5"]
    Z6 = point_dict["Z6"]
    Z7 = point_dict["Z7"]
    Z8 = point_dict["Z8"]
    Z9 = point_dict["Z9"]
    Z10 = point_dict["Z10"]
    Z11 = point_dict["Z11"]
    Z12 = point_dict["Z12"]
    Zc1 = point_dict["Zc1"]
    Zc2 = point_dict["Zc2"]

    surf_list = list()

    surf_list = list()
    # Create all the surfaces for all the cases
    # Air surface Zc1 with magnet_0
    curve_list = list()
    if self.W2 > 0:
        curve_list.append(Segment(Z1, Z2))
    curve_list.append(Segment(Z2, Z3))
    curve_list.append(Arc1(begin=Z3, end=Z4, radius=R0, is_trigo_direction=True))
    curve_list.append(Segment(Z4, Z5))
    if self.W2 > 0:
        curve_list.append(Segment(Z5, Z6))
    curve_list.append(Segment(Z6, Z1))
    point_ref = Zc1
    S1 = SurfLine(line_list=curve_list, point_ref=point_ref)

    # Magnet_0 surface
    curve_list = list()
    curve_list.append(Segment(Z1, Z6))
    curve_list.append(Segment(Z6, Z7))
    curve_list.append(Segment(Z7, Z12))
    curve_list.append(Segment(Z12, Z1))
    point_ref = (Z1 + Z6 + Z7 + Z12) / 4

    S2 = SurfLine(line_list=curve_list, label=mag_label + "T0-S0", point_ref=point_ref)

    # Air surface Zc2 with magnet_0
    curve_list = list()
    curve_list.append(Segment(Z12, Z7))
    if self.W2 + self.W1 < self.W0:
        curve_list.append(Segment(Z7, Z8))
    curve_list.append(Segment(Z8, Z9))
    curve_list.append(Arc1(begin=Z9, end=Z10, radius=R0, is_trigo_direction=True))
    curve_list.append(Segment(Z10, Z11))
    if self.W2 + self.W1 < self.W0:
        curve_list.append(Segment(Z11, Z12))
    point_ref = Zc2
    S3 = SurfLine(line_list=curve_list, point_ref=point_ref)

    # Full surface, no magnet
    curve_list = list()
    curve_list.append(Segment(Z2, Z3))
    curve_list.append(Arc1(begin=Z3, end=Z4, radius=R0, is_trigo_direction=True))
    curve_list.append(Segment(Z4, Z5))
    curve_list.append(Segment(Z5, Z8))
    curve_list.append(Segment(Z8, Z9))
    curve_list.append(Arc1(begin=Z9, end=Z10, radius=R0, is_trigo_direction=True))
    curve_list.append(Segment(Z10, Z11))
    curve_list.append(Segment(Z11, Z2))
    point_ref = Rext - self.H0 - self.H2 / 2
    S4 = SurfLine(line_list=curve_list, point_ref=point_ref)

    # Create the surface list by selecting the correct ones
    if self.magnet_0:
        S1.label = vent_label + "T0-S0"  # Hole
        S3.label = vent_label + "T1-S0"  # Hole
        surf_list = [S1, S2, S3]
    else:
        S4.label = vent_label + "T0-S0"  # Hole
        surf_list = [S4]

    # Apply the transformations
    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)

    return surf_list
