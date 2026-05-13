const STORAGE_KEY = "ecommerce_admin_users";

const initialUsers = [
  {
    id: crypto.randomUUID(),
    username: "alice01",
    email: "alice@example.com",
    phone: "13800138000",
    role: "会员",
    status: "active",
    locked: true,
    createdAt: "2025-11-12T08:20:00.000Z",
    lastLoginAt: "2026-05-08T16:05:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    username: "zhangsan",
    email: "zhangsan@example.com",
    phone: "13900139000",
    role: "普通用户",
    status: "disabled",
    locked: false,
    createdAt: "2025-09-03T06:30:00.000Z",
    lastLoginAt: "2026-04-29T11:18:00.000Z",
  },
  {
    id: crypto.randomUUID(),
    username: "vipbuyer",
    email: "vipbuyer@example.com",
    phone: "13700137000",
    role: "VIP",
    status: "active",
    locked: false,
    createdAt: "2025-10-24T03:43:00.000Z",
    lastLoginAt: "2026-05-09T03:09:00.000Z",
  },
];

const state = {
  users: loadUsers(),
  searchKeyword: "",
  statusFilter: "all",
  roleFilter: "all",
  lockFilter: "all",
};

const elements = {
  summaryCards: document.querySelector("#summaryCards"),
  tableBody: document.querySelector("#userTableBody"),
  searchInput: document.querySelector("#searchInput"),
  statusFilter: document.querySelector("#statusFilter"),
  roleFilter: document.querySelector("#roleFilter"),
  resetFilters: document.querySelector("#resetFilters"),
  createUserButton: document.querySelector("#createUserButton"),
  userDialog: document.querySelector("#userDialog"),
  dialogTitle: document.querySelector("#dialogTitle"),
  userForm: document.querySelector("#userForm"),
  editingUserId: document.querySelector("#editingUserId"),
  usernameInput: document.querySelector("#usernameInput"),
  emailInput: document.querySelector("#emailInput"),
  phoneInput: document.querySelector("#phoneInput"),
  roleInput: document.querySelector("#roleInput"),
  statusInput: document.querySelector("#statusInput"),
  lockedInput: document.querySelector("#lockedInput"),
  cancelDialogButton: document.querySelector("#cancelDialogButton"),
  lockFilter: document.querySelector("#lockFilter"),
};

function normalizeUser(user) {
  if (!user || typeof user !== "object") return null;
  return {
    ...user,
    locked: Boolean(user.locked),
  };
}

function loadUsers() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(initialUsers));
      return initialUsers.map((u) => normalizeUser(u));
    }
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return initialUsers.map((u) => normalizeUser(u));
    const normalized = parsed.map((u) => normalizeUser(u)).filter(Boolean);
    const needsPersist = parsed.some((u) => u && typeof u.locked !== "boolean");
    if (needsPersist) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(normalized));
    }
    return normalized;
  } catch (error) {
    console.error("读取用户数据失败：", error);
    return initialUsers.map((u) => normalizeUser(u));
  }
}

function persistUsers() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.users));
}

function formatTime(value) {
  return new Date(value).toLocaleString("zh-CN", { hour12: false });
}

function getFilteredUsers() {
  const keyword = state.searchKeyword.trim().toLowerCase();
  return state.users.filter((user) => {
    const matchesKeyword =
      !keyword ||
      user.username.toLowerCase().includes(keyword) ||
      user.email.toLowerCase().includes(keyword) ||
      user.phone.includes(keyword);
    const matchesStatus = state.statusFilter === "all" || user.status === state.statusFilter;
    const matchesRole = state.roleFilter === "all" || user.role === state.roleFilter;
    const matchesLock =
      state.lockFilter === "all" ||
      (state.lockFilter === "locked" && user.locked) ||
      (state.lockFilter === "unlocked" && !user.locked);
    return matchesKeyword && matchesStatus && matchesRole && matchesLock;
  });
}

function renderSummary() {
  const total = state.users.length;
  const active = state.users.filter((user) => user.status === "active").length;
  const disabled = total - active;
  const locked = state.users.filter((user) => user.locked).length;
  const vip = state.users.filter((user) => user.role === "VIP").length;
  const items = [
    { label: "用户总数", value: total },
    { label: "正常用户", value: active },
    { label: "禁用用户", value: disabled },
    { label: "已锁定", value: locked },
    { label: "VIP 用户", value: vip },
  ];
  elements.summaryCards.innerHTML = items
    .map((item) => `<article class="summary-item"><span>${item.label}</span><strong>${item.value}</strong></article>`)
    .join("");
}

