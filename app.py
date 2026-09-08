import streamlit as st
from grader import grade_all
from rubric import RUBRIC

st.set_page_config(
    page_title="정치 과정 수행평가 자동 채점",
    page_icon="🗳️",
    layout="wide",
)

st.title("🗳️ 정치 과정 수행평가 자동 채점 시스템")
st.caption("2026학년도 2학년 2학기 명문고등학교 정치 | 총 30점")

defaults = {
    "student_id":        "",
    "student_name":      "",
    "q1_1_title":        "",
    "q1_1_background":   "",
    "q1_1_issue":        "",
    "q1_1_process":      "",
    "q1_2_demand":       "",
    "q1_2_support":      "",
    "q1_2_output":       "",
    "q1_2_feedback":     "",
    "q1_3_actor":        "",
    "q1_3_role":         "",
    "q1_3_body":         "",
    "q1_3_prole":        "",
    "q1_4":              "",
    "q2_1_name":         "",
    "q2_1_purpose":      "",
    "q2_1_effect":       "",
    "q2_2_target":       "",
    "q2_2_method_select": [],
    "q2_2_content":      "",
    "results":           None,
    "answers":           {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.header("📋 학생 정보")
    st.text_input("학번", placeholder="예: 20241234", key="student_id")
    st.text_input("이름", placeholder="예: 홍길동", key="student_name")
    st.divider()
    st.info("""
    **채점 안내**
    - 총점: 30점
    - 1부: 20점 (4문항 각 5점)
    - 2부: 10점 (2문항 각 5점)
    - 교과서 3개 사례 사용 시 감점
    """)
    st.warning("""
    **교과서 제외 사례**
    - 어린이 보호구역 (민식이법)
    - 한글날 공휴일 지정
    - 정당 가입 연령 하향
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "📘 1부. 정치 과정 분석 (20점)",
    "📗 2부. 시민 단체 만들기 (10점)",
    "📊 채점 결과",
    "📖 복습할 내용",
])

with tab1:
    st.subheader("문항 1-1. 정치 과정 사례 정리 (5점)")
    st.caption("내가 살고 있는 지역 또는 우리나라의 정치 과정이 드러나는 사례를 찾아보세요.")
    st.error("⛔ 사용 불가 사례: 어린이 보호구역 / 한글날 공휴일 지정 / 정당 가입 연령 하향")

    st.text_input("📌 사례 제목", placeholder="예: 탄소중립기본법 제정 과정", key="q1_1_title")
    st.text_area("🔹 배경", height=100, placeholder="문제가 발생한 상황이나 시민들이 관심을 가지게 된 이유를 서술하세요.", key="q1_1_background")
    st.text_area("🔹 쟁점 (2가지 이상 입장 제시)", height=100, placeholder="찬성 측 주장과 반대 측 주장 각각의 구체적 논거를 서술하세요.", key="q1_1_issue")
    st.text_area("🔹 전개 과정 (4줄 이상)", height=180, placeholder="문제 제기부터 해결 방안 마련까지의 순서를 4줄 이상 서술하세요.", key="q1_1_process")

    st.divider()

    st.subheader("문항 1-2. 이스턴(Easton) 정치 과정 모형 분석 (5점)")
    st.caption("1에서 정리한 사례를 이스턴의 정치 과정 모형에 근거하여 분석하세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔷 투입 (Input)**")
        st.text_area("요구", height=100, placeholder="예: 청소년 기후행동 단체가 더 강력한 탄소 감축 목표를 요구", key="q1_2_demand")
        st.text_area("지지", height=100, placeholder="예: 국제사회의 탄소중립 흐름, 여론의 환경 보호 동의", key="q1_2_support")
    with col2:
        st.markdown("**🔷 산출 & 환류**")
        st.text_area("산출", height=100, placeholder="예: 탄소중립기본법 제정·공포 (2050년 탄소중립 목표 명시)", key="q1_2_output")
        st.text_area("환류", height=100, placeholder="예: 법 제정 이후 시민단체가 이행 감시 요구를 다시 제기", key="q1_2_feedback")

    st.divider()

    st.subheader("문항 1-3. 비공식적 정치 주체 & 정책 결정 기구 (5점)")
    st.caption("비공식적 정치 주체와 정책 결정 기구를 각각 분석하세요.")

    col3, col4 = st.columns(2)
    with col3:
        st.text_input("비공식적 정치 주체 (유형 또는 명칭)", placeholder="예: 청소년기후행동 시민단체", key="q1_3_actor")
        st.text_area("비공식적 정치 주체의 역할", height=100, placeholder="예: 집회·헌법소원·서명운동을 통해 강력한 기후 입법 촉구", key="q1_3_role")
    with col4:
        st.text_input("정책 결정 기구 (공식 기관명)", placeholder="예: 국회", key="q1_3_body")
        st.text_area("정책 결정 기구의 역할", height=100, placeholder="예: 탄소중립기본법 심의·의결하여 2050 탄소중립 목표 법제화", key="q1_3_prole")

    st.divider()

    st.subheader("문항 1-4. 시민의 정치 참여 필요성 (5점)")
    st.caption("분석한 사례를 바탕으로 시민의 정치 참여가 왜 필요한지 3문장 이상 서술하세요.")

    with st.expander("💡 활용 가능한 논거 보기 (5가지 중 2가지 이상 포함 시 5점)"):
        st.markdown("""
| 논거 | 의미 |
|------|------|
| ① 국민 주권의 원리 | 국가 권력이 국민에게서 나온다는 것을 실현 |
| ② 다수 지배의 원리 | 다수 시민의 의사가 정책에 반영되어야 함 |
| ③ 정책의 정당성 부여 | 시민 동의를 얻은 정책이 민주적 권위를 가짐 |
| ④ 정치 효능감 | 내 참여가 변화를 만든다는 믿음 형성 |
| ⑤ 정치권력 남용 방지 | 권력자의 잘못된 결정을 감시·견제 |
        """)

    st.text_area("정치 참여 필요성 서술 (3문장 이상, 사례와 연계)", height=200, placeholder="분석한 사례를 구체적 근거로 활용하여 정치 참여의 필요성을 논거와 함께 서술하세요.", key="q1_4")

with tab2:
    st.subheader("문항 2-1. 시민 단체 설립 목적과 공익성 (5점)")
    st.caption("앞에서 분석한 사회 문제를 해결하는 데 도움이 되는 시민 단체를 만들어보세요.")

    st.text_input("🏢 단체명 (활동 목적이 드러나도록)", placeholder="예: 청소년기후행동연대", key="q2_1_name")
    st.text_area("📌 설립 목적 (4줄 이상)", height=180, placeholder="이 단체를 왜 만들었는지, 어떤 문제를 어떻게 바꾸고 싶은지 중심으로 4줄 이상 서술하세요.", key="q2_1_purpose")
    st.text_area("✨ 기대 효과 (3줄 이상)", height=140, placeholder="이 단체가 활동하면 어떤 사회적 변화가 나타날지 3줄 이상 서술하세요.", key="q2_1_effect")

    st.divider()

    st.subheader("문항 2-2. 캠페인 활동 계획 (5점)")
    st.caption("위 시민 단체가 할 수 있는 캠페인 활동을 구체적이고 실현 가능하게 계획해보세요.")

    st.text_input("🎯 대상", placeholder="예: ○○중학교 학생, 지역 주민 등 구체적 대상 명시", key="q2_2_target")

    method_options = ["포스터", "카드뉴스", "서명운동", "SNS 홍보", "설문조사", "캠페인 부스", "건의문 제출"]
    st.multiselect("📢 방법 선택 (1가지 이상)", method_options, key="q2_2_method_select")

    selected = st.session_state["q2_2_method_select"]
    if selected:
        with st.expander("💡 선택한 방법의 모범 활동 내용 예시 보기"):
            for sel in selected:
                model = RUBRIC["q2_2"]["model_answers"].get(sel)
                if model:
                    st.markdown(f"**✅ [{sel}] 모범 답안 예시**")
                    st.markdown(f"- **대상:** {model['대상']}")
                    st.markdown(f"- **방법:** {model['방법']}")
                    st.markdown("- **활동 내용:**")
                    st.code(model["활동내용"].strip(), language=None)
                    st.divider()

    st.text_area("📋 활동 내용 (인포그래픽 형식)", height=250, placeholder="""예시 (표 형식):
┌────────────────────────────────┐
│ [캠페인명]                     │
├──────────┬─────────────────────┤
│ 일시     │ 2025년 ○월 ○일      │
├──────────┼─────────────────────┤
│ 장소     │ 학교 교문 앞        │
├──────────┼─────────────────────┤
│ 활동     │ 체험 부스 + 서명    │
└──────────┴─────────────────────┘""", key="q2_2_content")

st.divider()
_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    run_grading = st.button("🔍 채점 실행", type="primary", use_container_width=True, key="btn_run_grading")

if run_grading:
    sid = st.session_state["student_id"]
    sname = st.session_state["student_name"]
    if not sid or not sname:
        st.warning("⚠️ 사이드바에서 학번과 이름을 먼저 입력하세요.")
    else:
        answers = {
            "q1_1_title":          st.session_state["q1_1_title"],
            "q1_1_background":     st.session_state["q1_1_background"],
            "q1_1_issue":          st.session_state["q1_1_issue"],
            "q1_1_process":        st.session_state["q1_1_process"],
            "q1_2_demand":         st.session_state["q1_2_demand"],
            "q1_2_support":        st.session_state["q1_2_support"],
            "q1_2_output":         st.session_state["q1_2_output"],
            "q1_2_feedback":       st.session_state["q1_2_feedback"],
            "q1_3_informal_actor": st.session_state["q1_3_actor"],
            "q1_3_informal_role":  st.session_state["q1_3_role"],
            "q1_3_policy_body":    st.session_state["q1_3_body"],
            "q1_3_policy_role":    st.session_state["q1_3_prole"],
            "q1_4":                st.session_state["q1_4"],
            "q2_1_name":           st.session_state["q2_1_name"],
            "q2_1_purpose":        st.session_state["q2_1_purpose"],
            "q2_1_effect":         st.session_state["q2_1_effect"],
            "q2_2_target":         st.session_state["q2_2_target"],
            "q2_2_method":         ", ".join(st.session_state["q2_2_method_select"]),
            "q2_2_content":        st.session_state["q2_2_content"],
        }
        st.session_state["results"] = grade_all(answers)
        st.session_state["answers"] = answers
        st.success("✅ 채점 완료! '채점 결과' 또는 '복습할 내용' 탭을 확인하세요.")

# ────────────────────────────────────────────────────────────────
# 공통 헬퍼
# ────────────────────────────────────────────────────────────────

def render_elements_ok(elements_ok: dict, label_map: dict):
    for k, v in elements_ok.items():
        icon = "✅" if v else "❌"
        st.markdown(f"- {icon} {label_map.get(k, k)}")

ELEM_LABELS = {
    "q1_2": {
        "투입_요구": "투입 — 요구",
        "투입_지지": "투입 — 지지",
        "산출":      "산출",
        "환류":      "환류",
    },
    "q1_3": {
        "비공식주체":   "비공식적 정치 주체",
        "비공식역할":   "비공식 주체 역할",
        "정책결정기구": "정책 결정 기구",
        "정책기구역할": "정책 결정 기구 역할",
    },
    "q2_1": {
        "단체명":   "단체명 (목적 드러남)",
        "설립목적": "설립 목적 (4줄 이상)",
        "기대효과": "기대 효과 (3줄 이상)",
        "공익성":   "공익성",
    },
    "q2_2": {
        "대상":     "대상 (구체적)",
        "방법":     "방법 (선택지 포함)",
        "활동내용": "활동 내용 (인포그래픽 형식)",
    },
}

Q_LABELS = {
    "q1_1": "문항 1-1. 정치 과정 사례 정리 (5점)",
    "q1_2": "문항 1-2. 이스턴 정치 과정 모형 (5점)",
    "q1_3": "문항 1-3. 비공식 주체 & 정책 결정 기구 (5점)",
    "q1_4": "문항 1-4. 정치 참여 필요성 (5점)",
    "q2_1": "문항 2-1. 시민 단체 설립 목적과 공익성 (5점)",
    "q2_2": "문항 2-2. 캠페인 활동 계획 (5점)",
}

def render_question_detail(q_key: str, r: dict):
    rubric = RUBRIC[q_key]
    score, max_score = r["score"], r["max_score"]

    st.progress(score / max_score)
    st.info(f"**채점 기준:** {rubric['score_levels'].get(score, '')}")

    if q_key == "q1_1" and r.get("is_forbidden_case"):
        st.error("⛔ 교과서 수록 사례 사용 → 최대 3점 상한 적용")

    if r.get("deductions"):
        st.markdown("**🔴 감점 사유:**")
        for d in r["deductions"]:
            st.error(f"• {d}")

    if r.get("feedback"):
        st.markdown("**💬 개선 피드백:**")
        for f in r["feedback"]:
            st.warning(f"💬 {f}")

    if q_key in ELEM_LABELS and r.get("elements_ok"):
        st.markdown("**🔷 요소별 충족 현황:**")
        render_elements_ok(r["elements_ok"], ELEM_LABELS[q_key])

    if q_key == "q1_4":
        col_x, col_y = st.columns(2)
        with col_x:
            found = r.get("arguments_found", [])
            st.markdown(f"**✅ 인정된 논거:** {', '.join(found) if found else '없음'}")
        with col_y:
            mc = r.get("misconceptions", [])
            if mc:
                st.markdown(f"**❌ 오개념 감지:** {', '.join(mc)}")
            sc = r.get("sentence_count", 0)
            st.markdown(
                f"**문장 수:** {sc}개 {'✅' if sc >= 3 else '❌'}  "
                f"| **사례 연계:** {'✅' if r.get('has_case_linkage') else '❌'}"
            )

    if q_key == "q2_2":
        if r.get("selected_methods"):
            st.markdown(f"**선택된 방법:** {', '.join(r['selected_methods'])}")
        if r.get("model_answer"):
            ma = r["model_answer"]
            st.markdown("**📌 선택 방법 기준 모범 답안:**")
            st.markdown(f"- **대상:** {ma['대상']}")
            st.markdown(f"- **방법:** {ma['방법']}")
            st.code(ma["활동내용"].strip(), language=None)

# ────────────────────────────────────────────────────────────────
# 복습 개념 데이터
# ────────────────────────────────────────────────────────────────

REVIEW_CONCEPTS = {
    "q1_1": {
        "concepts": [
            {
                "title": "📌 배경 서술이란?",
                "content": """
**배경**은 단순히 '무슨 일이 있었다'가 아니라,
**왜 그 문제가 사회적으로 주목받게 되었는지**를 설명하는 부분입니다.

✅ 포함해야 할 내용
- 문제가 발생하게 된 사회적 원인
- 시민들이 관심을 갖게 된 구체적 계기 (사건, 통계, 사고 등)

❌ 자주 하는 실수
- "이 문제는 오래전부터 있었다" → 원인 없이 상황만 서술
- "많은 사람들이 관심을 가졌다" → 계기 없이 결과만 서술
                """,
            },
            {
                "title": "📌 쟁점 서술이란?",
                "content": """
**쟁점**은 사회 구성원들 사이에서 **의견이 갈리는 지점**을 구체적으로 드러내는 것입니다.

✅ 올바른 쟁점 서술
- 찬성 측: 구체적 이유나 논거 제시
- 반대 측: 구체적 이유나 논거 제시

❌ 인정되지 않는 패턴
- "찬성과 반대가 있었다" → 내용 없는 형식만 서술
- "다양한 의견이 있었다" → 대립 구조가 드러나지 않음
                """,
            },
            {
                               "title": "📌 전개 과정 서술이란?",
                "content": """
**전개 과정**은 문제가 어떻게 사회적으로 다루어지고 해결되었는지
**흐름과 순서**가 드러나야 합니다.

✅ 반드시 포함할 3단계 흐름

**① 문제 제기**
- 누가(시민, 단체, 언론 등) 어떤 문제를 제기했는지 서술
- 단순히 "문제가 있었다"가 아니라, 구체적 사건·사고·통계 등을 계기로 제기되었음을 드러낼 것
- 예시: "2022년 ○○ 사고 이후 시민단체가 관련 법 제정을 촉구하며 서명운동을 시작하였다."

**② 관련 주체들의 대응**
- 비공식 주체(시민단체, 언론, 이익집단 등)와 공식 주체(국회, 행정부 등)가 각각 어떻게 반응했는지 서술
- 찬반 입장이 있었다면 양측의 대응 모두 포함할 것
- 예시: "시민단체는 집회와 청원을 통해 입법을 촉구하였고, 관련 기업은 경제적 부담을 이유로 반대 의견을 표명하였다. 국회에서는 관련 법안이 발의되어 위원회 심의가 시작되었다."

**③ 해결 방안 마련**
- 최종적으로 어떤 정책·법률·제도가 만들어졌는지 구체적으로 서술
- "해결되었다"는 표현만으로는 부족하며, 결정된 내용이 무엇인지 명시할 것
- 예시: "국회는 ○○법을 의결하였고, 정부는 시행령을 제정하여 ○○○년부터 시행하였다."

✅ 분량 기준: 최소 4줄

❌ 자주 하는 실수
- 결과만 서술하고 과정 생략
- 주체 없이 사건만 나열 ("법이 만들어졌다" → 누가 만들었는지 불분명)
- 4줄 미만 작성
                """,
            },
            {
                "title": "⛔ 교과서 사례 사용 금지",
                "content": """
| 금지 사례 | 포함되는 유사 표현 |
|-----------|------------------|
| 어린이 보호구역 | 스쿨존, 민식이법 |
| 한글날 공휴일 지정 | 공휴일 부활, 10월 9일 |
| 정당 가입 연령 하향 | 청소년 정당 가입, 정당법 개정 |

💡 대체 사례: 탄소중립기본법 / 중대재해처벌법 / 청소년 선거권 하향 등
                """,
            },
        ],
    },
    "q1_2": {
        "concepts": [
            {
                "title": "📌 이스턴 모형 4요소 핵심 정리",
                "content": """
| 요소 | 정의 | 예시 |
|------|------|------|
| **투입 — 요구** | 시민·집단이 정치 체계에 원하는 것 | 시민단체의 법 제정 촉구 |
| **투입 — 지지** | 정치 체계에 우호적인 환경·동의 | 여론의 지지, 국제사회 압력 |
| **산출** | 정책 결정 기구가 내린 구체적 결정물 | 법률 제정, 정책 시행 |
| **환류** | 산출 이후 반응이 다시 투입으로 연결 | 법 시행 후 이행 감시 요구 |
                """,
            },
            {
                "title": "⚠️ 오개념 주의 — 요소 혼동",
                "content": """
| 요소 | ❌ 쓰면 안 되는 내용 | ✅ 올바른 내용 |
|------|---------------------|--------------|
| 투입(요구) | "국회가 법을 제정했다" (→ 산출) | 시민이 원하는 것 |
| 산출 | "국회에서 논의했다" (→ 과정) | 확정된 법·정책 |
| 환류 | "결과가 좋았다" (→ 단순 평가) | 반응이 재투입으로 연결 |
                """,
            },
        ],
    },
    "q1_3": {
        "concepts": [
            {
                "title": "📌 비공식 vs 공식 주체 구별",
                "content": """
| 구분 | 해당 주체 |
|------|-----------|
| **비공식적 정치 주체** ✅ | 시민단체, 언론, 이익집단, NGO, 여론, 전문가 집단 |
| **공식 정치 기구** ❌ | 국회, 행정부, 대통령, 법원, 헌법재판소 |

⚠️ 공식 기구를 비공식 주체란에 쓰면 **오답**
⚠️ 비공식 주체를 정책 결정 기구란에 쓰면 **오답**
                """,
            },
            {
                "title": "📌 역할 서술 — 구체적으로 써야 함",
                "content": """
❌ 인정되지 않는 추상적 역할
- "관련 활동을 했다" / "역할을 담당했다"

✅ 인정되는 구체적 역할
- 시민단체: 서명운동·집회로 법 개정 촉구
- 언론: 지속 보도로 여론 형성
- 국회: 법안 심의·의결
- 행정부: 시행령 제정·집행
                """,
            },
        ],
    },
    "q1_4": {
        "concepts": [
            {
                "title": "📌 5가지 논거 — 개념별 핵심 의미",
                "content": """
| 논거 | 핵심 의미 | 혼동 주의 |
|------|-----------|-----------|
| 국민 주권 | 권력의 원천이 국민에게 있음을 실현 | 다수지배와 혼동 금지 |
| 다수 지배 | 더 많은 시민의 뜻이 정책에 반영됨 | 국민주권과 혼동 금지 |
| 정당성 부여 | 시민 동의를 얻은 정책이 권위를 가짐 | 효능감과 혼동 금지 |
| 정치 효능감 | 내 참여가 변화를 만든다는 믿음 형성 | "뿌듯하다"는 감정 표현만으로 오답 |
| 권력 남용 방지 | 권력자의 결정을 감시·견제 | 효능감과 혼동 금지 |
                """,
            },
            {
                "title": "📌 결론 방향 & 분량 조건",
                "content": """
✅ 결론은 반드시 **"참여가 필요하다"** 방향

❌ 오답 결론 패턴
- "참여하지 않아도 된다"
- "대의민주주의로 충분하다"

✅ 분량 조건: 완성된 문장 **3개 이상**, 사례와 **구체적 연계** 필수
                """,
            },
            {
                "title": "📌 고득점 답안 문장 구조 (복사해서 활용하세요)",
                "content": "아래 각 문장을 복사해서 내 사례에 맞게 수정하세요.",
                "copyable_blocks": [
                    {
                        "label": "① 사례 연계 문장",
                        "text": "○○ 사례에서 시민들이 적극적으로 참여함으로써 ~한 변화가 나타났다.",
                    },
                    {
                        "label": "② 논거 1 — 국민 주권",
                        "text": "이처럼 시민의 정치 참여는 국가 권력의 원천이 국민에게 있음을 실현하는 국민 주권의 원리를 실현한다.",
                    },
                    {
                        "label": "② 논거 1 — 다수 지배",
                        "text": "이처럼 시민의 정치 참여는 더 많은 시민의 의사가 정책에 반영되도록 하는 다수 지배의 원리를 실현한다.",
                    },
                    {
                        "label": "② 논거 1 — 정당성 부여",
                        "text": "이처럼 시민의 정치 참여는 정책이 국민의 동의를 바탕으로 만들어지도록 하여 정책에 민주적 정당성을 부여한다.",
                    },
                    {
                        "label": "③ 논거 2 — 권력 남용 방지",
                        "text": "또한 시민의 정치 참여는 정치 권력의 남용을 감시하고 견제하는 기능을 한다.",
                    },
                    {
                        "label": "③ 논거 2 — 정치 효능감",
                        "text": "또한 시민이 정치에 참여하는 과정에서 자신의 참여가 실제 변화를 만들어낼 수 있다는 정치 효능감을 높일 수 있다.",
                    },
                    {
                        "label": "④ 결론 문장",
                        "text": "따라서 민주주의 사회에서 시민의 정치 참여는 반드시 필요하다.",
                    },
                ],
            },
        ],
    },
    "q2_1": {
        "concepts": [
            {
                "title": "📌 단체명·설립목적·기대효과 조건",
                "content": """
| 항목 | 조건 | 분량 |
|------|------|------|
| 단체명 | 활동 목적이 이름에서 드러날 것 | — |
| 설립 목적 | 해결할 사회 문제 + 바꾸고 싶은 방향 명시 | 4줄 이상 |
| 기대 효과 | 설립 목적과 **다른 내용**으로 사회적 변화 서술 | 3줄 이상 |

⚠️ 기대 효과가 설립 목적과 60% 이상 겹치면 감점
⚠️ 공익에 반하는 목적이면 오답
                """,
            },
            {
                "title": "📌 배점 기준 (5점 만점)",
                "content": """
| 점수 | 기준 |
|------|------|
| 5점 | 사회 문제, 단체명, 설립 목적 3가지 모두 작성 + 공익성 충족 |
| 4점 | 3가지 요소 중 1가지 누락 또는 공익성이 명확하지 않음 |
| 3점 | 3가지 요소 중 2가지만 작성, 공익성 불분명하거나 내용 불충분 |
| 2점 | 3가지 요소 중 2가지 이상 누락 또는 공익에 명백히 어긋남 |
                """,
            },
        ],
    },
    "q2_2": {
        "concepts": [
            {
                "title": "📌 대상·방법·활동내용 조건",
                "content": """
**대상**
- ❌ "모든 사람", "시민들" → 너무 포괄적
- ✅ "○○중학교 학생", "지역 아파트 30~50대 주민"

**방법 — 선택한 방법의 특성이 활동 내용에 드러나야 함**

| 방법 | 활동 내용에 포함할 특성 |
|------|------------------------|
| 포스터 | 시각, 게시, 부착, 인쇄 |
| 카드뉴스 | 카드 형식, SNS, 시리즈 |
| 서명운동 | 서명 수집, 동의서 전달 |
| SNS 홍보 | 해시태그, 공유, 게시 |
| 설문조사 | 문항, 응답, 결과 분석 |
| 캠페인 부스 | 현장, 체험, 오프라인 |
| 건의문 제출 | 건의문, 기관에 제출 |

**활동 내용 형식**
- ✅ 표·단계·번호 목록·흐름도 (인포그래픽)
- ❌ 일반 문단 글쓰기만으로 구성
                """,
            },
            {
                "title": "📌 배점 기준 (5점 만점)",
                "content": """
| 점수 | 기준 |
|------|------|
| 5점 | 대상, 방법, 활동 내용 3가지 모두 포함 + 구체적·실현 가능 |
| 4점 | 3가지 요소 중 2가지만 포함 |
| 3점 | 3가지 요소 중 1가지만 포함 |
| 2점 | 3가지 요소 모두 작성하지 않음 |
                """,
            },
        ],
    },
}

# ────────────────────────────────────────────────────────────────
# 채점 결과 탭
# ────────────────────────────────────────────────────────────────

with tab3:
    results = st.session_state.get("results")
    if not results:
        st.info("⬅️ 답안을 입력한 후 '채점 실행' 버튼을 눌러주세요.")
    else:
        sid   = st.session_state["student_id"]
        sname = st.session_state["student_name"]
        total = results["total"]

        st.header(f"📊 채점 결과 — {sname} ({sid})")
        pct = total["score"] / total["max_score"]
        st.metric("🏆 총점", f"{total['score']} / {total['max_score']}점", f"{pct*100:.1f}%")
        st.progress(pct)
        st.divider()

        for q_key, label in Q_LABELS.items():
            r = results[q_key]
            is_perfect = r["score"] == r["max_score"]
            with st.expander(
                f"{'✅' if is_perfect else '📝'} {label} → {r['score']}/{r['max_score']}점",
                expanded=not is_perfect,
            ):
                render_question_detail(q_key, r)

        st.divider()
        st.subheader("📋 문항별 점수 요약")
        summary = {
            "문항":     [Q_LABELS[q] for q in Q_LABELS],
            "취득점수": [results[q]["score"] for q in Q_LABELS],
            "만점":     [results[q]["max_score"] for q in Q_LABELS],
            "비율":     [f"{results[q]['score']/results[q]['max_score']*100:.0f}%" for q in Q_LABELS],
        }
        st.table(summary)

# ────────────────────────────────────────────────────────────────
# 복습할 내용 탭
# ────────────────────────────────────────────────────────────────

def render_concepts(review):
    for concept in review.get("concepts", []):
        st.markdown(f"#### {concept['title']}")
        st.markdown(concept["content"])
        if concept.get("copyable_blocks"):
            for block in concept["copyable_blocks"]:
                st.markdown(f"**{block['label']}**")
                st.code(block["text"], language=None)

with tab4:
    st.header("📖 복습할 내용")
    results = st.session_state.get("results")

    if not results:
        st.info("⬅️ 답안을 입력하고 '채점 실행'을 누르면 틀린 문항의 복습 내용이 여기에 표시됩니다.")
        with st.expander("💡 전체 개념 미리 보기 (채점 전 예습용)"):
            for q_key, review in REVIEW_CONCEPTS.items():
                st.markdown(f"### {Q_LABELS[q_key]}")
                render_concepts(review)
                st.divider()
    else:
        failed = {
            q: results[q]
            for q in Q_LABELS
            if results[q]["score"] < results[q]["max_score"]
        }

        total = results["total"]
        c1, c2, c3 = st.columns(3)
        c1.metric("🏆 총점",      f"{total['score']}/{total['max_score']}점")
        c2.metric("✅ 만점 문항", f"{len(Q_LABELS) - len(failed)}개")
        c3.metric("📝 복습 필요", f"{len(failed)}개")

        st.divider()

        if not failed:
            st.success("🎉 모든 문항을 조건에 맞게 작성했습니다! 복습할 내용이 없습니다.")
            st.balloons()
        else:
            st.warning(f"**{len(failed)}개 문항**에서 조건을 충족하지 못했습니다. 핵심 개념을 복습하고 답안을 보완해보세요.")

            for q_key, r in failed.items():
                score, max_score = r["score"], r["max_score"]
                lost = max_score - score
                review = REVIEW_CONCEPTS.get(q_key, {})

                with st.expander(
                    f"📝 {Q_LABELS[q_key]}  |  {score}/{max_score}점  (-{lost}점)",
                    expanded=True,
                ):
                    st.markdown("### 🔴 내 답안의 부족한 부분")
                    render_question_detail(q_key, r)
                    st.divider()
                    st.markdown("### 📚 핵심 복습 포인트")
                    render_concepts(review)
