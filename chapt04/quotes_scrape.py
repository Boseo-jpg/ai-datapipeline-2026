import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 초기 설정
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # 웹페이지 오픈
    driver.get('https://quotes.toscrape.com/')

    # 웹페이지가 로딩될 때까지 대기
    wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'footer')
        )
    )

    # 로그인 링크 가져오기
    login_link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, 'Login')
        )
    )

    # 로그인 페이지 이동
    login_link.click()

    # 아이디 입력창 대기
    username_input = wait.until(
        EC.presence_of_element_located(
            (By.ID, 'username')
        )
    )

    # 비밀번호 입력창
    password_input = driver.find_element(
        By.ID, 'password'
    )

    # 아이디 / 비밀번호 입력
    username_input.send_keys('admin')
    password_input.send_keys('admin')

    # 로그인 버튼
    login_btn = driver.find_element(
        By.CSS_SELECTOR,
        'input[type="submit"]'
    )

    # 로그인 버튼 클릭
    login_btn.click()

    # 로그인 완료 확인
    wait.until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, 'Logout')
        )
    )

    print('로그인 성공')

    # ==========================================
    # 데이터 수집
    # ==========================================

    rows = []

    # 총 10페이지 반복
    for page_num in range(1, 11):

        # 인용문이 화면에 나타날 때까지 대기
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.quote')
            )
        )

        print(f'{page_num} 페이지 수집')

        # 현재 페이지의 모든 인용문
        quotes = driver.find_elements(
            By.CSS_SELECTOR,
            '.quote'
        )

        # 한 페이지당 인용문 반복
        for quote in quotes:

            # 인용문
            text = quote.find_element(
                By.CSS_SELECTOR,
                '.text'
            ).text

            # 작성자
            author = quote.find_element(
                By.CSS_SELECTOR,
                '.author'
            ).text

            # 작성자 상세 링크
            link = quote.find_element(
                By.CSS_SELECTOR,
                '.author + a'
            ).get_attribute('href')

            # 태그 목록
            tags = quote.find_elements(
                By.CSS_SELECTOR,
                '.tags > a'
            )

            # 태그들을 문자열로 합치기
            tag_text = ','.join(
                tag.text for tag in tags
            )

            # 결과 저장
            rows.append({
                'text': text,
                'author': author,
                'link': link,
                'tags': tag_text
            })

        # ==========================================
        # 다음 페이지 이동
        # ==========================================

        next_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            'li.next a'
        )

        # 다음 페이지가 없으면 종료
        if not next_buttons:
            break

        # 다음 페이지 클릭
        next_buttons[0].click()

    # ==========================================
    # DataFrame 생성
    # ==========================================

    df_quotes = pd.DataFrame(rows)

    print()
    print(f'총 {len(df_quotes)}건 수집 완료')

    # 데이터 일부 확인
    print(df_quotes.head())

    # ==========================================
    # CSV 저장
    # ==========================================

    df_quotes.to_csv(
        'quotes_100.csv',
        encoding='utf-8-sig',
        index=False
    )

    print('파일 저장 완료 : quotes_100.csv')

    # ==========================================
    # 로그아웃
    # ==========================================

    logout_link = driver.find_element(
        By.LINK_TEXT,
        'Logout'
    )

    logout_link.click()

    print('로그아웃 완료')


except Exception as e:
    print('실행 중 오류 발생')
    print(e)


finally:
    # 브라우저 종료
    driver.quit()
    print('브라우저 종료')