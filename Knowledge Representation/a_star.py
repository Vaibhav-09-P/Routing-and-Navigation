from queue import PriorityQueue
from math import sin, cos, sqrt, atan2, radians, floor

def sld_between_cities(city1, city2):
    global city_gps
    # Unpack lats and longs for the cities
    (x1, y1), (x2, y2) = city_gps[city1], city_gps[city2]
    # Convert degrees to radians
    lat1 = radians(x1)
    lon1 = radians(y1)
    lat2 = radians(x2)
    lon2 = radians(y2)

    ### Begin cited code
    # approximate radius of earth in km
    R = 6373.0

    dlon = lon1 - lon2
    dlat = lat1 - lat2

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate distance and convert it into miles
    distance = (R * c) / 1.60934
    ### End cited code

    return floor(distance)

def road_dist(node):
    # Unpack the route from the node
    route = node[1]
    # Backtrack the route and identify the first parent with available GPS location
    parent = ''
    reverse_route = list( reversed( route.split() ) )
    for city in reverse_route[1:]:
        if city in city_gps.keys():
            parent = city
            break
    # If not parent on the route has a GPS location, return zero
    if not len(parent):
        return 0
    # Else, return the total road distance on the route from parent city to child city
    else:
        dist_parent_to_child = 0
        route_parent_to_child = route.split()[ route.split().index(parent) :]
        for i in range(0, len(route_parent_to_child) - 1 ):
            for key, value in road_seg.items():
                if (route_parent_to_child[i] in key) and (route_parent_to_child[i+1] in key):
                    dist_parent_to_child += value[0]

        return dist_parent_to_child

def sld_between_nodes(node1, node2):
    global end_city
    # Unpack routes from the nodes
    route1, route2 = node1[1], node2[1]
    # Initialize city1 and city2
    city1 = ''
    city2 = ''
    # Track each city on route1 in reverse order and return sld between the first available city and goal city
    for city in reversed( route1.split() ):
        if city in city_gps.keys():
            city1 = city
            break
    # Track each city on route2 in reverse order and return sld between the first available city and goal city
    for city in reversed( route2.split() ):
        if city in city_gps.keys():
            city2 = city
            break
    # Assign goal city as the corresponding city if no city on route1 or route2 has a GPS location
    if not len(city1):
        city1 = end_city
    if not len(city2):
        city2 = end_city

    return sld_between_cities(city1, city2)

def sld_to_goal(node):
    global end_city
    # Unpack route from the node
    route = node[1]
    # Track each city on route in reverse order and return sld between the first available city and goal city
    for city in reversed( route.split() ):
        if city in city_gps.keys():
            return sld_between_cities(city, end_city)
    # Return zero if no city on the route has a GPS location
    return 0

def segments(child_node, algo):
    # Unpack child node
    city, route, dist, time, seg = child_node
    g = seg
    h = 1 if algo == 'astar' else 0
    return g + h

def travel_distance(child_node, parent_node, algo):
    global city_gps
    # Pass distance to child city as the cost
    g = child_node[2]
    # Evaluate heuristic as per the routing algorithm
    if algo == 'uniform':
        h = 0
    else:
        # For A* search, check for inaccuracy in child city's GPS location
        if ( sld_between_nodes(parent_node, child_node) > road_dist(child_node) ) or ( not sld_between_nodes(parent_node, child_node) ):
            inaccuracy_factor = road_dist(child_node)
            h = min( sld_to_goal(child_node), max(0, ( sld_to_goal(parent_node) -  inaccuracy_factor ) ) )
        else:
            h = sld_to_goal(child_node)

    return g + h

