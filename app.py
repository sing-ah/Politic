# app.py — Streamlit 웹앱 메인

import streamlit as st
from grader import grade_all
from rubric import RUBRIC

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="정치 과정 수행평가 자동 채점",
    page_icon="🗳️",
    layout="wide",
)

st.title("🗳️ 정치 과정 수행평가 자동 채점 시스템")
st.caption("2026학년도 2학년 2학기 명문고등학교 정치 | 총 30점")

# ─────────────────────────────────────────
# 사이드바 — 학생 정보 입력
# ─────────────────────────────────────────
with st.sidebar:
    st.header("📋 학생 정보")
    student_id = st.text_input("학번", placeholder="예: 20241234")
    student_name = st.text_input("이름", placeholder="예: 홍길동")
    st.divider()
    st.info("""
    **채점 안내**
    - 총점: 30점
    - 1부: 20점 (4문항)
    - 2부: 10점 (2문항)
    - 교과서 3개 사례 사용 시 감점
    """)
    st.warning("""
    **교과서 제외 사례**
    - 어린이 보호구역 (민식이법)
    - 한글날 공휴일 지정
    - 정당 가입 연령 하향
    """)

answers = {}

# ─────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📘 1부. 정치 과정 분석 (20점)",
    "📗 2부. 시민 단체 만들기 (10점)",
    "📊 채점 결과",
])

# ─────────────────────────────────────────
# 1부 입력
# ─────────────────────────────────────────
with tab1:

    # 문항 1-1
    st.subheader("문항 1-1. 정치 과정 사례 정리 (5점)")
    st.caption("내가 살고 있는 지역 또는 우리나라의 정치 과정이 드러나는 사례를 찾아보세요.")
    st.error("⛔ 사용 불가 사례: 어린이 보호구역 / 한글날 공휴일 지정 / 정당 가입 연령 하향")

    answers["q1_1_title"] = st.text_input(
        "📌 사례 제목",
        placeholder="예: 탄소중립기본법 제정 과정",
        key="q1_1_title"
    )
    answers["q1_1_background"] = st.text_area(
        "🔹 배경 — 문제가 발생한 상황, 시민들이 관심을 가지게 된 이유",
        height=100,
        placeholder="문제가 발생한 상황이나 시민들이 관심을 가지게 된 이유를 서술하세요.",
        key="q1_1_background"
    )
    answers["q1_1_issue"] = st.text_area(
        "🔹 쟁점 — 사회 구성원의 의견이 어떻게 달랐는지 (2가지 이상 입장 제시)",
        height=100,
        placeholder="찬성 측 주장과 반대 측 주장 각각의 구체적 논거를 서술하세요.",
        key="q1_1_issue"
    )
    answers["q1_1_process"] = st.text_area(
        "🔹 전개 과정 — 문제 제기 → 주체 대응 → 해결 방안 (4줄 이상)",
        height=180,
        placeholder="문제 제기부터 해결 방안 마련까지의 순서를 4줄 이상 서술하세요.",
        key="q1_1_process"
    )

    st.divider()

    # 문항 1-2
    st.subheader("문항 1-2. 이스턴(Easton) 정치 과정 모형 분석 (5점)")
    st.caption("1에서 정리한 사례를 이스턴의 정치 과정 모형에 근거하여 분석하세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔷 투입 (Input)**")
        answers["q1_2_demand"] = st.text_area(
            "요구 — 시민·집단이 정치 체계에 무엇을 원했는지",
            height=100,
            placeholder="예: 청소년 기후행동 단체가 더 강력한 탄소 감축 목표를 요구",
            key="q1_2_demand"
        )
        answers["q1_2_support"] = st.text_area(
            "지지 — 정치 체계에 우호적인 환경",
            height=100,
            placeholder="예: 국제사회의 탄소중립 흐름, 여론의 환경 보호 동의",
            key="q1_2_support"
        )
    with col2:
        st.markdown("**🔷 산출 & 환류**")
        answers["q1_2_output"] = st.text_area(
            "산출 — 정책 결정 기구가 내린 구체적 결정물",
            height=100,
            placeholder="예: 탄소중립기본법 제정·공포 (2050년 탄소중립 목표 명시)",
            key="q1_2_output"
        )
        answers["q1_2_feedback"] = st.text_area(
            "환류 — 산출 이후 반응이 다시 투입으로 연결되는 흐름",
            height=100,
            placeholder="예: 법 제정 이후 시민단체가 이행 감시 요구를 다시 제기",
            key="q1_2_feedback"
        )

    st.markdown("**🔷 비공식적 정치 주체 & 정책 결정 기구**")
    st.caption("문항 1-3: 비공식적 정치 주체와 정책 결정 기구를 각각 분석하세요.")

    col3, col4 = st.columns(2)
    with col3:
        answers["q1_3_informal_actor"] = st.text_input(
            "비공식적 정치 주체 (유형 또는 명칭)",
            placeholder="예: 청소년기후행동 시민단체",
            key="q1_3_actor"
        )
        answers["q1_3_informal_role"] = st.text_area(
            "비공식적 정치 주체의 역할 (구체적으로)",
            height=80,
            placeholder="예: 집회·헌법소원·서명운동을 통해 강력한 기후 입법 촉구",
            key="q1_3_role"
        )
    with col4:
        answers["q1_3_policy_body"] = st.text_input(
            "정책 결정 기구 (공식 기관명)",
            placeholder="예: 국회",
            key="q1_3_body"
        )
        answers["q1_3_policy_role"] = st.text_area(
            "정책 결정 기구의 역할",
            height=80,
            placeholder="예: 탄소중립기본법 심의·의결하여 2050 탄소중립 목표 법제화",
            key="q1_3_prole"
        )

    st.divider()

    # 문항 1-4
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

    answers["q1_4"] = st.text_area(
        "정치 참여 필요성 서술 (3문장 이상, 사례와 연계)",
        height=200,
        placeholder="분석한 사례를 구체적 근거로 활용하여 정치 참여의 필요성을 논거와 함께 서술하세요.",
        key="q1_4"
    )

