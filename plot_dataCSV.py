import matplotlib.pyplot as plt
import numpy as np

file_name = 'test.csv' 
file_path = './plot_data/' + file_name

print(f"Loading data from {file_path}...")

#need to skip row and use columns 0-5 to avoid saving variable that can not cast to double
all_data = np.loadtxt(file_path, delimiter=',', skiprows=1, usecols=(0,1,2,3,4,5))

#slice the columns by index (0=x,1=y,2=z,3=roll,4=pitch,5=yaw)
x_translation = all_data[:, 0]
y_translation = all_data[:, 1]
z_translation = all_data[:, 2]

roll_rotation = all_data[:, 3]
pitch_rotation = all_data[:, 4]
yaw_rotation  = all_data[:, 5]

print(f"Data points loaded: {len(x_translation)}")


#median
x_median = float(np.median(x_translation))
y_median = float(np.median(y_translation))
z_median = float(np.median(z_translation))
xyz_medians = [x_median, y_median, z_median]

roll_median = float(np.median(roll_rotation))
pitch_median = float(np.median(pitch_rotation))
yaw_median = float(np.median(yaw_rotation))
rpy_medians = [roll_median, pitch_median, yaw_median]

#std deviation
x_stddev = float(np.std(x_translation))
y_stddev = float(np.std(y_translation))
z_stddev = float(np.std(z_translation))
xyz_stddev = [x_stddev, y_stddev, z_stddev] 

roll_stddev = float(np.std(roll_rotation))
pitch_stddev = float(np.std(pitch_rotation))
yaw_stddev = float(np.std(yaw_rotation))
rpy_stddev = [roll_stddev, pitch_stddev, yaw_stddev]

#mean
x_mean = float(np.mean(x_translation))
y_mean = float(np.mean(y_translation))
z_mean = float(np.mean(z_translation))
xyz_means = [x_mean, y_mean, z_mean]

roll_mean = float(np.mean(roll_rotation))
pitch_mean = float(np.mean(pitch_rotation))
yaw_mean = float(np.mean(yaw_rotation))
rpy_means = [roll_mean, pitch_mean, yaw_mean]

print("-" * 30)
print("Translation Stats (X, Y, Z):")
print("Mean:   ", xyz_means)
print("Median: ", xyz_medians)
print("StdDev: ", xyz_stddev)

print("-" * 30)
print("Rotation Stats (Roll, Pitch, Yaw):")
print("Mean:   ", rpy_means)
print("Median: ", rpy_medians)
print("StdDev: ", rpy_stddev)
print("-" * 30)

y_x = [-1] * len(x_translation)
y_y = [0] * len(y_translation)
y_z = [1] * len(z_translation)

y_roll = [-1] * len(roll_rotation)
y_pitch = [0] * len(pitch_rotation)
y_yaw = [1] * len(yaw_rotation)


fig, axs = plt.subplots(6, 1, figsize=(10, 10), constrained_layout=True)
fig.suptitle(file_name)

y_zeros = [0] * len(x_translation)

axs[0].scatter(x_translation, y_zeros, c='b', marker='x', alpha=0.5)
axs[0].set_title("X Translation")
axs[0].set_xlabel("meters")
axs[0].set_yticks([]) # Hide Y-axis ticks since they are just 0

axs[1].scatter(y_translation, y_zeros, c='g', marker='x', alpha=0.5)
axs[1].set_title("Y Translation")
axs[1].set_xlabel("meters")
axs[1].set_yticks([])

axs[2].scatter(z_translation, y_zeros, c='r', marker='x', alpha=0.5)
axs[2].set_title("Z Translation")
axs[2].set_xlabel("meters")
axs[2].set_yticks([])

axs[3].scatter(roll_rotation, y_zeros, c='b', marker='x', alpha=0.5)
axs[3].set_title("Roll Rotation")
axs[3].set_xlabel("degrees")
axs[3].set_yticks([]) # Hide Y-axis ticks since they are just 0

axs[4].scatter(pitch_rotation, y_zeros, c='g', marker='x', alpha=0.5)
axs[4].set_title("Pitch Rotation")
axs[4].set_xlabel("degrees")
axs[4].set_yticks([])

axs[5].scatter(yaw_rotation, y_zeros, c='r', marker='x', alpha=0.5)
axs[5].set_title("Yaw Rotation")
axs[5].set_xlabel("degrees")
axs[5].set_yticks([])

plt.show()