const STORAGE_KEY = "ecommerce_admin_products";

const initialProducts = [
  {
    id: crypto.randomUUID(),
    name: "iPhone 16 Pro",
    price: 8999,
    stock: 120,
    category: "手机",
    status: "on",
    createdAt: "2025-11-15T08:00:00.000Z",
    updatedAt: "2025-11-15T08:00:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    name: "MacBook Air M4",
    price: 9499,
    stock: 85,
    category: "电脑",
    status: "on",
    createdAt: "2025-12-01T10:30:00.000Z",
    updatedAt: "2025-12-01T10:30:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    name: "iPad Air",
    price: 4799,
    stock: 200,
    category: "平板",
    status: "on",
    createdAt: "2026-01-20T14:00:00.000Z",
    updatedAt: "2026-01-20T14:00:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    name: "AirPods Pro 3",
    price: 1899,
    stock: 350,
    category: "耳机",
    status: "off",
    createdAt: "2026-03-10T09:15:00.000Z",
    updatedAt: "2026-04-15T11:00:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    name: "小米手环 9",
    price: 249,
    stock: 500,
    category: "智能设备",
    status: "on",
    createdAt: "2026-04-05T16:45:00.000Z",
    updatedAt: "2026-04-05T16:45:00.000Z",
  },
];

const state = {
  products: loadProducts(),
  searchKeyword: "",
  categoryFilter: "all",
  statusFilter: "all",
};

const elements = {
  summaryCards: document.querySelector("#summaryCards"),
  tableBody: document.querySelector("#productTableBody"),
  searchInput: document.querySelector("#searchInput"),
  categoryFilter: document.querySelector("#categoryFilter"),
  statusFilter: document.querySelector("#statusFilter"),
  resetFilters: document.querySelector("#resetFilters"),
  createProductButton: document.querySelector("#createProductButton"),
  productDialog: document.querySelector("#productDialog"),
  dialogTitle: document.querySelector("#dialogTitle"),
  productForm: document.querySelector("#productForm"),
  editingProductId: document.querySelector("#editingProductId"),
  nameInput: document.querySelector("#nameInput"),
  priceInput: document.querySelector("#priceInput"),
  stockInput: document.querySelector("#stockInput"),
  categoryInput: document.querySelector("#categoryInput"),
  statusInput: document.querySelector("#statusInput"),
  cancelDialogButton: document.querySelector("#cancelDialogButton"),
};

function loadProducts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(initialProducts));
      return initialProducts;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : initialProducts;
  } catch (error) {
    console.error("读取商品数据失败：", error);
    return initialProducts;
  }
}

function persistProducts() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.products));
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function formatTime(value) {
  return new Date(value).toLocaleString("zh-CN", { hour12: false });
}

