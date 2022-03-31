#!/usr/bin/env python
from math import sin, cos, sqrt
import rospy
import roslib
from std_msgs.msg import Float64, Float64MultiArray, Bool
from sensor_msgs.msg import Range
import time
import serial

l = 0.1          #длинна луча
velocity = 200    #скорость
cornerMotor_to_distance = 2105

x_pos, y_pos, theta_pos, l_enc, r_enc, yaw = 0,0,0,0,0,0
r_ping, l_ping, f_ping = 0,0,0
integral, prevErr = 0,0


pub_linear_y = rospy.Publisher('linear_y', Float64, queue_size=10)
pub_lmotor = rospy.Publisher('v_left', Float64, queue_size=10)
pub_bmotor = rospy.Publisher('v_back', Float64, queue_size=10)
pub_rmotor = rospy.Publisher('v_right', Float64, queue_size=10)
pub = rospy.Publisher('moveing', Bool, queue_size=1)



try:
    ser_navx = serial.Serial('/dev/ttyACM3')
except:
    try:
        ser_navx = serial.Serial('/dev/ttyACM2')
    except:
        try:
            ser_navx = serial.Serial('/dev/ttyACM1')
        except:
            ser_navx = serial.Serial('/dev/ttyACM0')




def x_y_local(x, y, corner_absolute=0):                       #перевод из мировых координат в локальные(относительно позиции робота)
    x_local = cos(corner_absolute)*x + sin(corner_absolute)*y
    y_local = cos(corner_absolute)*y - sin(corner_absolute)*x
    return x_local, y_local

def x_y_world(x, y, corner_absolute=0):                      #перевод из локальных координат в мировые
    x_world = cos(corner_absolute)*x - sin(corner_absolute)*y
    y_world = cos(corner_absolute)*y + sin(corner_absolute)*x
    return x_world, y_world

def v1v2v3(x_local, y_local, corner_change=0):             #формулы для расчета скоростей, относительно скорости Х и У
    v_l = -x_local/2 - sqrt(3)*y_local/2 + l*corner_change
    v_b = x_local + l*corner_change
    v_r = -x_local/2 + sqrt(3)*y_local/2 + l*corner_change
    return v_l, v_r, v_b

def v1v2v3_to_xylocal(v1, v2, v3):                       #скорости на моторы перевести в координаты Х У (не используется)
    x_local = (2*v2 - v1 - v3)/3
    y_local = ((sqrt(3))*v3 - sqrt(3)*v1)/3
    corner_change = (v1, v2, v3)/3
    return x_local, y_local, corner_change

def kinematik_local(xv, yv, corner_to_change=0):                   #публикует команды на моторы в топики
    global moveing
    moveing = True
    v1, v2, v3 = v1v2v3(xv, yv, corner_to_change)
    v2 = -v2
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v3)
    pub_bmotor.publish(v2)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    print(v1, v2, v3)

def kinematik_world(data):               #не готово
    pub.publish(Bool(False))
    x_plus_y = data.data[0] + data.data[1]
    xv = velocity * (data.data[0] / x_plus_y)
    yv = velocity * (data.data[1] / x_plus_y)
    time_move = x_plus_y / velocity
    if len(data.data) < 3:
        corner_change = 0
    else:
        corner_change = data.data[2]
    xv, yv = x_y_local(xv, yv)
    v1, v2, v3 = v1v2v3(xv, yv, corner_change)
    print(v1, v2, v3)
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    pub_bmotor.publish(v3)
    time.sleep(time_move)
    print('stop')
    pub.publish(Bool(True))


def stop():                                    #функция для остановки робота, публикует нули в топики
    for i in range(10):
        pub_lmotor.publish(0)
        pub_rmotor.publish(0)
        pub_bmotor.publish(0)
    print('stop')
    pub.publish(Bool(True))     #говорит, что остановился
    moveing = False

