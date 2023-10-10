class Room:
    def __init__(self, x, y, rubbish_weight=0, rubbish_size=0, disposal_room=False):
        self.x = x
        self.y = y
        self.rubbish_weight = rubbish_weight
        self.rubbish_size = rubbish_size
        self.disposal_room = disposal_room


room_coordinates = [
    (-5, 4), (-4, 4), (-3, 4), (-2, 4), (-1, 4), (0, 4),
    (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3),
    (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2),
    (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
    (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
    (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
    (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
    (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3),
    (-1, -4), (0, -4), (1, -4), (2, -4), (3, -4), (4, -4)
]

rubbish_locations = {
    (-5, 4): (10, 1),
    (-2, 3): (30, 3),
    (-1, 2): (5, 1),
    (1, 1): (5, 1),
    (-2, 1): (5, 3),
    (0, 0): (10, 2),
    (-2, 0): (20, 1),
    (2, -2): (10, 2),
    (-1, -2): (5, 2),
    (4, -3): (30, 1),
    (1, -3): (20, 2),
    (3, -4): (10, 3),
}

disposal_rooms = [
    (-4, 2),
    (-1, -4),
    (3, -1),
    (-3, 3),  # New disposal room location
    (0, -2)  # New disposal room location
]



class RubbishBin:
    def __init__(self, weight_capacity, size_capacity):
        self.weight_capacity = weight_capacity
        self.size_capacity = size_capacity
        self.current_weight = 0
        self.current_size = 0

    def can_collect(self, weight, size):
        return self.current_weight + weight <= self.weight_capacity and self.current_size + size <= self.size_capacity

    def collect_rubbish(self, weight, size):
        self.current_weight += weight
        self.current_size += size

    def dispose_rubbish(self):
        self.current_weight = 0
        self.current_size = 0


def find_optimal_path(start_room, rubbish_locations, disposal_rooms):
    path = []
    rubbish_bin = RubbishBin(40, 5)
    cumulative_distance = 0

    while rubbish_locations:
        # Find the nearest room with rubbish that satisfies the weight and size constraints
        nearest_room = None
        min_distance = float('inf')

        for room_coord, rubbish in rubbish_locations.items():
            distance = distanceOf(start_room, Room(*room_coord))
            if distance < min_distance and rubbish_bin.can_collect(rubbish[0], rubbish[1]):
                min_distance = distance
                nearest_room = Room(*room_coord, rubbish_weight=rubbish[0], rubbish_size=rubbish[1])

        if nearest_room is not None:
            # Collect rubbish
            rubbish_bin.collect_rubbish(nearest_room.rubbish_weight, nearest_room.rubbish_size)
            cumulative_distance += min_distance
            path.append((nearest_room, cumulative_distance))
            del rubbish_locations[(nearest_room.x, nearest_room.y)]
            start_room = nearest_room

        # Check if the rubbish bin is full or there are no more remaining suitable rubbish locations
        if rubbish_bin.current_weight == rubbish_bin.weight_capacity or rubbish_bin.current_size == rubbish_bin.size_capacity or not any(rubbish_bin.can_collect(weight, size) for weight, size in rubbish_locations.values()):
            # Dispose rubbish in the nearest disposal room
            disposal_room = get_nearest_disposal_room(start_room, disposal_rooms)
            cumulative_distance += distanceOf(start_room, disposal_room)
            path.append((disposal_room, cumulative_distance))
            rubbish_bin.dispose_rubbish()
            start_room = disposal_room

    return path


def distanceOf(current_room, goal_room):
    dx = goal_room.x - current_room.x
    dy = goal_room.y - current_room.y

    if (dx >= 0 and dy >= 0) or (dx < 0 and dy < 0):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))


def get_nearest_disposal_room(current_room, disposal_rooms):
    min_distance = float('inf')
    nearest_disposal_room = None

    for disposal_room_coordinates in disposal_rooms:
        disposal_room = Room(*disposal_room_coordinates, disposal_room=True)
        distance = distanceOf(current_room, disposal_room)
        if distance < min_distance:
            min_distance = distance
            nearest_disposal_room = disposal_room

    return nearest_disposal_room


# Define the starting room
start_room = Room(0, 4)

# Find the optimal path
path = find_optimal_path(start_room, rubbish_locations, disposal_rooms)

print("Start at ({}, {}) [Bin Weight: 0 kg, Bin Size: 0 m^3], Cumulative Distance: 0 units".format(start_room.x, start_room.y))
print()

# Print the optimal path with rubbish bin weight and size
rubbish_bin = RubbishBin(40, 5)
for room, cumulative_distance in path:
    if room.disposal_room:
        print("Dispose rubbish at ({}, {}) [Bin Weight: 0 kg, Rubbish Size: 0 m^3], Cumulative Distance: {} units"
              .format(room.x, room.y, cumulative_distance))
        rubbish_bin.dispose_rubbish()
        print()
    else:
        rubbish_bin.collect_rubbish(room.rubbish_weight, room.rubbish_size)
        print("Collect rubbish at ({}, {}) [Bin Weight: {} kg, Rubbish Size: {} m^3], Cumulative Distance: {} units"
              .format(room.x, room.y, rubbish_bin.current_weight, rubbish_bin.current_size, cumulative_distance))
        print()