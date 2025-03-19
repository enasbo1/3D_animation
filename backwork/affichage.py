from backwork.dddirection import*


def per_point(x,y,xcam,ycam,zcam,dcam,vcam,xpoint,ypoint,zpoint):
    """
    Comme expliqué plusieurs fois dans 'sujet',
    c'est la fonction qui projete les points en coordonées
    xpoint, ypoint et zpoint
    et renvoie les coordonées obtenue dans un
    repère orthonormé ((dcam,vcam),xi,xj).
    """

    D=dir(xcam,ycam,dcam,xpoint,ypoint)
    if -pi/2<D<pi/2:
        xop = xpoint - xcam
        yop = ypoint - ycam
        zop = zpoint - zcam
        xc, yc, zc = avixyz(1, dcam, vcam)
        cop = xc*xop + yc*yop + zc*zop
        if cop!=0:
            O = 1/cop
            cosv = cos(vcam)
            sinv = sin(vcam)
            if cosv!=0:
                B=((O*zop)-zc)/cosv
                sind = sin(dcam)
                cosd = cos(dcam)
                if cosd!=0:
                    A=-(yop/(cop*cosd)-(sind/cosd)*(cosv-B*sinv))
                else:
                    A=xop/(cop*sind)+(cosd/sind)*(B*sinv-cosv)
                A=x/2-(A*x)
                B=y/2+(B*x)
            else:
                A, B=2*x, 2*y
        else:
            A, B=2*x, 2*y
    else:
        A, B=2*x, 2*y
    return[A,B]