def move_local_time(x, y):                            #принимает Х, У; считает время, которое ему нужно двигаться; движется и останавливается 
    distance = sqrt(x**2+y**2)
    time_move = (distance / velocity ) * 100
    xv = (x/distance)*velocity
    yv = (y/distance)*velocity
    kinematik_local(xv, yv)
    time.sleep(time_move)
    stop()




def get_position_odom(odom_l, odom_r, odom_b):
    global x_pos, y_pos, theta_pos
    x_pos = (2*odom_b - odom_l - odom_r)/3 * cornerMotor_to_distance
    y_pos = (sqrt(3)*odom_r - sqrt(3)*odom_l)/3 * cornerMotor_to_distance
    theta_pos = (odom_l + odom_r + odom_b)/3*l

def get_yaw_navx():
    return float(ser_navx.readline()[2:9])


def left_enc(data):
    global l_enc
    l_enc = data.data
def right_enc(data):
    global r_enc
    r_enc = data.data
def front_ping(data):
    global f_ping
    f_ping = data.range
def left_ping(data):
    global l_ping
    l_ping = data.range
def right_ping(data):
    global r_ping
    r_ping = data.range



def move_local_odom(x, y):                            #принимает Х, У; движется по координатам и останавливается 
    distance = sqrt(x**2+y**2)
    xv = (x/distance)*velocity
    yv = (y/distance)*velocity
    kinematik_local(xv, yv)
    delta_x = 10
    delta_y = 10
    while (abs(delta_x) > 1 or abs(delta_y) > 1) and not rospy.is_shutdown():
        rospy.Subscriber('ENCL_POS', Float64, left_enc)
        rospy.Subscriber('ENCR_POS', Float64, right_enc)
        get_position_odom(l_enc, r_enc, 0)
        delta_x = x - x_pos
        delta_y = y - y_pos
        print('x: ', x_pos, end="      ")
        print('y: ', y_pos, end="      ")
        print("theta ", theta_pos)
    stop()



dt = 0.3

def vel_odom():
    global vel_left_odom, vel_right_odom
    rospy.Subscriber('ENCL_POS', Float64, left_enc)
    rospy.Subscriber('ENCR_POS', Float64, right_enc)
    time.sleep(0.1)
    left_last = l_enc
    right_last = r_enc
    time.sleep(1)
    rospy.Subscriber('ENCL_POS', Float64, left_enc)
    rospy.Subscriber('ENCR_POS', Float64, right_enc)
    time.sleep(0.1)
    vel_left_odom = (l_enc - left_last)
    vel_right_odom = (r_enc - right_last)
    print('L: ', vel_left_odom, 'R: ', vel_right_odom, 'L_enc: ', l_enc, "R_enc: ", r_enc)
    return vel_left_odom, vel_right_odom




kp= 0.7
kd = 0.0
ki = 0
def corect_left_motor(prevErr):
    vel_left_odom, vel_right_odom = vel_odom()
    err = vel_left_odom - vel_right_odom
    integ = err * dt
    d = (err - prevErr) / dt
    prevErr = err
    output =  err * kp + ki*integ + kd * 3
    pub_lmotor.publish(output)
    print(output)
    return prevErr


def pid(inp, setpoint, kp=20, ki=0.01, kd=10, dt=0.03):
    global integral, prevErr
    err = setpoint - inp
    integral = integral + err * dt * ki
    if integral > 255: integral = 255
    elif integral < -255: integral = -255
    D = (err - prevErr) / dt
    res = err * kp + integral + D * kd
   # if res > 255: res = 255
   # elif res < -255: res = -255
    prevErr = err
    return res
 



def move_forward_odom(distance):
    rospy.Subscriber('ENCL_POS', Float64, left_enc)
    rospy.Subscriber('ENCR_POS', Float64, right_enc)
    v1, v2, v3 = v1v2v3(0, velocity*0.7)
    err = (l_enc + r_enc)*0.1
    v1 = v1 - err
    v2 = v2 + err
    if v1 > 255: v1 = 255
    elif v1 < -255: v1 = -255
    if v2 > 255: v2 = 255
    elif v2 < -255: v2 = -255
    pub_lmotor.publish(v1)
    pub_rmotor.publish(v2)
    print(v1, v2, l_enc, r_enc, err)
    