# ─────────────────────────────────────────
# 2부 입력
# ─────────────────────────────────────────
with tab2:

    # 문항 2-1
    st.subheader("문항 2-1. 시민 단체 만들기 (4점)")
    st.caption("앞에서 분석한 사회 문제를 해결하는 데 도움이 되는 시민 단체를 만들어보세요.")

    answers["q2_1_name"] = st.text_input(
        "🏢 단체명 (활동 목적이 드러나도록)",
        placeholder="예: 청소년기후행동연대",
        key="q2_1_name"
    )
    answers["q2_1_purpose"] = st.text_area(
        "📌 설립 목적 (4줄 이상 — 사회 문제 명시 + 바꾸고 싶은 방향)",
        height=180,
        placeholder="이 단체를 왜 만들었는지, 어떤 문제를 어떻게 바꾸고 싶은지 중심으로 4줄 이상 서술하세요.",
        key="q2_1_purpose"
    )
    answers["q2_1_effect"] = st.text_area(
        "✨ 기대 효과 (3줄 이상 — 설립 목적과 다른 내용으로 사회적 변화 서술)",
        height=140,
        placeholder="이 단체가 활동하면 어떤 사회적 변화가 나타날지 3줄 이상 서술하세요.",
        key="q2_1_effect"
    )

    st.divider()

    # 문항 2-2
    st.subheader("문항 2-2. 캠페인 활동 계획 (3점)")
    st.caption("위 시민 단체가 할 수 있는 캠페인 활동을 구체적이고 실현 가능하게 계획해보세요.")

    answers["q2_2_target"] = st.text_input(
        "🎯 대상 — 누구에게 알리거나 참여를 요청할 것인지 (구체적으로)",
        placeholder="예: ○○중학교 학생, 지역 주민 등 구체적 대상 명시",
        key="q2_2_target"
    )

    method_options = [
        "포스터", "카드뉴스", "서명운동",
        "SNS 홍보", "설문조사", "캠페인 부스", "건의문 제출"
    ]
    selected = st.multiselect(
        "📢 방법 — 캠페인 방법 선택 (1가지 이상)",
        method_options,
        key="q2_2_method_select"
    )
    answers["q2_2_method"] = ", ".join(selected)

    # 선택한 방법에 따른 모범 답안 힌트 표시
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

    answers["q2_2_content"] = st.text_area(
        "📋 활동 내용 — 인포그래픽 형식으로 구성 (표·도식·단계·흐름도 등)",
        height=250,
        placeholder="""예시 (표 형식):
┌────────────────────────────────┐
│ [캠페인명]                     │
├──────────┬─────────────────────┤
│ 일시     │ 2025년 ○월 ○일      │
├──────────┼─────────────────────┤
│ 장소     │ 학교 교문 앞        │
├──────────┼─────────────────────┤
│ 활동     │ 체험 부스 + 서명    │
└──────────┴─────────────────────┘""",
        key="q2_2_content"
    )

# ─────────────────────────────────────────
# 채점 실행 버튼
# ─────────────────────────────────────────
st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_grading = st.button(
        "🔍 채점 실행",
        type="primary",
        use_container_width=True,
    )

