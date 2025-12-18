---
title: "Module 6: Humanoid Kinematics"
sidebar_position: 6
---

# Module 6: Humanoid Kinematics

Welcome to the Humanoid Kinematics module! In this module, you'll learn the mathematical foundations for understanding and controlling humanoid robot movements. Kinematics is the study of motion without considering the forces that cause it, and it's essential for controlling humanoid robots.

## Learning Objectives

By the end of this module, you will be able to:
- Understand forward and inverse kinematics for humanoid robots
- Apply Denavit-Hartenberg (DH) parameters to humanoid structures
- Implement kinematic models for humanoid limbs
- Solve kinematic problems using analytical and numerical methods
- Understand the relationship between kinematics and robot control

## Prerequisites

- Completion of Modules 1-5
- Basic understanding of linear algebra and trigonometry
- Familiarity with coordinate systems and transformations
- Understanding of joint types and robot structures

## Table of Contents

1. [Introduction to Kinematics](#introduction-to-kinematics)
2. [Coordinate Systems and Transformations](#coordinate-systems-and-transformations)
3. [Forward Kinematics](#forward-kinematics)
4. [Inverse Kinematics](#inverse-kinematics)
5. [Denavit-Hartenberg Parameters](#denavit-hartenberg-parameters)
6. [Humanoid-Specific Kinematics](#humanoid-specific-kinematics)
7. [Kinematic Control](#kinematic-control)
8. [Applications in Humanoid Robotics](#applications-in-humanoid-robotics)

## Introduction to Kinematics

Kinematics is the branch of mechanics that describes the motion of objects without considering the forces that cause the motion. In robotics, kinematics deals with the relationship between joint positions and the position and orientation of the robot's end-effectors.

### Key Concepts

- **Forward Kinematics**: Calculating end-effector position/orientation from joint angles
- **Inverse Kinematics**: Calculating joint angles from desired end-effector position/orientation
- **Configuration Space**: The space of all possible joint configurations
- **Task Space**: The space of all possible end-effector positions/orientations

### Why Kinematics Matters for Humanoids

Humanoid robots have complex kinematic structures with multiple degrees of freedom (DOF) in each limb. Understanding kinematics is crucial for:
- Controlling limb movements
- Planning reaching and manipulation tasks
- Maintaining balance and stability
- Generating natural human-like motions

## Coordinate Systems and Transformations

### Homogeneous Transformations

Homogeneous transformations are used to represent both rotation and translation in a single 4x4 matrix:

```python
import numpy as np

def homogeneous_transform(rotation_matrix, translation_vector):
    """
    Create a 4x4 homogeneous transformation matrix
    """
    transform = np.eye(4)
    transform[0:3, 0:3] = rotation_matrix
    transform[0:3, 3] = translation_vector
    return transform

def rotation_x(angle):
    """Rotation matrix around X-axis"""
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])

def rotation_y(angle):
    """Rotation matrix around Y-axis"""
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])

def rotation_z(angle):
    """Rotation matrix around Z-axis"""
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
```

### Denavit-Hartenberg Convention

The Denavit-Hartenberg (DH) convention provides a systematic way to define coordinate frames on robot links:

```python
def dh_transform(a, alpha, d, theta):
    """
    Denavit-Hartenberg transformation matrix
    a: link length
    alpha: link twist
    d: link offset
    theta: joint angle
    """
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])
```

## Forward Kinematics

Forward kinematics calculates the end-effector position and orientation given the joint angles.

### Simple Planar Arm Example

```python
def planar_arm_fk(joint_angles, link_lengths):
    """
    Forward kinematics for a simple 2-DOF planar arm
    joint_angles: [theta1, theta2]
    link_lengths: [l1, l2]
    """
    theta1, theta2 = joint_angles
    l1, l2 = link_lengths

    # Calculate end-effector position
    x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)

    return np.array([x, y, 0])  # z=0 for planar arm
```

### 3D Arm Forward Kinematics

```python
class SerialArmFK:
    def __init__(self, dh_params):
        """
        Initialize with DH parameters
        dh_params: list of [a, alpha, d, theta] for each joint
        """
        self.dh_params = dh_params

    def forward_kinematics(self, joint_angles):
        """
        Calculate forward kinematics for a serial chain
        """
        transform = np.eye(4)  # Identity transformation

        for i, (a, alpha, d, _) in enumerate(self.dh_params):
            # Update theta with current joint angle
            theta = joint_angles[i] if i < len(joint_angles) else 0
            joint_transform = dh_transform(a, alpha, d, theta)
            transform = transform @ joint_transform

        return transform  # 4x4 transformation matrix

# Example: 3-DOF arm
dh_params = [
    [0.1, np.pi/2, 0.2, 0],    # Joint 1
    [0.3, 0, 0, 0],            # Joint 2
    [0.25, 0, 0, 0]            # Joint 3
]

arm = SerialArmFK(dh_params)
joint_angles = [np.pi/4, np.pi/6, -np.pi/3]
end_effector_pose = arm.forward_kinematics(joint_angles)
```

### Humanoid Limb Kinematics

```python
class HumanoidLimbFK:
    def __init__(self):
        # Typical humanoid arm DH parameters (simplified)
        self.right_arm_dh = [
            [0, np.pi/2, 0.2, 0],      # Shoulder yaw
            [0, -np.pi/2, 0, 0],       # Shoulder pitch
            [0.3, 0, 0, 0],            # Shoulder roll
            [0, np.pi/2, 0, 0],        # Elbow
            [0.25, 0, 0, 0]            # Wrist
        ]

    def right_arm_fk(self, joint_angles):
        """
        Forward kinematics for humanoid right arm
        joint_angles: [shoulder_yaw, shoulder_pitch, shoulder_roll, elbow, wrist]
        """
        transform = np.eye(4)

        for i, (a, alpha, d, _) in enumerate(self.right_arm_dh):
            if i < len(joint_angles):
                theta = joint_angles[i]
            else:
                theta = 0

            joint_transform = dh_transform(a, alpha, d, theta)
            transform = transform @ joint_transform

        return transform

    def left_arm_fk(self, joint_angles):
        """
        Forward kinematics for humanoid left arm
        Same as right but mirrored
        """
        # For simplicity, same as right arm (in practice, would account for mirroring)
        return self.right_arm_fk(joint_angles)
```

## Inverse Kinematics

Inverse kinematics (IK) calculates the joint angles required to achieve a desired end-effector position and orientation.

### Analytical Inverse Kinematics

For simple structures, analytical solutions may exist:

```python
def planar_arm_ik(target_pos, link_lengths):
    """
    Inverse kinematics for 2-DOF planar arm
    target_pos: [x, y] desired end-effector position
    link_lengths: [l1, l2]
    """
    x, y = target_pos
    l1, l2 = link_lengths

    # Calculate distance from origin to target
    r = np.sqrt(x**2 + y**2)

    # Check if target is reachable
    if r > l1 + l2:
        raise ValueError("Target position is out of reach")
    if r < abs(l1 - l2):
        raise ValueError("Target position is too close")

    # Calculate joint angles
    cos_theta2 = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
    sin_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sin_theta2, cos_theta2)

    k1 = l1 + l2 * cos_theta2
    k2 = l2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return np.array([theta1, theta2])
```

### Numerical Inverse Kinematics

For complex structures, numerical methods are often necessary:

```python
from scipy.optimize import minimize

def numerical_ik(target_pose, initial_joints, fk_function, max_iter=1000):
    """
    Numerical inverse kinematics using optimization
    """
    def objective(joint_angles):
        # Calculate current pose
        current_pose = fk_function(joint_angles)

        # Calculate error (position and orientation)
        pos_error = np.linalg.norm(target_pose[0:3, 3] - current_pose[0:3, 3])

        # Simple orientation error (this can be improved)
        rot_error = np.linalg.norm(target_pose[0:3, 0:3] - current_pose[0:3, 0:3])

        return pos_error + 0.1 * rot_error  # Weight position more than orientation

    result = minimize(objective, initial_joints, method='BFGS')

    if result.success:
        return result.x
    else:
        raise ValueError("IK solution not found")
```

### Jacobian-Based Methods

The Jacobian matrix relates joint velocities to end-effector velocities:

```python
def calculate_jacobian(fk_func, joint_angles, epsilon=1e-6):
    """
    Calculate Jacobian matrix using finite differences
    """
    n_joints = len(joint_angles)

    # Calculate base pose
    base_pose = fk_func(joint_angles)
    base_pos = base_pose[0:3, 3]

    jacobian = np.zeros((6, n_joints))  # 6 DOF: 3 pos + 3 rot

    for i in range(n_joints):
        # Perturb joint angle
        perturbed_angles = joint_angles.copy()
        perturbed_angles[i] += epsilon

        # Calculate perturbed pose
        perturbed_pose = fk_func(perturbed_angles)
        perturbed_pos = perturbed_pose[0:3, 3]

        # Calculate position change
        pos_change = (perturbed_pos - base_pos) / epsilon
        jacobian[0:3, i] = pos_change

    return jacobian

def jacobian_ik_step(jacobian, target_velocity, alpha=0.01):
    """
    Single step of Jacobian-based IK
    """
    # Use pseudo-inverse to solve for joint velocities
    joint_velocities = np.linalg.pinv(jacobian) @ target_velocity
    return alpha * joint_velocities
```

## Denavit-Hartenberg Parameters

### DH Parameter Definition

The Denavit-Hartenberg convention defines four parameters for each joint:

1. **a_i** (link length): Distance along x_i from z_i to z_{i+1}
2. **α_i** (link twist): Angle between z_i and z_{i+1} around x_i
3. **d_i** (link offset): Distance along z_i from x_i to x_{i+1}
4. **θ_i** (joint angle): Angle between x_i and x_{i+1} around z_i

### Humanoid DH Parameter Examples

```python
class HumanoidDHParams:
    def __init__(self):
        # Right arm DH parameters (simplified)
        self.right_arm = [
            [0, np.pi/2, 0.2, 0],      # Shoulder (yaw)
            [0, -np.pi/2, 0, 0],       # Shoulder (pitch)
            [0.3, 0, 0, 0],            # Shoulder (roll)
            [0, np.pi/2, 0, 0],        # Elbow
            [0.25, 0, 0, 0]            # Wrist
        ]

        # Left arm DH parameters (mirrored)
        self.left_arm = [
            [0, np.pi/2, 0.2, 0],      # Shoulder (yaw)
            [0, -np.pi/2, 0, 0],       # Shoulder (pitch)
            [-0.3, 0, 0, 0],           # Shoulder (roll) - negative for left arm
            [0, np.pi/2, 0, 0],        # Elbow
            [0.25, 0, 0, 0]            # Wrist
        ]

        # Right leg DH parameters
        self.right_leg = [
            [0, np.pi/2, 0.1, 0],      # Hip (yaw)
            [0, -np.pi/2, 0, 0],       # Hip (pitch)
            [0, 0, 0.4, 0],            # Hip (roll)
            [0, np.pi/2, 0, 0],        # Knee
            [0, 0, 0.4, 0]             # Ankle
        ]

    def get_chain_transform(self, dh_params, joint_angles):
        """
        Calculate transformation for a kinematic chain
        """
        transform = np.eye(4)

        for i, (a, alpha, d, _) in enumerate(dh_params):
            theta = joint_angles[i] if i < len(joint_angles) else 0
            joint_transform = dh_transform(a, alpha, d, theta)
            transform = transform @ joint_transform

        return transform
```

## Humanoid-Specific Kinematics

### Whole-Body Kinematics

Humanoid robots have multiple kinematic chains that must work together:

```python
class HumanoidKinematics:
    def __init__(self):
        self.dh_params = HumanoidDHParams()
        self.torso_height = 0.6  # Height of torso from ground

    def calculate_all_poses(self, joint_angles_dict):
        """
        Calculate poses for all limbs given joint angles
        joint_angles_dict: dictionary with keys like 'right_arm', 'left_arm', etc.
        """
        poses = {}

        # Calculate torso pose (assuming fixed for now)
        torso_transform = np.eye(4)
        torso_transform[2, 3] = self.torso_height  # Height offset

        # Calculate right arm pose
        if 'right_arm' in joint_angles_dict:
            right_arm_transform = self.dh_params.get_chain_transform(
                self.dh_params.right_arm,
                joint_angles_dict['right_arm']
            )
            poses['right_arm'] = torso_transform @ right_arm_transform

        # Calculate left arm pose
        if 'left_arm' in joint_angles_dict:
            left_arm_transform = self.dh_params.get_chain_transform(
                self.dh_params.left_arm,
                joint_angles_dict['left_arm']
            )
            poses['left_arm'] = torso_transform @ left_arm_transform

        # Calculate right leg pose
        if 'right_leg' in joint_angles_dict:
            right_leg_transform = self.dh_params.get_chain_transform(
                self.dh_params.right_leg,
                joint_angles_dict['right_leg']
            )
            # Right leg attaches at hip (different base transform)
            hip_transform = torso_transform.copy()
            hip_transform[0, 3] = 0.1  # Slight offset
            poses['right_leg'] = hip_transform @ right_leg_transform

        return poses

    def center_of_mass(self, joint_angles_dict, link_masses):
        """
        Calculate approximate center of mass
        """
        poses = self.calculate_all_poses(joint_angles_dict)
        total_mass = sum(link_masses.values())

        weighted_pos = np.zeros(3)
        for link_name, pose in poses.items():
            if link_name in link_masses:
                link_pos = pose[0:3, 3]  # Extract position
                weighted_pos += link_masses[link_name] * link_pos

        com = weighted_pos / total_mass if total_mass > 0 else np.zeros(3)
        return com
```

### Balance and Stability

Maintaining balance is critical for humanoid robots:

```python
def calculate_zmp(pose, com_height=0.8, gravity=9.81):
    """
    Calculate Zero Moment Point (ZMP) for balance
    """
    # Simplified ZMP calculation
    # ZMP_x = CoM_x - (CoM_height / gravity) * CoM_acc_x
    # For static case with no acceleration:
    com_pos = pose[0:3, 3]
    zmp = com_pos.copy()
    zmp[2] = 0  # Project to ground plane

    return zmp

def check_stability(zmp, support_polygon):
    """
    Check if ZMP is within support polygon
    """
    # Simplified stability check (convex hull check in practice)
    # For biped, support polygon is area between feet
    zmp_x, zmp_y = zmp[0], zmp[1]

    # Define support polygon (simplified as rectangle between feet)
    foot_separation = 0.2  # Distance between feet
    support_x_min, support_x_max = -0.1, 0.1
    support_y_min, support_y_max = -foot_separation/2, foot_separation/2

    is_stable = (support_x_min <= zmp_x <= support_x_max and
                 support_y_min <= zmp_y <= support_y_max)

    return is_stable
```

## Kinematic Control

### Operational Space Control

Control end-effectors in Cartesian space:

```python
class OperationalSpaceController:
    def __init__(self, robot_model):
        self.robot = robot_model

    def compute_control(self, desired_pose, current_pose, Kp=100, Kd=20):
        """
        Compute operational space control
        """
        # Calculate pose error
        pos_error = desired_pose[0:3, 3] - current_pose[0:3, 3]
        rot_error = self.rotation_error(desired_pose[0:3, 0:3],
                                       current_pose[0:3, 0:3])

        # Calculate desired velocity
        desired_vel = np.zeros(6)  # 3 pos + 3 rot
        desired_vel[0:3] = Kp * pos_error
        desired_vel[3:6] = Kp * rot_error

        # Calculate Jacobian
        jacobian = self.robot.calculate_jacobian()

        # Calculate joint velocities
        joint_velocities = np.linalg.pinv(jacobian) @ desired_vel

        return joint_velocities

    def rotation_error(self, R_desired, R_current):
        """
        Calculate rotation error using angle-axis representation
        """
        R_error = R_desired @ R_current.T
        angle_axis = self.rotation_matrix_to_angle_axis(R_error)
        return angle_axis

    def rotation_matrix_to_angle_axis(self, R):
        """
        Convert rotation matrix to angle-axis representation
        """
        trace = np.trace(R)
        angle = np.arccos(np.clip((trace - 1) / 2, -1, 1))

        if angle < 1e-6:
            return np.zeros(3)

        axis = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1]
        ]) / (2 * np.sin(angle))

        return angle * axis
```

### Trajectory Generation

Smooth trajectories for kinematic control:

```python
def cubic_trajectory(start_pos, end_pos, duration, current_time):
    """
    Generate smooth cubic trajectory
    """
    if current_time >= duration:
        return end_pos, 0, 0  # Final position, zero velocity, zero acceleration

    t = current_time / duration
    t2 = t * t
    t3 = t2 * t

    # Cubic polynomial coefficients for smooth start/stop
    a0 = start_pos
    a1 = 0  # Zero initial velocity
    a2 = 3 * (end_pos - start_pos) / (duration**2)
    a3 = -2 * (end_pos - start_pos) / (duration**3)

    pos = a0 + a1*t + a2*t2 + a3*t3
    vel = a1 + 2*a2*t + 3*a3*t2
    acc = 2*a2 + 6*a3*t

    return pos, vel, acc

def generate_joint_trajectory(ik_solver, waypoints, time_per_waypoint=1.0):
    """
    Generate joint trajectory through waypoints
    """
    trajectory = []
    current_joints = np.zeros(ik_solver.n_joints)  # Starting configuration

    for i, waypoint in enumerate(waypoints):
        # Solve IK for this waypoint
        target_joints = ik_solver.inverse_kinematics(waypoint, current_joints)

        # Generate trajectory to this joint configuration
        joint_trajectory = cubic_trajectory(
            current_joints, target_joints, time_per_waypoint, 0
        )

        trajectory.append({
            'time': i * time_per_waypoint,
            'joints': target_joints,
            'waypoint': waypoint
        })

        current_joints = target_joints

    return trajectory
```

## Applications in Humanoid Robotics

### Walking Pattern Generation

```python
class WalkingPatternGenerator:
    def __init__(self, step_length=0.3, step_height=0.1, step_time=0.8):
        self.step_length = step_length
        self.step_height = step_height
        self.step_time = step_time

    def generate_step_trajectory(self, start_pos, direction, step_number):
        """
        Generate trajectory for a single step
        """
        # Calculate step target
        target_pos = start_pos + direction * self.step_length

        # Generate foot trajectory (cycloid for smooth motion)
        t = np.linspace(0, self.step_time, 100)
        x_traj = start_pos[0] + (target_pos[0] - start_pos[0]) * (t / self.step_time)
        z_traj = start_pos[2] + self.step_height * (1 - np.cos(np.pi * t / self.step_time))

        return np.column_stack([x_traj, start_pos[1] * np.ones(len(t)), z_traj])
```

### Manipulation Planning

```python
def plan_reaching_motion(robot, target_pos, start_joints):
    """
    Plan reaching motion using IK
    """
    # Use numerical IK to find joint configuration for target
    def fk_with_joints(joints):
        # This would use the robot's FK implementation
        return robot.forward_kinematics(joints)

    def ik_objective(joints):
        current_pos = fk_with_joints(joints)[0:3, 3]
        error = np.linalg.norm(target_pos - current_pos)
        return error

    from scipy.optimize import minimize
    result = minimize(ik_objective, start_joints, method='BFGS')

    if result.success:
        return result.x
    else:
        raise ValueError("Could not find reaching configuration")
```

## Summary

In this module, you've learned:
- The mathematical foundations of forward and inverse kinematics
- How to use homogeneous transformations and DH parameters
- Techniques for solving both analytical and numerical IK problems
- How to apply kinematics specifically to humanoid robot structures
- Methods for kinematic control and trajectory generation
- Applications of kinematics in humanoid robotics

Kinematics forms the foundation for all movement in humanoid robots, enabling precise control of limbs and maintaining balance during complex tasks.

## Next Steps

In the next module, we'll explore motion planning, where you'll learn how to plan complex movements for humanoid robots in dynamic environments.

---

## APA Citations

- Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson Prentice Hall.
- Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. John Wiley & Sons.
- Siciliano, B., & Khatib, O. (Eds.). (2016). *Springer Handbook of Robotics* (2nd ed.). Springer.
- Murray, R. M., Li, Z., & Sastry, S. S. (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.
- Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer.