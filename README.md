# 서울 Airbnb 데이터 수집 및 시각화 프로젝트

서울 지역의 Airbnb 숙소 정보를 수집하고, 이를 시각적으로 분석할 수 있는 대시보드 프로젝트입니다.

## 🚀 주요 기능
- **데이터 수집**: Airbnb API를 사용하여 서울 지역 숙소 정보(제목, 가격, 평점 등) 자동 수집
- **데이터 저장**: SQLite 데이터베이스 (`airbnb_scraping_seoul.db`)에 수집 결과 저장
- **시각화 대시보드**: Streamlit을 활용한 가격 분포, 평점 분석 및 필터링 기능 제공

## 🛠️ 설치 및 실행 방법

### 1. 환경 설정
본 프로젝트는 `uv`를 사용하여 패키지를 관리합니다.

```bash
# 종속성 설치
uv pip install -r requirements.txt
```

### 2. 데이터 수집 실행
```bash
uv run python airbnb_scraping.py
```

### 3. 대시보드 실행
```bash
uv run streamlit run airbnb_app.py
```

## 🌐 GitHub 및 Streamlit Cloud 배포 방법
1. **GitHub 저장소 생성**: 새 저장소를 만들고 코드를 푸시합니다.
2. **Streamlit Cloud 연결**: [Streamlit Cloud](https://share.streamlit.io/)에 접속하여 GitHub 저장소를 연결합니다.
3. **Main File 설정**: `airbnb_app.py`를 메인 실행 파일로 지정합니다.

## 📁 주요 파일 구조
- `airbnb_scraping.py`: 데이터 수집 스크립트
- `airbnb_app.py`: Streamlit 대시보드 소스
- `airbnb_scraping_seoul.db`: 수집된 데이터 (SQLite)
- `requirements.txt`: 배포용 패키지 목록
- `.gitignore`: 깃 허브 업로드 제외 설정
