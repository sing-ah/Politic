# grader.py — 채점 로직 모듈

import re
from rubric import RUBRIC


def count_sentences(text: str) -> int:
    """완성된 문장 수 계산"""
    sentences = re.split(r'[.!?。]\s*', text.strip())
    return len([s for s in sentences if len(s.strip()) > 5])


def count_lines(text: str) -> int:
    """실질적 내용이 있는 줄 수 계산"""
    lines = text.strip().split('\n')
    return len([l for l in lines if len(l.strip()) > 3])


def check_keyword_or_meaning(text: str, keywords: list, equivalents: list = None) -> bool:
    """키워드 또는 의미 동치 표현 포함 여부 확인"""
    for kw in keywords:
        if kw in text:
            return True
    if equivalents:
        for equiv in equivalents:
            if equiv in text:
                return True
    return False


def check_misconception(text: str, misconception_keywords: list) -> bool:
    """오개념 패턴 감지"""
    for mkw in misconception_keywords:
        if mkw in text:
            return True
    return False


def check_forbidden_case(text: str) -> bool:
    """교과서 금지 사례 사용 여부 확인"""
    forbidden = RUBRIC["q1_1"]["forbidden_cases"]
    for case in forbidden:
        if case in text:
            return True
    return False


def check_political_process(text: str) -> bool:
    """정치 과정 드러나는지 확인"""
    keywords = RUBRIC["q1_1"]["political_process_keywords"]
    count = sum(1 for kw in keywords if kw in text)
    return count >= 2


# ─────────────────────────────────────────
# 문항별 채점 함수
# ─────────────────────────────────────────

def grade_q1_1(title: str, background: str, issue: str, process: str) -> dict:
    """문항 1-1 채점: 정치 과정 사례 정리"""
    rubric = RUBRIC["q1_1"]
    full_text = f"{title} {background} {issue} {process}"
    feedback = []
    deductions = []

    # 교과서 금지 사례 확인
    is_forbidden = check_forbidden_case(full_text)
    if is_forbidden:
        deductions.append("⛔ 교과서 수록 사례 사용 → 최대 3점 상한 적용")

    # 정치 과정 드러나는지
    has_political_process = check_political_process(full_text)
    if not has_political_process:
        deductions.append("⚠️ 정치 과정이 드러나지 않는 단순 사회 문제로 판단됨")
        feedback.append("정치 과정(시민 참여, 정부 대응, 입법 등)이 드러나는 사례를 선택해야 합니다.")

    # 배경 확인
    bg_keywords = rubric["required_elements"]["배경"]["keywords"]
    has_background = check_keyword_or_meaning(background, bg_keywords) or len(background.strip()) > 20
    if not has_background:
        deductions.append("배경 서술 미흡")
        feedback.append("문제가 발생한 상황이나 시민들이 관심을 가지게 된 이유를 서술하세요.")

    # 쟁점 확인 — 2가지 이상 입장 필요
    issue_keywords = rubric["required_elements"]["쟁점"]["keywords"]
    has_issue = check_keyword_or_meaning(issue, issue_keywords) or len(issue.strip()) > 20
    # 추상적 쟁점 패턴 감지
    wrong_issue = any(p in issue for p in rubric["wrong_patterns"])
    if wrong_issue:
        deductions.append("쟁점을 내용 없이 형식만 서술 (예: '찬성과 반대가 있었다')")
        feedback.append("찬성·반대 각각의 구체적 논거나 입장을 서술하세요.")

    # 전개 과정 — 4줄 이상 + 순서 흐름
    process_lines = count_lines(process)
    has_sequence = any(kw in process for kw in ["제기", "대응", "마련", "과정", "이후", "결과"])
    if process_lines < 4:
        deductions.append(f"전개 과정 분량 미충족 ({process_lines}줄 / 최소 4줄)")
        feedback.append("전개 과정은 최소 4줄(네 번째 줄 전체를 채워) 서술해야 합니다.")
    if not has_sequence:
        deductions.append("전개 과정에서 순서 흐름(제기→대응→해결)이 드러나지 않음")
        feedback.append("문제 제기 → 주체 대응 → 해결 방안 마련의 순서로 서술하세요.")

    # 점수 계산
    element_score = sum([
        has_background,
        has_issue and not wrong_issue,
        process_lines >= 4 and has_sequence,
    ])

    if not has_political_process:
        score = 2
    elif element_score == 3:
        score = 5
    elif element_score == 2:
        score = 4
    elif element_score == 1:
        score = 3
    else:
        score = 2

    # 교과서 사례 상한 적용
    if is_forbidden:
        score = min(score, rubric["forbidden_max_score"])

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "deductions": deductions,
        "feedback": feedback,
        "is_forbidden_case": is_forbidden,
    }


