import cv2 as cv
import numpy as np
import math


x_points = []
y_points = []


def mouse_callback(event, x, y, flags, param):
    if (event == cv.EVENT_LBUTTONUP) :
        print("x :", x, "y :", y)
        x_points.append(x)
        y_points.append(y)


def distance(a, b):
    result = math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))
    return result


path = './org/height.png'
img = cv.imread(path)
cv.namedWindow('image')
cv.setMouseCallback('image', mouse_callback)

while(True):
        cv.imshow('image', img)
        k = cv.waitKey(1) & 0xFF    
        if k == 27:
            break
cv.destroyAllWindows()

# 1. 양쪽 vanish point를 차례대로 찍는다
# 2. b와 br을 찍는다
# 3. t와 tr을 찍는다

# vanishing line 만들기
vanishing_point1 = np.array([x_points[0], y_points[0], 1]).T
vanishing_point2 = np.array([x_points[1], y_points[1], 1]).T
b = np.array([x_points[2], y_points[2], 1]).T
# p = np.array([x_points[4], y_points[4]+50, 1])
br = np.array([x_points[3], y_points[3], 1]).T
t = np.array([x_points[4], y_points[4], 1]).T
tr = np.array([x_points[5], y_points[5], 1]).T
p = np.cross(t, b).T

l = np.cross(vanishing_point1, vanishing_point2)

hr = 201

# i = (p x b) x (tr x (l x (br x b)))

br_b = np.cross(br, b)  # (br x b) 직선
q = np.cross(l, br_b)  # (l x (br x b) 점
q = q / q[2]
print("q : ", q)   # -> 대략 (x : 99 y : 404) 언저리 나오면 됨.
tr_l_br_b = np.cross(tr, q)    # (tr x (l x (br x b))) 직선
p_b = np.cross(p, b)    # (p x b) 직선
t_b = np.cross(t, b)
i = np.cross(t_b, tr_l_br_b)    # 점
i = i / i[2]
# i = np.array([714, 343, 1]) # -> 이 값 넣으면 맞게 추정
print("i : ", i)

# (xw 1).T = H(xi 1).T
H = np.array([[hr * (distance(p, b) - distance(i, b)), 0],
              [-distance(i, b), distance(p, b) * distance(i, b)]])

s = np.dot(H, np.array([distance(t, b), 1]))

print("s : ", s)

h = s[0]/s[1]

print("height : ", h)


