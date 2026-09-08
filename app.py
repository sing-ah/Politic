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