def grade_q1_2(input_demand: str, input_support: str,
               output: str, feedback_text: str) -> dict:
    """문항 1-2 채점: 이스턴 정치 과정 모형"""
    rubric = RUBRIC["q1_2"]
    deductions = []
    feedback = []
    elements_ok = {}

    # 투입 — 요구
    demand_ok = check_keyword_or_meaning(
        input_demand,
        rubric["elements"]["투입_요구"]["keywords"]
    )
    demand_misconception = check_misconception(
        input_demand,
        rubric["elements"]["투입_요구"]["misconception_keywords"]
    )
    if demand_misconception:
        deductions.append("⚠️ 오개념: 투입(요구)에 산출(법 제정·정책 결정) 내용을 사용")
        feedback.append("투입의 '요구'는 시민·집단이 정부에 원하는 것이며, 법 제정 등 결과는 '산출'입니다.")
        elements_ok["투입_요구"] = False
    else:
        elements_ok["투입_요구"] = demand_ok or len(input_demand.strip()) > 15

    # 투입 — 지지
    support_ok = check_keyword_or_meaning(
        input_support,
        rubric["elements"]["투입_지지"]["keywords"]
    )
    support_misconception = check_misconception(
        input_support,
        rubric["elements"]["투입_지지"]["misconception_keywords"]
    )
    if support_misconception:
        deductions.append("⚠️ 오개념: 투입(지지)에 반대·비판 내용을 사용")
        feedback.append("투입의 '지지'는 정치 체계에 대한 우호적 환경·동의입니다.")
        elements_ok["투입_지지"] = False
    else:
        elements_ok["투입_지지"] = support_ok or len(input_support.strip()) > 10

    # 산출
    output_misconception = check_misconception(
        output,
        rubric["elements"]["산출"]["misconception_keywords"]
    )
    if output_misconception:
        deductions.append("⚠️ 오개념: 산출에 과정(논의·심의)을 서술")
        feedback.append("산출은 정책 결정 기구가 내린 구체적 결정물(법률·정책·제도)이어야 합니다.")
        elements_ok["산출"] = False
    else:
        output_ok = check_keyword_or_meaning(
            output, rubric["elements"]["산출"]["keywords"]
        )
        elements_ok["산출"] = output_ok or len(output.strip()) > 10

    # 환류
    reinput_ok = any(kw in feedback_text for kw in ["다시", "재투입", "이후", "반응", "연결"])
    feedback_misconception = check_misconception(
        feedback_text,
        rubric["elements"]["환류"]["misconception_keywords"]
    )
    if feedback_misconception and not reinput_ok:
        deductions.append("⚠️ 오개념: 환류를 단순 평가(좋다/나쁘다)로만 서술")
        feedback.append("환류는 산출 이후 시민·집단의 반응이 다시 투입으로 연결되는 흐름을 서술해야 합니다.")
        elements_ok["환류"] = False
    else:
        fb_ok = check_keyword_or_meaning(
            feedback_text, rubric["elements"]["환류"]["keywords"]
        )
        elements_ok["환류"] = (fb_ok or len(feedback_text.strip()) > 10) and reinput_ok

    # 점수 계산
    ok_count = sum(elements_ok.values())
    if ok_count == 4:
        score = 5
    elif ok_count == 3:
        score = 4
    elif ok_count == 2:
        score = 3
    else:
        score = 2

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "elements_ok": elements_ok,
        "deductions": deductions,
        "feedback": feedback,
    }


