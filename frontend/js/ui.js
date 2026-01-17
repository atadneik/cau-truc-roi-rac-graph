/**
 * UI.js - Xử lý các sự kiện UI
 */

// Các đối tượng toàn cục
let graph = new Graph();
let canvas = null;
let api = new API();

// Trạng thái UI
let currentMode = 'default';  // default, addNode, addEdge, delete, selectStartNode, selectEndNode
let selectedNode = null;
let tempEdgeStart = null;
let algorithmToRun = null;
let algorithmStartNode = null;

// Khởi tạo khi DOM đã tải xong
document.addEventListener('DOMContentLoaded', function () {
    // Làm cho graph có thể truy cập toàn cục
    window.graph = graph;
    window.api = api;

    initializeCanvas();
    initializeToolbar();
    initializeDropdowns();
    // Khởi tạo Modal
    initializeModal();

    // Khởi tạo sidebar
    if (typeof updateGraphDataSidebar === 'function') {
        updateGraphDataSidebar();
    }
});

/**
 * Khởi tạo các sự kiện Modal
 */
function initializeModal() {
    const modal = document.getElementById('addEdgeModal');
    const closeBtn = document.querySelector('.close');
    const slider = document.getElementById('edgeWeightSlider');
    const input = document.getElementById('edgeWeightInput');
    const presets = document.querySelectorAll('.btn-preset');
    const directedBtn = document.getElementById('addDirectedEdgeBtn');
    const undirectedBtn = document.getElementById('addUndirectedEdgeBtn');

    // Đóng modal
    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => {
        if (event.target == modal) modal.style.display = 'none';
    };

    // Đồng bộ slider và input
    slider.oninput = function () {
        input.value = this.value;
    };
    input.oninput = function () {
        slider.value = this.value;
    };

    // Các nút preset
    presets.forEach(btn => {
        btn.onclick = function () {
            input.value = this.getAttribute('data-value');
            if (input.value !== 'has no weight') {
                slider.value = input.value;
            }
        };
    });

    // Các hành động thêm cạnh
    directedBtn.onclick = () => addEdgeFromModal(true);
    undirectedBtn.onclick = () => addEdgeFromModal(false);
}

let pendingEdgeStart = null;
let pendingEdgeEnd = null;

function showAddEdgeModal(startNode, endNode) {
    pendingEdgeStart = startNode;
    pendingEdgeEnd = endNode;

    const modal = document.getElementById('addEdgeModal');
    const input = document.getElementById('edgeWeightInput');
    const slider = document.getElementById('edgeWeightSlider');

    // Reset giá trị
    input.value = 'has no weight';
    slider.value = 0;

    modal.style.display = 'block';
}

function addEdgeFromModal(isDirected) {
    console.log("addEdgeFromModal được gọi với isDirected:", isDirected);
    try {
        const modal = document.getElementById('addEdgeModal');
        const input = document.getElementById('edgeWeightInput');

        let weight = 1;
        if (input.value !== 'has no weight') {
            weight = parseFloat(input.value) || 1;
        }

        if (!pendingEdgeStart || !pendingEdgeEnd) {
            console.error("Thiếu đỉnh bắt đầu hoặc kết thúc cho cạnh.");
            modal.style.display = 'none';
            return;
        }

        // Cập nhật hướng đồ thị nếu khác với lựa chọn của người dùng
        // if (isDirected !== graph.directed) {
        //    graph.setDirected(isDirected);
        // }

        // Truyền isDirected vào addEdge
        const edge = graph.addEdge(pendingEdgeStart.id, pendingEdgeEnd.id, weight, isDirected);

        if (!edge) {
            // Cạnh có thể đã tồn tại
            console.log("Cạnh đã tồn tại hoặc không thể thêm.");
        }

        canvas.clearHighlights();
        canvas.redraw();
        if (typeof updateGraphDataSidebar === 'function') updateGraphDataSidebar();

        modal.style.display = 'none';
        pendingEdgeStart = null;
        pendingEdgeEnd = null;
        tempEdgeStart = null;

    } catch (error) {
        console.error("Lỗi khi thêm cạnh:", error);
        alert("Có lỗi xảy ra khi thêm cạnh: " + error.message);
    }
}

/**
 * Khởi tạo canvas và các sự kiện chuột
 */
function initializeCanvas() {
    canvas = new GraphCanvas('graphCanvas', graph);
    const canvasElement = document.getElementById('graphCanvas');

    canvasElement.addEventListener('click', handleCanvasClick);
    canvasElement.addEventListener('contextmenu', handleCanvasRightClick);
    canvasElement.addEventListener('mousemove', handleCanvasMouseMove);

    // Thay đổi kích thước canvas để vừa với container
    window.addEventListener('resize', () => {
        canvas.resize();
    });

    // Buộc resize ban đầu
    setTimeout(() => canvas.resize(), 100);
}

/**
 * Xử lý click trên canvas
 */
function handleCanvasClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    console.log(`Click tại ${x}, ${y}, Chế độ: ${currentMode}`);

    const clickedNode = graph.findNodeAt(x, y);

    switch (currentMode) {
        case 'addNode':
            if (!clickedNode) {
                graph.addNode(x, y);
                canvas.redraw();
                if (typeof updateGraphDataSidebar === 'function') updateGraphDataSidebar();
            }
            break;

        case 'addEdge':
            if (clickedNode) {
                if (!tempEdgeStart) {
                    // Chọn đỉnh bắt đầu
                    tempEdgeStart = clickedNode;
                    canvas.highlightNodes([clickedNode.id]);
                } else if (tempEdgeStart.id !== clickedNode.id) {
                    // Chọn đỉnh kết thúc và hiển thị modal
                    showAddEdgeModal(tempEdgeStart, clickedNode);

                    // Lưu ý: Chúng ta chưa xóa highlight hay vẽ lại ở đây,
                    // chờ hành động từ modal.
                } else {
                    // Hủy nếu click vào cùng một đỉnh
                    tempEdgeStart = null;
                    canvas.clearHighlights();
                }
            }
            break;

        case 'delete':
            if (clickedNode) {
                if (confirm(`Xóa đỉnh ${clickedNode.label}?`)) {
                    graph.removeNode(clickedNode.id);
                    canvas.redraw();
                    if (typeof updateGraphDataSidebar === 'function') updateGraphDataSidebar();
                }
            }
            break;

        case 'selectStartNode':
            if (clickedNode) {
                algorithmStartNode = clickedNode.id;
                canvas.highlightNodes([clickedNode.id]);

                // Nếu thuật toán cần đỉnh kết thúc, chuyển chế độ
                if (['dijkstra', 'bellman-ford', 'ford-fulkerson'].includes(algorithmToRun)) {
                    updateInfoBar(`Đã chọn đỉnh bắt đầu: ${clickedNode.label}. Vui lòng chọn đỉnh kết thúc.`);
                    currentMode = 'selectEndNode';
                } else {
                    // Chạy ngay lập tức
                    runAlgorithmStep2(algorithmToRun, algorithmStartNode, null);
                    currentMode = 'default';
                }
            }
            break;

        case 'selectEndNode':
            if (clickedNode) {
                canvas.highlightNodes([algorithmStartNode, clickedNode.id]); // Highlight cả hai
                runAlgorithmStep2(algorithmToRun, algorithmStartNode, clickedNode.id);
                currentMode = 'default';
            }
            break;

        case 'default':
        default:
            if (clickedNode) {
                // Logic chọn đỉnh nếu cần
                selectedNode = clickedNode;
                canvas.highlightNodes([clickedNode.id]);
            } else {
                selectedNode = null;
                canvas.clearHighlights();
            }
            break;
    }
}

/**
 * Xử lý di chuyển chuột trên canvas (Hiệu ứng Hover)
 */
function handleCanvasMouseMove(event) {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const hoveredNode = graph.findNodeAt(x, y);

    if (hoveredNode) {
        canvas.setHoveredNode(hoveredNode.id);
        canvas.canvas.style.cursor = 'pointer';
    } else {
        canvas.setHoveredNode(null);
        canvas.canvas.style.cursor = 'default';
    }
}

/**
 * Xử lý click chuột phải
 */
function handleCanvasRightClick(event) {
    event.preventDefault();
    // Logic menu ngữ cảnh có thể đặt ở đây
}

/**
 * Khởi tạo các nút trên thanh công cụ
 */
function initializeToolbar() {
    // Các nút chế độ
    document.getElementById('defaultModeBtn').addEventListener('click', () => setMode('default'));
    document.getElementById('addVertexBtn').addEventListener('click', () => setMode('addNode'));
    document.getElementById('connectVerticesBtn').addEventListener('click', () => setMode('addEdge'));
    document.getElementById('removeObjectBtn').addEventListener('click', () => setMode('delete'));

    // Menu Đồ thị
    document.getElementById('newGraphBtn').addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Tạo đồ thị mới? Các thay đổi chưa lưu sẽ bị mất.')) {
            graph.clear();
            canvas.redraw();
            if (typeof updateGraphDataSidebar === 'function') updateGraphDataSidebar();
        }
    });

    document.getElementById('saveGraphBtn').addEventListener('click', (e) => {
        e.preventDefault();
        saveGraph();
    });

    document.getElementById('loadGraphBtn').addEventListener('click', (e) => {
        e.preventDefault();
        loadGraph();
    });






}

/**
 * Khởi tạo dropdowns (Thuật toán)
 */
function initializeDropdowns() {
    const algoLinks = document.querySelectorAll('#algorithmsDropdown a');
    algoLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const algo = e.target.getAttribute('data-algo');
            runAlgorithm(algo);
        });
    });
}

/**
 * Thiết lập chế độ tương tác
 */
function setMode(mode) {
    console.log('Đặt chế độ:', mode);
    currentMode = mode;
    tempEdgeStart = null;
    canvas.clearHighlights();

    // Cập nhật kiểu nút
    const btnMap = {
        'default': 'defaultModeBtn',
        'addNode': 'addVertexBtn',
        'addEdge': 'connectVerticesBtn',
        'delete': 'removeObjectBtn'
    };

    document.querySelectorAll('.btn-tool').forEach(btn => {
        btn.classList.remove('active');
    });

    if (btnMap[mode]) {
        document.getElementById(btnMap[mode]).classList.add('active');
    }
}