function renderTable() {
  const users = getFilteredUsers();
  if (!users.length) {
    elements.tableBody.innerHTML = `
      <tr>
        <td colspan="8">暂无匹配用户</td>
      </tr>
    `;
    return;
  }

  elements.tableBody.innerHTML = users
    .map(
      (user) => `
      <tr>
        <td>${user.username}</td>
        <td>${user.email}</td>
        <td>${user.phone}</td>
        <td>${user.role}</td>
        <td>
          <span class="status-badges">
            <span class="status ${user.status}">${user.status === "active" ? "正常" : "禁用"}</span>
            ${user.locked ? '<span class="status locked">已锁定</span>' : ""}
          </span>
        </td>
        <td>${formatTime(user.createdAt)}</td>
        <td>${formatTime(user.lastLoginAt)}</td>
        <td>
          <div class="actions">
            <button data-action="edit" data-id="${user.id}">编辑</button>
            <button data-action="toggle" data-id="${user.id}">
              ${user.status === "active" ? "禁用" : "启用"}
            </button>
            <button type="button" class="warn" data-action="lock-toggle" data-id="${user.id}">
              ${user.locked ? "解锁" : "锁定"}
            </button>
            <button data-action="delete" data-id="${user.id}">删除</button>
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
  elements.editingUserId.value = "";
  elements.userForm.reset();
  elements.statusInput.value = "active";
  elements.roleInput.value = "普通用户";
  elements.lockedInput.checked = false;
}

function openCreateDialog() {
  elements.dialogTitle.textContent = "新建用户";
  resetForm();
  elements.userDialog.showModal();
}

function openEditDialog(userId) {
  const user = state.users.find((item) => item.id === userId);
  if (!user) return;
  elements.dialogTitle.textContent = "编辑用户";
  elements.editingUserId.value = user.id;
  elements.usernameInput.value = user.username;
  elements.emailInput.value = user.email;
  elements.phoneInput.value = user.phone;
  elements.roleInput.value = user.role;
  elements.statusInput.value = user.status;
  elements.lockedInput.checked = Boolean(user.locked);
  elements.userDialog.showModal();
}

function upsertUser(formData) {
  const editingId = elements.editingUserId.value;
  const duplicated = state.users.find(
    (user) =>
      user.id !== editingId &&
      (user.email === formData.email || user.phone === formData.phone || user.username === formData.username),
  );
  if (duplicated) {
    alert("用户名、邮箱或手机号已存在");
    return;
  }

  if (editingId) {
    state.users = state.users.map((user) =>
      user.id === editingId
        ? {
            ...user,
            ...formData,
          }
        : user,
    );
  } else {
    state.users.unshift({
      id: crypto.randomUUID(),
      ...formData,
      locked: Boolean(formData.locked),
      createdAt: new Date().toISOString(),
      lastLoginAt: new Date().toISOString(),
    });
  }
  persistUsers();
  render();
  elements.userDialog.close();
}

function deleteUser(userId) {
  const user = state.users.find((item) => item.id === userId);
  if (!user) return;
  if (!confirm(`确认删除用户 ${user.username} 吗？`)) return;
  state.users = state.users.filter((item) => item.id !== userId);
  persistUsers();
  render();
}

function toggleUserStatus(userId) {
  state.users = state.users.map((user) =>
    user.id === userId
      ? {
          ...user,
          status: user.status === "active" ? "disabled" : "active",
        }
      : user,
  );
  persistUsers();
  render();
}

function toggleUserLock(userId) {
  const user = state.users.find((item) => item.id === userId);
  if (!user) return;
  const nextLocked = !user.locked;
  const verb = nextLocked ? "锁定" : "解锁";
  if (!confirm(`确认${verb}用户 ${user.username} 吗？`)) return;
  state.users = state.users.map((item) =>
    item.id === userId ? { ...item, locked: nextLocked } : item,
  );
  persistUsers();
  render();
}

function bindEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    state.searchKeyword = event.target.value;
    renderTable();
  });

  elements.statusFilter.addEventListener("change", (event) => {
    state.statusFilter = event.target.value;
    renderTable();
  });

  elements.roleFilter.addEventListener("change", (event) => {
    state.roleFilter = event.target.value;
    renderTable();
  });

  elements.lockFilter.addEventListener("change", (event) => {
    state.lockFilter = event.target.value;
    renderTable();
  });

  elements.resetFilters.addEventListener("click", () => {
    state.searchKeyword = "";
    state.statusFilter = "all";
    state.roleFilter = "all";
    state.lockFilter = "all";
    elements.searchInput.value = "";
    elements.statusFilter.value = "all";
    elements.roleFilter.value = "all";
    elements.lockFilter.value = "all";
    renderTable();
  });

  elements.createUserButton.addEventListener("click", openCreateDialog);
  elements.cancelDialogButton.addEventListener("click", () => elements.userDialog.close());

  elements.userForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = {
      username: elements.usernameInput.value.trim(),
      email: elements.emailInput.value.trim(),
      phone: elements.phoneInput.value.trim(),
      role: elements.roleInput.value,
      status: elements.statusInput.value,
      locked: elements.lockedInput.checked,
    };
    upsertUser(formData);
  });

  elements.tableBody.addEventListener("click", (event) => {
    const target = event.target.closest("button");
    if (!target) return;
    const { action, id } = target.dataset;
    if (action === "edit") openEditDialog(id);
    if (action === "toggle") toggleUserStatus(id);
    if (action === "lock-toggle") toggleUserLock(id);
    if (action === "delete") deleteUser(id);
  });
}

bindEvents();
render();