def grade_q1_3(informal_actor: str, informal_role: str,
               policy_body: str, policy_role: str) -> dict:
    """문항 1-3 채점: 비공식 주체 & 정책 결정 기구"""
    rubric = RUBRIC["q1_3"]
    deductions = []
    feedback = []
    elements_ok = {}

    # 비공식 주체 유효성 확인
    invalid_informal = any(
        inv in informal_actor
        for inv in rubric["informal_actors"]["invalid_types"]
    )
    if invalid_informal:
        deductions.append("⚠️ 오개념: 공식 정치 기구(국회·정부·법원 등)를 비공식 주체로 분류")
        feedback.append("비공식적 정치 주체는 시민단체·언론·이익집단 등이며, 국회·정부는 공식 기구입니다.")
        elements_ok["비공식주체"] = False
    else:
        elements_ok["비공식주체"] = len(informal_actor.strip()) > 2

    # 비공식 주체 역할 — 추상적 표현 감지
    abstract_role = any(
        p in informal_role
        for p in rubric["informal_actors"]["abstract_role_patterns"]
    )
    if abstract_role:
        deductions.append("비공식 주체 역할을 추상적으로만 서술")
        feedback.append("비공식 주체가 구체적으로 무엇을 했는지(청원, 시위, 서명, 언론 보도 등) 서술하세요.")
        elements_ok["비공식역할"] = False
    else:
        elements_ok["비공식역할"] = len(informal_role.strip()) > 10

    # 정책 결정 기구 유효성 확인
    invalid_policy = any(
        inv in policy_body
        for inv in rubric["policy_bodies"]["invalid_types"]
    )
    if invalid_policy:
        deductions.append("⚠️ 오개념: 비공식 주체(시민단체·언론 등)를 정책 결정 기구로 분류")
        feedback.append("정책 결정 기구는 국회·행정부·법원·헌법재판소 등 공식 기관입니다.")
        elements_ok["정책결정기구"] = False
    else:
        elements_ok["정책결정기구"] = len(policy_body.strip()) > 2

    # 정책 결정 기구 역할
    role_keywords = rubric["policy_bodies"]["role_keywords"]
    has_role = check_keyword_or_meaning(policy_role, role_keywords) or len(policy_role.strip()) > 10
    elements_ok["정책기구역할"] = has_role

    # 점수 계산
    ok_count = sum(elements_ok.values())
    if ok_count == 4:
        score = 5
    elif ok_count == 3:
        score = 4
    elif ok_count == 2:
        score = 3
    else:
        score = 2

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "elements_ok": elements_ok,
        "deductions": deductions,
        "feedback": feedback,
    }