# ─────────────────────────────────────────
# 채점 결과 탭
# ─────────────────────────────────────────
with tab3:
    if run_grading:
        if not student_name or not student_id:
            st.warning("⚠️ 사이드바에서 학번과 이름을 먼저 입력하세요.")
        else:
            results = grade_all(answers)

            # 헤더
            st.header(f"📊 채점 결과 — {student_name} ({student_id})")
            total = results["total"]

            # 총점 게이지
            score_pct = total["score"] / total["max_score"]
            st.metric(
                label="🏆 총점",
                value=f"{total['score']} / {total['max_score']}점",
                delta=f"{score_pct*100:.1f}%"
            )
            st.progress(score_pct)
            st.divider()

            # 문항별 결과
            q_labels = {
                "q1_1": "문항 1-1. 정치 과정 사례 정리",
                "q1_2": "문항 1-2. 이스턴 정치 과정 모형",
                "q1_3": "문항 1-3. 비공식 주체 & 정책 결정 기구",
                "q1_4": "문항 1-4. 정치 참여 필요성",
                "q2_1": "문항 2-1. 시민 단체 만들기",
                "q2_2": "문항 2-2. 캠페인 활동 계획",
            }

            for q_key, label in q_labels.items():
                r = results[q_key]
                score = r["score"]
                max_score = r["max_score"]
                is_perfect = score == max_score

                with st.expander(
                    f"{'✅' if is_perfect else '📝'} {label} → "
                    f"{score} / {max_score}점",
                    expanded=not is_perfect
                ):
                    # 점수 바
                    st.progress(score / max_score)

                    # 점수 레벨 설명
                    rubric = RUBRIC[q_key]
                    level_desc = rubric["score_levels"].get(score, "")
                    st.info(f"**채점 기준:** {level_desc}")

                    # 교과서 사례 경고
                    if q_key == "q1_1" and r.get("is_forbidden_case"):
                        st.error("⛔ 교과서 수록 사례 사용 → 최대 3점 상한 적용")

                    # 감점 사유
                    if r.get("deductions"):
                        st.markdown("**🔴 감점 사유:**")
                        for d in r["deductions"]:
                            st.markdown(f"- {d}")

                    # 피드백
                    if r.get("feedback"):
                        st.markdown("**💬 개선 피드백:**")
                        for f in r["feedback"]:
                            st.markdown(f"- {f}")

                    # 문항별 추가 정보
                    if q_key == "q1_2" and r.get("elements_ok"):
                        st.markdown("**🔷 요소별 충족 현황:**")
                        elem_map = {
                            "투입_요구": "투입 — 요구",
                            "투입_지지": "투입 — 지지",
                            "산출": "산출",
                            "환류": "환류",
                        }
                        for k, v in r["elements_ok"].items():
                            icon = "✅" if v else "❌"
                            st.markdown(f"- {icon} {elem_map.get(k, k)}")

                    if q_key == "q1_3" and r.get("elements_ok"):
                        st.markdown("**🔷 요소별 충족 현황:**")
                        elem_map = {
                            "비공식주체": "비공식적 정치 주체",
                            "비공식역할": "비공식 주체 역할",
                            "정책결정기구": "정책 결정 기구",
                            "정책기구역할": "정책 결정 기구 역할",
                        }
                        for k, v in r["elements_ok"].items():
                            icon = "✅" if v else "❌"
                            st.markdown(f"- {icon} {elem_map.get(k, k)}")

                    if q_key == "q1_4":
                        if r.get("arguments_found"):
                            st.markdown("**✅ 인정된 논거:**")
                            for arg in r["arguments_found"]:
                                st.markdown(f"- {arg}")
                        if r.get("misconceptions"):
                            st.markdown("**❌ 오개념 감지된 논거:**")
                            for mc in r["misconceptions"]:
                                st.markdown(f"- {mc}")
                        st.markdown(
                            f"**문장 수:** {r.get('sentence_count', 0)}개 "
                            f"({'✅' if r.get('sentence_count', 0) >= 3 else '❌'} / 최소 3개)"
                        )
                        st.markdown(
                            f"**사례 연계:** {'✅ 인정' if r.get('has_case_linkage') else '❌ 미인정'}"
                        )

                    if q_key == "q2_1" and r.get("elements_ok"):
                        st.markdown("**🔷 요소별 충족 현황:**")
                        elem_map = {
                            "단체명": "단체명 (목적 드러남)",
                            "설립목적": "설립 목적 (4줄 이상)",
                            "기대효과": "기대 효과 (3줄 이상)",
                            "공익성": "공익성",
                        }
                        for k, v in r["elements_ok"].items():
                            icon = "✅" if v else "❌"
                            st.markdown(f"- {icon} {elem_map.get(k, k)}")

                    if q_key == "q2_2":
                        if r.get("selected_methods"):
                            st.markdown(
                                f"**선택된 방법:** {', '.join(r['selected_methods'])}"
                            )
                        if r.get("elements_ok"):
                            st.markdown("**🔷 요소별 충족 현황:**")
                            elem_map = {
                                "대상": "대상 (구체적)",
                                "방법": "방법 (선택지 포함)",
                                "활동내용": "활동 내용 (인포그래픽 형식)",
                            }
                            for k, v in r["elements_ok"].items():
                                icon = "✅" if v else "❌"
                                st.markdown(f"- {icon} {elem_map.get(k, k)}")
                        # 모범 답안 표시
                        if r.get("model_answer"):
                            ma = r["model_answer"]
                            st.markdown("**📌 선택 방법 기준 모범 답안:**")
                            st.markdown(f"- **대상:** {ma['대상']}")
                            st.markdown(f"- **방법:** {ma['방법']}")
                            st.markdown("- **활동 내용:**")
                            st.code(ma["활동내용"].strip(), language=None)

            st.divider()

            # 총점 요약 테이블
            st.subheader("📋 문항별 점수 요약")
            summary_data = {
                "문항": [],
                "취득점수": [],
                "만점": [],
                "비율": [],
            }
            for q_key, label in q_labels.items():
                r = results[q_key]
                summary_data["문항"].append(label)
                summary_data["취득점수"].append(r["score"])
                summary_data["만점"].append(r["max_score"])
                summary_data["비율"].append(
                    f"{r['score']/r['max_score']*100:.0f}%"
                )
            st.table(summary_data)

    else:
        st.info("⬅️ 1부, 2부 탭에서 답안을 모두 입력한 후 '채점 실행' 버튼을 눌러주세요.")
        st.markdown("""
        ### 📌 채점 시스템 특징
        - ✅ **의미 동치 허용**: 교과 개념어 없이 의미가 담기면 인정
        - ✅ **선택지 방법 특성 확인**: 선택한 방법의 특성이 활동 내용에 드러나야 함
        - ✅ **오개념 자동 감지**: 한 개념의 특성을 다른 개념 설명에 사용 시 오답 처리
        - ✅ **결론 방향 확인**: 요구한 결론이 답안에 명확히 드러나야 통과
        - ⛔ **교과서 사례 제한**: 어린이 보호구역 / 한글날 공휴일 / 정당 가입 연령 → 최대 3점
        """)
        # app.py — Streamlit 웹앱 메인 (복습 탭 추가 버전)

import streamlit as st
from grader import grade_all
from rubric import RUBRIC

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="정치 과정 수행평가 자동 채점",
    page_icon="🗳️",
    layout="wide",
)

st.title("🗳️ 정치 과정 수행평가 자동 채점 시스템")
st.caption("2026학년도 2학년 2학기 명문고등학교 정치 | 총 30점")

# ─────────────────────────────────────────
# 사이드바 — 학생 정보 입력
# ─────────────────────────────────────────
with st.sidebar:
    st.header("📋 학생 정보")
    student_id = st.text_input("학번", placeholder="예: 20241234")
    student_name = st.text_input("이름", placeholder="예: 홍길동")
    st.divider()
    st.info("""
    **채점 안내**
    - 총점: 30점
    - 1부: 20점 (4문항)
    - 2부: 10점 (2문항)
    - 교과서 3개 사례 사용 시 감점
    """)
    st.warning("""
    **교과서 제외 사례**
    - 어린이 보호구역 (민식이법)
    - 한글날 공휴일 지정
    - 정당 가입 연령 하향
    """)

answers = {}

# ─────────────────────────────────────────
# 탭 구성 — 복습할 내용 탭 추가
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 1부. 정치 과정 분석 (20점)",
    "📗 2부. 시민 단체 만들기 (10점)",
    "📊 채점 결과",
    "📖 복습할 내용",   # ← 새로 추가
])

