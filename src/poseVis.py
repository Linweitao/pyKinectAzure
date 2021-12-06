import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json

index = 91

p3ds = []
out_file_json = "../pose_result/" + index + ".json"
with open(out_file_json) as f:
    line = f.readline()
    data = json.loads(line)
    print(data)

for joint in data:
    p3ds.append(joint["position3d"])
p3ds=np.array(p3ds)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(-2000, 2000)
ax.set_ylim3d(-2000, 2000)
ax.set_zlim3d(1000, 5000)

connections = [[1, 0],
               [2, 1],
               [3, 2],
               [4, 2],
               [5, 4],
               [6, 5],
               [7, 6],
               [8, 7],
               [9, 8],
               [10, 7],
               [11, 2],
               [12, 11],
               [13, 12],
               [14, 13],
               [15, 14],
               [16, 15],
               [17, 14],
               [18, 0],
               [19, 18],
               [20, 19],
               [21, 20],
               [22, 0],
               [23, 22],
               [24, 23],
               [25, 24],
               [26, 3],
               [27, 26],
               [28, 26],
               [29, 26],
               [30, 26],
               [31, 26]]
# dist = np.linalg.norm(p3ds[6] - p3ds[7])
# print("dist:")
# print(dist)
for _c in connections:
    # print(p3ds[_c[0]])
    # print(p3ds[_c[1]])
    ax.plot(xs=[p3ds[_c[0], 0], p3ds[_c[1], 0]], ys=[p3ds[_c[0], 1], p3ds[_c[1], 1]],
            zs=[p3ds[_c[0], 2], p3ds[_c[1], 2]], c='red')
ax.set_title('This figure can be rotated.')
# uncomment to see the triangulated pose. This may cause a crash if youre also using cv.imshow() above.
plt.show()