def grade_q1_4(answer: str) -> dict:
    """문항 1-4 채점: 정치 참여 필요성"""
    rubric = RUBRIC["q1_4"]
    deductions = []
    feedback = []
    arguments_found = []
    misconceptions = []

    # 결론 방향 확인 — 반드시 "필요하다" 방향
    invalid_conclusions = rubric["invalid_conclusions"]
    has_invalid_conclusion = any(ic in answer for ic in invalid_conclusions)
    if has_invalid_conclusion:
        deductions.append("⚠️ 결론 방향 오류: 정치 참여가 불필요하다는 방향의 결론")
        feedback.append("시민의 정치 참여가 '필요하다'는 결론이 명확히 드러나야 합니다.")

    # 사례 연계 확인
    case_keywords = ["사례", "과정에서", "결과", "이를 통해", "처럼", "와 같이", "에서 볼 수 있듯"]
    has_case_linkage = any(kw in answer for kw in case_keywords)
    case_specific = len([kw for kw in case_keywords if kw in answer]) >= 2

    # 논거별 확인
    for arg_name, arg_data in rubric["arguments"].items():
        keywords = arg_data["keywords"]
        equivalents = arg_data.get("meaning_equivalents", [])
        misconception = arg_data.get("misconception", "")
        invalid_expr = arg_data.get("invalid_expressions", [])

        # 유효하지 않은 표현 감지
        has_invalid = any(inv in answer for inv in invalid_expr)
        # 의미 동치 포함 여부
        has_arg = check_keyword_or_meaning(answer, keywords, equivalents)
        # 오개념 감지
        has_misconception = misconception and misconception[:10] in answer

        if has_invalid:
            deductions.append(f"⚠️ '{arg_name}' 논거에 인정 불가 표현 사용")
            feedback.append(f"'{arg_name}'은 단순 감정적 표현이 아닌 개념적 서술이 필요합니다.")
        elif has_arg and not has_misconception:
            arguments_found.append(arg_name)
        elif has_misconception:
            misconceptions.append(arg_name)
            deductions.append(f"⚠️ 오개념: '{arg_name}'의 설명에 다른 개념 특성 혼용")

    # 문장 수 확인
    sentence_count = count_sentences(answer)
    if sentence_count < rubric["min_sentences"]:
        deductions.append(f"문장 수 미충족 ({sentence_count}개 / 최소 3개)")
        feedback.append("완성된 문장 3개 이상 서술해야 합니다.")

    # 점수 계산
    arg_count = len(arguments_found)
    has_enough_sentences = sentence_count >= rubric["min_sentences"]

    if has_invalid_conclusion:
        score = 2
    elif arg_count >= 2 and has_enough_sentences and case_specific:
        score = 5
    elif arg_count >= 1 and has_enough_sentences and has_case_linkage:
        score = 4
    elif has_enough_sentences:
        score = 3
    else:
        score = 2

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "arguments_found": arguments_found,
        "misconceptions": misconceptions,
        "sentence_count": sentence_count,
        "has_case_linkage": has_case_linkage,
        "deductions": deductions,
        "feedback": feedback,
    }


