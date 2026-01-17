/**
 * Cập nhật sidebar với thông tin đồ thị
 */
function updateGraphDataSidebar() {
    // Cập nhật số lượng đỉnh
    const nodeCountEl = document.getElementById('nodeCount');
    if (nodeCountEl && window.graph) {
        nodeCountEl.textContent = window.graph.nodes.length;
    }

    // Cập nhật danh sách dữ liệu đồ thị (dạng kề)
    const graphDataListEl = document.getElementById('graphDataList');
    if (graphDataListEl && window.graph) {
        graphDataListEl.innerHTML = '';

        // Xây dựng danh sách kề
        const adjList = {};
        window.graph.nodes.forEach(node => {
            adjList[node.id] = [];
        });

        window.graph.edges.forEach(edge => {
            if (!adjList[edge.from]) adjList[edge.from] = [];
            adjList[edge.from].push(edge.to);

            // Với đồ thị vô hướng, thêm cạnh ngược lại
            if (!window.graph.directed && !edge.isDirected) {
                if (!adjList[edge.to]) adjList[edge.to] = [];
                adjList[edge.to].push(edge.from);
            }
        });

        // Hiển thị
        Object.keys(adjList).sort((a, b) => parseInt(a) - parseInt(b)).forEach(nodeId => {
            const connections = adjList[nodeId].sort((a, b) => parseInt(a) - parseInt(b));
            const dataRow = document.createElement('div');
            dataRow.className = 'data-row';
            dataRow.innerHTML = `
                <span class="data-index">${nodeId}</span>
                <span class="data-value">${connections.join(' ')}</span>
            `;
            graphDataListEl.appendChild(dataRow);
        });
    }

    // Tự động cập nhật chuyển đổi khi đồ thị thay đổi
    updateConversion();
}

/**
 * Chuyển đổi đồ thị sang định dạng chỉ định và hiển thị
 */
async function updateConversion() {
    const activeTab = document.querySelector('.conversion-tab.active');
    const outputEl = document.getElementById('conversionText');

    if (!activeTab || !outputEl || !window.graph || !window.api) {
        return;
    }

    const toType = activeTab.dataset.type;

    // Nếu đồ thị trống, hiển thị thông báo
    if (window.graph.nodes.length === 0) {
        outputEl.textContent = 'Đồ thị trống';
        return;
    }

    try {
        // Xây dựng dữ liệu đồ thị cho API
        const graphData = buildGraphDataForAPI();

        // Gọi API để chuyển đổi (giả sử định dạng hiện tại là 'list')
        const response = await window.api.convert(graphData, 'list', toType);

        if (response && response.result) {
            // Định dạng và hiển thị kết quả
            const formattedOutput = formatConversionOutput(response.result, toType);
            outputEl.textContent = formattedOutput;
        }
    } catch (error) {
        console.error('Lỗi chuyển đổi:', error);
        outputEl.textContent = 'Lỗi chuyển đổi';
    }
}

/**
 * Xây dựng đối tượng dữ liệu đồ thị cho cuộc gọi API
 */
function buildGraphDataForAPI() {
    const adjList = {};

    // Khởi tạo tất cả các đỉnh
    window.graph.nodes.forEach(node => {
        adjList[node.id] = [];
    });

    // Thêm cạnh với trọng số
    window.graph.edges.forEach(edge => {
        const weight = edge.weight === 'has no weight' ? 1 : parseFloat(edge.weight);

        if (!adjList[edge.from]) adjList[edge.from] = [];
        adjList[edge.from].push({
            to: edge.to,
            weight: weight
        });

        // Với vô hướng, thêm ngược lại
        if (!window.graph.directed && !edge.isDirected) {
            if (!adjList[edge.to]) adjList[edge.to] = [];
            adjList[edge.to].push({
                to: edge.from,
                weight: weight
            });
        }
    });

    return {
        adjacency_list: adjList,
        directed: window.graph.directed || false
    };
}

/**
 * Định dạng kết quả chuyển đổi để hiển thị
 */
function formatConversionOutput(result, toType) {
    if (toType === 'matrix') {
        // Định dạng ma trận kề
        const matrix = result.matrix;
        const nodes = result.nodes;

        // Tìm độ dài lớn nhất để padding
        let maxLen = 1;
        matrix.forEach(row => {
            row.forEach(val => {
                maxLen = Math.max(maxLen, String(val).length);
            });
        });
        nodes.forEach(node => {
            maxLen = Math.max(maxLen, String(node).length);
        });

        const pad = (s, n) => String(s).padStart(n, ' ');

        let output = ' '.repeat(maxLen + 1) + nodes.map(n => pad(n, maxLen)).join(' ') + '\n';
        matrix.forEach((row, i) => {
            output += pad(nodes[i], maxLen) + ' ' + row.map(v => pad(v, maxLen)).join(' ') + '\n';
        });
        return output;

    } else if (toType === 'list') {
        // Định dạng danh sách kề
        const adjList = result.adjacency_list;
        let output = '';

        Object.keys(adjList).sort((a, b) => parseInt(a) - parseInt(b)).forEach(node => {
            const neighbors = adjList[node];
            if (neighbors.length > 0) {
                const neighborStr = neighbors.map(n => `${n.to}(${n.weight})`).join(', ');
                output += `${node}: ${neighborStr}\n`;
            } else {
                output += `${node}: -\n`;
            }
        });
        return output;

    } else if (toType === 'edges') {
        // Định dạng danh sách cạnh
        const edges = result.edges;
        let output = '';

        edges.forEach(edge => {
            output += `${edge.from} → ${edge.to} (${edge.weight})\n`;
        });
        return output || 'Không có cạnh';
    }

    return 'Định dạng không hợp lệ';
}

// Gắn vào sự kiện đồ thị
if (typeof GraphEventEmitter !== 'undefined') {
    const eventEmitter = new GraphEventEmitter();
    eventEmitter.on('graphChanged', updateGraphDataSidebar);
}

// Khởi tạo listener cho các tab chuyển đổi
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.conversion-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            updateConversion();
        });
    });
});

// Xuất để sử dụng trong các module khác
if (typeof window !== 'undefined') {
    window.updateGraphDataSidebar = updateGraphDataSidebar;
    window.updateConversion = updateConversion;
}
