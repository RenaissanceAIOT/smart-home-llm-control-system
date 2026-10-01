"""Streamlit control-room demo for the hybrid smart-home pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from smart_home_control.audit import AuditLogger
from smart_home_control.automation import AutomationStore, parse_automation
from smart_home_control.catalog import DEVICE_CATALOG, DEVICES_BY_ID
from smart_home_control.controller import SmartHomeController

ROOT = Path(__file__).parent
RUNTIME = ROOT / "runtime"

st.set_page_config(
    page_title="HomeSignal · 智能家居安全控制台",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<!--
THESIS: Natural-language control is a routed signal that must clear every interlock; this refuses the generic chatbot dashboard.
OWN-WORLD: Warm instrument-paper ground, graphite rails, signal green/amber/red, condensed operational labels, and one continuous route diagram.
STORY: The operator speaks naturally, sees the route resolve, understands every safety decision, and executes only a validated plan.
FIRST VIEWPORT: A wide route strip owns the top, followed by one command bench with examples at left and the live decision trace at right.
FORM: Railway signal desk, grounded direction 5, seed 039f2a10.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md
-->
<style>
:root {
  --paper: #f4f0e7;
  --paper-deep: #e9e2d3;
  --ink: #18201f;
  --muted: #56605d;
  --rail: #263230;
  --green: #117a65;
  --amber: #bd6b18;
  --red: #a43b32;
  --line: #b9b2a5;
}
.stApp { background: var(--paper); color: var(--ink); }
[data-testid="stHeader"] { background: rgba(244, 240, 231, .92); }
[data-testid="stSidebar"] { background: var(--rail); }
[data-testid="stSidebar"] * { color: #f7f3ea; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: var(--ink); }
.block-container { max-width: 1320px; padding-top: 2rem; padding-bottom: 4rem; }
h1, h2, h3 { color: var(--ink); letter-spacing: -.025em; }
h1 { font-size: clamp(2.4rem, 5vw, 4.8rem) !important; line-height: .98 !important; max-width: 860px; }
p, li { color: var(--muted); }
a { text-underline-offset: 3px; }
textarea, input { caret-color: var(--amber) !important; }
textarea::placeholder, input::placeholder { color: #66706d !important; opacity: 1; }
* { scrollbar-color: var(--muted) var(--paper-deep); scrollbar-width: thin; }
button:disabled { opacity: .55 !important; cursor: not-allowed !important; }
button, [data-baseweb="tab"], [data-testid="stMetricValue"] { font-variant-numeric: tabular-nums; }
::selection { background: #f2c66d; color: var(--ink); }
*:focus-visible { outline: 3px solid #f2a83b !important; outline-offset: 2px; }
.signal-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 2rem; margin: .5rem 0 1.4rem; }
.signal-head p { max-width: 58ch; margin: 0 0 .35rem; font-size: 1.02rem; }
.system-badge { flex: 0 0 auto; border: 1px solid var(--rail); padding: .55rem .8rem; font-weight: 700; font-size: .78rem; letter-spacing: .06em; text-transform: uppercase; }
.route { display: grid; grid-template-columns: repeat(5, 1fr); background: var(--rail); color: white; margin: 1rem 0 2.2rem; overflow: hidden; border-radius: 14px; box-shadow: 0 16px 34px rgba(38, 50, 48, .16); }
.route-step { position: relative; min-height: 118px; padding: 1.15rem 1.1rem 1rem; border-right: 1px solid rgba(255,255,255,.17); }
.route-step:last-child { border-right: 0; }
.route-step::after { content: ""; position: absolute; top: 1.5rem; left: 2.25rem; right: -.65rem; height: 2px; background: #5d6966; z-index: 0; }
.route-step:last-child::after { display: none; }
.route-step.complete::after, .route-step.current::after { background: #45d6a9; }
.route-step.blocked::after { background: linear-gradient(90deg, #f2a83b 0 44%, #5d6966 44% 100%); }
.route-step b { display: block; color: white; font-size: 1.05rem; margin-top: .58rem; }
.route-step span { color: #cdd6d3; font-size: .8rem; }
.lamp { position: relative; z-index: 1; width: 13px; height: 13px; border-radius: 50%; background: #76817e; box-shadow: inset 0 0 0 2px rgba(0,0,0,.25); }
.route-step.complete .lamp, .route-step.current .lamp { background: #45d6a9; box-shadow: 0 0 0 5px rgba(69,214,169,.15), 0 0 18px rgba(69,214,169,.55); }
.route-step.blocked .lamp { background: #f2a83b; box-shadow: 0 0 0 5px rgba(242,168,59,.14); }
.route-step.current .lamp, .route-step.blocked .lamp { animation: signal-resolve 620ms cubic-bezier(.16, 1, .3, 1) both; }
.state-label { display: block; margin-top: .35rem; color: #9faaa7 !important; font-size: .68rem !important; letter-spacing: .04em; text-transform: uppercase; }
.route-step.complete .state-label, .route-step.current .state-label { color: #74e4c2 !important; }
.route-step.blocked .state-label { color: #ffc363 !important; }
@keyframes signal-resolve { from { transform: scale(.72); filter: blur(2px); } to { transform: scale(1); filter: blur(0); } }
.trace { border-top: 2px solid var(--rail); padding-top: 1rem; margin-top: 1rem; }
.trace-row { display: grid; grid-template-columns: 140px 1fr; gap: 1.2rem; padding: .72rem 0; border-bottom: 1px solid var(--line); }
.trace-row dt { color: var(--muted); font-size: .8rem; letter-spacing: .04em; text-transform: uppercase; }
.trace-row dd { margin: 0; color: var(--ink); font-weight: 650; }
.status-executed, .status-confirmation_required, .status-rejected, .status-no_match, .status-planned { display:inline-block; padding:.42rem .68rem; color:white; font-weight:800; border-radius:999px; }
.status-executed { background: var(--green); }
.status-confirmation_required, .status-planned { background: var(--amber); }
.status-rejected, .status-no_match { background: var(--red); }
[data-testid="stMetric"] { background: transparent; border-top: 1px solid var(--line); padding-top: .8rem; }
[data-testid="stMetricValue"] { font-variant-numeric: tabular-nums; }
.stButton > button { border-radius: 9px; border: 1px solid var(--rail); font-weight: 700; transition: transform 160ms ease-out, box-shadow 160ms ease-out; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(38,50,48,.14); }
[data-testid="stForm"] { border: 0; border-top: 2px solid var(--rail); border-radius: 0; padding: 1.3rem 0 0; }
[data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
[data-baseweb="tab"] { border-radius: 8px 8px 0 0; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
@media (max-width: 760px) {
  .block-container { padding-top: 1rem; }
  .signal-head { display: block; }
  .signal-head h1 { margin: 0 0 .45rem; font-size: 2.15rem !important; line-height: 1.02 !important; }
  .signal-head p { margin: 0; font-size: .88rem; line-height: 1.45; }
  .system-badge { display: inline-block; margin-top: .55rem; padding: .32rem .48rem; font-size: .64rem; }
  .route { grid-template-columns: repeat(2, minmax(0, 1fr)); margin: .7rem 0 .8rem; }
  .route-step { min-height: 58px; padding: .55rem .55rem .42rem 2rem; border-right: 1px solid rgba(255,255,255,.17); border-bottom: 1px solid rgba(255,255,255,.17); }
  .route-step:nth-child(1) { grid-column: 1; grid-row: 1; }
  .route-step:nth-child(2) { grid-column: 2; grid-row: 1; border-right: 0; }
  .route-step:nth-child(3) { grid-column: 2; grid-row: 2; border-right: 0; }
  .route-step:nth-child(4) { grid-column: 1; grid-row: 2; }
  .route-step:nth-child(5) { grid-column: 1 / -1; grid-row: 3; border-bottom: 0; }
  .route-step .lamp { position: absolute; top: .72rem; left: .7rem; width: 11px; height: 11px; }
  .route-step::after { display: block; top: 1rem; left: 1.18rem; right: -.75rem; height: 2px; }
  .route-step:nth-child(2)::after, .route-step:nth-child(4)::after { top: 1.2rem; left: .98rem; right: auto; width: 2px; height: calc(100% - .1rem); }
  .route-step:nth-child(3)::after { top: 1rem; left: calc(-100% + .95rem); right: auto; width: 100%; height: 2px; }
  .route-step:nth-child(5)::after { display: none; }
  .route-step b { margin-top: 0; font-size: .9rem; line-height: 1.15; }
  .route-step > span:not(.state-label) { display: none; }
  .state-label { margin-top: .18rem; font-size: .62rem !important; }
  [data-baseweb="tab-list"] { gap: 0; }
  [data-baseweb="tab"] { padding-left: .55rem; padding-right: .55rem; }
  [data-testid="stHeadingWithActionElements"] h3 { margin-top: .35rem; }
  .trace-row { grid-template-columns: 1fr; gap: .2rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


def controller(enable_llm: bool) -> SmartHomeController:
    key = f"controller:{enable_llm}"
    if key not in st.session_state:
        st.session_state[key] = SmartHomeController(
            enable_llm_from_env=enable_llm,
            audit_logger=AuditLogger(RUNTIME / "audit.jsonl"),
        )
    return st.session_state[key]


def render_route(status: str | None) -> None:
    completed = {
        None: 0,
        "no_match": 1,
        "rejected": 3,
        "confirmation_required": 4,
        "planned": 2,
        "executed": 5,
    }[status]
    labels = (
        ("输入", "规范化自然语言"),
        ("识别", "规则优先 / LLM 受限"),
        ("规划", "固定意图映射"),
        ("联锁", "白名单与参数边界"),
        ("执行", "确认后模拟控制"),
    )
    cells = []
    for index, (title, subtitle) in enumerate(labels, start=1):
        state = "pending"
        state_text = "等待"
        if index < completed:
            state = "complete"
            state_text = "已通过"
        elif index == completed and completed > 0:
            state = "current"
            state_text = "当前"
        if status in {"rejected", "confirmation_required"} and index == completed:
            state = "blocked"
            state_text = "已拒绝" if status == "rejected" else "待确认"
        elif status == "executed" and index == completed:
            state_text = "已执行"
        cells.append(
            f'<div class="route-step {state}"><div class="lamp"></div><b>{title}</b>'
            f'<span>{subtitle}</span><small class="state-label">{state_text}</small></div>'
        )
    st.markdown('<div class="route">' + "".join(cells) + "</div>", unsafe_allow_html=True)


def render_decision(decision) -> None:
    st.markdown(
        f"""