/**
 * Ghi kết quả vào thanh thông tin
 */
function logResult(title, content) {
    const infoText = document.getElementById('infoText');
    // Định dạng: "<strong>Title:</strong> Content"
    infoText.innerHTML = `<strong>${title}:</strong> ${content}`;
}


/**
 * Chạy thuật toán
 */
async function runAlgorithm(algorithm) {
    if (graph.nodes.length === 0) {
        alert('Vui lòng vẽ đồ thị trước!');
        return;
    }

    let startNode = null;
    let endNode = null;

    // Hỏi đỉnh bắt đầu/kết thúc nếu cần
    if (['bfs', 'dfs', 'dijkstra', 'bellman-ford', 'ford-fulkerson'].includes(algorithm)) {
        algorithmToRun = algorithm;
        currentMode = 'selectStartNode';
        updateInfoBar('Vui lòng CLICK chọn đỉnh bắt đầu trên đồ thị.');
        return;
    }

    // Chạy các thuật toán không cần input ngay lập tức
    runAlgorithmStep2(algorithm, null, null);
}

async function runAlgorithmStep2(algorithm, startNode, endNode) {

    canvas.clearHighlights();
    updateInfoBar('Đang chạy ' + algorithm + '...');

    try {
        const graphData = graph.toJSON();
        let result;

        switch (algorithm) {
            case 'bfs':
                result = await api.bfs(graphData, startNode);
                if (result.steps) await canvas.animateSteps(result.steps, 500);
                logResult('Thứ tự duyệt BFS', result.order.join(' '));
                break;

            case 'dfs':
                result = await api.dfs(graphData, startNode);
                if (result.steps) await canvas.animateSteps(result.steps, 500);
                logResult('Thứ tự duyệt DFS', result.order.join(' '));
                break;

            case 'dijkstra':
            case 'bellman-ford':
                result = await api.shortestPath(graphData, startNode, endNode, algorithm);
                if (result.found) {
                    canvas.setPath(result.path);
                    logResult('Đường đi ngắn nhất', `${result.path.join(' ')} (Độ dài: ${result.distance})`);
                } else {
                    logResult('Kết quả', 'Không tìm thấy đường đi!');
                }
                break;

            case 'bipartite':
                result = await api.checkBipartite(graphData);
                if (result.is_bipartite) {
                    canvas.setNodeColors(result.coloring);
                    logResult('Kiểm tra đồ thị 2 phía', 'Đồ thị là đồ thị 2 phía! (Có thể chia các đỉnh thành 2 tập màu khác nhau)');
                } else {
                    logResult('Kiểm tra đồ thị 2 phía', 'Đồ thị KHÔNG phải là đồ thị 2 phía! (Không thể tô bằng 2 màu, có chứa chu trình lẻ)');
                }
                break;

            case 'prim':
                result = await api.prim(graphData);
                if (result.steps) await canvas.animateSteps(result.steps, 500);
                logResult('MST (Prim)', `Tổng trọng số: ${result.total_weight}`);
                break;

            case 'kruskal':
                result = await api.kruskal(graphData);
                if (result.steps) await canvas.animateSteps(result.steps, 500);
                logResult('MST (Kruskal)', `Tổng trọng số: ${result.total_weight}`);
                break;

            case 'ford-fulkerson':
                result = await api.fordFulkerson(graphData, startNode, endNode);
                if (result.steps) await canvas.animateSteps(result.steps, 1000);
                logResult('Luồng cực đại', `Giá trị: ${result.max_flow}`);
                break;

            case 'fleury':
                result = await api.fleury(graphData, startNode);
                if (result.exists) {
                    canvas.setPath(result.path);
                    logResult('Đường đi Euler', result.path.join(' -> '));
                } else {
                    logResult('Kết quả', 'Không tìm thấy đường đi Euler.');
                }
                break;

            case 'hierholzer':
                result = await api.hierholzer(graphData);
                if (result.exists) {
                    canvas.setPath(result.path);
                    logResult('Chu trình Euler', result.path.join(' -> '));
                } else {
                    logResult('Kết quả', 'Không tìm thấy chu trình Euler.');
                }
                break;
        }
        // updateInfoBar('Hoàn tất.'); // Đã xóa để tránh ghi đè kết quả
    } catch (error) {
        console.error(error);
        alert('Lỗi: ' + error.message);
        updateInfoBar('Đã xảy ra lỗi.');
    }
}

function updateInfoBar(text) {
    const infoText = document.getElementById('infoText');
    if (infoText) infoText.textContent = text;
}

/**
 * Lưu đồ thị
 */
function saveGraph() {
    const data = JSON.stringify(graph.toJSON(), null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'graph.json';
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Tải đồ thị
 */
function loadGraph() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                graph.fromJSON(data);
                canvas.redraw();
                if (typeof updateGraphDataSidebar === 'function') updateGraphDataSidebar();
            } catch (err) {
                alert('File không hợp lệ');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

