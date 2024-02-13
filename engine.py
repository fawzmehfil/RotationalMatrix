# This class does all the calculations for the rotation matrix

# Importing math and matplotlib as they were used throughout this file
import math, matplotlib.pyplot as plt, matplotlib

# Calculating the rotation process
def rotate(points, xyz_rotation_dict, completed_steps, fig, ax):
  new_points = []

# Assigning the rotation values based off user input, as accepted from the console
  rotation_degree_x = (xyz_rotation_dict["x"]*completed_steps) % 360
  rotation_degree_y = (xyz_rotation_dict["y"]*completed_steps) % 360
  rotation_degree_z = (xyz_rotation_dict["z"]*completed_steps) % 360

  # Calculating the positions for each new point
  for point in points:
    new_point = rotate_around_x(point, rotation_degree_x)
    new_point = rotate_around_y(new_point, rotation_degree_y)
    new_point = rotate_around_z(new_point, rotation_degree_z)
    new_points.append(new_point)
    
  # Re-draw all points at the same time
  draw(new_points, fig, ax)

# Do the next cycle of rotation
# rotate(new_points, xyz_rotation_dict, completed_steps)
# Cannot be left here because RecursionError occurs incredibly fast and wont work for long times

# Finalizing and displaying the x rotation
def rotate_around_x(point, rotation_degree_x):
  rotated_point = []
  rotated_point.append(point[0]) # not affected at all
  rotated_point.append(point[1] * math.cos(math.radians(rotation_degree_x)) - point[2] * math.sin(math.radians(rotation_degree_x)))
  rotated_point.append(point[1] * math.sin(math.radians(rotation_degree_x)) + point[2] * math.cos(math.radians(rotation_degree_x)))
  return rotated_point

# Finalizing and displaying the y rotation
def rotate_around_y(rotated_point, rotation_degree_y):
  new_rotated_point = []
  new_rotated_point.append(rotated_point[0] * math.cos(math.radians(rotation_degree_y)) + rotated_point[2] * math.sin(math.radians(rotation_degree_y)))
  new_rotated_point.append(rotated_point[1]) # not affected at all
  new_rotated_point.append(0 - rotated_point[0] * math.sin(math.radians(rotation_degree_y)) + rotated_point[2] * math.cos(math.radians(rotation_degree_y)))
  return new_rotated_point

# Finalizing and displaying the z rotation
def rotate_around_z(rotated_point, rotation_degree_z):
  new_rotated_point = []
  new_rotated_point.append(rotated_point[0] * math.cos(math.radians(rotation_degree_z)) - rotated_point[1] * math.sin(math.radians(rotation_degree_z)))
  new_rotated_point.append(rotated_point[0] * math.sin(math.radians(rotation_degree_z)) + rotated_point[1] * math.cos(math.radians(rotation_degree_z)))
  new_rotated_point.append(rotated_point[2]) # not affected at all
  return new_rotated_point

# Drawing all the points onto the display
def draw(points, fig, ax):
  ax.clear()
  draw_points_x,draw_points_y,draw_points_z = [],[],[]
  for spot_in_points in range(len(points)):
    draw_points_x.append(points[spot_in_points][0])
    draw_points_y.append(points[spot_in_points][1])
    draw_points_z.append(points[spot_in_points][2])

# This makes the lines connect top to bottom aswell for the appearance
  connector_lines_x,connector_lines_y,connector_lines_z = [],[],[]
  for i in range(4): 
    connector_lines_x.append(points[i][0])
    connector_lines_y.append(points[i][1])
    connector_lines_z.append(points[i][2])
    connector_lines_x.append(points[i+4][0])
    connector_lines_y.append(points[i+4][1])
    connector_lines_z.append(points[i+4][2])
    
  # Plots all the connector lines
  plt.plot(connector_lines_x,connector_lines_y,connector_lines_z,'b-')
  
  # Plots all the points
  plt.plot(draw_points_x, draw_points_y, draw_points_z, "b-")

# Draws all of the points
  ax.set_xlim([-150, 150])
  ax.set_ylim([-150, 150])
  ax.set_zlim([-150, 150])
  fig.canvas.draw()