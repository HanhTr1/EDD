from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS


apikey="c5a5b9f230f4a2ffabacf63e19350867"

def get_db_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='elfdeliverydash',
        user='root',
        password='192055',
        autocommit=True,
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci', )
    return connection

app = Flask(__name__)
CORS(app)


@app.route('/get_top_players', methods=['GET'])
def get_top_players():

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        sql_ranking = f"SELECT ranking, player_name, letter_count  FROM player WHERE result = 'win'  ORDER BY ranking ASC LIMIT 10"
        cursor.execute(sql_ranking)
        top_players = cursor.fetchmany(size=10)

        if top_players:
            cursor.close()
            connection.close()
            return jsonify({"top_players": top_players})

        else:
            cursor.close()
            connection.close()
            return jsonify({"error": "No players found"}), 404

    except Exception as e:
        app.logger.error(f"Error getting top players: {e}")
        return jsonify({"error": "Internal server error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
