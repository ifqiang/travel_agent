# AI 旅行助手 - 历史对话面板

**目标：** 在现有单页里追加右侧历史会话侧边栏，支持查看/切换/删除/清空  
**技术栈：** 单文件 HTML + TailwindCSS（CDN）+ 原生 JS，localStorage 持久化

---

## Task 1: 导航栏新增「历史对话」按钮

> 在顶部导航栏「快速推荐」旁插入按钮，并预留移动端汉堡菜单位置

**文件：** `index.html`

- [x] 在 `#nav-right` 区域插入「历史对话」按钮（图标+文字）
- [x] 添加 `data-panel-toggle` 属性用于 JS 绑定
- [x] 保持粉紫渐变 hover 效果与圆角样式

---

## Task 2: 右侧历史对话侧边面板结构

> 固定定位右侧滑出面板，包含标题、会话列表、底部清空按钮

**文件：** `index.html`

- [x] 添加 `<aside id="historyPanel">` 容器，默认 `translate-x-full`
- [x] 内部结构：面板标题 + 关闭按钮 + 会话列表区 + 底部「清空全部」
- [x] 列表项模板：标题、时间、删除图标，绑定 `data-session-id`

---

## Task 3: 历史会话本地存储与读取逻辑

> 封装 localStorage 存取、生成会话标题、时间戳工具函数

**文件：** `index.html`（`<script>` 内新增模块）

- [x] `saveConversation(sessionId, messages)` 序列化存储
- [x] `loadConversation(sessionId)` 反序列化并填充左侧对话区
- [x] `getAllSessions()` 返回数组供列表渲染
- [x] `deleteSession(sessionId)` / `clearAllSessions()` 删除接口

---

## Task 4: 面板交互与状态同步

> 按钮点击滑出/收回、列表点击切换会话、删除与清空实时刷新

**文件：** `index.html`

- [x] 绑定「历史对话」按钮 → 切换 `translate-x-0 / full`
- [x] 列表项点击 → 调用 `loadConversation` 并关闭面板
- [x] 删除图标点击 → 阻止冒泡，删除后重新渲染列表
- [x] 清空按钮 → 二次确认后清空并刷新列表
- [x] 当前活跃会话高亮样式同步

---

## Task 5: 响应式与视觉一致性微调

> 确保面板在移动端全宽、按钮不换行、滚动条美化

**文件：** `index.html`

- [x] 移动端 `w-full sm:max-w-sm` 限制宽度
- [x] 列表区 `overflow-y-auto` 最大高度计算
- [x] 滚动条颜色与粉紫主题统一
- [x] 关闭按钮添加过渡动画