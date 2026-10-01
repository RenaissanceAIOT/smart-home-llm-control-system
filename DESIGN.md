---
name: HomeSignal
description: 以铁路信号台语言呈现可审计、安全优先的智能家居控制链路。
colors:
  paper: "#f4f0e7"
  paper-deep: "#e9e2d3"
  ink: "#18201f"
  muted: "#56605d"
  rail: "#263230"
  line: "#b9b2a5"
  signal-green: "#117a65"
  signal-amber: "#bd6b18"
  signal-red: "#a43b32"
  signal-green-bright: "#45d6a9"
  signal-amber-bright: "#f2a83b"
  on-dark: "#ffffff"
typography:
  display:
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"
    fontSize: "clamp(2.4rem, 5vw, 4.8rem)"
    lineHeight: 0.98
    letterSpacing: "-0.025em"
  body:
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"
  label:
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    letterSpacing: "0.06em"
rounded:
  route: "14px"
  control: "9px"
  tab: "8px 8px 0 0"
  pill: "999px"
  lamp: "50%"
components:
  signal-route:
    backgroundColor: "{colors.rail}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.route}"
  control-button:
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
  text-field:
    textColor: "{colors.ink}"
  system-badge:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "0.55rem 0.8rem"
  status-executed:
    backgroundColor: "{colors.signal-green}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.pill}"
    padding: "0.42rem 0.68rem"
  status-confirmation-required:
    backgroundColor: "{colors.signal-amber}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.pill}"
    padding: "0.42rem 0.68rem"
  status-rejected:
    backgroundColor: "{colors.signal-red}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.pill}"
    padding: "0.42rem 0.68rem"
  navigation-tab:
    rounded: "{rounded.tab}"
  decision-trace-row:
    textColor: "{colors.ink}"
    padding: "0.72rem 0"
---

# Design System: HomeSignal

## Overview

**Creative North Star: "安全信号台 / Railway Signal Desk"**

HomeSignal 把自然语言控制理解为一段必须逐站通过联锁的信号，而不是一次不可见的聊天式推断。暖色仪表纸承载内容，石墨色轨道组织关键流程，绿、琥珀与红色信号只在状态需要被判断时出现；整个界面应像一张可信、可查、可操作的控制桌。

这是一套紧凑但不拥挤的 Operate 界面。视觉表达来自清晰的线路、编号式操作标签、状态灯与审计轨迹，而不是装饰性科技效果。桌面与移动端共享同一条五阶段路线；移动端改变折线路径，不改变流程顺序或语义。

**Key Characteristics:**

- 暖仪表纸底色与高对比石墨轨道。
- 一条连续的五阶段控制路线，而非分散的进度卡片。
- 信号绿、琥珀、红与文字状态共同表达安全结果。
- 中文系统无衬线字体，优先保障可读性、加载可靠性与许可清晰度。
- 扁平、可审计的信息层级，只在路线与交互反馈上使用有限抬升。

## Colors

色彩像铁路信号系统一样克制：中性色构成绝大部分界面，信号色只负责传达控制链路与风险状态。规范值以 frontmatter 为准。

### Primary

- **联锁绿（signal-green）：** 用于已执行状态胶囊，表达确定完成。
- **通行灯绿（signal-green-bright）：** 用于路线上的已通过、当前节点与灯光辉光；不作为大面积背景。

### Secondary

- **待确认琥珀（signal-amber）：** 用于计划中或等待确认的状态胶囊。
- **警示灯琥珀（signal-amber-bright）：** 用于被联锁暂停的线路、键盘焦点与明确的操作警示。

### Tertiary

- **拒绝红（signal-red）：** 仅用于拒绝与无匹配等终止状态。

### Neutral

- **仪表纸（paper）：** 应用主背景与默认阅读表面。
- **深纸（paper-deep）：** 用于滚动槽等低层次区域。
- **墨色（ink）：** 主标题、关键值与正文中的高强调信息。
- **注释灰（muted）：** 说明文字与次级信息。
- **石墨轨道（rail）：** 侧栏、路线主体、强分隔和控件轮廓。
- **铅线（line）：** 表格化轨迹、指标与标签页的细分隔线。
- **轨道反白（on-dark）：** 石墨表面上的高优先级文字。

### Named Rules

**The Signal-Is-State Rule.** 信号色必须对应可解释的执行状态，并始终与文字标签共同出现；颜色不能单独承担含义。

**The Paper-Before-Chrome Rule.** 让纸张与石墨中性色占据画面，明亮信号色保持稀少，才能让一次状态变化真正可见。

## Typography

**Display Font:** 中文系统无衬线字体栈。
**Body Font:** 同一中文系统无衬线字体栈。
**Label Font:** 同一字体栈，通过较高字重、紧凑字号与字距形成操作标签语气。

**Character:** 字体选择服务于中文清晰度、跨平台可用性与许可确定性。系统不依赖外部 Web Font；“控制台”气质来自字重、大小写、字距与数字等宽特性，而不是仿机械字体。

### Hierarchy

- **Display：** 首页命题使用响应式大标题，紧行高与轻微负字距形成连续、坚实的标题块；移动端收束为较小的固定字号。
- **Headline / Title：** 分区标题沿用墨色、粗字重和紧字距，优先标识任务，不制造额外装饰层。
- **Body：** 说明文字使用注释灰，行长受控；头部说明不超过约 58 个字符宽。
- **Label：** 系统徽标使用高字重、较宽字距和大写英文；路线状态与审计字段使用更小的操作标签尺度。

