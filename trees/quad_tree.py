import pandas as pd
import numpy as np

# Convert letters to indices
def alphabet_index(letter):
    return ord(letter.lower()) - ord('a')

# A point in 3D space with coordinates and data
class DataPoint:
    def __init__(self, x, y, z, data):
        self.x = x
        self.y = y
        self.z = z
        self.data = data

# A 3D  space for the algorithm
class DataSpace:
    def __init__(self, cx, cy, cz, w, h, d):
        self.cx = cx      #x coord for the center of the quad
        self.cy = cy      #y coord for the center of the quad
        self.cz = cz      #z coord for the center of the quad
        self.w = w        #width of quad
        self.h = h        #height of quad
        self.d = d        #depth of quad

        #the edges for the 3d data space
        self.left_edge = cx - w / 2
        self.right_edge = cx + w / 2
        self.top_edge = cy - h / 2
        self.bottom_edge = cy + h / 2
        self.front_edge = cz - d / 2
        self.back_edge = cz + d / 2

    def contains(self, point):#checks if the space contains the point
        point_x, point_y, point_z = point.x, point.y, point.z
        return (
            self.left_edge <= point_x <= self.right_edge and
            self.top_edge <= point_y <= self.bottom_edge and
            self.front_edge <= point_z <= self.back_edge
        )

    def intersects(self, other):#checks if two spaces intersect each other
        return not (
            other.left_edge > self.right_edge or
            other.right_edge < self.left_edge or
            other.top_edge > self.bottom_edge or
            other.bottom_edge < self.top_edge or
            other.front_edge > self.back_edge or
            other.back_edge < self.front_edge
        )

# Quad tree for data points
class DataQuadTree:
    def __init__(self, space, max_points=8, depth=0):
        self.space = space #the space the tree covers
        self.max_points = max_points  #max points in a node
        self.points = []       #points list in a node
        self.depth = depth     #depth of the node
        self.divided = False   #check if node is divided
        self.nw = None         #northwest
        self.ne = None         #northeast
        self.se = None         #southeast
        self.sw = None         #southwest

    def divide(self):#divide each node to 8 sub-nodes 
        cx, cy, cz = self.space.cx, self.space.cy, self.space.cz
        w, h, d = self.space.w / 2, self.space.h / 2, self.space.d / 2

        self.nw = DataQuadTree(DataSpace(cx - w/2, cy - h/2, cz - d/2, w, h, d), self.max_points, self.depth + 1)
        self.ne = DataQuadTree(DataSpace(cx + w/2, cy - h/2, cz - d/2, w, h, d), self.max_points, self.depth + 1)
        self.sw = DataQuadTree(DataSpace(cx - w/2, cy + h/2, cz - d/2, w, h, d), self.max_points, self.depth + 1)
        self.se = DataQuadTree(DataSpace(cx + w/2, cy + h/2, cz - d/2, w, h, d), self.max_points, self.depth + 1)
        self.nwf = DataQuadTree(DataSpace(cx - w/2, cy - h/2, cz + d/2, w, h, d), self.max_points, self.depth + 1)
        self.nef = DataQuadTree(DataSpace(cx + w/2, cy - h/2, cz + d/2, w, h, d), self.max_points, self.depth + 1)
        self.swf = DataQuadTree(DataSpace(cx - w/2, cy + h/2, cz + d/2, w, h, d), self.max_points, self.depth + 1)
        self.sef = DataQuadTree(DataSpace(cx + w/2, cy + h/2, cz + d/2, w, h, d), self.max_points, self.depth + 1)

        self.divided = True

    def insert(self, point):
        
        if not self.space.contains(point):#check if the point is in the space
            return False
        if len(self.points) < self.max_points:#check if there is enough space
            self.points.append(point)           
            return True
        
        
        #divide and insert into a sub-node
        if not self.divided: 
            self.divide()
        
        return (
            self.ne.insert(point) or
            self.nw.insert(point) or
            self.se.insert(point) or
            self.sw.insert(point) or
            self.nwf.insert(point) or
            self.nef.insert(point) or
            self.sef.insert(point) or
            self.swf.insert(point)
        )

    def query(self, space, found_points):
       
        if not self.space.intersects(space):  # No intersection with the query space
            return False

        for point in self.points:
            if space.contains(point):
                found_points.append(point)

        if self.divided:
            self.nw.query(space, found_points)
            self.ne.query(space, found_points)
            self.se.query(space, found_points)
            self.sw.query(space, found_points)
            self.nwf.query(space, found_points)
            self.nef.query(space, found_points)
            self.sef.query(space, found_points)
            self.swf.query(space, found_points)

        return found_points

def read_data():
    df = pd.read_csv(r'C:\Users\Thomas\Desktop\Multidimensional-Data-Structures\data\scientists_data_complete.csv')
    points = []

    #insert data into points
    for i in range(len(df)):
        x = alphabet_index(df.iloc[i]['lastName'][0])#we use the number of the first letter of the name
        y = df.iloc[i]['awards']
        z = df.iloc[i]['dblp_records']
        data = (df.iloc[i]['lastName'], df.iloc[i]['awards'],df.iloc[i]['education'], df.iloc[i]['dblp_records'])
        points.append((x, y, z, data))

    return points

def build_data_quad_tree():
    points = read_data()
    point_objects = [DataPoint(x, y, z, data) for x, y, z, data in points]

    max_x = max(point[0] for point in points) 
    max_y = max(point[1] for point in points) 
    max_z = max(point[2] for point in points) 


    boundary = DataSpace(max_x/2  , max_y/2  , max_z/2  , max_x  , max_y , max_z )
    data_quad_tree = DataQuadTree(boundary, max_points=4)
    count = 0
    for point in point_objects:
        count += 1
        data_quad_tree.insert(point)
    #print (count)  
    return data_quad_tree

def test_data_quad_tree(quad_tree,min_l,max_l,min_aw,_min_dblp,_max_dblp):
    min_index = alphabet_index(min_l)
    max_index = alphabet_index(max_l)
    min_awards = min_aw
    min_dblp = _min_dblp
    max_dblp = _max_dblp
    
    points = read_data()
    max_awards = max(point[1] for point in points)

    center_x = (min_index + max_index) / 2
    center_y = (min_awards + max_awards) / 2
    center_z = (min_dblp + max_dblp) / 2
    width = max_index - min_index
    height = max_awards - min_awards 
    depth = max_dblp - min_dblp
    query_space = DataSpace(
        center_x,
        center_y,
        center_z,
        width,
        height,
        depth
    )

    query_results = quad_tree.query(query_space, [])

    #print("Number of scientists found:")
    count=0
    results = []
    
    for res in query_results:
        results.append({
            "lastName": res.data[0],
            "awards": res.data[1],
            "education": res.data[2],
            "dblp_records": res.data[3]
        })
        count+=1

    #print(count)
    return results

# Call the function to build and test the Quad Tree
quad_tree = build_data_quad_tree()
quad_tree_results = test_data_quad_tree(quad_tree,'A','A',3,0,200)

#create an array for the education for LSH
education_strings = [result["education"].encode('utf-8') for result in quad_tree_results]
education_array_from_quad_tree = np.array(education_strings)
print("len of quad_tree data = ",len(education_array_from_quad_tree))
#print(quad_tree_results)
