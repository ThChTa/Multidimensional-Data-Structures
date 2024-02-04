import pandas as pd  # Εισαγωγή της βιβλιοθήκης pandas
import numpy as np


#Συνάρτηση για μετατροπή γραμμάτων σε αριθμούς
def letter_to_index(letter):
    return ord(letter.lower()) - 97

#Κλάση για τον κόμβο του KD δένδρου
class KDNode:
    def __init__(self, point, dimension):
        self.point = point  #Σημείο του κόμβου
        self.left_child = None  
        self.right_child = None  
        self.dimension = dimension 

#Κλάση για το KD δένδρο
class KDDimensionalTree:
    def __init__(self):
        self.root_node = None

    #Συνάρτηση για τη δημιουργία του δένδρου
    def construct(self, points, depth=0):
        if not points:
            return None

        k = depth % 3  #Επιλογή διάστασης
        points.sort(key=lambda x: x[k])  #Ταξινόμηση σημείων
        median_index = len(points) // 2  #Εύρεση μέσης τιμής

        node = KDNode(points[median_index], k)
        node.left_child = self.construct(points[:median_index], depth + 1)
        node.right_child = self.construct(points[median_index + 1:], depth + 1)

        return node 

    #Συνάρτηση για εισαγωγή σημείου στο δένδρο
    def insert_point(self, point, depth=0, current_node=None):
        if current_node is None:
            if self.root_node is None:
                self.root_node = KDNode(point, 0)
                return
            current_node = self.root_node

        k = depth % 3  #Επιλογή διάστασης

        #Σύγκριση και εισαγωγή σημείου
        if point[k] < current_node.point[k]:
            if current_node.left_child is None:
                current_node.left_child = KDNode(point, (depth + 1) % 3)
            else:
                self.insert_point(point, depth + 1, current_node.left_child)
        else:
            if current_node.right_child is None:
                current_node.right_child = KDNode(point, (depth + 1) % 3)
            else:
                self.insert_point(point, depth + 1, current_node.right_child)

    #Συνάρτηση για αναζήτηση σημείων εντός περιοχής
    def search(self, area, current_node=None):
        if current_node is None:
            current_node = self.root_node

        if current_node is None:
            return []

        x_min, y_min, z_min, x_max, y_max, z_max = area  #Οριοθέτηση περιοχής
        found_points = []

        #Έλεγχος αν το σημείο βρίσκεται εντός της περιοχής
        if x_min <= current_node.point[0] <= x_max and y_min <= current_node.point[1] <= y_max and z_min <= current_node.point[2] <= z_max:
            found_points.append(current_node.point)

        #Αναδρομική αναζήτηση στα παιδιά του κόμβου
        if current_node.left_child and (current_node.dimension != 0 or (x_min <= current_node.point[0])):
            found_points.extend(self.search(area, current_node.left_child))

        if current_node.right_child and (current_node.dimension != 0 or (x_max >= current_node.point[0])):
            found_points.extend(self.search(area, current_node.right_child))

        return found_points

#Συνάρτηση για δημιουργία KD δένδρου και αναζήτηση
def create_and_query_kdtree(file_path, min_letter, max_letter, min_awards, min_dblp, max_dblp):
    df = pd.read_csv(file_path)  #Φόρτωση δεδομένων από το csv αρχείο
    points = []

    #Δημιουργία σημείων από τα δεδομένα
    for i in range(len(df)):
        x = letter_to_index(df.iloc[i]['lastName'][0])
        y = df.iloc[i]['awards']
        z = df.iloc[i]['dblp_records']
        points.append((x, y, z, i))

    kd_tree = KDDimensionalTree()
    kd_tree.root_node = kd_tree.construct(points)  #Δημιουργία δένδρου

    min_l = letter_to_index(min_letter)
    max_l = letter_to_index(max_letter)

    #Οριοθέτηση περιοχής για την αναζήτηση
    query_area = (min_l, min_awards, min_dblp, max_l, float('inf'), max_dblp)
    query_results = kd_tree.search(query_area)  #Αναζήτηση στο δένδρο

    results = []
    for point in query_results:
        idx = point[3]  #Αντιστοίχιση σημείου με δεδομένα
        results.append({
            "lastName": df.iloc[idx]['lastName'],  
            "awards": df.iloc[idx]['awards'],  
            "education": df.iloc[idx]['education'],  
            "dblp_records": df.iloc[idx]['dblp_records']  
        })

    return results

#Δημιουργία και αναζήτηση στο KD δένδρο
kd_tree_results = create_and_query_kdtree('./data/scientists_data_complete.csv', 'A', 'A', 3, 0, 200)

lastname = [result["lastName"].encode('utf-8') for result in kd_tree_results]
awards = [str(result["awards"]).encode('utf-8') for result in kd_tree_results]
education_strings = [result["education"].encode('utf-8') for result in kd_tree_results]
dblp_records = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]

lastname_array_from_kd_tree = np.array(lastname)
awards_array_from_kd_tree = np.array(awards)
education_array_from_kd_tree = np.array(education_strings)  #for lsh
dblp_records_array_from_kd_tree = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]


print("len of kd_tree data = ",len(education_array_from_kd_tree))
#print(kd_tree_results)