# ─────────────────────────────────────────
# 1부 입력
# ─────────────────────────────────────────
with tab1:

    st.subheader("문항 1-1. 정치 과정 사례 정리 (5점)")
    st.caption("내가 살고 있는 지역 또는 우리나라의 정치 과정이 드러나는 사례를 찾아보세요.")
    st.error("⛔ 사용 불가 사례: 어린이 보호구역 / 한글날 공휴일 지정 / 정당 가입 연령 하향")

    answers["q1_1_title"] = st.text_input(
        "📌 사례 제목",
        placeholder="예: 탄소중립기본법 제정 과정",
        key="q1_1_title"
    )
    answers["q1_1_background"] = st.text_area(
        "🔹 배경 — 문제가 발생한 상황, 시민들이 관심을 가지게 된 이유",
        height=100,
        placeholder="문제가 발생한 상황이나 시민들이 관심을 가지게 된 이유를 서술하세요.",
        key="q1_1_background"
    )
    answers["q1_1_issue"] = st.text_area(
        "🔹 쟁점 — 사회 구성원의 의견이 어떻게 달랐는지 (2가지 이상 입장 제시)",
        height=100,
        placeholder="찬성 측 주장과 반대 측 주장 각각의 구체적 논거를 서술하세요.",
        key="q1_1_issue"
    )
    answers["q1_1_process"] = st.text_area(
        "🔹 전개 과정 — 문제 제기 → 주체 대응 → 해결 방안 (4줄 이상)",
        height=180,
        placeholder="문제 제기부터 해결 방안 마련까지의 순서를 4줄 이상 서술하세요.",
        key="q1_1_process"
    )

    st.divider()

    st.subheader("문항 1-2. 이스턴(Easton) 정치 과정 모형 분석 (5점)")
    st.caption("1에서 정리한 사례를 이스턴의 정치 과정 모형에 근거하여 분석하세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔷 투입 (Input)**")
        answers["q1_2_demand"] = st.text_area(
            "요구 — 시민·집단이 정치 체계에 무엇을 원했는지",
            height=100,
            placeholder="예: 청소년 기후행동 단체가 더 강력한 탄소 감축 목표를 요구",
            key="q1_2_demand"
        )
        answers["q1_2_support"] = st.text_area(
            "지지 — 정치 체계에 우호적인 환경",
            height=100,
            placeholder="예: 국제사회의 탄소중립 흐름, 여론의 환경 보호 동의",
            key="q1_2_support"
        )
    with col2:
        st.markdown("**🔷 산출 & 환류**")
        answers["q1_2_output"] = st.text_area(
            "산출 — 정책 결정 기구가 내린 구체적 결정물",
            height=100,
            placeholder="예: 탄소중립기본법 제정·공포 (2050년 탄소중립 목표 명시)",
            key="q1_2_output"
        )
        answers["q1_2_feedback"] = st.text_area(
            "환류 — 산출 이후 반응이 다시 투입으로 연결되는 흐름",
            height=100,
            placeholder="예: 법 제정 이후 시민단체가 이행 감시 요구를 다시 제기",
            key="q1_2_feedback"
        )

    st.markdown("**🔷 비공식적 정치 주체 & 정책 결정 기구**")
    st.caption("문항 1-3: 비공식적 정치 주체와 정책 결정 기구를 각각 분석하세요.")

    col3, col4 = st.columns(2)
    with col3:
        answers["q1_3_informal_actor"] = st.text_input(
            "비공식적 정치 주체 (유형 또는 명칭)",
            placeholder="예: 청소년기후행동 시민단체",
            key="q1_3_actor"
        )
        answers["q1_3_informal_role"] = st.text_area(
            "비공식적 정치 주체의 역할 (구체적으로)",
            height=80,
            placeholder="예: 집회·헌법소원·서명운동을 통해 강력한 기후 입법 촉구",
            key="q1_3_role"
        )
    with col4:
        answers["q1_3_policy_body"] = st.text_input(
            "정책 결정 기구 (공식 기관명)",
            placeholder="예: 국회",
            key="q1_3_body"
        )
        answers["q1_3_policy_role"] = st.text_area(
            "정책 결정 기구의 역할",
            height=80,
            placeholder="예: 탄소중립기본법 심의·의결하여 2050 탄소중립 목표 법제화",
            key="q1_3_prole"
        )

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

    answers["q1_4"] = st.text_area(
        "정치 참여 필요성 서술 (3문장 이상, 사례와 연계)",
        height=200,
        placeholder="분석한 사례를 구체적 근거로 활용하여 정치 참여의 필요성을 논거와 함께 서술하세요.",
        key="q1_4"
    )

# ─────────────────────────────────────────
# 2부 입력
# ─────────────────────────────────────────
with tab2:

    st.subheader("문항 2-1. 시민 단체 만들기 (4점)")
    st.caption("앞에서 분석한 사회 문제를 해결하는 데 도움이 되는 시민 단체를 만들어보세요.")

    answers["q2_1_name"] = st.text_input(
        "🏢 단체명 (활동 목적이 드러나도록)",
        placeholder="예: 청소년기후행동연대",
        key="q2_1_name"
    )
    answers["q2_1_purpose"] = st.text_area(
        "📌 설립 목적 (4줄 이상 — 사회 문제 명시 + 바꾸고 싶은 방향)",
        height=180,
        placeholder="이 단체를 왜 만들었는지, 어떤 문제를 어떻게 바꾸고 싶은지 중심으로 4줄 이상 서술하세요.",
        key="q2_1_purpose"
    )
    answers["q2_1_effect"] = st.text_area(
        "✨ 기대 효과 (3줄 이상 — 설립 목적과 다른 내용으로 사회적 변화 서술)",
        height=140,
        placeholder="이 단체가 활동하면 어떤 사회적 변화가 나타날지 3줄 이상 서술하세요.",
        key="q2_1_effect"
    )

    st.divider()

    st.subheader("문항 2-2. 캠페인 활동 계획 (3점)")
    st.caption("위 시민 단체가 할 수 있는 캠페인 활동을 구체적이고 실현 가능하게 계획해보세요.")

    answers["q2_2_target"] = st.text_input(
        "🎯 대상 — 누구에게 알리거나 참여를 요청할 것인지 (구체적으로)",
        placeholder="예: ○○중학교 학생, 지역 주민 등 구체적 대상 명시",
        key="q2_2_target"
    )

    method_options = [
        "포스터", "카드뉴스", "서명운동",
        "SNS 홍보", "설문조사", "캠페인 부스", "건의문 제출"
    ]
    selected = st.multiselect(
        "📢 방법 — 캠페인 방법 선택 (1가지 이상)",
        method_options,
        key="q2_2_method_select"
    )
    answers["q2_2_method"] = ", ".join(selected)

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

    answers["q2_2_content"] = st.text_area(
        "📋 활동 내용 — 인포그래픽 형식으로 구성 (표·도식·단계·흐름도 등)",
        height=250,
        placeholder="""예시 (표 형식):
┌────────────────────────────────┐
│ [캠페인명]                     │
├──────────┬─────────────────────┤
│ 일시     │ 2025년 ○월 ○일      │
├──────────┼─────────────────────┤
│ 장소     │ 학교 교문 앞        │
├──────────┼─────────────────────┤
│ 활동     │ 체험 부스 + 서명    │
└──────────┴─────────────────────┘""",
        key="q2_2_content"
    )