def travel_time(child_node, parent_node, algo):
    global city_gps
    # Use 65 mph as the max speed to calculate the time heuristic
    max_speed = 65
    # Pass travel time to child city as the cost
    g = child_node[3]
    # Evaluate heuristic as per the routing algorithm
    if algo == 'uniform':
        h = 0
    else:
        # Check for inaccuracy/unavailability of child city's GPS location
        if ( sld_between_nodes(parent_node, child_node) > road_dist(child_node) ) or ( not sld_between_nodes(parent_node, child_node) ):
            inaccuracy_factor = road_dist(child_node)
            min_dist = min( sld_to_goal(child_node), max(0, ( sld_to_goal(parent_node) -  inaccuracy_factor ) ) )
        else:
            min_dist = sld_to_goal(child_node)
        h = min_dist / max_speed

    return g + h

def estimate(child_node, parent_node, algo):
    global cost_func

    # Call appropriate evaluation function
    if cost_func == 'segments':
        f = segments(child_node, algo)
    elif cost_func == 'distance':
        f = travel_distance(child_node, parent_node, algo)
    elif cost_func == 'time':
        f = travel_time(child_node, parent_node, algo)
    else:
        f = -1

    return f

def successors(parent_node):
    global road_seg
    # Unpack parent node
    parent_city, parent_route, parent_dist, parent_time, parent_seg = parent_node
    child_nodes = []
    # Initialize a var for cities already visited on the current route
    visited = [node for node in parent_route.split()]
    # Begin traversing the road segments
    for key, value in road_seg.items():
        # Unpack road segment
        city1, city2, dist, speed, highway = key[0], key[1], value[0], value[1], value[2]
        # Check if parent city is in the road segment
        if parent_city in (city1, city2):
            child_city = city2 if parent_city == city1 else city1
            # Check of the child city has already been visited
            if child_city not in visited:
                child_route = parent_route + " " + child_city
                child_dist = dist + parent_dist
                child_time = parent_time + (dist/speed)
                child_seg = parent_seg + 1
                # Pack child node
                child_node = (child_city, child_route, child_dist, child_time, child_seg)
                child_nodes += [child_node]

    return child_nodes

def is_goal(city):
    global end_city
    return end_city == city

def uniform():
    global start_city
    # Structure of node: (current_city, route_to_city, journey_distance, journey_time, number_of_road_segments)
    # Pack & initialize initial node
    initial_node = (start_city, start_city, 0, 0, 0)
    # Initialize fringe with initial node
    fringe = PriorityQueue()
    fringe.put( (0,  initial_node) )
    while not fringe.empty():
        (f, parent_node) = fringe.get()
        city, route, dist, time, seg = parent_node
        if is_goal(city):
            optimal = 'yes'
            print("Total number of turns on the route:", seg)
            return (optimal, dist, round(time, 4), route)
        for child_node in successors(parent_node):
            f = estimate(child_node, parent_node, 'uniform')
            if f == -1:
                print("Please punch-in one of the following costs:\nsegments, distance, time")
                return False
            else:
                fringe.put( (f, child_node) )

    return False

def astar():
    global start_city
    global end_city
    # Check for end city's GPS location availability
    if end_city not in list(city_gps.keys()):
        print("Cannot locate destination city on the GPS. Running Uniform-cost algorithm instead...")
        solution = uniform()
        return solution
    else:
        # Structure of node: (current_city, route_to_city, journey_distance, journey_time, number_of_road_segments)
        # Pack & initialize initial node
        initial_node = (start_city, start_city, 0, 0, 0)
        # Initialize fringe with initial node
        fringe = PriorityQueue()
        fringe.put( (0,  initial_node) )
        while not fringe.empty():
            (f, parent_node) = fringe.get()
            city, route, dist, time, seg = parent_node
            if is_goal(city):
                # Check noise flag and assign optimality
                optimal = 'yes'
                print("Total number of turns on the route:", seg)
                return (optimal, dist, round(time, 4), route)
            for child_node in successors(parent_node):
                f = estimate(child_node, parent_node, 'astar')
                if f == -1:
                    print("Please punch-in one of the following costs:\nsegments, distance, time")
                    return False
                else:
                    fringe.put( (f, child_node) )

    return False