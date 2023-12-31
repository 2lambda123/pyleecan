from os.path import join
from numpy.testing import assert_almost_equal

from Tests import save_validation_path as save_path
from numpy import sqrt, pi
from multiprocessing import cpu_count

import pytest

from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.Electrical import Electrical
from pyleecan.Classes.EEC_LSRPM import EEC_LSRPM
from pyleecan.Classes.MagFEMM import MagFEMM
from pyleecan.Classes.Output import Output
from pyleecan.Functions.load import load
from pyleecan.Functions.Plot import dict_2D


@pytest.mark.long_5s
@pytest.mark.MagFEMM
@pytest.mark.EEC_LSRPM
@pytest.mark.IPMSM
@pytest.mark.periodicity
@pytest.mark.SingleOP
@pytest.mark.skip(reason="Work in progress")
def test_EEC_LSRPM(nb_worker=int(0.5 * cpu_count())):
    """Validation of LSRPM EEC from Sijie's PhD thesis"""

    LSRPM = load("LSRPM_001.json")
    simu = Simu1(name="test_EEC_LSRPM", machine=LSRPM)

    # Definition of the input
    simu.input = InputCurrent(N0=2000, Nt_tot=10, Na_tot=2048)
    simu.input.set_Id_Iq(I0=250 / sqrt(2), Phi0=60 * pi / 180)

    # Define second simu for FEMM comparison
    simu2 = simu.copy()
    simu2.name = "test_EEC_LSRPM_FEMM"

    # Definition of the electrical simulation (FEMM)
    simu.elec = Electrical()
    simu.elec.eec = EEC_LSRPM(
        fluxlink=MagFEMM(
            is_periodicity_t=True,
            is_periodicity_a=True,
            nb_worker=nb_worker,
        )
    )

    simu.mag = None
    simu.force = None
    simu.struct = None

    out = Output(simu=simu)
    simu.run()

    # Definition of the magnetic simulation (FEMM)
    simu2.mag = MagFEMM(
        type_BH_stator=0,
        type_BH_rotor=0,
        is_periodicity_a=True,
        nb_worker=nb_worker,
    )

    out2 = Output(simu=simu2)
    simu2.run()

    # Plot 3-phase current function of time
    out.elec.get_Is().plot_2D_Data(
        "time",
        "phase[]",
        save_path=join(save_path, "EEC_FEMM_IPMSM_currents.png"),
        is_show_fig=False,
        **dict_2D
    )

    # from Yang et al, 2013
    assert_almost_equal(out.elec.Tem_av, 81.81, decimal=1)
    assert_almost_equal(out2.mag.Tem_av, 81.70, decimal=1)

    return out, out2


# To run it without pytest
if __name__ == "__main__":
    out, out2 = test_EEC_LSRPM()
