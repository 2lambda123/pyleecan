from numpy import abs, exp


def draw_FEMM(
    self,
    femm,
    nodeprop=None,
    maxseg=None,
    element_size=None,
    propname=None,
    hide=False,
    group=None,
    is_draw=True,
):
    """Draw the Arc object in FEMM and assign the property

    Parameters
    ----------
    femm : FEMMHandler
        client to send command to a FEMM instance
    nodeprop :
        Nodal property
         (Default value = None)
    maxseg :
        Meshed with elements that span at most maxsegdeg degrees per element
         (Default value = None)
    propname :
        Boundary property ’propname’
         (Default value = None)
    hide :
        0 = not hidden in post-processor, 1 == hidden in post processor
         (Default value = False)
    group :
        the group the Arc1 object belongs
         (Default value = None)
    is_draw : bool
        1 to draw the list of surfaces given

    Returns
    -------
    None
    """

    # split if arc angle > 180
    angle = self.get_angle(is_deg=True)

    # Compute the coordinate of the nodes
    begin = self.get_begin()
    mid = self.get_middle()
    end = self.get_end()
    X1, Y1 = begin.real, begin.imag
    X2, Y2 = mid.real, mid.imag
    X3, Y3 = end.real, end.imag

    if is_draw:
        # Adding nodes
        femm.mi_addnode(X1, Y1)
        femm.mi_addnode(X3, Y3)

    femm.mi_selectnode(X1, Y1)
    femm.mi_setnodeprop(nodeprop, group)
    femm.mi_clearselected()

    femm.mi_selectnode(X3, Y3)
    femm.mi_setnodeprop(nodeprop, group)
    femm.mi_clearselected()

    if abs(angle) > 180:
        if is_draw:
            femm.mi_addnode(X2, Y2)

        femm.mi_selectnode(X2, Y2)
        femm.mi_setnodeprop(nodeprop, group)
        femm.mi_clearselected()

    # invert the nodes
    if angle < 0:
        angle = -angle
        X1, Y1, X3, Y3 = X3, Y3, X1, Y1

    if is_draw:
        if angle > 180:
            femm.mi_addarc(X1, Y1, X2, Y2, angle / 2, 2)
            femm.mi_addarc(X2, Y2, X3, Y3, angle / 2, 2)
        else:
            femm.mi_addarc(X1, Y1, X3, Y3, angle, 2)

    # Set Arc properties
    if angle > 180:
        cent = self.get_center()
        mid1 = cent + (mid - cent) * exp(1j * angle / 4)
        mid2 = cent + (mid - cent) * exp(-1j * angle / 4)
        femm.mi_selectarcsegment(mid1.real, mid1.imag)
        femm.mi_selectarcsegment(mid2.real, mid1.imag)
    else:
        femm.mi_selectarcsegment(X2, Y2)

    maxseg = self.comp_maxseg(element_size, maxseg)
    femm.mi_setarcsegmentprop(maxseg, propname, hide, group)
    femm.mi_clearselected()
