

"""This file is dedicated to performing the suggested logic for the movement vitamins"""


def suggest_vitamins(screening):
    target_areas = []
    focus_areas = []
    squat_tag = ""

    # Shoulder Rotation
    if screening.shoulder_rotation == "N":
        target_areas.append("Shoulder Rotation")
    elif screening.shoulder_rotation == "L":
        target_areas.append("Shoulder Rotation")
        focus_areas.append("Left Shoulder Rotation")
    elif screening.shoulder_rotation == "R": 
        target_areas.append("Shoulder Rotation")
        focus_areas.append("Right Shoulder Rotation")

    # Ankle Mobility
    if screening.ankle_mobility == "N":
        target_areas.append("Ankle")
    elif screening.ankle_mobility == "L":
        target_areas.append("Ankle")
        focus_areas.append("Left Ankle Mobility")
    elif screening.ankle_mobility == "R":
        target_areas.append("Ankle")
        focus_areas.append("Right Ankle Mobility")

    # Ankle Stability
    if screening.foot_collapse == "Y":
        target_areas.append("Ankle")
        focus_areas.append("Ankle Stability")
    if screening.foot_collapse == "L":
        target_areas.append("Ankle")
        focus_areas.append("Left Ankle Stability")
    if screening.foot_collapse == "R":
        target_areas.append("Ankle")
        focus_areas.append("Right Ankle Stability")
        
    # Shoulder Flexion
    if screening.shoulder_flexion == "N":
        target_areas.append("Shoulder Flexion")
    elif screening.shoulder_flexion == "L":
        target_areas.append("Shoulder Flexion")
        focus_areas.append("Left Shoulder Flexion")
    elif screening.shoulder_flexion == "R":
        target_areas.append("Shoulder Flexion")
        focus_areas.append("Right Shoulder Flexion")

    # Hip Mobility (supine squat)
    if screening.supine_squat == "N":
        target_areas.append("Hips")

    # Hip Mobility (Active Straight Leg Raise)
    if screening.leg_raise == "N":
        target_areas.append("Hips")
    elif screening.leg_raise == "L":
        target_areas.append("Hips")
        focus_areas.append("Left Hip Mobility")
    elif screening.leg_raise == "R":
        target_areas.append("Hips")
        focus_areas.append("Left Hip Mobility")
    
    # Hip Stability (Overhead Squat)
    if screening.overhead_squat == "N":
        target_areas.append("Hips")
        focus_areas.append("Hip Stability")

    # Upper Body Stability (shoulder_rotation)
    if screening.shoulder_rotation in ["L", "N", "R"]:
        target_areas.append("Upper Body")


    # calculate squat tag
    if screening.overhead_squat == "Y":
        squat_tag == "Back Squat"
    elif screening.arms_extended_squat == "Y" and screening.foot_collapse == "Y":
        squat_tag == "Back Squat"
    elif screening.arms_extended_squat == "Y" and screening.foot_collapse != "Y":
        squat_tag == "Front Squat"
    else:
        squat_tag == "Goblet Squat/Hex Bar Deadlift"

    return target_areas, focus_areas, squat_tag