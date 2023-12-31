def comp_volume_magnets(self):
    """Compute the volume of the hole magnets (some of them may be missing)

    Parameters
    ----------
    self : HoleMag
        A HoleMag object

    Returns
    -------
    Vmag: float
        volume of the magnets [m**3]
    """

    V = 0
    mag_list = self.get_magnet_list()
    for ii, mag in enumerate(mag_list):
        if mag is not None:
            Smag = self.comp_surface_magnet_id(ii)
            if mag.Lmag is None:
                Lmag = self.parent.L1
            else:
                Lmag = mag.Lmag
            V += Smag * Lmag

    return V
