# This class is the user input file that uses the console to obtain rotation degree for x, y, and z from the user

# Used to get the rotation degree from the user
def get_user_rotations(axis):
  rotationspeed = int(input("how many degrees do you want to rotate per step in the "+ axis + " axis: "))
  return rotationspeed

# Returns hard coded 3d shape
def get_user_shape_3d():
  user_shape_test =[ [100,100,100],[100,-100,100],[-100,-100,100],[-100,100,100],[100,100,-100],[100,-100,-100],[-100,-100,-100],[-100,100,-100] ]
  return user_shape_test

# Not necessary for current rotation - left empty
# Can be utilized in the future for 2D rotation, so it stays included
def get_user_shape_2d():
  pass