# ─────────────────────────────────────────
# 채점 실행 버튼
# ─────────────────────────────────────────
st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_grading = st.button(
        "🔍 채점 실행",
        type="primary",
        use_container_width=True,
    )

# ─────────────────────────────────────────
# 채점 결과 저장 (탭 간 공유)
# ─────────────────────────────────────────
if run_grading:
    if not student_name or not student_id:
        st.warning("⚠️ 사이드바에서 학번과 이름을 먼저 입력하세요.")
        st.session_state["results"] = None
    else:
        st.session_state["results"] = grade_all(answers)
        st.session_state["answers"] = answers

# ─────────────────────────────────────────
# 채점 결과 탭
# ─────────────────────────────────────────
with tab3:
    results = st.session_state.get("results")

    if results:
        total = results["total"]

        st.header(f"📊 채점 결과 — {student_name} ({student_id})")
        score_pct = total["score"] / total["max_score"]
        st.metric(
            label="🏆 총점",
            value=f"{total['score']} / {total['max_score']}점",
            delta=f"{score_pct*100:.1f}%"
        )
        st.progress(score_pct)
        st.divider()

        q_labels = {
            "q1_1": "문항 1-1. 정치 과정 사례 정리",
            "q1_2": "문항 1-2. 이스턴 정치 과정 모형",
            "q1_3": "문항 1-3. 비공식 주체 & 정책 결정 기구",
            "q1_4": "문항 1-4. 정치 참여 필요성",
            "q2_1": "문항 2-1. 시민 단체 만들기",
            "q2_2": "문항 2-2. 캠페인 활동 계획",
        }

        for q_key, label in q_labels.items():
            r = results[q_key]
            score = r["score"]
            max_score = r["max_score"]
            is_perfect = score == max_score

            with st.expander(
                f"{'✅' if is_perfect else '📝'} {label} → {score} / {max_score}점",
                expanded=not is_perfect
            ):
                st.progress(score / max_score)
                rubric = RUBRIC[q_key]
                level_desc = rubric["score_levels"].get(score, "")
                st.info(f"**채점 기준:** {level_desc}")

                if q_key == "q1_1" and r.get("is_forbidden_case"):
                    st.error("⛔ 교과서 수록 사례 사용 → 최대 3점 상한 적용")

                if r.get("deductions"):
                    st.markdown("**🔴 감점 사유:**")
                    for d in r["deductions"]:
                        st.markdown(f"- {d}")

                if r.get("feedback"):
                    st.markdown("**💬 개선 피드백:**")
                    for f in r["feedback"]:
                        st.markdown(f"- {f}")

                if q_key == "q1_2" and r.get("elements_ok"):
                    st.markdown("**🔷 요소별 충족 현황:**")
                    elem_map = {
                        "투입_요구": "투입 — 요구",
                        "투입_지지": "투입 — 지지",
                        "산출": "산출",
                        "환류": "환류",
                    }
                    for k, v in r["elements_ok"].items():
                        st.markdown(f"- {'✅' if v else '❌'} {elem_map.get(k, k)}")

                if q_key == "q1_3" and r.get("elements_ok"):
                    st.markdown("**🔷 요소별 충족 현황:**")
                    elem_map = {
                        "비공식주체": "비공식적 정치 주체",
                        "비공식역할": "비공식 주체 역할",
                        "정책결정기구": "정책 결정 기구",
                        "정책기구역할": "정책 결정 기구 역할",
                    }
                    for k, v in r["elements_ok"].items():
                        st.markdown(f"- {'✅' if v else '❌'} {elem_map.get(k, k)}")

                if q_key == "q1_4":
                    if r.get("arguments_found"):
                        st.markdown("**✅ 인정된 논거:**")
                        for arg in r["arguments_found"]:
                            st.markdown(f"- {arg}")
                    if r.get("misconceptions"):
                        st.markdown("**❌ 오개념 감지된 논거:**")
                        for mc in r["misconceptions"]:
                            st.markdown(f"- {mc}")
                    st.markdown(
                        f"**문장 수:** {r.get('sentence_count', 0)}개 "
                        f"({'✅' if r.get('sentence_count', 0) >= 3 else '❌'} / 최소 3개)"
                    )
                    st.markdown(
                        f"**사례 연계:** {'✅ 인정' if r.get('has_case_linkage') else '❌ 미인정'}"
                    )

                if q_key == "q2_1" and r.get("elements_ok"):
                    st.markdown("**🔷 요소별 충족 현황:**")
                    elem_map = {
                        "단체명": "단체명 (목적 드러남)",
                        "설립목적": "설립 목적 (4줄 이상)",
                        "기대효과": "기대 효과 (3줄 이상)",
                        "공익성": "공익성",
                    }
                    for k, v in r["elements_ok"].items():
                        st.markdown(f"- {'✅' if v else '❌'} {elem_map.get(k, k)}")

                if q_key == "q2_2":
                    if r.get("selected_methods"):
                        st.markdown(f"**선택된 방법:** {', '.join(r['selected_methods'])}")
                    if r.get("elements_ok"):
                        st.markdown("**🔷 요소별 충족 현황:**")
                        elem_map = {
                            "대상": "대상 (구체적)",
                            "방법": "방법 (선택지 포함)",
                            "활동내용": "활동 내용 (인포그래픽 형식)",
                        }
                        for k, v in r["elements_ok"].items():
                            st.markdown(f"- {'✅' if v else '❌'} {elem_map.get(k, k)}")
                    if r.get("model_answer"):
                        ma = r["model_answer"]
                        st.markdown("**📌 선택 방법 기준 모범 답안:**")
                        st.markdown(f"- **대상:** {ma['대상']}")
                        st.markdown(f"- **방법:** {ma['방법']}")
                        st.code(ma["활동내용"].strip(), language=None)

        st.divider()
        st.subheader("📋 문항별 점수 요약")
        summary_data = {
            "문항": [],
            "취득점수": [],
            "만점": [],
            "비율": [],
        }
        for q_key, label in q_labels.items():
            r = results[q_key]
            summary_data["문항"].append(label)
            summary_data["취득점수"].append(r["score"])
            summary_data["만점"].append(r["max_score"])
            summary_data["비율"].append(f"{r['score']/r['max_score']*100:.0f}%")
        st.table(summary_data)

    else:
        st.info("⬅️ 답안을 입력한 후 '채점 실행' 버튼을 눌러주세요.")

