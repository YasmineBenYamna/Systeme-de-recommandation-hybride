import mysql.connector
import nltk
from nltk.stem.snowball import FrenchStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm
import numpy
from nltk.corpus import stopwords
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr

# (Optionnel) Téléchargement des ressources NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sysrec"
)
cursor = conn.cursor()

# Fonctions de similarité
def SimilariteCosinus(i, j, matriceTFIDF):
    vecteur_i = matriceTFIDF[i]
    vecteur_j = matriceTFIDF[j]
    if norm(vecteur_i) == 0 or norm(vecteur_j) == 0:
        return 0
    return dot(vecteur_i, vecteur_j) / (norm(vecteur_i) * norm(vecteur_j))

def SimilariteJaccard(i, j, matriceTFIDF):
    set_i = set(matriceTFIDF[i])
    set_j = set(matriceTFIDF[j])
    intersection = len(set_i.intersection(set_j))
    union = len(set_i.union(set_j))
    return intersection / union if union != 0 else 0

def SimilariteEuclidienne(i, j, matriceTFIDF):
    return euclidean(matriceTFIDF[i], matriceTFIDF[j])

def SimilaritePearson(i, j, matriceTFIDF):
    corr, _ = pearsonr(matriceTFIDF[i], matriceTFIDF[j])
    return corr if not numpy.isnan(corr) else 0

# Récupération des produits
cursor.execute("SELECT * FROM produit")
Produits = cursor.fetchall()

dictProduits = {}
idProduits = []
StopList = set(stopwords.words('french'))
stemer = FrenchStemmer()

# Prétraitement des descriptions
for p in Produits:
    idPdt = int(p[0])
    idProduits.append(idPdt)
    Description = p[1]
    Mots = nltk.word_tokenize(Description)
    MotsStems = [stemer.stem(m.lower()) for m in Mots]
    ListFinalMots = [m for m in MotsStems if m not in StopList]
    dictProduits[idPdt] = ListFinalMots

# TF-IDF
descriptions = [' '.join(dictProduits[idPdt]) for idPdt in idProduits]
vectorizer = TfidfVectorizer()
matriceTFIDF = vectorizer.fit_transform(descriptions).toarray()

# Matrices de similarité (Cosinus ici)
matriceSimilariteCosinus = numpy.zeros((len(idProduits), len(idProduits)))
for i in range(len(idProduits)):
    for j in range(len(idProduits)):
        matriceSimilariteCosinus[i][j] = SimilariteCosinus(i, j, matriceTFIDF)

# Affichage TF-IDF
print("\nListe des termes TF-IDF :")
termes = vectorizer.get_feature_names_out()
print(termes)

print("\nMatrice TF-IDF :")
for i, vecteur in enumerate(matriceTFIDF):
    print(f"\nProduit {idProduits[i]} :")
    for j, score in enumerate(vecteur):
        if score > 0:
            print(f"  {termes[j]} : {score:.4f}")

# Ajout colonnes top1/top2/top3 si manquantes
for top in ['top1', 'top2', 'top3']:
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'produit' AND COLUMN_NAME = '{top}'
    """)
    if cursor.fetchone() is None:
        cursor.execute(f"ALTER TABLE produit ADD COLUMN {top} INT")

# Calcul et insertion des recommandations
N = 3
for i in range(len(idProduits)):
    idProduitCible = idProduits[i]
    similarites = matriceSimilariteCosinus[i]
    produits_similaires = sorted(
        [(j, similarites[j]) for j in range(len(similarites)) if j != i],
        key=lambda x: x[1], reverse=True
    )
    recommandations = [idProduits[j] for j, _ in produits_similaires[:N]]
    cursor.execute("""
        UPDATE produit
        SET top1 = %s, top2 = %s, top3 = %s
        WHERE id_produit = %s
    """, (
        recommandations[0] if len(recommandations) > 0 else None,
        recommandations[1] if len(recommandations) > 1 else None,
        recommandations[2] if len(recommandations) > 2 else None,
        idProduitCible
    ))

conn.commit()

# Affichage des recommandations
cursor.execute("SELECT id_produit, top1, top2, top3 FROM produit")
for row in cursor.fetchall():
    print(f"Produit ID {row[0]}: Top 1 - {row[1]}, Top 2 - {row[2]}, Top 3 - {row[3]}")

# Fermeture
conn.close()