def move_forward_navx(target_distance, target_yaw=0):
    v_left, v_right, v_back = v1v2v3(0, velocity)
    _, target_r,_ = v1v2v3(0, target_distance)
    target_r = target_r / cornerMotor_to_distance
    while r_enc < target_r*0.95 and not rospy.is_shutdown():
        now_yaw = get_yaw_navx()
        err = (now_yaw - target_yaw)*0.005
        v_left = velocity*(1-err)
        v_right = velocity*(-1-err)
        if v_left > 255: v_left = 255
        elif v_left < -255: v_left = -255
        if v_right > 255: v_right = 255
        elif v_right < -255: v_right = -255
        pub_lmotor.publish(v_left)
        pub_rmotor.publish(-v_right)
        pub_bmotor.publish(0)
        rospy.Subscriber('ENCR_POS', Float64, right_enc)
        print(v_left, v_right, now_yaw, err)
    stop()



def move_navx_odom(target_x, target_y, target_yaw=0):
    distance = sqrt(target_x**2+target_y**2)
    xv = (target_x/distance)*velocity
    yv = (target_y/distance)*velocity
    v_l, v_r, v_b = v1v2v3(xv, yv)
    rospy.Subscriber('ENCR_POS', Float64, left_enc)
    time.sleep(0.1)
    first_l_enc = l_enc
    target_l, target_r,_ = v1v2v3(target_x, target_y)
    print(target_r)
    target_l = target_l * cornerMotor_to_distance
    while abs(-l_enc+first_l_enc) < abs(target_l) and not rospy.is_shutdown():
        try:
            now_yaw = get_yaw_navx()
        except:
            pass
        err = (now_yaw - target_yaw)*0.02
        v_left = v_l+err*velocity
        v_right = v_r+err*velocity
        v_back = v_b+err*velocity
        if v_left > 255: v_left = 255
        elif v_left < -255: v_left = -255
        if v_right > 255: v_right = 255
        elif v_right < -255: v_right = -255
        if v_back > 255: v_back = 255
        elif v_back < -255: v_back = -255
        pub_lmotor.publish(v_left*0.6)
        pub_rmotor.publish(-v_right)
        pub_bmotor.publish(v_back*0.6)
        rospy.Subscriber('ENCR_POS', Float64, left_enc)
        print(now_yaw, v_left*0.6, v_right, v_back*0.6)
        print(l_enc,first_l_enc,  target_l)
        #time.sleep(0.1)
    stop()

def move_yaw(target_yaw):
    while not rospy.is_shutdown():
        try:
            now_yaw = get_yaw_navx()
        except:
            pass
        if abs(now_yaw - target_yaw) < 4:
            break
        err = pid(now_yaw, target_yaw, kp=1, ki=10, kd=0, dt=0.03)
        v_left = -err
        v_right = -err
        v_back = -err
        if v_left > 255: v_left = 255
        elif v_left < -255: v_left = -255
        if v_right > 255: v_right = 255
        elif v_right < -255: v_right = -255
        if v_back > 255: v_back = 255
        elif v_back < -255: v_back = -255
        pub_lmotor.publish(v_left*0.6)
        pub_rmotor.publish(-v_right)
        pub_bmotor.publish(v_back*0.6)
    stop()
    stop()
    stop()
    print('stop')



