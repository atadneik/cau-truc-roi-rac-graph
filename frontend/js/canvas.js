/**
 * Class GraphCanvas - Vẽ đồ thị lên canvas
 * Xử lý trực quan hóa và hoạt hình (animation)
 */
class GraphCanvas {
    constructor(canvasId, graph) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.graph = graph;

        // Trạng thái trực quan hóa
        this.highlightedNodes = new Set();
        this.highlightedEdges = new Set();
        this.nodeColors = {};  // Cho tô màu đồ thị 2 phía (bipartite)
        this.pathEdges = [];   // Cho đường đi ngắn nhất
        this.hoveredNode = null; // Node đang được hover

        // Hằng số
        this.NODE_RADIUS = 25;
        this.ARROW_SIZE = 10;

        this.resize();
        this.redraw();
    }

    /**
     * Thay đổi kích thước canvas để vừa với container
     */
    resize() {
        const parent = this.canvas.parentElement;
        this.canvas.width = parent.clientWidth;
        this.canvas.height = parent.clientHeight;
        this.redraw();
    }

    /**
     * Vẽ lại toàn bộ canvas
     */
    redraw() {
        // Xóa canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Vẽ cạnh trước
        this.graph.edges.forEach(edge => {
            this.drawEdge(edge);
        });

        // Vẽ đỉnh sau (để đỉnh nằm trên cạnh)
        this.graph.nodes.forEach(node => {
            this.drawNode(node);
        });
    }

    /**
     * Vẽ một đỉnh
     */
    drawNode(node) {
        const x = node.x;
        const y = node.y;

        // Xác định màu
        let fillColor = '#fff'; // Nền trắng
        let strokeColor = '#2196F3'; // Viền xanh
        let textColor = '#2196F3'; // Chữ xanh

        if (this.nodeColors[node.id] !== undefined) {
            // Tô màu Bipartite
            fillColor = this.nodeColors[node.id] === 0 ? '#4CAF50' : '#FF5722';
            strokeColor = fillColor;
            textColor = '#fff';
        } else if (this.highlightedNodes.has(node.id)) {
            // Node được highlight (trong quá trình thuật toán hoặc kết quả)
            fillColor = '#FF8F00'; // Cam đậm
            strokeColor = '#FF8F00';
            textColor = '#fff';
        } else if (this.hoveredNode === node.id) {
            // Node đang được hover
            fillColor = '#E1F5FE'; // Xanh nhạt
            strokeColor = '#2196F3';
            textColor = '#2196F3';
        }

        // Vẽ vòng tròn
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.NODE_RADIUS, 0, 2 * Math.PI);
        this.ctx.fillStyle = fillColor;
        this.ctx.fill();
        this.ctx.strokeStyle = strokeColor;
        this.ctx.lineWidth = 2;
        this.ctx.stroke();

        // Vẽ nhãn (label)
        this.ctx.fillStyle = textColor;
        this.ctx.font = 'bold 14px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(node.label, x, y);
    }

    /**
     * Vẽ một cạnh
     */
    drawEdge(edge) {
        const fromNode = this.graph.getNode(edge.from);
        const toNode = this.graph.getNode(edge.to);

        if (!fromNode || !toNode) return;

        // Xác định màu
        const edgeKey = `${edge.from}-${edge.to}`;
        const reverseEdgeKey = `${edge.to}-${edge.from}`;

        let strokeColor = '#2196F3'; // Xanh mặc định
        let lineWidth = 2;

        if (this.pathEdges.includes(edgeKey) || this.pathEdges.includes(reverseEdgeKey)) {
            strokeColor = '#FF8F00'; // Cam đậm/Vàng cho đường đi kết quả
            lineWidth = 4;
        } else if (this.highlightedEdges.has(edgeKey) || this.highlightedEdges.has(reverseEdgeKey)) {
            strokeColor = '#FFB300'; // Vàng đậm/Hổ phách cho Animation
            lineWidth = 3;
        }

        // Tính toán điểm bắt đầu và kết thúc (trên viền đỉnh)
        const angle = Math.atan2(toNode.y - fromNode.y, toNode.x - fromNode.x);
        const startX = fromNode.x + this.NODE_RADIUS * Math.cos(angle);
        const startY = fromNode.y + this.NODE_RADIUS * Math.sin(angle);
        const endX = toNode.x - this.NODE_RADIUS * Math.cos(angle);
        const endY = toNode.y - this.NODE_RADIUS * Math.sin(angle);

        // Vẽ đường thẳng
        this.ctx.beginPath();
        this.ctx.moveTo(startX, startY);
        this.ctx.lineTo(endX, endY);
        this.ctx.strokeStyle = strokeColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.stroke();

        // Vẽ mũi tên nếu cạnh có hướng hoặc đồ thị có hướng
        console.log(`Vẽ cạnh ${edge.from}-${edge.to}: isDirected=${edge.isDirected}, graph.directed=${this.graph.directed}`);
        if (edge.isDirected || this.graph.directed) {
            this.drawArrow(endX, endY, angle);
        }

        // Vẽ trọng số (nếu không phải 1)
        if (edge.weight !== 1) {
            const midX = (startX + endX) / 2;
            const midY = (startY + endY) / 2;

            // Nền cho text
            this.ctx.fillStyle = '#FFF';
            this.ctx.fillRect(midX - 10, midY - 10, 20, 20);

            // Viền cho hộp trọng số
            this.ctx.strokeStyle = strokeColor;
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(midX - 10, midY - 10, 20, 20);

            // Text
            this.ctx.fillStyle = strokeColor;
            this.ctx.font = 'bold 12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(edge.weight.toString(), midX, midY);
        }
    }

    /**
     * Vẽ mũi tên
     */
    drawArrow(x, y, angle) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(angle);

        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-this.ARROW_SIZE, -this.ARROW_SIZE / 2);
        this.ctx.lineTo(-this.ARROW_SIZE, this.ARROW_SIZE / 2);
        this.ctx.closePath();
        this.ctx.fillStyle = this.ctx.strokeStyle;
        this.ctx.fill();

        this.ctx.restore();
    }

    /**
     * Highlight các đỉnh
     */
    highlightNodes(nodeIds) {
        this.highlightedNodes = new Set(nodeIds);
        this.redraw();
    }

    /**
     * Highlight các cạnh
     */
    highlightEdges(edgeKeys) {
        this.highlightedEdges = new Set(edgeKeys);
        this.redraw();
    }

    /**
     * Set màu cho các node (bipartite)
     */
    setNodeColors(colors) {
        this.nodeColors = colors;
        this.redraw();
    }

    /**
     * Highlight đường đi (shortest path, euler path, etc.)
     */
    setPath(path) {
        this.pathEdges = [];
        // Highlight các cạnh
        for (let i = 0; i < path.length - 1; i++) {
            this.pathEdges.push(`${path[i]}-${path[i + 1]}`);
        }

        // Highlight các đỉnh
        path.forEach(nodeId => {
            this.highlightedNodes.add(nodeId);
        });

        this.redraw();
    }

    /**
     * Xóa tất cả highlight
     */
    clearHighlights() {
        this.highlightedNodes.clear();
        this.highlightedEdges.clear();
        this.nodeColors = {};
        this.pathEdges = [];
        this.redraw();
    }

    /**
     * Set node đang được hover
     */
    setHoveredNode(nodeId) {
        if (this.hoveredNode !== nodeId) {
            this.hoveredNode = nodeId;
            this.redraw();
        }
    }

    /**
     * Animation - chạy từng bước
     */
    async animateSteps(steps, speed = 500) {
        for (const step of steps) {
            await this.processStep(step);
            await this.sleep(speed);
        }
    }

    /**
     * Xử lý một bước của animation
     */
    async processStep(step) {
        switch (step.type || step.action) { // Xử lý cả 'type' và 'action'
            case 'visit':
            case 'start': // Xử lý action 'start' từ Prim
                if (step.node) this.highlightedNodes.add(step.node);
                if (step.from && step.node) {
                    this.highlightedEdges.add(`${step.from}-${step.node}`);
                }
                break;
            case 'discover':
            case 'update':
                if (step.node) {
                    this.highlightedNodes.add(step.node);
                }
                if (step.from && step.node) {
                    this.highlightedEdges.add(`${step.from}-${step.node}`);
                }
                break;
            case 'color':
                this.nodeColors[step.node] = step.color;
                break;
            case 'add_edge':
                let u, v;
                if (Array.isArray(step.edge)) {
                    [u, v] = step.edge;
                } else {
                    u = step.edge.from;
                    v = step.edge.to;
                }
                const edgeKey = `${u}-${v}`;
                this.highlightedEdges.add(edgeKey);
                // Highlight cả các đỉnh
                this.highlightedNodes.add(u);
                this.highlightedNodes.add(v);
                break;
            case 'highlight_path':
                // Highlight các cạnh
                if (step.path) {
                    step.path.forEach(edge => {
                        let u, v;
                        if (Array.isArray(edge)) {
                            [u, v] = edge;
                        } else {
                            u = edge.from;
                            v = edge.to;
                        }
                        this.highlightedEdges.add(`${u}-${v}`);
                    });
                }
                // Highlight các đỉnh
                if (step.nodes) {
                    step.nodes.forEach(nodeId => {
                        this.highlightedNodes.add(nodeId);
                    });
                }
                break;
        }
        this.redraw();
    }

    /**
     * Hàm sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Xuất canvas thành hình ảnh
     */
    exportAsImage() {
        return this.canvas.toDataURL('image/png');
    }
}