def grade_q2_1(org_name: str, purpose: str, expected_effect: str) -> dict:
    """문항 2-1 채점: 시민 단체 설립"""
    rubric = RUBRIC["q2_1"]
    deductions = []
    feedback = []
    elements_ok = {}

    # 단체명 — 목적 드러나는지
    invalid_names = rubric["elements"]["단체명"]["invalid_examples"]
    name_invalid = any(inv in org_name for inv in invalid_names) or len(org_name.strip()) < 3
    if name_invalid:
        deductions.append("단체명에 활동 목적이 드러나지 않음")
        feedback.append("단체명만 봐도 활동 목적을 알 수 있도록 이름을 지으세요.")
        elements_ok["단체명"] = False
    else:
        elements_ok["단체명"] = True

    # 설립 목적 — 4줄 이상 + 구체적 사회 문제 + 방향
    purpose_lines = count_lines(purpose)
    invalid_purpose = any(p in purpose for p in rubric["elements"]["설립목적"]["invalid_patterns"])
    if purpose_lines < 4:
        deductions.append(f"설립 목적 분량 미충족 ({purpose_lines}줄 / 최소 4줄)")
        feedback.append("설립 목적은 최소 4줄(네 번째 줄 전체를 채워) 서술해야 합니다.")
        elements_ok["설립목적"] = False
    elif invalid_purpose:
        deductions.append("설립 목적을 추상적으로만 서술")
        feedback.append("해결하려는 사회 문제를 구체적으로 명시하고, 어떻게 바꾸고 싶은지 방향을 서술하세요.")
        elements_ok["설립목적"] = False
    else:
        elements_ok["설립목적"] = True

    # 기대 효과 — 3줄 이상 + 설립 목적과 다른 내용
    effect_lines = count_lines(expected_effect)
    # 목적과 기대효과 중복 확인
    purpose_words = set(purpose.split())
    effect_words = set(expected_effect.split())
    overlap_ratio = len(purpose_words & effect_words) / max(len(effect_words), 1)

    if effect_lines < 3:
        deductions.append(f"기대 효과 분량 미충족 ({effect_lines}줄 / 최소 3줄)")
        feedback.append("기대 효과는 최소 3줄(세 번째 줄 전체를 채워) 서술해야 합니다.")
        elements_ok["기대효과"] = False
    elif overlap_ratio > 0.6:
        deductions.append("기대 효과가 설립 목적과 내용이 지나치게 중복됨")
        feedback.append("기대 효과는 단체 활동으로 나타날 사회적 변화를 설립 목적과 다르게 서술하세요.")
        elements_ok["기대효과"] = False
    else:
        elements_ok["기대효과"] = True

    # 공익성 확인
    invalid_public = rubric["public_interest_check"]["invalid_patterns"]
    has_invalid_public = any(p in f"{purpose} {expected_effect}" for p in invalid_public)
    if has_invalid_public:
        deductions.append("⚠️ 공익성 위반: 특정 기업·정당·개인의 이익 추구")
        feedback.append("시민 단체는 공공의 이익에 부합하는 활동을 목적으로 해야 합니다.")
        elements_ok["공익성"] = False
    else:
        elements_ok["공익성"] = True

    # 점수 계산
    ok_count = sum(elements_ok.values())
    if ok_count == 4:
        score = 4
    elif ok_count == 3:
        score = 3
    elif ok_count == 2:
        score = 2
    else:
        score = 1

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "elements_ok": elements_ok,
        "deductions": deductions,
        "feedback": feedback,
    }


