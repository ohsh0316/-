
import streamlit as st
import pandas as pd

# ==========================================
# 1. 웹사이트 기본 설정
# ==========================================

st.set_page_config(
    page_title="반도체 수율 분석",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ 반도체 소자 수율 분석 시스템")
st.write("반도체별 생산 소자 및 불량 소자 개수를 이용한 수율 분석")
st.markdown("---")


# ==========================================
# 2. 함수: 개별 반도체 수율 계산
# ==========================================

def calculate_yield(total, defect):

    good = total - defect

    yield_rate = (good / total) * 100

    return yield_rate


# ==========================================
# 3. 함수: 수율 상태 판정
# ==========================================

def evaluate_yield(rate):

    if rate >= 90:
        return "양호"

    elif rate >= 85:
        return "보통"

    else:
        return "개선 필요"


# ==========================================
# 4. 함수: 평균 수율 계산
# ==========================================

def calculate_average(rates):

    total = 0

    for rate in rates:
        total += rate

    average = total / len(rates)

    return average


# ==========================================
# 5. 반도체 개수 입력
# ==========================================

st.header("1. 분석할 반도체 개수")

num = st.number_input(
    "분석할 반도체 종류의 개수를 입력하세요.",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)


# ==========================================
# 6. 리스트 생성
# ==========================================

semiconductor_names = []
total_counts = []
defect_counts = []
yield_rates = []
results = []


# ==========================================
# 7. 반도체별 데이터 입력
# ==========================================

st.header("2. 반도체별 생산 및 불량 데이터 입력")

for i in range(int(num)):

    st.subheader(f"반도체 {i+1}")

    name = st.text_input(
        "반도체 이름",
        value=f"반도체 {i+1}",
        key=f"name_{i}"
    )

    total = st.number_input(
        "전체 소자 개수",
        min_value=1,
        value=1000,
        step=100,
        key=f"total_{i}"
    )

    defect = st.number_input(
        "불량 소자 개수",
        min_value=0,
        value=100,
        step=1,
        key=f"defect_{i}"
    )

    semiconductor_names.append(name)
    total_counts.append(total)
    defect_counts.append(defect)

    st.markdown("---")


# ==========================================
# 8. 수율 분석 버튼
# ==========================================

if st.button("🔍 수율 분석하기", use_container_width=True):

    valid = True

    # 조건문과 반복문을 이용한 데이터 검사
    for i in range(int(num)):

        if defect_counts[i] > total_counts[i]:

            st.error(
                f"{semiconductor_names[i]}의 불량 개수가 "
                "전체 소자 개수보다 많습니다."
            )

            valid = False

        if semiconductor_names[i].strip() == "":

            st.error(f"반도체 {i+1}의 이름을 입력하세요.")

            valid = False

    # 모든 데이터가 정상일 경우 분석 실행
    if valid:

        # ==================================
        # 9. 개별 반도체 수율 분석
        # ==================================

        st.header("3. 반도체별 수율 분석 결과")

        for i in range(int(num)):

            # 함수 실행
            rate = calculate_yield(
                total_counts[i],
                defect_counts[i]
            )

            yield_rates.append(rate)

            # 조건문으로 상태 판정
            status = evaluate_yield(rate)

            results.append(status)

            # 분석 결과 출력
            st.subheader(semiconductor_names[i])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "전체 소자 개수",
                f"{total_counts[i]:,}개"
            )

            col2.metric(
                "불량 소자 개수",
                f"{defect_counts[i]:,}개"
            )

            col3.metric(
                "수율",
                f"{rate:.2f}%"
            )

            # 수율 진행 막대
            st.progress(int(rate))

            # 수율 상태 출력
            if rate >= 90:

                st.success("🟢 양호")

            elif rate >= 85:

                st.warning("🟡 보통")

            else:

                st.error("🔴 개선 필요")

            st.markdown("---")


        # ==================================
        # 10. 전체 반도체 평균 수율 계산
        # ==================================

        st.header("4. 전체 반도체 평균 수율")

        average_yield = calculate_average(yield_rates)

        st.metric(
            label="평균 수율",
            value=f"{average_yield:.2f}%"
        )

        # 평균 수율에 따른 상태 판정
        if average_yield >= 90:

            st.success("전체 평균 수율: 양호")

        elif average_yield >= 85:

            st.warning("전체 평균 수율: 보통")

        else:

            st.error("전체 평균 수율: 개선 필요")


        # ==================================
        # 11. 반도체 수율 목록 테이블
        # ==================================

        st.markdown("---")

        st.header("5. 반도체 수율 목록")

        # 테이블 데이터 리스트 생성
        table_data = []

        # 반복문을 이용하여 테이블 데이터 저장
        for i in range(int(num)):

            table_data.append({

                "반도체 번호": f"반도체 {i+1}",

                "수율(%)": f"{yield_rates[i]:.2f}%",

                "상태": results[i]

            })

        # 리스트를 데이터프레임으로 변환
        df = pd.DataFrame(table_data)

        # 테이블 출력
        st.table(df)


        # ==================================
        # 12. 분석 결과 다운로드
        # ==================================

        st.markdown("---")

        st.header("6. 분석 결과 다운로드")

        csv = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 수율 분석 결과 다운로드",
            data=csv,
            file_name="semiconductor_yield.csv",
            mime="text/csv"
        )

        st.success("모든 반도체의 수율 분석이 완료되었습니다!")