<div class="trace">
  <span class="status-{decision.status}">{decision.status.replace("_", " ")}</span>
  <dl>
    <div class="trace-row"><dt>标准意图</dt><dd>{decision.intent}</dd></div>
    <div class="trace-row"><dt>识别来源</dt><dd>{decision.intent_source} · {decision.confidence:.0%}</dd></div>
    <div class="trace-row"><dt>风险等级</dt><dd>{decision.risk_level}</dd></div>
    <div class="trace-row"><dt>系统答复</dt><dd>{decision.message}</dd></div>
  </dl>
</div>
""",
        unsafe_allow_html=True,
    )
    if decision.commands:
        st.markdown("#### 候选动作")
        st.dataframe(
            [
                {
                    "设备": DEVICES_BY_ID[command.device_id].name,
                    "设备 ID": command.device_id,
                    "动作": command.action,
                    "参数": json.dumps(command.parameters, ensure_ascii=False) or "—",
                }
                for command in decision.commands
            ],
            width="stretch",
            hide_index=True,
        )
    if decision.findings:
        st.markdown("#### 安全联锁记录")
        for finding in decision.findings:
            if finding.severity == "error":
                st.error(f"{finding.code} · {finding.message}")
            elif finding.severity == "warning":
                st.warning(f"{finding.code} · {finding.message}")
            else:
                st.info(f"{finding.code} · {finding.message}")


with st.sidebar:
    st.markdown("## HomeSignal")
    st.caption("安全优先的自然语言控制原型")
    enable_llm = st.toggle(
        "启用 LLM 降级分类", value=False, help="仅在规则无法识别时调用；LLM 不生成设备命令。"
    )
    st.divider()
    st.markdown("**运行边界**")
    st.write("47 台白名单设备")
    st.write("模拟执行器")
    st.write("高风险必须确认")
    if enable_llm:
        st.info("需要 LLM_API_KEY 或 OPENAI_API_KEY。无密钥时自动保持本地保守模式。")
    st.caption("研究 Demo · 不连接真实硬件")

st.markdown(
    """