def grade_q2_2(target: str, method: str, activity_content: str) -> dict:
    """문항 2-2 채점: 캠페인 활동 계획"""
    rubric = RUBRIC["q2_2"]
    deductions = []
    feedback = []
    elements_ok = {}

    # 대상 — 구체적 대상 필수
    invalid_targets = rubric["elements"]["대상"]["invalid_patterns"]
    has_invalid_target = any(p in target for p in invalid_targets)
    if has_invalid_target:
        deductions.append("대상이 지나치게 포괄적 (모든 사람, 시민들 등)")
        feedback.append("'학교 학생', '지역 주민', '중장년층' 등 구체적 대상을 명시하세요.")
        elements_ok["대상"] = False
    else:
        elements_ok["대상"] = len(target.strip()) > 2

    # 방법 — 선택지 중 1가지 이상 선택 (의미 동치 허용)
    choices = rubric["elements"]["방법"]["choices"]
    equivalents = rubric["elements"]["방법"]["meaning_equivalents"]
    characteristics = rubric["elements"]["방법"]["method_characteristics"]

    selected_methods = []
    for choice in choices:
        equiv_list = equivalents.get(choice, [])
        if choice in method or any(e in method for e in equiv_list):
            selected_methods.append(choice)
        # 의미 동치: 활동 내용에서도 확인
        elif any(e in activity_content for e in equiv_list):
            selected_methods.append(choice)

    if not selected_methods:
        deductions.append("방법란에 선택지 외의 방법만 제시하거나 방법 미기재")
        feedback.append("포스터, 카드뉴스, 서명운동, SNS 홍보, 설문조사, 캠페인 부스, 건의문 제출 중 1가지 이상을 선택하세요.")
        elements_ok["방법"] = False
    else:
        elements_ok["방법"] = True
        # 선택 방법의 특성이 활동 내용에 드러나는지 확인
        method_characteristic_ok = False
        for sel_method in selected_methods:
            char_keywords = characteristics.get(sel_method, [])
            if any(ck in activity_content for ck in char_keywords):
                method_characteristic_ok = True
                break
        if not method_characteristic_ok:
            deductions.append(f"⚠️ 선택한 방법({', '.join(selected_methods)})의 특성이 활동 내용에 드러나지 않음")
            feedback.append(f"선택한 방법({', '.join(selected_methods)})의 특성(예: 포스터→시각적 게시물 제작·부착)이 활동 내용에 구체적으로 드러나야 합니다.")

    # 활동 내용 — 인포그래픽 형식 + 구체적 + 실현 가능
    infographic_formats = rubric["elements"]["활동내용"]["infographic_formats"]
    has_infographic = any(fmt in activity_content for fmt in infographic_formats)
    invalid_activity = any(
        p in activity_content
        for p in rubric["elements"]["활동내용"]["invalid_patterns"]
    )

    if not has_infographic:
        deductions.append("활동 내용이 인포그래픽 형식이 아닌 산문체로만 서술됨")
        feedback.append("표·도식·흐름도·카드 형식 등 시각적 구조로 활동 내용을 구성하세요.")
        elements_ok["활동내용"] = False
    elif invalid_activity:
        deductions.append("실현 불가능한 활동 계획 포함")
        feedback.append("실제로 실행 가능한 수준의 캠페인 활동 계획을 작성하세요.")
        elements_ok["활동내용"] = False
    else:
        elements_ok["활동내용"] = len(activity_content.strip()) > 30

    # 점수 계산
    ok_count = sum(elements_ok.values())
    if ok_count == 3 and not deductions:
        score = 3
    elif ok_count == 3:
        score = 2
    elif ok_count == 2:
        score = 2
    else:
        score = 1

    # 모범 답안 제공 (선택한 방법 기준)
    model_answer = None
    if selected_methods:
        model_answer = rubric["model_answers"].get(selected_methods[0])

    return {
        "score": score,
        "max_score": rubric["max_score"],
        "elements_ok": elements_ok,
        "selected_methods": selected_methods,
        "deductions": deductions,
        "feedback": feedback,
        "model_answer": model_answer,
    }


def grade_all(answers: dict) -> dict:
    """전체 채점 통합 실행"""
    results = {}

    results["q1_1"] = grade_q1_1(
        title=answers.get("q1_1_title", ""),
        background=answers.get("q1_1_background", ""),
        issue=answers.get("q1_1_issue", ""),
        process=answers.get("q1_1_process", ""),
    )
    results["q1_2"] = grade_q1_2(
        input_demand=answers.get("q1_2_demand", ""),
        input_support=answers.get("q1_2_support", ""),
        output=answers.get("q1_2_output", ""),
        feedback_text=answers.get("q1_2_feedback", ""),
    )
    results["q1_3"] = grade_q1_3(
        informal_actor=answers.get("q1_3_informal_actor", ""),
        informal_role=answers.get("q1_3_informal_role", ""),
        policy_body=answers.get("q1_3_policy_body", ""),
        policy_role=answers.get("q1_3_policy_role", ""),
    )
    results["q1_4"] = grade_q1_4(answer=answers.get("q1_4", ""))
    results["q2_1"] = grade_q2_1(
        org_name=answers.get("q2_1_name", ""),
        purpose=answers.get("q2_1_purpose", ""),
        expected_effect=answers.get("q2_1_effect", ""),
    )
    results["q2_2"] = grade_q2_2(
        target=answers.get("q2_2_target", ""),
        method=answers.get("q2_2_method", ""),
        activity_content=answers.get("q2_2_content", ""),
    )

    total = sum(r["score"] for r in results.values())
    max_total = sum(r["max_score"] for r in results.values())

    results["total"] = {"score": total, "max_score": max_total}
    return results