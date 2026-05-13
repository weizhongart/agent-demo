const STORAGE_KEY = "ecommerce_admin_inventory";

const initialRecords = [
  {
    id: crypto.randomUUID(),
    productName: "iPhone 16 Pro",
    type: "in",
    quantity: 200,
    operator: "张三",
    remark: "首批到货",
    createdAt: "2025-11-15T08:00:00.000Z",
    updatedAt: "2025-11-15T08:00:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    productName: "iPhone 16 Pro",
    type: "out",
    quantity: 80,
    operator: "李四",
    remark: "线上订单发货",
    createdAt: "2025-12-20T10:30:00.000Z",
    updatedAt: "2025-12-20T10:30:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    productName: "MacBook Air M4",
    type: "in",
    quantity: 100,
    operator: "张三",
    remark: "供应商补货",
    createdAt: "2025-12-01T10:30:00.000Z",
    updatedAt: "2025-12-01T10:30:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    productName: "AirPods Pro 3",
    type: "in",
    quantity: 500,
    operator: "王五",
    remark: "新品入库",
    createdAt: "2026-03-10T09:15:00.000Z",
    updatedAt: "2026-03-10T09:15:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    productName: "小米手环 9",
    type: "out",
    quantity: 150,
    operator: "李四",
    remark: "促销活动出库",
    createdAt: "2026-04-20T14:00:00.000Z",
    updatedAt: "2026-04-20T14:00:00.000Z",
  },
];

const state = {
  records: loadRecords(),
  searchKeyword: "",
  typeFilter: "all",
};

const elements = {
  summaryCards: document.querySelector("#summaryCards"),
  tableBody: document.querySelector("#inventoryTableBody"),
  searchInput: document.querySelector("#searchInput"),
  typeFilter: document.querySelector("#typeFilter"),
  resetFilters: document.querySelector("#resetFilters"),
  createRecordButton: document.querySelector("#createRecordButton"),
  recordDialog: document.querySelector("#recordDialog"),
  dialogTitle: document.querySelector("#dialogTitle"),
  recordForm: document.querySelector("#recordForm"),
  editingRecordId: document.querySelector("#editingRecordId"),
  productNameInput: document.querySelector("#productNameInput"),
  typeInput: document.querySelector("#typeInput"),
  quantityInput: document.querySelector("#quantityInput"),
  operatorInput: document.querySelector("#operatorInput"),
  remarkInput: document.querySelector("#remarkInput"),
  cancelDialogButton: document.querySelector("#cancelDialogButton"),
};

function loadRecords() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(initialRecords));
      return initialRecords;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : initialRecords;
  } catch (error) {
    console.error("读取库存数据失败：", error);
    return initialRecords;
  }
}

function persistRecords() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.records));
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function formatTime(value) {
  return new Date(value).toLocaleString("zh-CN", { hour12: false });
}

function getFilteredRecords() {
  const keyword = state.searchKeyword.trim().toLowerCase();
  return state.records.filter((record) => {
    const matchesKeyword = !keyword || record.productName.toLowerCase().includes(keyword);
    const matchesType = state.typeFilter === "all" || record.type === state.typeFilter;
    return matchesKeyword && matchesType;
  });
}

function renderSummary() {
  const total = state.records.length;
  const inCount = state.records.filter((r) => r.type === "in").length;
  const outCount = state.records.filter((r) => r.type === "out").length;
  const totalInQty = state.records
    .filter((r) => r.type === "in")
    .reduce((sum, r) => sum + r.quantity, 0);
  const totalOutQty = state.records
    .filter((r) => r.type === "out")
    .reduce((sum, r) => sum + r.quantity, 0);
  const items = [
    { label: "记录总数", value: total },
    { label: "入库记录", value: inCount },
    { label: "出库记录", value: outCount },
    { label: "净入库量", value: totalInQty - totalOutQty },
  ];
  elements.summaryCards.innerHTML = items
    .map((item) => `<article class="summary-item"><span>${item.label}</span><strong>${item.value}</strong></article>`)
    .join("");
}

