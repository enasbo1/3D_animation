from backwork.dddirection import*

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D

def per_point(x,y, camVector : Vector3D, dcam, vcam, pointPosition : Vector3D):
    dirCam = Vector3D.from_polar(dcam, vcam)
    posRep = pointPosition - camVector

    cop = dirCam.scalar(posRep)
    if cop>0:
        O = 1/cop
        cosv = cos(vcam)
        sinv = dirCam.z
        if cosv!=0:
            B=((O*posRep.z)-sinv)/cosv
            sind = sin(dcam)
            cosd = cos(dcam)
            if cosd!=0:
                A = -(posRep.y / (cop*cosd) - (sind/cosd) * (cosv-B*sinv))
            else:
                A  =  posRep.x / (cop*sind) + (cosd/sind) * (B*sinv-cosv)
            A=x/2-(A*x)
            B=y/2+(B*x)
        else:
            A, B = 2*x, 2*y
    else:
        A, B = 2*x, 2*y
    return Vector2D(A, B)