import heapq


def dijkstraB(graph, source):
    # Using minimizing heap for the priority queue to implement Dijkstra's algorithm

    # Store the shortest known distance from the source to every vertex
    distances = [float("inf")] * len(graph)
    distances[source] = 0

    # Each heap entry is (distance from source, vertex)
    min_heap = [(0, source)]

    while min_heap:
        # Process the entry with the smallest distance
        current_distance, vertex = heapq.heappop(min_heap)

        # Skip this entry if a shorter route was already found
        if current_distance > distances[vertex]:
            continue

        # graph[vertex] contains (neighbour, edge weight) pairs
        for neighbour, weight in graph[vertex]:
            new_distance = current_distance + weight

            # Update the neighbour when this route is shorter
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbour))

    return distances
