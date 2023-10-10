import random

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

rubbish_locations = [
    (10, 1, -5, 4),
    (30, 3, -2, 3),
    (5, 1, -1, 2),
    (5, 1, 1, 1),
    (5, 3, -2, 1),
    (10, 2, 0, 0),
    (20, 1, -2, 0),
    (10, 2, 2, -2),
    (5, 2, -1, -2),
    (30, 1, 4, -3),
    (20, 2, 1, -3),
    (10, 3, 3, -4),
]

disposal_rooms = [
    (-4, 2),
    (-1, -4),
    (3, -1)
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
    random.shuffle(rubbish_locations)  # Shuffle the rubbish locations randomly
    rubbish_bin = RubbishBin(40, 5)
    path = []
    cumulative_distance = 0

    def distance_of(room1, room2):
        return abs(room1.x - room2.x) + abs(room1.y - room2.y)

    def get_nearest_room(start, locations):
        min_distance = float('inf')
        nearest_room = None

        for room in locations:
            room_object = Room(room[2], room[3], rubbish_weight=room[0], rubbish_size=room[1])
            dist = distance_of(start, room_object)
            if dist < min_distance:
                min_distance = dist
                nearest_room = room_object

        return nearest_room, min_distance

    def get_nearest_disposal_room(start, rooms):
        min_distance = float('inf')
        nearest_room = None

        for room in rooms:
            room_object = Room(room[0], room[1], disposal_room=True)
            dist = distance_of(start, room_object)
            if dist < min_distance:
                min_distance = dist
                nearest_room = room_object

        return nearest_room

    while rubbish_locations:
        nearest_room, min_distance = get_nearest_room(start_room, rubbish_locations)
        
        # Collect rubbish
        if rubbish_bin.can_collect(nearest_room.rubbish_weight, nearest_room.rubbish_size):
            rubbish_bin.collect_rubbish(nearest_room.rubbish_weight, nearest_room.rubbish_size)
            cumulative_distance += min_distance
            path.append((nearest_room, cumulative_distance))
            rubbish_locations.remove((nearest_room.rubbish_weight, nearest_room.rubbish_size, nearest_room.x, nearest_room.y))
            start_room = nearest_room
        else:
            # Dispose rubbish in the nearest disposal room
            disposal_room = get_nearest_disposal_room(start_room, disposal_rooms)
            cumulative_distance += distance_of(start_room, disposal_room)
            path.append((disposal_room, cumulative_distance))
            rubbish_bin.dispose_rubbish()
            start_room = disposal_room

    return path


# Define the starting room
start_room = Room(0, 4)

# Find the optimal path
path = find_optimal_path(start_room, rubbish_locations, disposal_rooms)

print("Start at ({}, {}) [Bin Weight: 0 kg, Rubbish Size: 0 m^3], Cumulative Distance: 0 units".format(start_room.x, start_room.y))
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
