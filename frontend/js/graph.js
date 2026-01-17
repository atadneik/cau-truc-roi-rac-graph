/**
 * Class Graph - Quản lý cấu trúc đồ thị
 * Lưu trữ nodes và edges
 */
class Graph {
    constructor() {
        this.nodes = [];
        this.edges = [];
        this.directed = false;
        this.nodeIdCounter = 1;
    }

    /**
     * Thêm đỉnh mới
     */
    addNode(x, y, id = null) {
        const nodeId = id || this.nodeIdCounter++;
        const node = {
            id: nodeId,
            x: x,
            y: y,
            label: nodeId.toString()
        };
        this.nodes.push(node);
        this.emitGraphUpdate();
        return node;
    }

    /**
     * Xóa đỉnh
     */
    removeNode(nodeId) {
        // Xóa tất cả cạnh liên quan
        this.edges = this.edges.filter(edge =>
            edge.from !== nodeId && edge.to !== nodeId
        );
        // Xóa đỉnh
        this.nodes = this.nodes.filter(node => node.id !== nodeId);
        this.emitGraphUpdate();
    }

    /**
     * Thêm cạnh
     */
    addEdge(fromId, toId, weight = 1, isDirected = false) {
        // Kiểm tra cạnh đã tồn tại chưa
        const existingEdge = this.edges.find(e => e.from === fromId && e.to === toId);
        if (existingEdge) {
            // Cập nhật cạnh hiện có
            existingEdge.weight = weight;
            existingEdge.isDirected = isDirected;
            this.emitGraphUpdate();
            return existingEdge;
        }

        const edge = {
            from: fromId,
            to: toId,
            weight: weight,
            isDirected: isDirected
        };
        this.edges.push(edge);
        this.emitGraphUpdate();
        return edge;
    }

    /**
     * Xóa cạnh
     */
    removeEdge(fromId, toId) {
        this.edges = this.edges.filter(edge =>
            !(edge.from === fromId && edge.to === toId)
        );
        this.emitGraphUpdate();
    }

    /**
     * Kiểm tra cạnh tồn tại
     */
    hasEdge(fromId, toId) {
        return this.edges.some(edge =>
            edge.from === fromId && edge.to === toId
        );
    }

    /**
     * Tìm đỉnh tại vị trí (x, y)
     */
    findNodeAt(x, y, radius = 25) {
        return this.nodes.find(node => {
            const dx = node.x - x;
            const dy = node.y - y;
            return Math.sqrt(dx * dx + dy * dy) <= radius;
        });
    }

    /**
     * Lấy đỉnh theo ID
     */
    getNode(nodeId) {
        return this.nodes.find(node => node.id === nodeId);
    }

    /**
     * Set loại đồ thị
     */
    setDirected(directed) {
        this.directed = directed;
    }

    /**
     * Chuyển đổi sang JSON
     */
    toJSON() {
        return {
            nodes: this.nodes,
            edges: this.edges,
            directed: this.directed
        };
    }

    /**
     * Tải từ JSON
     */
    fromJSON(data) {
        this.nodes = data.nodes || [];
        this.edges = data.edges || [];
        this.directed = data.directed || false;

        // Cập nhật counter
        if (this.nodes.length > 0) {
            const maxId = Math.max(...this.nodes.map(n =>
                typeof n.id === 'number' ? n.id : parseInt(n.id) || 0
            ));
            this.nodeIdCounter = maxId + 1;
        }
    }

    /**
     * Xóa toàn bộ đồ thị
     */
    clear() {
        this.nodes = [];
        this.edges = [];
        this.nodeIdCounter = 1;
    }

    /**
     * Chuyển sang ma trận kề
     */
    toAdjacencyMatrix() {
        const n = this.nodes.length;
        const matrix = Array(n).fill(0).map(() => Array(n).fill(0));
        const nodeIndexMap = {};

        this.nodes.forEach((node, index) => {
            nodeIndexMap[node.id] = index;
        });

        this.edges.forEach(edge => {
            const i = nodeIndexMap[edge.from];
            const j = nodeIndexMap[edge.to];
            matrix[i][j] = edge.weight;
            if (!this.directed) {
                matrix[j][i] = edge.weight;
            }
        });

        return {
            matrix: matrix,
            nodes: this.nodes.map(n => n.id),
            directed: this.directed
        };
    }

    /**
     * Chuyển sang danh sách kề
     */
    toAdjacencyList() {
        const adjList = {};

        this.nodes.forEach(node => {
            adjList[node.id] = [];
        });

        this.edges.forEach(edge => {
            adjList[edge.from].push({
                to: edge.to,
                weight: edge.weight
            });
            if (!this.directed) {
                adjList[edge.to].push({
                    to: edge.from,
                    weight: edge.weight
                });
            }
        });

        return {
            adjacency_list: adjList,
            directed: this.directed
        };
    }

    /**
     * Lấy định dạng danh sách cạnh
     */
    toEdgeList() {
        return {
            nodes: this.nodes,
            edges: this.edges,
            directed: this.directed
        };
    }

    /**
     * Phát sự kiện cập nhật đồ thị
     */
    emitGraphUpdate() {
        if (typeof window !== 'undefined') {
            window.dispatchEvent(new Event('graphUpdated'));
        }
    }
}