def move_navx_f_ping(target_x, target_y, target_f=0, target_l=0, target_r=0, dist_to_wall=True, target_yaw=0):
    distance = sqrt(target_x**2+target_y**2)
    xv = (target_x/distance)*velocity
    yv = (target_y/distance)*velocity
    v_l, v_r, v_b = v1v2v3(xv, yv)
    rospy.Subscriber('range_front_ping', Range, front_ping)
    rospy.Subscriber('range_left_ping', Range, left_ping)
    rospy.Subscriber('range_right_ping', Range, right_ping)
    time.sleep(0.05)
    if dist_to_wall:
        pass
    if target_y > 0:
        pass
    try:
        now_yaw = get_yaw_navx()
    except:
        pass

    while not rospy.is_shutdown():
        if target_y > 0:
            if target_f and (f_ping < target_f):
                print(f_ping)
                break
            elif target_l and (l_ping < target_l):
                break
            elif target_r and (r_ping < target_r):
                break
        elif target_y < 0:
            if target_f and (f_ping > target_f):
                break
            elif target_l and (l_ping > target_l):
                break
            elif target_r and (r_ping > target_r):
                break
        try:
            now_yaw = get_yaw_navx()
        except:
            pass
        err = pid(now_yaw, target_yaw)
        v_left = v_l-err
        v_right = v_r-err
        v_back = v_b-err
        if v_left > 255: v_left = 255
        elif v_left < -255: v_left = -255
        if v_right > 255: v_right = 255
        elif v_right < -255: v_right = -255
        if v_back > 255: v_back = 255
        elif v_back < -255: v_back = -255
        pub_lmotor.publish(v_left*0.6)
        pub_rmotor.publish(-v_right)
        pub_bmotor.publish(v_back*0.6)
        rospy.Subscriber('range_front_ping', Range, front_ping)
        rospy.Subscriber('range_left_ping', Range, left_ping)
        rospy.Subscriber('range_right_ping', Range, right_ping)
        print(now_yaw, v_left*0.6, v_right, v_back*0.6)
        #time.sleep(0.1)
    stop()
    while not rospy.is_shutdown():
        if abs(now_yaw - target_yaw) < 10:
            break
        try:
            now_yaw = get_yaw_navx()
        except:
            pass
        err = pid(now_yaw, target_yaw)
        v_left = -err
        v_right = -err
        v_back = -err
        if v_left > 255: v_left = 255
        elif v_left < -255: v_left = -255
        if v_right > 255: v_right = 255
        elif v_right < -255: v_right = -255
        if v_back > 255: v_back = 255
        elif v_back < -255: v_back = -255
        pub_lmotor.publish(v_left*0.6)
        pub_rmotor.publish(-v_right)
        pub_bmotor.publish(v_back*0.6)
    stop()
    stop()
    stop()




def main():                              #главный код
    global moveing
    rospy.init_node('kinematik')
    # print('x: ', x_pos)
    # print('y: ', y_pos)
    # print('theta: ', theta_pos)
    # print()
   # kinematik_local(100, 250)
   # time.sleep(2)
   # stop()
   # time.sleep(1)
   # kinematik_local(100, -250)
   # pub_bmotor.publish(200)
   # time.sleep(2)
    # move_local_time(-0.7,3)
    # time.sleep(2)
    # move_local_time(0.7,-3)
    #pub_rmotor.publish(150)
    #prevErr = 0
    #while not rospy.is_shutdown():
   # while not rospy.is_shutdown():
   #     a = input("Input x y theta: ").split()
   #     move_navx_f_ping(float(a[0]), float(a[1]), target_f=float(a[2]))
        #move_yaw(float(a[0]))
   # time.sleep(1)
   # move_navx(-0.5,0)
   # time.sleep(1)
   # move_navx(-0.7,0, -90)
   # time.sleep(1)
   # move_navx(-0.7, 0.7, 45)
   # time.sleep(1)
   # move_navx(0.2,-0.8, -30)
   # time.sleep(10)
   # move_navx(0.3, 0.5, -50)
   # time.sleep(1)
   # move_navx(0,0.5)
   # time.sleep(1)
   # move_navx(0.3, -0.5)
    time.sleep(15)
   # move_navx(-0.7,-0.2, 45)
    #while not rospy.is_shutdown():
    #    print(ser_navx.readline())
    #pub_linear_y.publish(50)
    move_navx_f_ping(0, 1, 25)

    stop()










if __name__ == '__main__':	
    try:
        main()
    except rospy.ROSInterruptException: pass
