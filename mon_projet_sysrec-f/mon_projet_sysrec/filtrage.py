import pymysql.cursors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
    def __init__(self):
        self.conn = None
        self.users = []
        self.products = []
        self.ratings_matrix = None
        self.user_index = {}
        self.product_index = {}

    def connect_db(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="sysrec",
                autocommit=False
            )
            return True
        except pymysql.MySQLError as err:
            print(f"Erreur MySQL: {err}")
            return False

    def load_data(self, conn):
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id_user FROM user ORDER BY id_user")
            self.users = [row['id_user'] for row in cursor.fetchall()]
            self.user_index = {user_id: idx for idx, user_id in enumerate(self.users)}

            cursor.execute("SELECT id_produit FROM produit ORDER BY id_produit")
            self.products = [row['id_produit'] for row in cursor.fetchall()]
            self.product_index = {prod_id: idx for idx, prod_id in enumerate(self.products)}

            self.ratings_matrix = np.zeros((len(self.users), len(self.products)))

            cursor.execute("SELECT id_user, id_produit, note FROM notes")
            for row in cursor.fetchall():
                try:
                    user_idx = self.user_index[row['id_user']]
                    prod_idx = self.product_index[row['id_produit']]
                    if row['note'] is None or row['note'] == 0:
                        self.ratings_matrix[user_idx][prod_idx] = 0
                    else:
                        self.ratings_matrix[user_idx][prod_idx] = row['note']
                except KeyError:
                    continue

            return True
        except Exception as e:
            print(f"Erreur chargement données: {e}")
            return False

    def calculate_similarities(self):
        try:
            # Remplace les 0 par NaN pour ignorer dans le calcul de la moyenne
            masked_ratings = np.where(self.ratings_matrix > 0, self.ratings_matrix, np.nan)
            user_means = np.nanmean(masked_ratings, axis=1, keepdims=True)
            norm_ratings = self.ratings_matrix - np.nan_to_num(user_means)
            return cosine_similarity(norm_ratings)
        except Exception as e:
            print(f"Erreur calcul similarités: {e}")
            return None

    def get_recommendations(self, user_id, similarity_matrix, k=3):
        if user_id not in self.user_index:
            return []
    
        user_idx = self.user_index[user_id]
        predictions = []
    
        for prod_idx, product_id in enumerate(self.products):
            if self.ratings_matrix[user_idx][prod_idx] == 0:  # Produit non noté
                similar_users = []
                for other_user_idx in range(len(self.users)):
                    if other_user_idx != user_idx and self.ratings_matrix[other_user_idx][prod_idx] > 0:
                        similarity = similarity_matrix[user_idx][other_user_idx]
                        rating = self.ratings_matrix[other_user_idx][prod_idx]
                        similar_users.append((similarity, rating))
    
                similar_users.sort(reverse=True)
                similar_users = similar_users[:k]
    
                if similar_users:
                    sum_sim = sum(sim for sim, _ in similar_users)
                    if sum_sim > 0:
                        pred_rating = sum(sim * rating for sim, rating in similar_users) / sum_sim
                        print(f"Produit {product_id} - Prédiction: {pred_rating} (utilisé par {len(similar_users)} utilisateurs similaires)")
                        if pred_rating >= 0:
                            predictions.append((product_id, pred_rating))
                    else:
                        print(f"Produit {product_id} - Similarité nulle ou négative")
                else:
                    print(f"Produit {product_id} - Aucun utilisateur similaire avec une note")
        return sorted(predictions, key=lambda x: x[1], reverse=True)


def recommander_produits(user_id, conn):
    try:
        cf = CollaborativeFiltering()
        if cf.load_data(conn):
            sim_matrix = cf.calculate_similarities()
            if sim_matrix is not None:
                recommandations = cf.get_recommendations(user_id, sim_matrix)
                print("Recommandations trouvées :", recommandations)
                return [prod_id for prod_id, _ in recommandations]
        return []
    except Exception as e:
        print("Erreur dans recommander_produits:", e)
        return []