function renderTable() {
  const records = getFilteredRecords();
  if (!records.length) {
    elements.tableBody.innerHTML = `
      <tr>
        <td colspan="8">暂无匹配记录</td>
      </tr>
    `;
    return;
  }

  elements.tableBody.innerHTML = records
    .map(
      (record) => `
      <tr>
        <td>${escapeHtml(record.productName)}</td>
        <td><span class="status ${record.type === "in" ? "in" : "out"}">${record.type === "in" ? "入库" : "出库"}</span></td>
        <td>${record.quantity}</td>
        <td>${escapeHtml(record.operator)}</td>
        <td>${escapeHtml(record.remark || "")}</td>
        <td>${formatTime(record.createdAt)}</td>
        <td>${formatTime(record.updatedAt)}</td>
        <td>
          <div class="actions">
            <button data-action="edit" data-id="${record.id}">编辑</button>
            <button data-action="delete" data-id="${record.id}">删除</button>
          </div>
        </td>
      </tr>
    `,
    )
    .join("");
}

function render() {
  renderSummary();
  renderTable();
}

function resetForm() {
  elements.editingRecordId.value = "";
  elements.recordForm.reset();
  elements.typeInput.value = "in";
}

function openCreateDialog() {
  elements.dialogTitle.textContent = "新建记录";
  resetForm();
  elements.recordDialog.showModal();
}

function openEditDialog(recordId) {
  const record = state.records.find((item) => item.id === recordId);
  if (!record) return;
  elements.dialogTitle.textContent = "编辑记录";
  elements.editingRecordId.value = record.id;
  elements.productNameInput.value = record.productName;
  elements.typeInput.value = record.type;
  elements.quantityInput.value = record.quantity;
  elements.operatorInput.value = record.operator;
  elements.remarkInput.value = record.remark || "";
  elements.recordDialog.showModal();
}

function upsertRecord(formData) {
  const editingId = elements.editingRecordId.value;

  if (editingId) {
    state.records = state.records.map((record) =>
      record.id === editingId
        ? {
            ...record,
            ...formData,
            updatedAt: new Date().toISOString(),
          }
        : record,
    );
  } else {
    state.records.unshift({
      id: crypto.randomUUID(),
      ...formData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  }
  persistRecords();
  render();
  elements.recordDialog.close();
}

function deleteRecord(recordId) {
  const record = state.records.find((item) => item.id === recordId);
  if (!record) return;
  if (!confirm(`确认删除该库存记录吗？（${record.productName} ${record.type === "in" ? "入库" : "出库"} ${record.quantity}）`)) return;
  state.records = state.records.filter((item) => item.id !== recordId);
  persistRecords();
  render();
}

function bindEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    state.searchKeyword = event.target.value;
    renderTable();
  });

  elements.typeFilter.addEventListener("change", (event) => {
    state.typeFilter = event.target.value;
    renderTable();
  });

  elements.resetFilters.addEventListener("click", () => {
    state.searchKeyword = "";
    state.typeFilter = "all";
    elements.searchInput.value = "";
    elements.typeFilter.value = "all";
    renderTable();
  });

  elements.createRecordButton.addEventListener("click", openCreateDialog);
  elements.cancelDialogButton.addEventListener("click", () => elements.recordDialog.close());

  elements.recordForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = {
      productName: elements.productNameInput.value.trim(),
      type: elements.typeInput.value,
      quantity: Number(elements.quantityInput.value),
      operator: elements.operatorInput.value.trim(),
      remark: elements.remarkInput.value.trim(),
    };
    upsertRecord(formData);
  });

  elements.tableBody.addEventListener("click", (event) => {
    const target = event.target.closest("button");
    if (!target) return;
    const { action, id } = target.dataset;
    if (action === "edit") openEditDialog(id);
    if (action === "delete") deleteRecord(id);
  });
}

bindEvents();
render();
