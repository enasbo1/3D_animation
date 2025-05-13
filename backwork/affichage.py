from backwork.dddirection import*

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D

__per_point_d = 0
__per_point_v = 0
__per_point_cosd = 1
__per_point_cosv = 1
__per_point_sind = 0
__per_point_sinv = 0
_per_point_dirCam = Vector3D(1,0,0)

def per_point(x:float,y:float, camVector : Vector3D, dcam:float, vcam:float, pointPosition : Vector3D) -> Vector2D:
    global __per_point_d, __per_point_v
    global __per_point_cosd, __per_point_cosv, __per_point_sind, __per_point_sinv, _per_point_dirCam

    same_cam = (__per_point_d == dcam) & (__per_point_v == vcam)

    __per_point_d = dcam
    __per_point_b = vcam

    if same_cam:
        dirCam = _per_point_dirCam
    else:
        dirCam = Vector3D.from_polar(dcam, vcam)
        _per_point_dirCam = dirCam
    posRep = pointPosition - camVector

    cop = dirCam.scalar(posRep)
    if cop!=0:
        O = 1/cop
        if same_cam:
            cosv = __per_point_cosv
            sinv = __per_point_sinv
        else:
            cosv = cos(vcam)
            sinv = dirCam.z
            __per_point_cosv = cosv
            __per_point_sinv = sinv

        if cosv!=0:
            B=((O*posRep.z)-sinv)/cosv
            if same_cam:
                cosd = __per_point_cosd
                sind = __per_point_sind
            else:
                sind = sin(dcam)
                cosd = cos(dcam)
                __per_point_cosd = cosd
                __per_point_sind = sind

            if cosd!=0:
                A = -(posRep.y / (cop*cosd) - (sind/cosd) * (cosv-B*sinv))
            else:
                A  =  posRep.x / (cop*sind) + (cosd/sind) * (B*sinv-cosv)
            A=(A*x)
            B=(B*x)
        else:
            A, B = 2*x, 2*y
    else:
        A, B = 2*x, 2*y
    return Vector2D(A, B)