# ─────────────────────────────────────────
# 📖 복습할 내용 탭 (신규 추가)
# ─────────────────────────────────────────

# 문항별 핵심 개념 복습 데이터
REVIEW_CONCEPTS = {
    "q1_1": {
        "label": "문항 1-1. 정치 과정 사례 정리",
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
- 두 입장이 **대립하는 구조**가 보여야 함

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
① 문제 제기 → ② 관련 주체들의 대응 → ③ 해결 방안 마련

✅ 분량 기준
- 최소 4줄 (네 번째 줄 전체를 채워 작성)

❌ 자주 하는 실수
- 결과만 서술하고 과정 생략
- 4줄 미만으로 작성
- 순서 없이 나열만 함
                """,
            },
            {
                "title": "⛔ 교과서 사례 사용 금지",
                "content": """
아래 3가지 사례는 교과서에 수록된 사례로, **사용 시 최대 3점 상한**이 적용됩니다.

| 금지 사례 | 포함되는 유사 표현 |
|-----------|------------------|
| 어린이 보호구역 | 스쿨존, 민식이법, 어린이 교통안전 |
| 한글날 공휴일 지정 | 공휴일 부활, 10월 9일 공휴일 |
| 정당 가입 연령 하향 | 청소년 정당 가입, 정당법 연령 개정 |

💡 **대체 사례 예시**
- 탄소중립기본법 제정
- 중대재해처벌법 도입
- 청소년 선거권 연령 하향 (공직선거법 개정)
- 장애인 이동권 시위와 교통약자법 개정
                """,
            },
        ],
    },

    "q1_2": {
        "label": "문항 1-2. 이스턴 정치 과정 모형",
        "concepts": [
            {
                "title": "📌 이스턴 모형 4요소 핵심 정리",
                "content": """
| 요소 | 정의 | 예시 |
|------|------|------|
| **투입 — 요구** | 시민·집단이 정치 체계에 원하는 것 | 시민단체의 법 제정 촉구, 청원 |
| **투입 — 지지** | 정치 체계에 우호적인 환경·동의 | 여론의 지지, 국제사회 압력 |
| **산출** | 정책 결정 기구가 내린 구체적 결정물 | 법률 제정, 정책 시행, 예산 결정 |
| **환류** | 산출 이후 반응이 다시 투입으로 연결 | 법 시행 후 시민단체의 이행 감시 요구 |
                """,
            },
            {
                "title": "⚠️ 오개념 주의 — 요소 혼동",
                "content": """
**투입(요구)** 에 쓰면 안 되는 내용
- ❌ "국회가 법을 제정했다" → 이건 **산출**입니다

**산출** 에 쓰면 안 되는 내용
- ❌ "국회에서 논의했다", "심의 중이다" → 이건 **과정**입니다
- ✅ 산출 = 심의가 끝난 **결과물** (법률, 정책, 제도)

**환류** 에 쓰면 안 되는 내용
- ❌ "결과가 좋았다", "성공적이었다" → 단순 평가는 환류가 아님
- ✅ 환류 = 산출 이후 반응이 **다시 투입으로 연결**되는 흐름
산출(법 제정) → 시민 반응 → 새로운 요구(투입) 발생
                """,
            },
        ],
    },

    "q1_3": {
        "label": "문항 1-3. 비공식 주체 & 정책 결정 기구",
        "concepts": [
            {
                "title": "📌 비공식 vs 공식 주체 구별",
                "content": """
| 구분 | 해당 주체 |
|------|-----------|
| **비공식적 정치 주체** ✅ | 시민단체, 언론, 이익집단, NGO, 여론, 전문가 집단 |
| **공식 정치 기구** ❌ | 국회, 행정부, 대통령, 법원, 헌법재판소, 지방의회 |

⚠️ **혼동 주의**
- 공식 기구를 비공식 주체란에 쓰면 **오답 처리**
- 비공식 주체를 정책 결정 기구란에 쓰면 **오답 처리**

💡 **정당**은 경계 사례 → 비공식 주체로 쓸 수 있으나  
정책 결정 기구로 서술하면 오답
                """,
            },
            {
                "title": "📌 역할 서술 — 구체적으로 써야 함",
                "content": """
❌ 인정되지 않는 추상적 역할 서술
- "관련 활동을 했다"
- "역할을 담당했다"
- "참여했다"

✅ 인정되는 구체적 역할 서술 예시

**비공식 주체 역할**
- 시민단체: 서명운동·집회를 통해 법 개정 촉구
- 언론: 문제를 지속 보도하여 여론 형성
- 이익집단: 국회의원에게 입법 로비 활동

**정책 결정 기구 역할**
- 국회: 법안 심의·의결
- 행정부: 시행령 제정·집행
- 헌법재판소: 위헌 여부 심판
                """,
            },
        ],
    },

    "q1_4": {
        "label": "문항 1-4. 정치 참여 필요성",
        "concepts": [
            {
                "title": "📌 5가지 논거 — 개념별 핵심 의미",
                "content": """
| 논거 | 핵심 의미 | 혼동 주의 |
|------|-----------|-----------|
| **국민 주권** | 권력의 원천이 국민에게 있음을 실현 | 다수결(다수지배)과 혼동 금지 |
| **다수 지배** | 더 많은 시민의 뜻이 정책에 반영됨 | 국민 주권(권력의 원천)과 혼동 금지 |
| **정당성 부여** | 시민 동의를 얻은 정책이 권위를 가짐 | 효능감(내가 영향을 줌)과 혼동 금지 |
| **정치 효능감** | 내 참여가 변화를 만든다는 믿음 형성 | "뿌듯하다"는 감정 표현으로만 쓰면 오답 |
| **권력 남용 방지** | 권력자의 잘못된 결정을 감시·견제 | 효능감과 혼동 금지 |
                """,
            },
            {
                "title": "📌 결론 방향 & 분량 조건",
                "content": """
✅ 결론은 반드시 **"참여가 필요하다"** 방향이어야 함

❌ 아래 방향의 결론은 오답 처리
- "참여하지 않아도 된다"
- "대의민주주의로 충분하다"
- "참여가 불필요하다"

✅ 분량 조건
- **완성된 문장 3개 이상** (세 번째 줄 전체를 채워 작성)
- 사례와 **구체적으로 연계**해야 5점

💡 **고득점 답안 구조 예시**
[사례 연계] ○○ 사례에서 시민들이 참여함으로써 ~한 변화가 나타났다.
[논거 1] 이처럼 시민의 정치 참여는 국민 주권의 원리를 실현하는 데 필수적이다.
[논거 2] 또한 시민 참여는 정치 권력의 남용을 감시·견제하는 기능을 한다.
[결론] 따라서 민주주의 사회에서 시민의 정치 참여는 반드시 필요하다.
                """,
            },
        ],
    },

    "q2_1": {
        "label": "문항 2-1. 시민 단체 만들기",
        "concepts": [
            {
                "title": "📌 단체명 — 목적이 드러나야 함",
                "content": """
✅ 좋은 단체명 조건
- 단체명만 봐도 **무엇을 하는 단체인지** 알 수 있어야 함
- 활동 대상 또는 해결 목표가 이름에 포함

✅ 예시
- "청소년기후행동연대" → 청소년, 기후, 행동이 드러남
- "장애인이동권보장시민모임" → 대상·목적 명확

❌ 인정되지 않는 단체명
- "우리들의 모임", "좋은 사회", "행복 단체" → 목적 불분명
                """,
            },
            {
                "title": "📌 설립 목적 & 기대 효과 구별",
                "content": """
| 항목 | 내용 | 분량 |
|------|------|------|
| **설립 목적** | 왜 만들었는지 + 어떤 문제를 어떻게 바꾸고 싶은지 | 4줄 이상 |
| **기대 효과** | 활동 후 나타날 **사회적 변화** | 3줄 이상 |

⚠️ **기대 효과 ≠ 설립 목적 반복**
- 설립 목적: "기후 위기 대응 정책 마련을 촉구하기 위해"
- 기대 효과: "청소년들의 기후 인식이 높아지고, 지역사회 탄소 감축 실천이 늘어남"

❌ 두 항목이 60% 이상 내용이 겹치면 감점
                """,
            },
            {
                "title": "📌 공익성 조건",
                "content": """
시민단체는 **공공의 이익**을 위한 활동을 목적으로 해야 합니다.

❌ 공익성 위반 사례
- 특정 기업 홍보 목적
- 특정 정당 지지 활동
- 개인 이익 추구
- 영리 활동 포함

✅ 공익성 충족 기준
- 불특정 다수 또는 사회 전체에 도움이 되는 목적
- 정치적으로 중립적인 방향성
                """,
            },
        ],
    },

    "q2_2": {
        "label": "문항 2-2. 캠페인 활동 계획",
        "concepts": [
            {
                "title": "📌 대상 — 구체적이어야 함",
                "content": """
❌ 인정되지 않는 포괄적 대상
- "모든 사람", "시민들", "국민 전체"

✅ 인정되는 구체적 대상 예시
- ○○중학교 재학생
- 지역 아파트 주민 (30~50대)
- 학부모 및 교사
- 지역구 청소년
                """,
            },
            {
                "title": "📌 선택 방법의 특성이 활동 내용에 드러나야 함",
                "content": """
방법을 선택했다면, **그 방법의 고유한 특성**이 활동 내용에 반드시 보여야 합니다.

| 선택 방법 | 활동 내용에 반드시 포함할 특성 키워드 |
|-----------|--------------------------------------|
| 포스터 | 시각, 게시, 부착, 인쇄, 이미지 |
| 카드뉴스 | 카드, ○장, SNS, 시리즈, 인스타 |
| 서명운동 | 서명, 동의서, 수집, 전달 |
| SNS 홍보 | 해시태그, 공유, 게시, 인스타, 유튜브 |
| 설문조사 | 문항, 응답, 조사, 결과 분석 |
| 캠페인 부스 | 부스, 현장, 체험, 오프라인 |
| 건의문 제출 | 건의문, 제출, 기관에 전달 |

❌ 방법을 선택만 하고 활동 내용에 특성이 없으면 감점
                """,
            },
            {
                "title": "📌 인포그래픽 형식이란?",
                "content": """
활동 내용은 **산문체(문단 글쓰기)가 아닌 시각적 구조**로 작성해야 합니다.

✅ 인정되는 형식
- 표 (┌─┐ 형식)
- 단계별 흐름 (Step 1 → Step 2 → Step 3)
- 번호 목록 (①②③)
- 도식 / 카드 형식

❌ 인정되지 않는 형식
- 일반 문단 글쓰기만으로 구성된 경우

❌ 실현 불가능한 계획
- "전 국민 대상 1:1 상담"
- "모든 국민 직접 방문"
                """,
            },
        ],
    },
}


with tab4:
    st.header("📖 복습할 내용")

    results = st.session_state.get("results")

    if not results:
        # 채점 전 안내
        st.info("⬅️ 답안을 입력하고 '채점 실행'을 누르면 틀린 문항의 복습 내용이 여기에 표시됩니다.")

        # 채점 전에도 전체 개념 미리보기 제공
        with st.expander("💡 전체 개념 미리 보기 (채점 전 예습용)"):
            for q_key, review in REVIEW_CONCEPTS.items():
                st.markdown(f"### {review['label']}")
                for concept in review["concepts"]:
                    st.markdown(f"#### {concept['title']}")
                    st.markdown(concept["content"])
                st.divider()

    else:
        q_labels = {
            "q1_1": "문항 1-1. 정치 과정 사례 정리",
            "q1_2": "문항 1-2. 이스턴 정치 과정 모형",
            "q1_3": "문항 1-3. 비공식 주체 & 정책 결정 기구",
            "q1_4": "문항 1-4. 정치 참여 필요성",
            "q2_1": "문항 2-1. 시민 단체 만들기",
            "q2_2": "문항 2-2. 캠페인 활동 계획",
        }

        # 조건 미충족 문항 필터링
        failed_questions = {
            q_key: results[q_key]
            for q_key in q_labels
            if results[q_key]["score"] < results[q_key]["max_score"]
        }

        # ── 결과 요약 헤더
        total = results["total"]
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🏆 총점", f"{total['score']} / {total['max_score']}점")
        with col_b:
            st.metric("✅ 만점 문항", f"{len(q_labels) - len(failed_questions)}개")
        with col_c:
            st.metric("📝 복습 필요 문항", f"{len(failed_questions)}개")

        st.divider()

        if not failed_questions:
            # 전체 만점
            st.success("🎉 모든 문항을 조건에 맞게 작성했습니다! 복습할 내용이 없습니다.")
            st.balloons()

        else:
            st.warning(
                f"아래 **{len(failed_questions)}개 문항**에서 조건을 충족하지 못했습니다. "
                "각 문항의 핵심 개념을 복습하고 답안을 보완해보세요."
            )

            for q_key, r in failed_questions.items():
                label = q_labels[q_key]
                score = r["score"]
                max_score = r["max_score"]
                review = REVIEW_CONCEPTS.get(q_key, {})
                lost = max_score - score

                # 문항 복습 카드
                with st.expander(
                    f"📝 {label} | {score}/{max_score}점 "
                    f"(-{lost}점 감점)",
                    expanded=True,
                ):
                    # ── 섹션 1: 내 답안의 부족한 부분
                    st.markdown("### 🔴 내 답안의 부족한 부분")

                    if r.get("deductions"):
                        for d in r["deductions"]:
                            st.error(f"• {d}")
                    if r.get("feedback"):
                        for f in r["feedback"]:
                            st.warning(f"💬 {f}")

                    # 문항별 요소 현황 추가 표시
                    if q_key in ("q1_2", "q1_3", "q2_1") and r.get("elements_ok"):
                        elem_labels = {
                            "q1_2": {
                                "투입_요구": "투입 — 요구",
                                "투입_지지": "투입 — 지지",
                                "산출": "산출",
                                "환류": "환류",
                            },
                            "q1_3": {
                                "비공식주체": "비공식적 정치 주체",
                                "비공식역할": "비공식 주체 역할",
                                "정책결정기구": "정책 결정 기구",
                                "정책기구역할": "정책 결정 기구 역할",
                            },
                            "q2_1": {
                                "단체명": "단체명 (목적 드러남)",
                                "설립목적": "설립 목적 (4줄 이상)",
                                "기대효과": "기대 효과 (3줄 이상)",
                                "공익성": "공익성",
                            },
                        }
                        st.markdown("**요소별 충족 현황:**")
                        for k, v in r["elements_ok"].items():
                            icon = "✅" if v else "❌"
                            emap = elem_labels.get(q_key, {})
                            st.markdown(f"- {icon} {emap.get(k, k)}")

                    if q_key == "q1_4":
                        col_x, col_y = st.columns(2)
                        with col_x:
                            if r.get("arguments_found"):
                                st.markdown("**✅ 인정된 논거:**")
                                for arg in r["arguments_found"]:
                                    st.markdown(f"- {arg}")
                            else:
                                st.markdown("**✅ 인정된 논거:** 없음")
                        with col_y:
                            if r.get("misconceptions"):
                                st.markdown("**❌ 오개념 감지:**")
                                for mc in r["misconceptions"]:
                                    st.markdown(f"- {mc}")
                            st.markdown(
                                f"**문장 수:** {r.get('sentence_count', 0)}개 "
                                f"({'✅' if r.get('sentence_count', 0) >= 3 else '❌'})"
                            )
                            st.markdown(
                                f"**사례 연계:** "
                                f"{'✅' if r.get('has_case_linkage') else '❌'}"
                            )

                    if q_key == "q2_2":
                        if r.get("selected_methods"):
                            st.markdown(
                                f"**선택된 방법:** {', '.join(r['selected_methods'])}"
                            )
                        if r.get("elements_ok"):
                            for k, v in r["elements_ok"].items():
                                icon = "✅" if v else "❌"
                                elem_map = {
                                    "대상": "대상 (구체적)",
                                    "방법": "방법 (선택지 포함)",
                                    "활동내용": "활동 내용 (인포그래픽 형식)",
                                }
                                st.markdown(f"- {icon} {elem_map.get(k, k)}")

                    st.divider()

                    # ── 섹션 2: 핵심 복습 포인트
                    st.markdown("### 📚 핵심 복습 포인트")

                    if review.get("concepts"):
                        for concept in review["concepts"]:
                            with st.container():
                                st.markdown(f"#### {concept['title']}")
                                st.markdown(concept["content"])
                                st.markdown("")
                    else:
                        st.info("복습 자료를 불러오는 중입니다.")

                    st.divider()

                    # ── 섹션 3: 모범 답안 (2-2 한정)
                    if q_key == "q2_2" and r.get("model_answer"):
                        st.markdown("### 📌 선택 방법 기준 모범 답안")
                        ma = r["model_answer"]
                        st.markdown(f"- **대상:** {ma['대상']}")
                        st.markdown(f"- **방법:** {ma['방법']}")
                        st.markdown("- **활동 내용:**")
                        st.code(ma["활동내용"].strip(), language=None)
