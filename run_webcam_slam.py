
import numpy as np
import cv2
import sys
import glob
from visual_odometry import PinholeCamera, VisualOdometry


#cam = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
cam = PinholeCamera(1280.0, 720.0, 718.8560, 718.8560*0.5, 640, 360)

vo = VisualOdometry(cam, 'tmp')


mycam = cv2.VideoCapture(0)
 
def get_image():
    retval, im = mycam.read()
    return im

def main():

    traj = np.zeros((600,600,3), dtype=np.uint8)

    img_id = 0
    while(1):
        frame = get_image()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vo.update(img, img_id)
        cur_t = vo.cur_t
        if(img_id > 2):
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0., 0., 0.
        draw_x, draw_y = int(x)+290, int(z)+90
        cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
        cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
        cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)
        cv2.imshow('Road facing camera', img)
        cv2.imshow('Trajectory', traj)
        cv2.waitKey(1)
        img_id += 1


if  __name__ == '__main__':
    main()