function formatPrice(value) {
  return "¥" + Number(value).toLocaleString("zh-CN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function getFilteredProducts() {
  const keyword = state.searchKeyword.trim().toLowerCase();
  return state.products.filter((product) => {
    const matchesKeyword = !keyword || product.name.toLowerCase().includes(keyword);
    const matchesCategory = state.categoryFilter === "all" || product.category === state.categoryFilter;
    const matchesStatus = state.statusFilter === "all" || product.status === state.statusFilter;
    return matchesKeyword && matchesCategory && matchesStatus;
  });
}

function renderSummary() {
  const total = state.products.length;
  const onShelf = state.products.filter((p) => p.status === "on").length;
  const offShelf = total - onShelf;
  const lowStock = state.products.filter((p) => p.stock < 10).length;
  const items = [
    { label: "商品总数", value: total },
    { label: "上架商品", value: onShelf },
    { label: "下架商品", value: offShelf },
    { label: "库存不足", value: lowStock },
  ];
  elements.summaryCards.innerHTML = items
    .map((item) => `<article class="summary-item"><span>${item.label}</span><strong>${item.value}</strong></article>`)
    .join("");
}

function renderTable() {
  const products = getFilteredProducts();
  if (!products.length) {
    elements.tableBody.innerHTML = `
      <tr>
        <td colspan="8">暂无匹配商品</td>
      </tr>
    `;
    return;
  }

  elements.tableBody.innerHTML = products
    .map(
      (product) => `
      <tr>
        <td>${escapeHtml(product.name)}</td>
        <td>${formatPrice(product.price)}</td>
        <td${product.stock < 10 ? ' class="low-stock"' : ''}>${product.stock}</td>
        <td>${escapeHtml(product.category)}</td>
        <td><span class="status ${product.status === "on" ? "on" : "off"}">${product.status === "on" ? "上架" : "下架"}</span></td>
        <td>${formatTime(product.createdAt)}</td>
        <td>${formatTime(product.updatedAt)}</td>
        <td>
          <div class="actions">
            <button data-action="edit" data-id="${product.id}">编辑</button>
            <button data-action="toggle" data-id="${product.id}">
              ${product.status === "on" ? "下架" : "上架"}
            </button>
            <button data-action="delete" data-id="${product.id}">删除</button>
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
  elements.editingProductId.value = "";
  elements.productForm.reset();
  elements.statusInput.value = "on";
  elements.categoryInput.value = "手机";
}

function openCreateDialog() {
  elements.dialogTitle.textContent = "新建商品";
  resetForm();
  elements.productDialog.showModal();
}

function openEditDialog(productId) {
  const product = state.products.find((item) => item.id === productId);
  if (!product) return;
  elements.dialogTitle.textContent = "编辑商品";
  elements.editingProductId.value = product.id;
  elements.nameInput.value = product.name;
  elements.priceInput.value = product.price;
  elements.stockInput.value = product.stock;
  elements.categoryInput.value = product.category;
  elements.statusInput.value = product.status;
  elements.productDialog.showModal();
}

function upsertProduct(formData) {
  const editingId = elements.editingProductId.value;
  const duplicated = state.products.find(
    (product) => product.id !== editingId && product.name === formData.name,
  );
  if (duplicated) {
    alert("商品名称已存在");
    return;
  }

  if (editingId) {
    state.products = state.products.map((product) =>
      product.id === editingId
        ? {
            ...product,
            ...formData,
            updatedAt: new Date().toISOString(),
          }
        : product,
    );
  } else {
    state.products.unshift({
      id: crypto.randomUUID(),
      ...formData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  }
  persistProducts();
  render();
  elements.productDialog.close();
}

function deleteProduct(productId) {
  const product = state.products.find((item) => item.id === productId);
  if (!product) return;
  if (!confirm(`确认删除商品 ${product.name} 吗？`)) return;
  state.products = state.products.filter((item) => item.id !== productId);
  persistProducts();
  render();
}

function toggleProductStatus(productId) {
  state.products = state.products.map((product) =>
    product.id === productId
      ? {
          ...product,
          status: product.status === "on" ? "off" : "on",
          updatedAt: new Date().toISOString(),
        }
      : product,
  );
  persistProducts();
  render();
}

function bindEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    state.searchKeyword = event.target.value;
    renderTable();
  });

  elements.categoryFilter.addEventListener("change", (event) => {
    state.categoryFilter = event.target.value;
    renderTable();
  });

  elements.statusFilter.addEventListener("change", (event) => {
    state.statusFilter = event.target.value;
    renderTable();
  });

  elements.resetFilters.addEventListener("click", () => {
    state.searchKeyword = "";
    state.categoryFilter = "all";
    state.statusFilter = "all";
    elements.searchInput.value = "";
    elements.categoryFilter.value = "all";
    elements.statusFilter.value = "all";
    renderTable();
  });

  elements.createProductButton.addEventListener("click", openCreateDialog);
  elements.cancelDialogButton.addEventListener("click", () => elements.productDialog.close());

  elements.productForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = {
      name: elements.nameInput.value.trim(),
      price: Number(elements.priceInput.value),
      stock: Number(elements.stockInput.value),
      category: elements.categoryInput.value,
      status: elements.statusInput.value,
    };
    upsertProduct(formData);
  });

  elements.tableBody.addEventListener("click", (event) => {
    const target = event.target.closest("button");
    if (!target) return;
    const { action, id } = target.dataset;
    if (action === "edit") openEditDialog(id);
    if (action === "toggle") toggleProductStatus(id);
    if (action === "delete") deleteProduct(id);
  });
}

bindEvents();
render();
