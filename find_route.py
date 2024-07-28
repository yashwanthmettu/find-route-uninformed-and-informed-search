import heapq
import sys

def find_route(filename, start_city, end_city, h_kassel=None):
    files=Maps(filename, h_kassel)
    if h_kassel:
        answer=files.informed_search(start_city, end_city)
    else:
        answer=files.uninformed_search(start_city, end_city)

    if answer is None:
        pass

    cost, pathway=answer
    print("total nodes popped: ",files.nodes_popped)
    print("total nodes expanded: ",files.nodes_expanded)
    print("total nodes generated: ",files.nodes_generated)

    if cost:
        cost=float(cost)
        #prints the optimal distance
        print(f"Distance: {cost} km")
    else:
        #prints "Infinity" if no optimal route is found
        print("Distance: Infinity")


    print("Route:")
    #prints the city routes information
    if pathway:
        for i in range(len(pathway)-1):
            start_city_name=pathway[i]
            end_city_name=pathway[i+1]
            city_from=files.road_connections[start_city_name]
            city_to=files.road_connections[end_city_name]
            distance=city_from.next_city[city_to]
            distance=float(distance)
            print(f"{start_city_name} to {end_city_name}: {distance} km")
    else:
        print("None")


class City:
    def __init__(self, city_name):
        self.name=city_name
        self.next_city={}
    def neighbor(self, city, distance):
        self.next_city[city]=distance

class Maps:
    def __init__(self,filename, h_kassel=None):
        self.road_connections = {} #dictionary to store city connections
        self.load_city_connections(filename)
        self.heuristic = {} #dictionary to store heuristic values
        if h_kassel:
            self.heuristic_load(h_kassel)
        self.nodes_popped=0
        self.nodes_expanded=0
        self.nodes_generated=1


    def load_city_connections(self, filename):
        with open(filename,'r') as file:
            for i in file:
                if i.strip()=="END OF INPUT":
                    break
                start_city, end_city, distance=i.strip().split()

                start_city_obj=self.road_connections.get(start_city,City(start_city))
                end_city_obj=self.road_connections.get(end_city,City(end_city))

                start_city_obj.neighbor(end_city_obj,int(distance))
                end_city_obj.neighbor(start_city_obj,int(distance))

                self.road_connections[start_city]=start_city_obj
                self.road_connections[end_city]=end_city_obj



    def uninformed_search(self, start_city, end_city):
        explored=set()
        nodes_queue=[(0,start_city,[])] #priority queue for nodes with start city as the initial node
        while nodes_queue:
            cost, city_name, pathway=heapq.heappop(nodes_queue)#pops the node with lowest cost from priority queue
            city=self.road_connections[city_name]
            self.nodes_popped+=1
            if city_name==end_city:
                return cost, pathway+[city_name]
            if city_name in explored:
                continue
            explored.add(city_name)
            self.nodes_expanded+=1
            for neighbor, length in city.next_city.items():
                updated_cost=cost + int(length)
                updated_path=pathway + [city_name]
                heapq.heappush(nodes_queue,(updated_cost, neighbor.name,updated_path)) #pushes the updated node to priority queue
                self.nodes_generated+=1
        return None, None

    def heuristic_load(self, filename):
        with open(filename, 'r') as file:
            for i in file:
                tokens = i.strip().split()
                if len(tokens) == 2:
                    city = tokens[0]
                    heuristic_value = tokens[1]
                    self.heuristic[city] = int(heuristic_value)
                elif i.strip() == "END OF INPUT":
                    pass

    def informed_search(self, start_city, end_city):

        explored = set()
        nodes_queue = [(self.heuristic[start_city], start_city, [])]
        while nodes_queue:
            cost, city_name, pathway = heapq.heappop(nodes_queue)
            city = self.road_connections[city_name]
            self.nodes_popped += 1
            if city_name == end_city:
                return cost, pathway + [city_name]

            if city_name in explored:
                continue
            explored.add(city_name)
            self.nodes_expanded+=1
            for neighbor, length in city.next_city.items():
                updated_cost = cost-self.heuristic[city_name]+length+self.heuristic.get(neighbor,0)
                updated_path = pathway + [city_name]
                heuristic_path=self.heuristic_cost(neighbor.name, end_city)
                heapq.heappush(nodes_queue, (updated_cost+heuristic_path, neighbor.name, updated_path))
                self.nodes_generated += 1

        return None, None

    def heuristic_cost(self, city_name, end):
        return self.heuristic.get(city_name,0)


if __name__=="__main__":
    if len(sys.argv)==4:
        find_route(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        find_route(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])





