from numpy import exp, pi

from ....Classes.Arc1 import Arc1
from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine
from ....Methods import ParentMissingError
from ....Functions.labels import (
    BOUNDARY_PROP_LAB,
    YSR_LAB,
    YSL_LAB,
    YOKE_LAB,
    NO_LAM_LAB,
    TOOTH_LAB,
)
from numpy import exp, pi


def get_surface_tooth(self):
    """Returns the surface delimiting the tooth (including yoke part)

    Parameters
    ----------
    self : Slot
        A Slot object

    Returns
    -------
    surface: SurfLine
        A SurfLine object representing the slot

    """

    if self.parent is not None:
        Ryoke = self.parent.get_Ryoke()
    else:
        raise ParentMissingError("Error: The slot is not inside a Lamination")

    curve_list = list()
    # tooth lines
    top_list = self.build_geometry_half_tooth(is_top=True)
    bot_list = self.build_geometry_half_tooth(is_top=False)
    # Yoke lines
    Z1 = Ryoke * exp(1j * pi / self.Zs)
    Z2 = Ryoke * exp(-1j * pi / self.Zs)
    curve_list.append(
        Segment(top_list[-1].get_end(), Z1, prop_dict={BOUNDARY_PROP_LAB: YSL_LAB})
    )
    if Ryoke > 0:
        curve_list.append(
            Arc1(
                begin=Z1,
                end=Z2,
                radius=-Ryoke,
                is_trigo_direction=False,
                prop_dict={BOUNDARY_PROP_LAB: YOKE_LAB},
            )
        )
    curve_list.append(
        Segment(Z2, bot_list[0].get_begin(), prop_dict={BOUNDARY_PROP_LAB: YSR_LAB})
    )
    # Second half of the tooth
    curve_list.extend(bot_list)
    curve_list.extend(top_list)

    if self.parent is not None:
        lam_label = self.parent.get_label()
    else:
        lam_label = NO_LAM_LAB
    label = lam_label + "_" + TOOTH_LAB
    return SurfLine(line_list=curve_list, label=label)
