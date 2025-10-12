from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify

import pymysql
from functools import wraps
from werkzeug.security import check_password_hash
from filtrage import recommander_produits

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'your_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'sysrec',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def db_connection_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = pymysql.connect(**DB_CONFIG)
            kwargs['conn'] = conn
            return f(*args, **kwargs)
        except pymysql.Error as e:
            print(f"Erreur MySQL: {e}")
            return render_template('error.html', error="Erreur de base de données"), 500
        finally:
            if conn:
                conn.close()
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM user WHERE login = %s', (username,))
                user = cursor.fetchone()

                if user and user['password'].strip() == password.strip():
                    session['user_id'] = user['id_user']
                    session['username'] = user['login']
                    flash('Connexion réussie!', 'success')
                    return redirect(url_for('utilisateur'))
                else:
                    flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
                    return redirect(url_for('login'))
        except Exception as e:
            print(f"Erreur : {e}")
            flash('Erreur lors de la connexion à la base de données.', 'danger')
            return redirect(url_for('login'))
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/utilisateur')
@db_connection_handler
def utilisateur(conn):
    if 'user_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    try:
        user_id = session['user_id']
        with conn.cursor() as cursor:
            # Produits déjà notés avec leurs notes
            cursor.execute('''
                SELECT p.*, n.note
                FROM produit p
                JOIN notes n ON n.id_produit = p.id_produit
                WHERE n.id_user = %s AND n.note IS NOT NULL
            ''', (user_id,))
            produits_notes = cursor.fetchall()

            # Produits recommandés
            ids_recommandes = recommander_produits(user_id, conn)
            print("Produits recommandés IDs:", ids_recommandes)

            produits_recommandes = []
            if ids_recommandes:
                placeholders = ','.join(['%s'] * len(ids_recommandes))
                cursor.execute(f'''
                    SELECT p.*, n.note
                    FROM produit p
                    LEFT JOIN notes n ON n.id_produit = p.id_produit AND n.id_user = %s
                    WHERE p.id_produit IN ({placeholders})
                ''', (user_id, *ids_recommandes))
                produits_recommandes = cursor.fetchall()

            # Produits disponibles avec leurs notes
            cursor.execute('''
                SELECT p.*, n.note
                FROM produit p
                LEFT JOIN notes n ON n.id_produit = p.id_produit AND n.id_user = %s
            ''', (user_id,))
            produits_disponibles = cursor.fetchall()

        return render_template(
            'utilisateur.html',
            produits_notes=produits_notes,
            produits_recommandes=produits_recommandes,
            produits_disponibles=produits_disponibles
        )

    except Exception as e:
        print(f"Erreur: {e}")
        flash('Une erreur est survenue.', 'danger')
        return redirect(url_for('index'))



@app.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté avec succès.', 'success')
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/computers')
@db_connection_handler
def computers(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM produit')
            products_list = cursor.fetchall()
        return render_template('computers.html', products=products_list)
    except Exception as e:
        print(f"Erreur : {e}")
        return render_template('error.html', error="Erreur lors de la récupération des produits"), 500



@app.route('/product/<int:id_produit>')
@db_connection_handler
def product_details(id_produit, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM produit WHERE id_produit = %s', (id_produit,))
            product = cursor.fetchone()
            if not product:
                return render_template('error.html', error="Produit non trouvé"), 404

            top_ids = [product.get('top1'), product.get('top2'), product.get('top3')]
            top_ids = [tid for tid in top_ids if tid is not None]

            related_products = []
            if top_ids:
                format_strings = ','.join(['%s'] * len(top_ids))
                cursor.execute(f"SELECT * FROM produit WHERE id_produit IN ({format_strings})", tuple(top_ids))
                related_products = cursor.fetchall()

        return render_template("details.html", product=product, products_dict={p['id_produit']: p for p in related_products})
    except Exception as e:
        print(f"Erreur : {e}")
        return render_template('error.html', error="Erreur lors de l'affichage des détails du produit"), 500

@app.route('/test')
def test():
    return "Page de test en fonctionnement !"

@app.route('/submit-rating', methods=['POST'])
@db_connection_handler
def submit_rating(conn):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Utilisateur non connecté'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Données manquantes'}), 400

        product_id = data.get('productId')
        rating = data.get('rating')
        user_id = session['user_id']

        if product_id is None or rating is None:
            return jsonify({'success': False, 'message': 'Produit ou note manquant'}), 400

        # Validation des données
        try:
            product_id = int(product_id)
            rating = int(rating)
        except ValueError:
            return jsonify({'success': False, 'message': 'Types invalides'}), 400

        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Note invalide (1 à 5 requis)'}), 400

        with conn.cursor() as cursor:
            # Vérification des clés étrangères
            cursor.execute("SELECT * FROM produit WHERE id_produit = %s", (product_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'Produit introuvable'}), 400

            cursor.execute("SELECT * FROM user WHERE id_user = %s", (user_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 400

            # Vérifie si une note existe déjà
            cursor.execute(
                "SELECT note FROM notes WHERE id_user = %s AND id_produit = %s",
                (user_id, product_id)
            )
            existing = cursor.fetchone()

            if existing:
                # Mise à jour de la note
                cursor.execute(
                    "UPDATE notes SET note = %s WHERE id_user = %s AND id_produit = %s",
                    (rating, user_id, product_id)
                )
            else:
                # Insertion de la nouvelle note
                cursor.execute(
                    "INSERT INTO notes (id_user, id_produit, note) VALUES (%s, %s, %s)",
                    (user_id, product_id, rating)
                )

            conn.commit()

        return jsonify({'success': True, 'message': 'Note enregistrée avec succès'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erreur serveur : {str(e)}'}), 500

@app.route('/submit-purchase', methods=['POST'])
@db_connection_handler
def submit_purchase(conn):
    # Vérification si l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Utilisateur non connecté'}), 401

    user_id = session['user_id']  # Récupération de l'ID utilisateur depuis la session
    product_id = request.json.get('productId')  # Récupération de l'ID du produit depuis la requête
    quantity = request.json.get('quantity', 1)  # Quantité (par défaut à 1)

    # Insertion dans la base de données
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO achats (id_user, id_produit, quantite)
                VALUES (%s, %s, %s)
            ''', (user_id, product_id, quantity))
            conn.commit()

        return jsonify({'success': True, 'message': 'Achat effectué avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5001, use_reloader=False)