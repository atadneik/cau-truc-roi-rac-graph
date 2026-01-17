/**
 * Class API - Gọi các endpoint backend
 */
class API {
    constructor(baseURL = null) {
        // Nếu có baseURL truyền vào thì dùng
        if (baseURL) {
            this.baseURL = baseURL;
        }
        // Nếu đang chạy trên localhost (dev), mặc định port 5000
        else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            this.baseURL = 'http://localhost:5000';
        }
        // Nếu chạy trên production (Render/Netlify), giả định backend cùng domain (nếu dùng proxy)
        // Hoặc người dùng có thể set biến global API_URL
        else {
            this.baseURL = window.API_URL || ''; // Empty string means relative path
        }
    }

    /**
     * Gọi API chung
     */
    async call(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                let errorMessage = `Lỗi HTTP! trạng thái: ${response.status}`;
                try {
                    const errorBody = await response.json();
                    if (errorBody.message) {
                        errorMessage += ` - ${errorBody.message}`;
                    } else if (errorBody.error) {
                        errorMessage += ` - ${errorBody.error}`;
                    }
                } catch (e) {
                    // Ignore JSON parse error if body is not JSON
                }
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('Gọi API thất bại:', error);
            throw error;
        }
    }

    /**
     * Đường đi ngắn nhất (Dijkstra / Bellman-Ford)
     */
    async shortestPath(graph, start, end, algorithm = 'dijkstra') {
        return await this.call('/api/shortest-path', {
            graph: graph,
            start: start,
            end: end,
            algorithm: algorithm
        });
    }

    /**
     * BFS
     */
    async bfs(graph, start) {
        return await this.call('/api/bfs', {
            graph: graph,
            start: start
        });
    }

    /**
     * DFS
     */
    async dfs(graph, start) {
        return await this.call('/api/dfs', {
            graph: graph,
            start: start
        });
    }

    /**
     * Kiểm tra đồ thị 2 phía (Bipartite)
     */
    async checkBipartite(graph) {
        return await this.call('/api/bipartite', {
            graph: graph
        });
    }

    /**
     * Chuyển đổi biểu diễn đồ thị
     */
    async convert(graph, fromType, toType) {
        return await this.call('/api/convert', {
            graph: graph,
            from_type: fromType,
            to_type: toType
        });
    }

    /**
     * Thuật toán Prim
     */
    async prim(graph) {
        return await this.call('/api/prim', {
            graph: graph
        });
    }

    /**
     * Thuật toán Kruskal
     */
    async kruskal(graph) {
        return await this.call('/api/kruskal', {
            graph: graph
        });
    }

    /**
     * Thuật toán Ford-Fulkerson
     */
    async fordFulkerson(graph, source, sink) {
        return await this.call('/api/ford-fulkerson', {
            graph: graph,
            source: source,
            sink: sink
        });
    }

    /**
     * Thuật toán Fleury
     */
    async fleury(graph, start = null) {
        return await this.call('/api/fleury', {
            graph: graph,
            start: start
        });
    }

    /**
     * Thuật toán Hierholzer
     */
    async hierholzer(graph) {
        return await this.call('/api/hierholzer', {
            graph: graph
        });
    }

    /**
     * Kiểm tra sức khỏe hệ thống
     */
    async health() {
        const response = await fetch(`${this.baseURL}/api/health`);
        return await response.json();
    }
}
