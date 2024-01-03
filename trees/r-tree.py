import pandas as pd
from rtree import index



def letter_to_number(letter):
    return ord(letter.upper()) - 65

class RTreeIndexer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.datas = []
        p = index.Property()
        p.dimension = 3
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.idx3d = index.Index(properties=p)
        self._build_index()

    def _build_index(self):
        for i, row in self.data.iterrows():
            # Αντικαταστήστε 'surname', 'awards', 'DBLP_Record' με τα σωστά ονόματα στηλών
            surname = letter_to_number(row['surname'][0])
            awards = row['awards']
            dblp_record = row['dblp']
            education = row['education']
            

            # Αντικαταστήστε αυτές τις συντεταγμένες με τη σωστή λογική μετατροπής στοιχείων σε συντεταγμένες
            self.idx3d.insert(i, (surname, awards, dblp_record, surname, awards, dblp_record))
            data =(row['surname'], row['awards'], row['education'], row['dblp'])
            self.datas.append(data)
            # print(self.idx3d)
            

    def query(self, left_letter, right_letter, awards_min, dblp_min, dblp_max):
        # Αντικαταστήστε αυτές τις συντεταγμένες με τη σωστή λογική μετατροπής των ερωτημάτων σε συντεταγμένες
        left_letter=letter_to_number(left_letter)
        right_letter=letter_to_number(right_letter)
        query_coordinates = (float(left_letter), awards_min, dblp_min, float(right_letter), float('inf'), dblp_max)
        # print([i for i in self.idx3d.intersection(query_coordinates)])
        results = list(self.idx3d.intersection(query_coordinates))
        print(results)
        query_results = []
        for result in results:
            surname, awards, education, dblp = self.datas[result]
            query_results.append({"surname": surname, "awards": awards, "education": education, "dblp": dblp})
        
        return query_results

rtree = RTreeIndexer('./data/data.csv')
query_results=rtree.query('A', 'A', 2, 100, 160)
print(query_results)

