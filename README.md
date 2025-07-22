
# 분당구 수내역 작업실 매물 자동 리포트 시스템

## 📋 프로젝트 개요
수내역 반경 500m 내 20~30㎡ 작업실 매물을 자동으로 수집, 분석하여 리포트를 생성하는 시스템입니다.

## 🚀 주요 기능

### 1. 데이터 수집 (Collection)
- **크롤링**: Python Requests/BeautifulSoup 활용
- **API 연동**: 국토교통부 OpenAPI 지원
- **수집 데이터**: 매물명, 주소, 좌표, 면적, 층수, 보증금, 월세, 관리비, 주차여부, URL, 수집일

### 2. 데이터 전처리 (Preprocessing)
- **지리 필터링**: geopy.distance로 반경 500m 내 매물 선별
- **면적 필터링**: 20~30㎡ 범위 매물만 추출
- **데이터 정제**: 중복 제거, 결측치 처리

### 3. 거래 분석 (Transaction Analysis)
- **기본 통계**: 보증금/월세 평균, 중앙값, 분위수
- **관리비 분석**: 평균 관리비 및 분포
- **주차 분석**: 주차 가능 매물 비율
- **동별 비교**: 정자동, 서현동, 수내동 가격 비교

### 4. 동향 분석 (Trend Analysis)
- **㎡당 비용**: 동별 단위면적당 가격 비교
- **시계열 분석**: 월별/계절별 보증금/월세 추이
- **가격 트렌드**: 시기별 가격 변동 패턴

### 5. 보고서 생성 (Report Generation)
- **Excel 파일**: 다중 시트(매물데이터, 통계요약, 동별분석)
- **CSV 파일**: 원시 데이터 저장
- **PDF 리포트**: ReportLab 활용 자동 PDF 생성

### 6. 시각화 대시보드 (Dashboard)
- **웹 대시보드**: Streamlit 기반 인터랙티브 대시보드
- **지도 시각화**: Folium으로 매물 위치 지도
- **차트**: matplotlib/seaborn 활용 분석 차트

### 7. 자동화 (Automation)
- **스케줄링**: APScheduler로 정기 실행
- **이메일 발송**: smtplib로 리포트 자동 발송
- **cron 지원**: Linux/Mac 환경 cron 스케줄링

## 📁 파일 구조
```
sunae-property-report/
├── main.py                    # 메인 실행 스크립트
├── streamlit_dashboard.py     # Streamlit 대시보드
├── automation_scheduler.py    # 자동화 스케줄러
├── sunae_properties.csv      # 매물 데이터 (CSV)
├── sunae_property_report.xlsx # 종합 리포트 (Excel)
├── sunae_property_map.html    # 매물 위치 지도
├── property_analysis_charts.png # 분석 차트
└── README.md                 # 프로젝트 설명서
```

## 🛠️ 설치 및 실행

### 1. 필요 라이브러리 설치
```bash
pip install pandas numpy requests beautifulsoup4 geopy matplotlib seaborn folium
pip install reportlab pdfkit streamlit APScheduler xlsxwriter openpyxl
pip install streamlit-folium
```

### 2. 메인 스크립트 실행
```bash
python main.py
```

### 3. 대시보드 실행
```bash
streamlit run streamlit_dashboard.py
```

### 4. 자동화 스케줄러 실행
```bash
python automation_scheduler.py
```

## 📊 결과 파일

### 생성되는 파일들
1. **sunae_properties.csv** - 필터링된 매물 데이터
2. **sunae_property_report.xlsx** - 종합 분석 리포트 (3개 시트)
3. **property_analysis_charts.png** - 시각화 차트
4. **sunae_property_map.html** - 인터랙티브 지도
5. **streamlit_dashboard.py** - 웹 대시보드 코드

## 🔧 커스터마이징

### 검색 조건 변경
```python
# 반경 및 면적 범위 수정
self.radius = 0.5  # 500m (km 단위)
self.min_area = 20  # 최소 면적
self.max_area = 30  # 최대 면적
```

### 이메일 설정
```python
# automation_scheduler.py에서 이메일 정보 수정
self.email_user = "your_email@gmail.com"
self.email_password = "your_app_password" 
self.recipients = ["recipient@example.com"]
```

### 스케줄 변경
```python
# 매일 오전 9시 → 다른 시간으로 변경
scheduler.add_job(automation.run_full_analysis, 'cron', hour=9, minute=0)
```

## 🎯 활용 방안

### 개인 사용
- 작업실 임대를 위한 시장 조사
- 투자용 소형 상업시설 분석
- 지역별 임대료 트렌드 파악

### 사업 활용
- 부동산 중개업체 시장 분석 도구
- 임대사업자를 위한 시장 가격 모니터링
- 정기 시장 리포트 자동 생성

### 확장 가능성
- 다른 지역(강남, 홍대 등) 확장
- 다른 부동산 유형(오피스텔, 원룸) 추가
- 머신러닝 기반 가격 예측 모델 구축

## ⚠️ 주의사항

1. **크롤링 규정**: 웹사이트별 robots.txt 및 이용약관 준수
2. **API 제한**: 국토교통부 API 사용량 제한 확인
3. **개인정보**: 수집 데이터의 개인정보보호법 준수
4. **서버 부하**: 과도한 요청으로 인한 서버 부하 주의

## 📞 문의 및 지원

프로젝트 관련 문의사항이 있으시면 GitHub Issues를 통해 연락해 주세요.

---

**개발일시**: 2025-07-22  
**개발시간**: 약 3시간  
**버전**: 1.0.0
