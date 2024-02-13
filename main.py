# This class ties the engine and user input together, and draws the rotation process using matplotlib

# Importing math, matplotlib, and the other two files in the program, as they were used throughout this file
import math, matplotlib.pyplot as plt, matplotlib
import user_input, engine as engine

# Creating the rotation ditionary in which we store all the rotational matrix axis values
xyz_rotation_dict = {
  "x": 0,
  "y": 0,
  "z": 0,
}

# Counter variable used for the rotation process
completed_steps = 0

for axis in xyz_rotation_dict:
  xyz_rotation_dict[axis] = user_input.get_user_rotations(axis) # accepts user input for rotation
print("Rotation Speeds: \n x: " + str(xyz_rotation_dict["x"]) + "\n y: " + str(xyz_rotation_dict["y"]) + "\n z: " + str(xyz_rotation_dict["z"]))

# Using the user input from the user input file
user_shape = user_input.get_user_shape_3d() 
# A hard coded option needs to be changed to work for user input in 2d and 3d

# Plotting, drawing, and rotation process using matplotlib
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
while True:
  plt.pause(1/60) # Approximately 60 fps 
  ax.set_title('Rotation Matrix Visual')
  ax.set_xlim([-150, 150])
  ax.set_ylim([-150, 150])
  ax.set_zlim([-150, 150])
  completed_steps += 1
  engine.rotate(user_shape, xyz_rotation_dict, completed_steps, fig, ax)