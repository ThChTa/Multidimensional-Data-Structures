import pandas as pd
import numpy as np

def letter_to_number(letter):
    return ord(letter.lower()) - 97

# Κλάση που αντιπροσωπεύει έναν κόμβο σε ένα range tree
class Node:
    def __init__(self, value, points=None, dimension=1):
        self.dimension = dimension
        
        #Αν ο κόμβος βρίσκεται σε ένα 1D δέντρο
        if self.dimension == 1: 
            self.y = value
            self.i_list = points if points else []
            
        #Αν ο κόμβος βρίσκεται σε ένα 2D δέντρο
        elif self.dimension == 2: 
            self.x = value
            self.y_tree = RangeTree1D(points) if points else None
            
        #Αν ο κόμβος βρίσκεται σε ένα 3D δέντρο
        elif self.dimension == 3: 
            self.z = value
            self.xy_tree = RangeTree2D(points) if points else None
            

        
        self.left = None #Αριστερό παιδί του κόμβου
        self.right = None  #Δεξί παιδί του κόμβου
        self.height = 1 #Ύψος του κόμβου στο δέντρο



class RangeTree1D:
    def __init__(self, points):
        #Κατασκευή 1D Range Tree βάσει των δοσμένων σημείων
        self.root = self.constructTree(points)

    def insert(self, root, y, i):
        #Εισαγωγή ενός νέου σημείου στο δέντρο
        if not root:
            return Node(y, [i])  #Δημιουργία νέου κόμβου εάν δεν υπάρχει

        if y < root.y:
            #Εισαγωγή στο αριστερό υποδέντρο εάν το y είναι μικρότερο από τον τρέχοντα κόμβο
            root.left = self.insert(root.left, y, i)
        else:
            #Εισαγωγή στο δεξί υποδέντρο εάν το y είναι μεγαλύτερο ή ίσο με τον τρέχοντα κόμβο
            root.right = self.insert(root.right, y, i)

        #Υπολογισμός ύψους του τρέχοντα κόμβου με βάση τα υποδέντρα που έχει μέχρι εκείνη την στιγμή
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        #Υπολογισμός ισορροπίας του κόμβου για την αποφυγή ανισορροπίας στο δέντρο
        balance = self.balance(root)

        #Περιπτώσεις ανισορροπίας και εκτέλεση ανάλογων περιστροφών
        if balance > 1:
            if y > root.left.y:
                root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)

        if balance < -1:
            if y < root.right.y:
                root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)

        return root

    def constructTree(self, points):
        #Δημιουργία του Range Tree από μία λίστα σημείων
        root = None
        for _, y, i in points:
            root = self.insert(root, y, i)
        return root

    def height(self, node):
        #Επιστρέφει το ύψος ενός κόμβου
        return 0 if not node else node.height

    def balance(self, node):
        #Υπολογισμός της ισορροπίας ενός κόμβου
        return 0 if not node else self.height(node.left) - self.height(node.right)

    def rotateRight(self, y):
        #Δεξιά περιστροφή για τη διατήρηση της ισορροπίας του δέντρου
        x = y.left
        temp1 = x.right
        x.right = y
        y.left = temp1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    def rotateLeft(self, x):
        #Αριστερή περιστροφή για τη διατήρηση της ισορροπίας του δέντρου
        y = x.right
        temp2 = y.left
        y.left = x
        x.right = temp2
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        return y

    def query(self, node, y1, y2, result):
        #Εκτέλεση ερωτήματος στο Range Tree για την εύρεση σημείων εντός ενός εύρους
        if not node:
            return
        if y1 <= node.y <= y2:
            for i in node.i_list:
                result.append((node.y, i))
        if y1 < node.y:
            self.query(node.left, y1, y2, result)
        if y2 > node.y:
            self.query(node.right, y1, y2, result)






class RangeTree2D:
    def __init__(self, points):
        self.root = self.constructTree(points) 

    def insert(self, root, x, y, i, points):
        
        if not root:
            return Node(x, [(x, y, i)], 2)
        
        if x < root.x:   
            root.left = self.insert(root.left, x, y, i, [(x, y, i)])
        else:              
            root.right = self.insert(root.right, x, y, i, [(x, y, i)])

        
        root.height = 1 + max(self.height(root.left), self.height(root.right))

       
        balance = self.balance(root)

       
        if balance > 1:
            
            if x > root.left.x:
                root.left = self.rotateLeft(root.left)
            
            return self.rotateRight(root)

        
        if balance < -1:
            
            if x < root.right.x:
                root.right = self.rotateRight(root.right)
            
            return self.rotateLeft(root)

        return root

    def constructTree(self, points):
        root = None
        for x,y,_,i in points:
            root = self.insert(root, x, y, i, [x,y,i])
        return root

    
    def height(self, node):
        if not node:
            return 0
        return node.height

    
    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    
    def rotateRight(self, y):
        x = y.left
        temp1 = x.right
        x.right = y
        y.left = temp1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    
    def rotateLeft(self, x):
        y = x.right
        temp2 = y.left
        y.left = x
        x.right = temp2
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        return y

 
    def query(self, node, x1, x2, y1, y2, result):
        if not node:
            return
        if x1 <= node.x <= x2:
            y_result = []
            node.y_tree.query(node.y_tree.root, y1, y2, y_result)
            for y, i in y_result:
                result.append((node.x, y, i))
        if x1 < node.x:
            self.query(node.left, x1, x2, y1, y2, result)
        if x2 > node.x:
            self.query(node.right, x1, x2, y1, y2, result)




