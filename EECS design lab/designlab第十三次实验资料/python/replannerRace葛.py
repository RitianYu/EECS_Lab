"""
State machine classes for planning paths in a grid map.
"""
import lib601.util as util
import lib601.sm as sm
import math
import lib601.ucSearch as ucSearch
import lib601.gridDynamics as gridDynamics
reload(gridDynamics)




def IsActionEq(a):
    if len(a) < 2:
        return 0
    original = len(a)
    if a[0] == (1, 1) or a[0] == (-1, -1) or a[0] == (1, -1) or a[0] == (-1, 1):
        return original - len(a)
    else:
        if a[0] == a[1]:
            a.pop(0)
            IsActionEq(a)
            return original - len(a) - 1
        else:
            return original - len(a)



class ReplannerWithDynamicMap(sm.SM):
    """
    This replanner state machine has a dynamic map, which is an input
    to the state machine.  Input to the machine is a pair C{(map,
    sensors)}, where C{map} is an instance of a subclass of
    C{gridMap.GridMap} and C{sensors} is an instance of
    C{io.SensorInput};  output is an instance of C{util.Point},
    representing the desired next subgoal.  The planner should
    guarantee that a straight-line path from the current pose to the
    output pose is collision-free in the current map.
    """
    def __init__(self, goalPoint):
        """
        @param goalPoint: fixed goal that the planner keeps trying to
        reach
        """
        self.goalPoint = goalPoint
        self.startState = None
        """
        State is the plan currently being executed.  No plan to start with.
        """

    def getNextValues(self, state, inp):
        (map, sensors) = inp
        # Make a model for planning in this particular map
        dynamicsModel = gridDynamics.GridDynamics(map)
        # Find the indices for the robot's current location and goal
        currentIndices = map.pointToIndices(sensors.odometry.point())
        goalIndices = map.pointToIndices(self.goalPoint)
        
        if timeToReplan(state, currentIndices, map, goalIndices):
            # Define heuristic to be Euclidean distance
            def h(s):

                # return self.goalPoint.distance(map.indicesToPoint(s))

                goal = map.indicesToPoint(goalIndices)
                node = map.indicesToPoint(s)
                dx = abs(node.x - goal.x)
                dy = abs(node.y - goal.y)
                return map.xStep * (dx + dy) + (map.xStep * 1.41421356 - 2 * map.xStep) * min(dx, dy)

                # n=map.indicesToPoint(s)
                # goal=map.indicesToPoint(goalIndices)
                # def h_diagonal(n):
                #     return min(abs(n.x-goal.x), abs(n.y-goal.y))
                # def h_straight(n):
                #     return (abs(n.x-goal.x) + abs(n.y-goal.y))
                # return map.xStep*1.41421356 * h_diagonal(n) + map.xStep * (h_straight(n) - 2*h_diagonal(n))

            # Define goal test
            def g(s):
                return s == goalIndices
            # Make a new plan
            plan = ucSearch.smSearch(dynamicsModel, currentIndices, g,
                                     heuristic = h, maxNodes = 5000)
            # Clear the old path from the map
            if state: map.undrawPath(state)

            if plan:
                # The call to the planner succeeded;  extract the list
                # of subgoals
                state = [s[:2] for (a, s) in plan]
                action = [a for (a, s) in plan]
                print 'New plan', state
                print 'Action',action

                needle = []
                for i in range(len(state) - 2):
                    if state[i][0] == state[i + 1][0] and state[i + 1][0] == state[i + 2][0]:
                        needle.append(i + 1)
                    elif state[i][1] == state[i + 1][1] and state[i + 1][1] == state[i + 2][1]:
                        needle.append(i + 1)
                n = 0
                for i in needle:
                    del state[i - n]
                    n += 1

                action = [a for (a, s) in plan]
                action.pop(0)
                more = IsActionEq(action)
                for i in range(more):
                    state.pop(1)

                # Draw the plan
                map.drawPath(state)
            else:
                # The call to the plan failed
                # Just show the start and goal indices, for debugging
                map.drawPath([currentIndices, goalIndices])
                state = None

        if not state or (currentIndices == state[0] and len(state) == 1):
            # If we don't have a plan or we've already arrived at the
            # goal, just ask the move machine to stay at the current pose.
            return (state, sensors.odometry)
        elif currentIndices == state[0] and len(state) > 1:
            # We have arrived at the next subgoal in our plan;  so we
            # Draw that square using the color it should have in the map
            map.drawSquare(state[0])
            # Remove that subgoal from the plan
            state = state[1:]
            # Redraw the rest of the plan
            map.drawPath(state)
        # Return the current plan and a subgoal in world coordinates
        return (state, map.indicesToPoint(state[0]))

def timeToReplan(plan, currentIndices, map, goalIndices):
    """
    Replan if the current plan is C{None}, if the plan is invalid in
    the map (because it is blocked), or if the plan is empty and we
    are not at the goal (which implies that the last time we tried to
    plan, we failed).
    """
    return plan == None or planInvalidInMap(map, plan, currentIndices) or \
            (plan == [] and not goalIndices == currentIndices)

def planInvalidInMap(map, plan, currentIndices):
    """
    Checks to be sure all the cells between the robot's current location
    and the first subgoal in the plan are occupiable.
    In low-noise conditions, it's useful to check the whole plan, so failures
    are discovered earlier;  but in high noise, we often have to get
    close to a location before we decide that it is really not safe to
    traverse.

    We actually ignore the case when the robot's current indices are
    occupied;  during mapMaking, we can sometimes decide the robot's
    current square is not occupiable, but we should just keep trying
    to get out of there.
    """
    if len(plan) == 0:
        return False
    wayPoint = plan[0]
    for p in util.lineIndicesConservative(currentIndices, wayPoint)[1:]:
        if not map.robotCanOccupy(p):
            print 'plan invalid', currentIndices, p, wayPoint, '-- replanning'
            return True
    return False