### Named Rules

**The Local-Legibility Rule.** 中文界面使用系统无衬线字体，不为氛围引入下载字体或窄体替代品；操作感由排版关系而非字体噱头完成。

## Layout

内容容器在桌面端限制为 1320px，并保留宽松的上下呼吸空间。首屏由标题与系统边界徽标、横向五阶段信号路线、标签导航以及控制/决策双栏依次构成；双栏比例略向决策轨迹倾斜，使输入与解释在一个视口内并列完成。

在 760px 及以下，页头改为垂直排列，控制区回到单列。信号路线改为两列蛇形：输入与识别占第一行，联锁与规划反向排列在第二行，执行独占第三行；线路仍连续，阶段顺序仍为输入、识别、规划、联锁、执行。移动端隐藏阶段副标题，但保留节点名和状态，避免在窄屏损失判断依据。

**The One-Route Rule.** 响应式重排只能折叠同一条路线，不能把五个阶段拆成互不相关的卡片或改写其语义顺序。

## Elevation & Depth

系统以平面和线性分隔为默认。路线面板使用一层宽而柔和的投影，使关键流程像安装在纸面上的仪表；按钮只在悬停时轻微上移并出现小范围阴影。信号灯的内嵌环与状态辉光表达“灯亮”，而不是装饰性霓虹。

### Shadow Vocabulary

- **路线抬升：** 仅用于完整信号路线，使其成为首要操作结构。
- **按钮悬停：** 与 1px 上移配合，作为可点击反馈。
- **信号辉光：** 仅附着于已通过、当前或被阻断的灯点；待机灯保持内嵌暗环。

### Named Rules

**The Flat-by-Default Rule.** 普通表单、轨迹行、指标和标签页依靠细线与留白分层；常驻阴影只属于信号路线。

## Shapes

形状语言是“工程面板上的有限圆角”：路线外壳使用最宽圆角，常规按钮使用中等圆角，标签页只圆上角，状态使用完整胶囊，信号灯始终为圆形。表单容器与轨迹区保持直角和明确的顶部轨道线，避免全界面卡片化。

**The Engineered-Corner Rule.** 圆角根据部件功能分级，不给所有容器套用同一个柔软卡片轮廓。

## Components

### Signal Route

- **Character:** 全局标志性组件，是一条可观察的联锁线路，而不是普通步骤器。
- **Structure:** 桌面五等分，移动端在既定断点折成蛇形路线；相邻节点由 2px 轨道连接。
- **State:** 待机为灰灯与“等待”；通过/当前为明绿线路和灯；阻断为琥珀灯与部分着色线路；每个颜色状态都有文字标签。
- **Motion:** 当前或阻断灯使用一次 620ms 的缩放与去模糊解析动效；减少动态偏好下近似禁用。

### Buttons

- **Shape:** 有限圆角与石墨 1px 描边。
- **Default:** 高字重，示例按钮保持安静，让输入与决策轨迹优先。
- **Hover / Focus:** 悬停上移 1px 并增加小范围阴影；键盘焦点使用清晰的琥珀色 3px 外轮廓。
- **Disabled:** 降低不透明度并使用不可用光标。

### Status Pills

- **Style:** 高字重白字、紧凑内边距和完整胶囊轮廓。
- **State:** 执行为绿，计划/待确认为琥珀，拒绝/无匹配为红；状态词始终保留。

### Inputs / Fields

- **Style:** 沿用 Streamlit 字段结构，输入光标使用琥珀色，placeholder 使用可读的深灰。
- **Focus:** 继承全局 3px 琥珀焦点轮廓与 2px 外偏移。
- **Error / Disabled:** 错误信息使用框架原生语义反馈；禁用操作降低不透明度，不仅改变颜色。

### Navigation

- **Style:** 标签页以细底线构成单一导航带；标签仅在上方使用圆角，活动态由框架指示线与文本共同表达。
- **Mobile:** 清除标签间额外间距并缩小水平内边距，四个入口保持同一行可扫读。

### System Boundary Badge

细石墨描边、紧凑内边距和大写操作标签明确声明 “Simulation / No live devices”。桌面靠右对齐，移动端位于说明文字下方；它是运行边界，不是营销徽章。

### Decision Trace

每行使用固定标签列与弹性值列，底部分隔线建立审计节奏；移动端折成上下两行。标签为小型操作文字，结果值使用更高字重。

## Do's and Don'ts

### Do:

- **Do** 让暖纸背景、石墨路线与一条连续的五阶段流程构成每个主操作面的视觉骨架。
- **Do** 让绿、琥珀、红状态同时带有明确文字，并保持焦点轮廓清晰可见。
- **Do** 在移动端保留完整阶段顺序和路线连续性，即使需要折成蛇形。
- **Do** 使用中文系统无衬线字体与本地回退，优先保证阅读、加载和许可可靠性。
- **Do** 把模拟执行、无真实设备等边界放在首屏可见位置。

### Don't:

- **Don't** 把界面改造成聊天气泡、消息流或黑箱式 AI 助手仪表盘。
- **Don't** 用大面积信号色、渐变科技光或泛滥阴影稀释状态信号。
- **Don't** 把每个区块包进相同的圆角卡片；表单和审计轨迹应依靠轨道线与留白组织。
- **Don't** 仅靠颜色表达通过、待确认、拒绝或焦点状态。
- **Don't** 使用下载型展示字体替换中文系统字体，或暗示界面已连接真实家居硬件。
