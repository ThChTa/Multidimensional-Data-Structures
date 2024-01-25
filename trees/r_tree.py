import pandas as pd
from rtree import index
import numpy as np


#Μετατροπή γράμματος σε αριθμό 
def letter_to_number(letter):
    return ord(letter.lower()) - 97

class RTreeIndexer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)#διαβάζουμε το csv αρχείο
        self.datas = []#εδώ θα γίνει αποθήκευση των δεδομένων από το csv αρχείο για χρήση στα queries
        #εδώ φτιάχνουμε τα properties του r-tree για 3 διαστάσεις
        p = index.Property()
        p.dimension = 3 
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.idx3d = index.Index(properties=p) 
        #φτιάχνουμε το index με τα δεδομένα
        self._build_index()

    def _build_index(self):
        #insert στο r-tree
        for i, row in self.data.iterrows():
            
            surname = letter_to_number(row['lastName'][0])
            awards = row['awards']
            dblp_record = row['dblp_records']
            education = row['education']
            self.idx3d.insert(i, (surname, awards, dblp_record, surname, awards, dblp_record)) #πέρασμα row στο r-tree
            data =(row['lastName'], row['awards'], row['education'], row['dblp_records'])#αποθήκευση στην λίστα μας
            self.datas.append(data)
            

    def query(self, left_letter, right_letter, awards_min, dblp_min, dblp_max):
        
        left_letter=letter_to_number(left_letter)
        right_letter=letter_to_number(right_letter)
        query_coordinates = (float(left_letter), awards_min, dblp_min, float(right_letter), float('inf'), dblp_max)#συντεταγμένες του query για να πάρουμε τα σχετικά αποτελέσματα
        
        results = list(self.idx3d.intersection(query_coordinates))
        
        #δομημένη επιστροφή των αποτελεσμάτων της αναζήτησης για χρήση τους στην πορεία
        query_results = []
        for result in results:
            lastName, awards, education, dblp_records = self.datas[result]
            query_results.append({"lastName": lastName, "awards": awards, "education": education, "dblp_records": dblp_records})
        
        return query_results

rtree = RTreeIndexer('./data/scientists_data_complete.csv')
query_results=rtree.query('A', 'C', 1, 0, 1000)
#print(query_results)

#create an array for the education for LSH
education_strings = [result["education"].encode('utf-8') for result in query_results]
education_array_from_r_tree = np.array(education_strings)
print("len of r_tree data = ",len(education_array_from_r_tree))
#print(education_array)