<div class="signal-head">
  <div>
    <h1>让每条自然语言指令<br>通过安全联锁</h1>
    <p>LLM 只理解意图。设备选择、动作生成、参数边界和高风险确认全部由确定性规则掌控。</p>
  </div>
  <div class="system-badge">Simulation / No live devices</div>
</div>
""",
    unsafe_allow_html=True,
)

current = st.session_state.get("last_decision")
render_route(current.status if current else None)

control_tab, devices_tab, automation_tab, research_tab = st.tabs(
    ["控制台", "设备状态", "自动化记忆", "实验与数据"]
)

with control_tab:
    left, right = st.columns([0.92, 1.08], gap="large")
    with left:
        st.markdown("### 下达指令")
        st.write("可以直接控制设备，也可以描述体感或生活场景。")
        examples = [
            "今天好热，我要去卧室休息一会",
            "我要洗澡了",
            "把客厅灯亮度调到50%",
            "打开门锁",
        ]
        cols = st.columns(2)
        for index, example in enumerate(examples):
            if cols[index % 2].button(example, width="stretch", key=f"example-{index}"):
                st.session_state["command_text"] = example
        with st.form("control-form"):
            text = st.text_area(
                "自然语言指令",
                value=st.session_state.get("command_text", ""),
                height=128,
                placeholder="例如：屋里太闷了，帮我通通风",
            )
            submitted = st.form_submit_button("发送到安全控制链路", width="stretch")
        if submitted:
            st.session_state["command_text"] = text
            with st.spinner("正在通过安全联锁…"):
                st.session_state["last_decision"] = controller(enable_llm).process(text)
            st.rerun()
    with right:
        st.markdown("### 决策轨迹")
        if current:
            render_decision(current)
            if current.needs_confirmation:
                if st.button("确认并执行高风险计划", type="primary", width="stretch"):
                    with st.spinner("正在执行已确认计划…"):
                        st.session_state["last_decision"] = controller(enable_llm).process(
                            current.text, confirmed=True
                        )
                    st.rerun()
        else:
            st.info("发送一条指令后，这里会显示意图、动作、风险和执行结果。")

with devices_tab:
    st.markdown("### 白名单设备与实时模拟状态")
    state = controller(enable_llm).executor.snapshot()
    category_filter = st.multiselect(
        "设备类别",
        sorted({device.category for device in DEVICE_CATALOG}),
        default=[],
        placeholder="全部类别",
    )
    rows = []
    for device in DEVICE_CATALOG:
        if category_filter and device.category not in category_filter:
            continue
        rows.append(
            {
                "房间": device.room,
                "设备": device.name,
                "类别": device.category,
                "能力": ", ".join(device.capabilities),
                "当前状态": json.dumps(state[device.device_id], ensure_ascii=False),
            }
        )
    st.dataframe(rows, width="stretch", hide_index=True, height=560)

with automation_tab:
    st.markdown("### 持久化习惯与定时计划")
    st.write("当前原型解析每日、工作日或周末的简单时间表达，并把固定命令写入本地 SQLite。")
    store = AutomationStore(RUNTIME / "automations.db")
    with st.form("automation-form"):
        automation_text = st.text_input(
            "自动化描述",
            placeholder="例如：每天早上6点起床，自动打开卧室窗帘",
        )
        save_automation = st.form_submit_button("解析并保存")
    if save_automation:
        parsed = parse_automation(automation_text)
        if parsed is None:
            st.error("没有解析出有效的时间与设备计划，请补充周期、时间和场景。")
        else:
            store.add(parsed)
            st.success(f"已保存：{parsed.title}")
    saved = store.list()
    if saved:
        st.dataframe(
            [
                {
                    "计划": item.title,
                    "周期": item.schedule,
                    "原始描述": item.source_text,
                    "动作数": len(item.commands),
                    "启用": item.enabled,
                }
                for item in saved
            ],
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("还没有保存自动化。所有计划只存储在本机 runtime/ 目录。")

with research_tab:
    st.markdown("### 数据与实验边界")
    summary_path = ROOT / "data" / "dataset_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    cols = st.columns(4)
    cols[0].metric("合成样本", summary.get("rows", "—"))
    cols[1].metric("显式指令", summary.get("instruction_type", {}).get("explicit", "—"))
    cols[2].metric("隐式指令", summary.get("instruction_type", {}).get("implicit", "—"))
    cols[3].metric("白名单设备", len(DEVICE_CATALOG))
    st.warning(
        "仓库内数据为模板生成的合成覆盖集，不是报告所述的原始用户记录。下表数值来自原报告，尚未由本仓库独立复现。"
    )
    st.dataframe(
        [
            {
                "系统": "纯规则",
                "显式准确率": "98.12%",
                "隐式准确率": "63.71%",
                "控制成功率": "79.89%",
                "幻觉率": "0.50%",
            },
            {
                "系统": "原生 LLM",
                "显式准确率": "91.25%",
                "隐式准确率": "83.26%",
                "控制成功率": "87.40%",
                "幻觉率": "10.72%",
            },
            {
                "系统": "LLM + 规则",
                "显式准确率": "97.89%",
                "隐式准确率": "92.57%",
                "控制成功率": "95.17%",
                "幻觉率": "1.16%",
            },
        ],
        width="stretch",
        hide_index=True,
    )
    st.caption("来源：项目 PDF 中记录的历史实验结果。请勿将其视为当前代码的自动评测输出。")
