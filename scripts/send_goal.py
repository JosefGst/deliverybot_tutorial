#!/usr/bin/env python

import rospy
import sys
import tf_conversions
import actionlib
from std_srvs.srv import Empty
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from actionlib_msgs.msg import GoalID
import geometry_msgs.msg
import time

global clear_costmap

start = [2.0, -1.0, 0.623545105957, 0.781787375721]
end_goal = [3.0, 3.0, -0.869922159932, 0.493189046573]

    

def movebase_client(x, y, z, w):
	"""
	:param x: the x goal coordintate
	:param y: the y goal coordintate
	:param z: the z value for the orientation in quaternion
    :param w: the w value for the orientation in quaternion
	the other positon and orientation values should be always 0 in the 2D plane.
	"""
	client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()

	goal.target_pose.pose.position.x = x
	goal.target_pose.pose.position.y = y
	goal.target_pose.pose.position.z = 0.0

	# quat = tf_conversions.transformations.quaternion_from_euler(
	# 	0.0,
	# 	0.0,
	# 	a
	# )

	goal.target_pose.pose.orientation.x = 0.0
	goal.target_pose.pose.orientation.y = 0.0
	goal.target_pose.pose.orientation.z = z
	goal.target_pose.pose.orientation.w = w
	
	client.send_goal(goal)
	wait = client.wait_for_result()
	rospy.loginfo("Sent Goal")
	if not wait:
		client.cancel_goal()
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available!")
	else:
		return client.get_result()

def execute_delivery():
	clear_costmap.call()
	
	# while not rospy.is_shutdown():
	movebase_client(start[0], start[1], start[2], start[3])
	movebase_client(end_goal[0], end_goal[1], end_goal[2], end_goal[3])
	time.sleep(3) 
	# return to Start
	movebase_client(start[0], start[1], start[2], start[3])
	return True


def cancle_move_base():
	cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=2)
	cancel_msg = GoalID()
	cancel_msg.id = ""
	cancel_pub.publish(cancel_msg)


		
if __name__ == "__main__":
	rospy.init_node("movebase_client_py")
	clear_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
	result = execute_delivery()