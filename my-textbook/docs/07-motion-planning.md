---
title: "Module 7: Motion Planning for Humanoid Robots"
sidebar_position: 7
---

# Module 7: Motion Planning for Humanoid Robots

Welcome to the Motion Planning module! In this module, you'll learn how to plan complex movements for humanoid robots in dynamic environments. Motion planning is essential for enabling humanoid robots to navigate, manipulate objects, and perform complex tasks safely and efficiently.

## Learning Objectives

By the end of this module, you will be able to:
- Understand the fundamentals of motion planning for humanoid robots
- Implement sampling-based planning algorithms (RRT, RRT*)
- Apply optimization-based motion planning techniques
- Handle dynamic environments and real-time replanning
- Integrate motion planning with humanoid kinematics and control
- Address humanoid-specific planning challenges

## Prerequisites

- Completion of Modules 1-6
- Understanding of humanoid kinematics and control
- Basic knowledge of graph algorithms and optimization
- Familiarity with collision detection concepts

## Table of Contents

1. [Introduction to Motion Planning](#introduction-to-motion-planning)
2. [Configuration Space and Obstacles](#configuration-space-and-obstacles)
3. [Sampling-Based Planning](#sampling-based-planning)
4. [Optimization-Based Planning](#optimization-based-planning)
5. [Dynamic Motion Planning](#dynamic-motion-planning)
6. [Humanoid-Specific Planning Challenges](#humanoid-specific-planning-challenges)
7. [Integration with Control Systems](#integration-with-control-systems)
8. [Applications in Humanoid Robotics](#applications-in-humanoid-robotics)

## Introduction to Motion Planning

Motion planning is the computational problem of finding a valid sequence of movements for a robot to navigate from a start configuration to a goal configuration while avoiding obstacles.

### Key Concepts

- **Configuration Space (C-space)**: The space of all possible robot configurations
- **Free Space**: The portion of C-space where the robot doesn't collide with obstacles
- **Path Planning**: Finding a collision-free path in C-space
- **Trajectory Planning**: Adding time and dynamics to a path
- **Replanning**: Adjusting plans when the environment changes

### Motion Planning Pipeline

```python
class MotionPlanner:
    def __init__(self):
        self.collision_checker = None
        self.start_config = None
        self.goal_config = None
        self.obstacles = []

    def plan_motion(self, start, goal, environment):
        """
        Complete motion planning pipeline
        """
        # 1. Define configuration space
        c_space = self.define_configuration_space()

        # 2. Identify obstacles in C-space
        c_obstacles = self.map_obstacles_to_cspace(environment)

        # 3. Plan path in free space
        path = self.find_path(start, goal, c_space, c_obstacles)

        # 4. Optimize trajectory
        trajectory = self.optimize_trajectory(path)

        return trajectory

    def define_configuration_space(self):
        """
        Define the configuration space based on robot DOF
        """
        # For humanoid: 26+ DOF (legs, arms, torso, head)
        # Each joint contributes to configuration space
        pass

    def map_obstacles_to_cspace(self, environment):
        """
        Map Cartesian space obstacles to configuration space
        """
        # Complex mapping for multi-DOF systems
        pass

    def find_path(self, start, goal, c_space, c_obstacles):
        """
        Find collision-free path in configuration space
        """
        pass

    def optimize_trajectory(self, path):
        """
        Convert path to time-parameterized trajectory
        """
        pass
```

## Configuration Space and Obstacles

### Configuration Space Representation

For humanoid robots, the configuration space is high-dimensional and complex:

```python
import numpy as np

class HumanoidConfigurationSpace:
    def __init__(self):
        # Typical humanoid DOF breakdown
        self.dof = {
            'left_leg': 6,    # hip, knee, ankle (3 each)
            'right_leg': 6,
            'left_arm': 7,    # shoulder, elbow, wrist (various DOF)
            'right_arm': 7,
            'torso': 6,       # 6 DOF for torso movement
            'head': 3         # neck joints
        }

    def get_total_dof(self):
        return sum(self.dof.values())

    def is_collision_free(self, configuration, obstacles):
        """
        Check if a configuration is collision-free
        """
        # Convert configuration to robot pose
        robot_pose = self.forward_kinematics(configuration)

        # Check each link against obstacles
        for link_pose in robot_pose:
            if self.check_collision_with_obstacles(link_pose, obstacles):
                return False

        return True

    def forward_kinematics(self, configuration):
        """
        Calculate forward kinematics for all links
        """
        # Implementation would use kinematic models from Module 6
        pass

    def check_collision_with_obstacles(self, link_pose, obstacles):
        """
        Check if a link collides with any obstacles
        """
        # Use collision detection algorithms
        pass
```

### High-Dimensional Spaces

Humanoid robots operate in high-dimensional configuration spaces:

```python
class HighDimSpacePlanner:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.dof = robot_model.get_dof()

    def sample_configuration(self):
        """
        Sample a random configuration in high-dimensional space
        """
        config = np.zeros(self.dof)
        joint_limits = self.robot_model.get_joint_limits()

        for i in range(self.dof):
            config[i] = np.random.uniform(
                joint_limits[i][0],  # min
                joint_limits[i][1]   # max
            )

        return config

    def interpolate_configs(self, config1, config2, alpha):
        """
        Interpolate between two configurations
        """
        return (1 - alpha) * config1 + alpha * config2

    def distance_configs(self, config1, config2):
        """
        Calculate distance between configurations
        """
        return np.linalg.norm(config1 - config2)
```

## Sampling-Based Planning

### RRT (Rapidly-exploring Random Trees)

RRT is particularly useful for high-dimensional spaces:

```python
import random

class RRTPlanner:
    def __init__(self, start_config, goal_config, config_space, step_size=0.1):
        self.start_config = start_config
        self.goal_config = goal_config
        self.config_space = config_space
        self.step_size = step_size
        self.tree = [start_config]  # List of configurations
        self.parent = {0: None}     # Parent relationships

    def plan(self, max_iterations=10000):
        """
        Plan path using RRT algorithm
        """
        for i in range(max_iterations):
            # Sample random configuration
            rand_config = self.config_space.sample_configuration()

            # Find nearest node in tree
            nearest_idx = self.nearest_node(rand_config)

            # Extend towards random configuration
            new_config = self.extend_towards(rand_config, nearest_idx)

            if new_config is not None:
                # Add to tree
                new_idx = len(self.tree)
                self.tree.append(new_config)
                self.parent[new_idx] = nearest_idx

                # Check if goal is reached
                if self.is_near_goal(new_config):
                    return self.extract_path(new_idx)

        return None  # No path found

    def nearest_node(self, config):
        """
        Find nearest node in tree to given configuration
        """
        min_dist = float('inf')
        nearest_idx = 0

        for i, tree_config in enumerate(self.tree):
            dist = self.config_space.distance_configs(config, tree_config)
            if dist < min_dist:
                min_dist = dist
                nearest_idx = i

        return nearest_idx

    def extend_towards(self, target_config, nearest_idx):
        """
        Extend tree towards target configuration
        """
        nearest_config = self.tree[nearest_idx]
        direction = target_config - nearest_config
        distance = np.linalg.norm(direction)

        if distance < self.step_size:
            new_config = target_config
        else:
            # Normalize direction and step
            direction = direction / distance
            new_config = nearest_config + direction * self.step_size

        # Check if new configuration is collision-free
        if self.config_space.is_collision_free(new_config):
            return new_config

        return None

    def is_near_goal(self, config):
        """
        Check if configuration is near goal
        """
        return (self.config_space.distance_configs(config, self.goal_config)
                < self.step_size)

    def extract_path(self, goal_idx):
        """
        Extract path from goal to start
        """
        path = []
        current_idx = goal_idx

        while current_idx is not None:
            path.append(self.tree[current_idx])
            current_idx = self.parent[current_idx]

        return path[::-1]  # Reverse to get start-to-goal path
```

### RRT* (Optimal RRT)

RRT* extends RRT to find optimal paths:

```python
class RRTStarPlanner(RRTPlanner):
    def __init__(self, start_config, goal_config, config_space, step_size=0.1):
        super().__init__(start_config, goal_config, config_space, step_size)
        self.cost = {0: 0.0}  # Cost from start to each node

    def plan(self, max_iterations=10000):
        """
        Plan path using RRT* algorithm with optimization
        """
        for i in range(max_iterations):
            rand_config = self.config_space.sample_configuration()

            # Find nearest node
            nearest_idx = self.nearest_node(rand_config)

            # Extend towards random configuration
            new_config = self.extend_towards(rand_config, nearest_idx)

            if new_config is not None:
                # Find nearby nodes for rewiring
                nearby_nodes = self.find_nearby_nodes(new_config)

                # Choose parent with minimum cost
                best_parent_idx, min_cost = self.choose_best_parent(
                    new_config, nearby_nodes
                )

                if best_parent_idx is not None:
                    # Add new node
                    new_idx = len(self.tree)
                    self.tree.append(new_config)
                    self.parent[new_idx] = best_parent_idx
                    self.cost[new_idx] = min_cost

                    # Rewire nearby nodes if cheaper path found
                    self.rewire(new_idx, nearby_nodes)

                    # Check goal
                    if self.is_near_goal(new_config):
                        return self.extract_path(new_idx)

        return None

    def find_nearby_nodes(self, config):
        """
        Find nodes within a certain radius
        """
        radius = self.calculate_radius(len(self.tree))
        nearby = []

        for i, tree_config in enumerate(self.tree):
            if (self.config_space.distance_configs(config, tree_config)
                < radius):
                nearby.append(i)

        return nearby

    def choose_best_parent(self, new_config, nearby_nodes):
        """
        Choose parent that minimizes cost to new configuration
        """
        min_cost = float('inf')
        best_parent = None

        for node_idx in nearby_nodes:
            node_config = self.tree[node_idx]

            # Check if path is collision-free
            if self.is_path_collision_free(node_config, new_config):
                cost = self.cost[node_idx] + self.config_space.distance_configs(
                    node_config, new_config
                )

                if cost < min_cost:
                    min_cost = cost
                    best_parent = node_idx

        return best_parent, min_cost

    def rewire(self, new_idx, nearby_nodes):
        """
        Rewire nearby nodes if new path is cheaper
        """
        new_config = self.tree[new_idx]

        for node_idx in nearby_nodes:
            if node_idx == new_idx:
                continue

            node_config = self.tree[node_idx]
            potential_cost = (self.cost[new_idx] +
                            self.config_space.distance_configs(new_config, node_config))

            if (potential_cost < self.cost[node_idx] and
                self.is_path_collision_free(new_config, node_config)):
                self.parent[node_idx] = new_idx
                self.cost[node_idx] = potential_cost

    def calculate_radius(self, num_nodes):
        """
        Calculate connection radius based on number of nodes
        """
        gamma = 2 * (1 + 1/self.config_space.get_dof())**(1/self.config_space.get_dof())
        volume = self.config_space.get_volume()
        return gamma * (np.log(num_nodes) / num_nodes)**(1/self.config_space.get_dof())
```

### PRM (Probabilistic Roadmap)

PRM pre-computes a roadmap for multiple queries:

```python
class PRMPlanner:
    def __init__(self, config_space):
        self.config_space = config_space
        self.roadmap = {}
        self.nodes = []

    def build_roadmap(self, num_samples=1000, connection_radius=0.5):
        """
        Build probabilistic roadmap
        """
        # Sample free configurations
        for i in range(num_samples):
            config = self.config_space.sample_configuration()
            if self.config_space.is_collision_free(config):
                self.nodes.append(config)
                self.roadmap[i] = []

        # Connect nearby nodes
        for i, config1 in enumerate(self.nodes):
            for j, config2 in enumerate(self.nodes[i+1:], i+1):
                distance = self.config_space.distance_configs(config1, config2)
                if (distance < connection_radius and
                    self.is_path_collision_free(config1, config2)):
                    self.roadmap[i].append(j)
                    self.roadmap[j].append(i)

    def query_path(self, start_config, goal_config):
        """
        Query path between start and goal configurations
        """
        # Find nearest roadmap nodes to start and goal
        start_idx = self.find_nearest_node(start_config)
        goal_idx = self.find_nearest_node(goal_config)

        # Connect start and goal to roadmap
        self.connect_to_roadmap(start_config, start_idx)
        self.connect_to_roadmap(goal_config, goal_idx)

        # Use graph search (e.g., Dijkstra) to find path
        path = self.graph_search(start_idx, goal_idx)

        return path

    def find_nearest_node(self, config):
        """
        Find nearest node in roadmap to given configuration
        """
        min_dist = float('inf')
        nearest_idx = 0

        for i, node_config in enumerate(self.nodes):
            dist = self.config_space.distance_configs(config, node_config)
            if dist < min_dist:
                min_dist = dist
                nearest_idx = i

        return nearest_idx

    def connect_to_roadmap(self, config, node_idx):
        """
        Connect configuration to nearby roadmap nodes
        """
        connection_radius = 0.5
        for i, node_config in enumerate(self.nodes):
            if (i != node_idx and
                self.config_space.distance_configs(config, node_config) < connection_radius):
                if self.is_path_collision_free(config, node_config):
                    self.roadmap[node_idx].append(i)
                    self.roadmap[i].append(node_idx)

    def is_path_collision_free(self, config1, config2):
        """
        Check if path between configurations is collision-free
        """
        # Interpolate path and check collisions at intervals
        steps = 10
        for alpha in np.linspace(0, 1, steps):
            config = (1 - alpha) * config1 + alpha * config2
            if not self.config_space.is_collision_free(config):
                return False
        return True
```

## Optimization-Based Planning

### Trajectory Optimization

Optimization-based methods directly optimize trajectories:

```python
import scipy.optimize as opt

class TrajectoryOptimizer:
    def __init__(self, robot_model):
        self.robot = robot_model
        self.n_waypoints = 20
        self.dt = 0.1  # Time step

    def optimize_trajectory(self, start_config, goal_config, obstacles):
        """
        Optimize trajectory using direct collocation
        """
        # Initial guess: straight line interpolation
        initial_trajectory = self.generate_initial_trajectory(
            start_config, goal_config
        )

        # Flatten trajectory for optimization
        x0 = initial_trajectory.flatten()

        # Define objective function
        def objective(x):
            trajectory = x.reshape(-1, len(start_config))
            return self.trajectory_cost(trajectory, obstacles)

        # Define constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: self.start_constraint(x, start_config)},
            {'type': 'eq', 'fun': lambda x: self.goal_constraint(x, goal_config)},
            {'type': 'ineq', 'fun': lambda x: self.dynamics_constraint(x)}
        ]

        # Optimize
        result = opt.minimize(
            objective, x0, method='SLSQP',
            constraints=constraints,
            options={'maxiter': 1000}
        )

        if result.success:
            return result.x.reshape(-1, len(start_config))
        else:
            return None

    def generate_initial_trajectory(self, start, goal):
        """
        Generate initial trajectory guess
        """
        trajectory = np.zeros((self.n_waypoints, len(start)))
        for i in range(self.n_waypoints):
            alpha = i / (self.n_waypoints - 1)
            trajectory[i] = (1 - alpha) * start + alpha * goal
        return trajectory

    def trajectory_cost(self, trajectory, obstacles):
        """
        Calculate total cost of trajectory
        """
        cost = 0

        # Smoothness cost (minimize velocity and acceleration)
        for i in range(1, len(trajectory)):
            velocity = (trajectory[i] - trajectory[i-1]) / self.dt
            cost += np.sum(velocity**2)

        # Collision cost
        for config in trajectory:
            if not self.robot.is_collision_free(config, obstacles):
                cost += 1000  # Large penalty for collisions

        # Distance to goal cost (for intermediate points)
        goal = trajectory[-1]
        for config in trajectory[:-1]:
            cost += np.sum((config - goal)**2) * 0.1

        return cost

    def start_constraint(self, x, start_config):
        """
        Constraint: first point must be start configuration
        """
        trajectory = x.reshape(-1, len(start_config))
        return trajectory[0] - start_config

    def goal_constraint(self, x, goal_config):
        """
        Constraint: last point must be goal configuration
        """
        trajectory = x.reshape(-1, len(goal_config))
        return trajectory[-1] - goal_config

    def dynamics_constraint(self, x):
        """
        Constraint: satisfy robot dynamics (simplified)
        """
        trajectory = x.reshape(-1, len(x)//self.n_waypoints)
        constraints = []

        for i in range(1, len(trajectory)-1):
            # Acceleration limits
            prev_vel = (trajectory[i] - trajectory[i-1]) / self.dt
            next_vel = (trajectory[i+1] - trajectory[i]) / self.dt
            acceleration = (next_vel - prev_vel) / self.dt

            # Limit maximum acceleration
            max_acc = 10.0  # rad/s^2
            constraints.extend(max_acc - np.abs(acceleration))

        return np.array(constraints)
```

### Model Predictive Control (MPC) for Motion Planning

MPC combines planning and control:

```python
class MPCMotionPlanner:
    def __init__(self, robot_model, horizon=10, dt=0.1):
        self.robot = robot_model
        self.horizon = horizon
        self.dt = dt
        self.Q = np.eye(robot_model.get_dof()) * 1.0  # State cost
        self.R = np.eye(robot_model.get_dof()) * 0.1  # Control cost

    def plan_step(self, current_state, goal_state, obstacles):
        """
        Plan single step using MPC
        """
        # Define optimization problem
        def mpc_objective(u_sequence):
            state = current_state.copy()
            total_cost = 0

            for i in range(self.horizon):
                # Apply control input
                control_input = u_sequence[i*len(current_state):(i+1)*len(current_state)]
                state = self.integrate_dynamics(state, control_input)

                # Add state cost
                state_error = state - goal_state
                total_cost += state_error.T @ self.Q @ state_error

                # Add control cost
                total_cost += control_input.T @ self.R @ control_input

                # Add collision cost
                if not self.robot.is_collision_free(state, obstacles):
                    total_cost += 1000

            return total_cost

        # Initial guess for control sequence
        u0 = np.zeros(self.horizon * len(current_state))

        # Optimize
        result = opt.minimize(mpc_objective, u0, method='BFGS')

        if result.success:
            # Return first control input
            first_control = result.x[:len(current_state)]
            return first_control
        else:
            return np.zeros(len(current_state))

    def integrate_dynamics(self, state, control_input):
        """
        Integrate robot dynamics for one time step
        """
        # Simplified integration (in practice, use robot-specific dynamics)
        new_state = state + control_input * self.dt
        return new_state
```

## Dynamic Motion Planning

### Real-Time Replanning

Handling dynamic environments requires continuous replanning:

```python
class DynamicPlanner:
    def __init__(self, base_planner):
        self.base_planner = base_planner
        self.current_trajectory = []
        self.tracking_idx = 0
        self.replan_threshold = 0.5  # Replan when 50% of path completed

    def update_and_track(self, current_pose, obstacles, goal_pose):
        """
        Update plan based on current state and environment
        """
        # Check if replanning is needed
        if self.should_replan(current_pose, obstacles):
            # Replan with updated information
            new_trajectory = self.base_planner.plan(
                current_pose, goal_pose, obstacles
            )
            if new_trajectory is not None:
                self.current_trajectory = new_trajectory
                self.tracking_idx = 0

        # Track current trajectory
        if self.current_trajectory:
            return self.get_next_waypoint()
        else:
            return None

    def should_replan(self, current_pose, obstacles):
        """
        Determine if replanning is necessary
        """
        # Replan if:
        # 1. Obstacle detected in path
        if self.obstacle_in_path(current_pose, obstacles):
            return True

        # 2. Significant deviation from path
        if self.path_deviation_exceeded(current_pose):
            return True

        # 3. Goal has changed significantly
        if self.goal_changed_significantly():
            return True

        # 4. Periodic replanning
        if self.time_for_periodic_replan():
            return True

        return False

    def obstacle_in_path(self, current_pose, obstacles):
        """
        Check if obstacles are blocking the current path
        """
        # Check path ahead of current position
        look_ahead = 5  # Check next 5 waypoints
        for i in range(self.tracking_idx,
                      min(self.tracking_idx + look_ahead, len(self.current_trajectory))):
            waypoint = self.current_trajectory[i]
            if self.robot_in_collision(waypoint, obstacles):
                return True
        return False

    def robot_in_collision(self, configuration, obstacles):
        """
        Check if robot configuration is in collision with obstacles
        """
        return not self.base_planner.config_space.is_collision_free(
            configuration, obstacles
        )
```

### Predictive Planning

Anticipating future changes in dynamic environments:

```python
class PredictivePlanner:
    def __init__(self, motion_model):
        self.motion_model = motion_model
        self.prediction_horizon = 5.0  # seconds

    def plan_with_predictions(self, start_config, goal_config,
                            dynamic_obstacles, current_time):
        """
        Plan considering predicted future obstacle positions
        """
        # Predict obstacle positions at future times
        future_obstacles = self.predict_obstacles(
            dynamic_obstacles, current_time
        )

        # Plan considering future obstacles
        plan = self.base_plan_with_obstacles(
            start_config, goal_config, future_obstacles
        )

        return plan

    def predict_obstacles(self, obstacles, current_time):
        """
        Predict future obstacle positions using motion models
        """
        future_obstacles = []

        for obstacle in obstacles:
            if hasattr(obstacle, 'velocity'):
                # Predict linear motion
                predicted_pos = (obstacle.position +
                               obstacle.velocity * self.prediction_horizon)
                future_obstacles.append({
                    'position': predicted_pos,
                    'size': obstacle.size,
                    'time': current_time + self.prediction_horizon
                })
            else:
                # Static obstacle - no change
                future_obstacles.append(obstacle)

        return future_obstacles
```

## Humanoid-Specific Planning Challenges

### Balance and Stability Constraints

Humanoid robots must maintain balance during motion:

```python
class BalancedMotionPlanner:
    def __init__(self, robot_model):
        self.robot = robot_model
        self.zmp_margin = 0.05  # Safety margin for ZMP

    def plan_balanced_motion(self, start_config, goal_config, obstacles):
        """
        Plan motion that maintains robot balance
        """
        # Plan initial trajectory
        trajectory = self.plan_with_balance_constraints(
            start_config, goal_config, obstacles
        )

        # Verify balance throughout trajectory
        if self.is_trajectory_balanced(trajectory):
            return trajectory
        else:
            # Plan with stricter balance constraints
            return self.plan_strictly_balanced_motion(
                start_config, goal_config, obstacles
            )

    def plan_with_balance_constraints(self, start, goal, obstacles):
        """
        Plan with balance constraints as soft constraints
        """
        # Use optimization with balance penalty
        def balance_penalized_cost(trajectory):
            base_cost = self.trajectory_cost(trajectory)
            balance_penalty = self.balance_constraint_violation(trajectory)
            return base_cost + 100 * balance_penalty

        # Optimize with balance penalty
        return self.optimize_trajectory(
            start, goal, obstacles, balance_penalized_cost
        )

    def balance_constraint_violation(self, trajectory):
        """
        Calculate total violation of balance constraints
        """
        total_violation = 0

        for config in trajectory:
            zmp = self.calculate_zmp(config)
            support_polygon = self.calculate_support_polygon(config)

            if not self.point_in_polygon(zmp, support_polygon):
                # Calculate distance to nearest support point
                dist = self.distance_to_support_polygon(zmp, support_polygon)
                total_violation += dist

        return total_violation

    def calculate_zmp(self, configuration):
        """
        Calculate Zero Moment Point for given configuration
        """
        # Calculate center of mass and ZMP
        com = self.robot.calculate_com(configuration)
        com_height = com[2]

        # Simplified ZMP calculation
        zmp = com[:2]  # Project CoM to ground with compensation
        return zmp

    def calculate_support_polygon(self, configuration):
        """
        Calculate support polygon based on foot positions
        """
        # Get foot positions from forward kinematics
        foot_poses = self.robot.get_foot_poses(configuration)
        support_points = [pose[0:2, 3] for pose in foot_poses]  # Extract x,y positions

        return support_points
```

### Multi-Limb Coordination

Coordinating multiple limbs for complex tasks:

```python
class MultiLimbPlanner:
    def __init__(self, robot_model):
        self.robot = robot_model

    def plan_coordinated_motion(self, task_descriptions):
        """
        Plan coordinated motion for multiple limbs
        task_descriptions: list of tasks for different limbs
        """
        # Decompose into individual limb planning problems
        individual_plans = {}
        for task in task_descriptions:
            limb = task['limb']
            target = task['target']
            individual_plans[limb] = self.plan_single_limb(limb, target)

        # Coordinate plans to avoid conflicts
        coordinated_plan = self.coordinate_plans(individual_plans)

        return coordinated_plan

    def plan_single_limb(self, limb, target):
        """
        Plan motion for a single limb
        """
        # Use IK to find target configuration for limb
        target_config = self.robot.inverse_kinematics(limb, target)

        # Plan path to target configuration
        planner = RRTPlanner(
            self.robot.get_current_config(),
            target_config,
            self.robot.get_config_space()
        )

        return planner.plan()

    def coordinate_plans(self, individual_plans):
        """
        Coordinate multiple limb plans to avoid conflicts
        """
        # Synchronize timing
        max_length = max(len(plan) for plan in individual_plans.values())

        # Extend shorter plans
        for limb, plan in individual_plans.items():
            while len(plan) < max_length:
                plan.append(plan[-1])  # Hold last position

        # Create coordinated trajectory
        coordinated = []
        for i in range(max_length):
            step = {}
            for limb, plan in individual_plans.items():
                step[limb] = plan[i]
            coordinated.append(step)

        return coordinated
```

## Integration with Control Systems

### Planning-Control Interface

Connecting motion planners with low-level controllers:

```python
class PlanningControlInterface:
    def __init__(self, planner, controller):
        self.planner = planner
        self.controller = controller
        self.trajectory = []
        self.current_idx = 0

    def execute_trajectory(self, start_config, goal_config, obstacles):
        """
        Execute planned trajectory with feedback control
        """
        # Plan trajectory
        self.trajectory = self.planner.plan(start_config, goal_config, obstacles)

        if self.trajectory is None:
            return False

        # Execute with feedback control
        self.current_idx = 0
        success = True

        while self.current_idx < len(self.trajectory) and success:
            desired_config = self.trajectory[self.current_idx]
            current_config = self.controller.get_current_configuration()

            # Compute control command
            control_command = self.controller.compute_command(
                current_config, desired_config
            )

            # Execute control command
            success = self.controller.execute_command(control_command)

            # Update for next step
            self.current_idx += 1

            # Check for replanning conditions
            if self.needs_replanning(current_config, obstacles):
                return self.replan_and_execute(
                    current_config, goal_config, obstacles
                )

        return success

    def needs_replanning(self, current_config, obstacles):
        """
        Check if replanning is needed during execution
        """
        # Check if significantly off planned path
        planned_config = self.trajectory[self.current_idx]
        deviation = np.linalg.norm(current_config - planned_config)

        if deviation > 0.2:  # Threshold for replanning
            return True

        # Check for new obstacles
        if self.obstacle_detected(current_config, obstacles):
            return True

        return False
```

## Applications in Humanoid Robotics

### Walking Pattern Generation

```python
class WalkingPatternGenerator:
    def __init__(self, step_length=0.3, step_height=0.1, step_time=0.8):
        self.step_length = step_length
        self.step_height = step_height
        self.step_time = step_time

    def generate_walking_trajectory(self, distance, direction):
        """
        Generate walking trajectory for humanoid
        """
        num_steps = int(distance / self.step_length)
        trajectory = []

        for i in range(num_steps):
            # Generate step pattern
            step_trajectory = self.generate_single_step(i % 2 == 0)  # Alternate feet
            trajectory.extend(step_trajectory)

        return trajectory

    def generate_single_step(self, is_left_support):
        """
        Generate trajectory for a single step
        """
        # Simplified step trajectory
        # In practice, would use inverted pendulum model or other walking patterns
        t = np.linspace(0, self.step_time, 50)

        # Swing foot trajectory
        x_swing = self.step_length * (t / self.step_time)
        z_swing = self.step_height * np.sin(np.pi * t / self.step_time)

        # Support foot stays in place
        x_support = np.zeros_like(t)
        z_support = np.zeros_like(t)

        return {
            'time': t,
            'left_foot': np.column_stack([x_support if is_left_support else x_swing,
                                         np.zeros_like(t),
                                         z_support if is_left_support else z_swing]),
            'right_foot': np.column_stack([x_swing if is_left_support else x_support,
                                          np.zeros_like(t),
                                          z_swing if is_left_support else z_support])
        }
```

### Manipulation Planning

```python
class ManipulationPlanner:
    def __init__(self, robot_model):
        self.robot = robot_model

    def plan_reaching_motion(self, target_pos, target_orientation=None):
        """
        Plan reaching motion for humanoid arm
        """
        # Solve inverse kinematics for target
        target_config = self.robot.inverse_kinematics(
            target_pos, target_orientation
        )

        # Plan path to target configuration
        current_config = self.robot.get_current_configuration()

        planner = RRTPlanner(
            current_config, target_config,
            self.robot.get_config_space()
        )

        return planner.plan()

    def plan_grasping_motion(self, object_pose):
        """
        Plan grasping motion for humanoid
        """
        # Approach phase
        approach_pos = object_pose[:3, 3] - object_pose[:3, 2] * 0.2  # 20cm before object
        approach_config = self.robot.inverse_kinematics(approach_pos)

        # Grasp phase
        grasp_config = self.robot.inverse_kinematics(object_pose[:3, 3])

        # Plan sequence
        trajectory = []
        trajectory.extend(self.plan_to_configuration(approach_config))
        trajectory.extend(self.plan_to_configuration(grasp_config))

        return trajectory
```

## Summary

In this module, you've learned:
- The fundamentals of motion planning for humanoid robots
- Sampling-based planning algorithms like RRT and RRT*
- Optimization-based planning techniques
- How to handle dynamic environments and real-time replanning
- Humanoid-specific challenges like balance and multi-limb coordination
- Integration of motion planning with control systems
- Applications in walking and manipulation

Motion planning is essential for enabling humanoid robots to operate safely and effectively in complex environments, requiring sophisticated algorithms that can handle high-dimensional spaces and dynamic constraints.

## Next Steps

In the next module, we'll explore the Capstone Project, where you'll integrate all the concepts learned throughout the textbook to build a complete humanoid robotics application.

---

## APA Citations

- LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
- Choset, H., et al. (2005). *Principles of Robot Motion: Theory, Algorithms, and Implementations*. MIT Press.
- Karaman, S., & Frazzoli, E. (2011). Sampling-based algorithms for optimal motion planning. *International Journal of Robotics Research*, 30(7), 846-894.
- Kuwata, Y., et al. (2009). Real-time motion planning with applications to autonomous urban driving. *IEEE Transactions on Robotics*, 25(5), 1105-1118.
- Zucker, M., et al. (2013). CHOMP: Covariant Hamiltonian optimization for motion planning. *International Journal of Robotics Research*, 32(9-10), 1164-1193.