class RangeTree3D:
    def __init__(self, points):
        self.root = self.constructTree(points) 

    def insert(self, root, x, y, z, i, points):
        
        if not root:
            return Node(z, [(x, y, z, i)], 3)
        
        if z < root.z:
            root.left = self.insert(root.left, x, y, z, i, [(x, y, z, i)])
        else:
            root.right = self.insert(root.right, x, y, z, i, [(x, y, z, i)])

        
        root.height = 1 + max(self.height(root.left), self.height(root.right))

       
        balance = self.balance(root)

       
        if balance > 1:
            if z > root.left.z:
                root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)

      
        if balance < -1:
            if z < root.right.z:
                root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)

        return root

    def height(self, node):
        if not node:
            return 0
        return node.height

    
    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

   
    def rotateRight(self, y):
        x = y.left
        temp1 = x.right
        x.right = y
        y.left = temp1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    
    def rotateLeft(self, x):
        y = x.right
        temp2 = y.left
        y.left = x
        x.right = temp2
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        return y

    def constructTree(self, points):
        root = None
        for point in points:
            x, y, z, i = point
            root = self.insert(root, x, y, z, i, [point])
        return root

   
    def query(self, node, x1, x2, y1, y2, z1, z2, result):
        if not node:
            return
        if z1 <= node.z <= z2:
            xy_result = []
            node.xy_tree.query(node.xy_tree.root, x1, x2, y1, y2, xy_result)
            for x, y, i in xy_result:
                result.append((x, y, node.z, i))
        if z1 < node.z:
            self.query(node.left, x1, x2, y1, y2, z1, z2, result)
        if z2 > node.z:
            self.query(node.right, x1, x2, y1, y2, z1, z2, result)

def build_range_tree():
    #Φορτώνει ένα αρχείο CSV σε ένα DataFrame
    df = pd.read_csv('./data/scientists_data_complete.csv')
    points = []

    #Επαναλαμβάνει μέσα στο DataFrame και μετατρέπει κάθε γραμμή σε ένα σημείο
    for i in range(len(df)):
        x = letter_to_number(df.iloc[i]['lastName'][0])  #Μετατρέπει το πρώτο γράμμα του επωνύμου σε αριθμό
        y = df.iloc[i]['awards']                         #Αριθμός βραβείων
        z = df.iloc[i]['dblp_records']                   #Αριθμός εγγραφών DBLP
        points.append((x, y, z, i))                      #Προσθέτει το σημείο (x, y, z, index) στη λίστα

    #Δημιουργεί ένα 3D range tree από τα σημεία
    range_tree = RangeTree3D(points)    
    return range_tree  #Επιστρέφει το δημιουργημένο range tree

def query_range_tree(range_tree, min_letter, max_letter, num_awards, min_dblp, max_dblp):
    #Μετατρέπει τις εισόδους γραμμάτων σε μορφή αριθμού
    min_letter = letter_to_number(min_letter)
    max_letter = letter_to_number(max_letter)

    #Καθορίζει τα εύρη ερωτήματος για κάθε διάσταση
    x_range = (min_letter, max_letter)  #Εύρος πρώτων γραμμάτων των επωνύμων
    y_range = (num_awards, float('inf')) #Ελάχιστος αριθμός βραβείων
    z_range = (min_dblp, max_dblp)       #Εύρος για εγγραφές DBLP

    query_results = []

    #Εκτελεί το εύρος ερωτήματος στο δέντρο
    range_tree.query(range_tree.root, x_range[0], x_range[1], y_range[0], y_range[1], z_range[0], z_range[1], query_results)

    final_results = []
    df = pd.read_csv('./data/scientists_data_complete.csv')
   
    #Εξάγει και διαμορφώνει τα αποτελέσματα του ερωτήματος
    for result in query_results:
        index = result[3]  #Λαμβάνει τον αρχικό δείκτη του DataFrame
        #Ανακτά και αποθηκεύει σχετικές πληροφορίες
        surname = df.iloc[index]['lastName']
        awards = df.iloc[index]['awards']
        education = df.iloc[index]['education']
        dblp_records = df.iloc[index]['dblp_records']
        final_results.append({"lastName": surname, "awards": awards, "education": education, "dblp_records": dblp_records})

    return final_results  #Επιστρέφει τα διαμορφωμένα αποτελέσματα


range_tree = build_range_tree()
results = query_range_tree(range_tree, 'A', 'A', 3, 0, 200)
education_strings = [result.get("education","").encode('utf-8') for result in results]
education_array_from_range_tree = np.array(education_strings)
print("len of range_tree data = ",len(education_array_from_range_tree))
#print(results)  
