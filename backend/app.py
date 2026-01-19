"""
Backend Flask server cung cấp API cho các thuật toán đồ thị.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms import shortest_path, traversal, bipartite, conversion
from algorithms import kruskal, ford_fulkerson, fleury, hierholzer

app = Flask(__name__)
# Cho phép CORS cho tất cả các domain, tất cả các route
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    """Route mặc định để kiểm tra server"""
    return jsonify({'status': 'Backend is running', 'message': 'Use /api/ endpoints'})


@app.errorhandler(Exception)
def handle_exception(e):
    """Xử lý lỗi toàn cục để trả về JSON thay vì HTML"""
    response = jsonify({
        "error": "Internal Server Error",
        "message": str(e)
    })
    response.status_code = 500
    # Đảm bảo CORS header luôn có ngay cả khi lỗi
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/shortest-path', methods=['POST'])
def shortest_path_api():
    """Tìm đường đi ngắn nhất"""
    data = request.json
    result = shortest_path.find_shortest_path(
        data['graph'], 
        data['start'], 
        data['end'], 
        data.get('algorithm', 'dijkstra')
    )
    return jsonify(result)


@app.route('/api/bfs', methods=['POST'])
def bfs_api():
    """Duyệt đồ thị theo BFS"""
    data = request.json
    result = traversal.bfs(data['graph'], data['start'])
    return jsonify(result)


@app.route('/api/dfs', methods=['POST'])
def dfs_api():
    """Duyệt đồ thị theo DFS"""
    data = request.json
    result = traversal.dfs(data['graph'], data['start'])
    return jsonify(result)


@app.route('/api/bipartite', methods=['POST'])
def bipartite_api():
    """Kiểm tra đồ thị 2 phía"""
    data = request.json
    result = bipartite.check_bipartite(data['graph'])
    return jsonify(result)


@app.route('/api/convert', methods=['POST'])
def convert_api():
    """Chuyển đổi biểu diễn đồ thị"""
    data = request.json
    result = conversion.convert_graph(
        data['graph'], 
        data['from_type'], 
        data['to_type']
    )
    return jsonify({'result': result})




@app.route('/api/kruskal', methods=['POST'])
def kruskal_api():
    """Thuật toán Kruskal - MST"""
    data = request.json
    result = kruskal.find_mst_kruskal(data['graph'])
    return jsonify(result)


@app.route('/api/ford-fulkerson', methods=['POST'])
def ford_fulkerson_api():
    """Thuật toán Ford-Fulkerson - Max Flow"""
    data = request.json
    result = ford_fulkerson.find_max_flow(
        data['graph'], 
        data['source'], 
        data['sink']
    )
    return jsonify(result)


@app.route('/api/fleury', methods=['POST'])
def fleury_api():
    """Thuật toán Fleury - Euler Path"""
    data = request.json
    result = fleury.find_euler_path(data['graph'], data.get('start'))
    return jsonify(result)


@app.route('/api/hierholzer', methods=['POST'])
def hierholzer_api():
    """Thuật toán Hierholzer - Euler Circuit"""
    data = request.json
    result = hierholzer.find_euler_circuit(data['graph'])
    return jsonify(result)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print(" Server đang chạy tại http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
