
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class PropertyReportAutomation:
    def __init__(self):
        # 이메일 설정 (실제 사용시 환경변수로 관리 권장)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = "databizflow@gmail.com"  # 실제 이메일로 변경
        self.email_password = "isby lkei xqag syzx"  # 앱 비밀번호
        self.recipients = ["databizflow@gmail.com"]  # 수신자 리스트

    def send_report_email(self, subject="수내역 작업실 매물 리포트"):
        """리포트 이메일 발송"""
        try:
            # 이메일 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = ", ".join(self.recipients)
            msg['Subject'] = f"{subject} - {datetime.now().strftime('%Y-%m-%d')}"

            # 이메일 본문
            body = f"""
            안녕하세요,

            분당구 수내역 반경 500m 내 20-30㎡ 작업실 매물 리포트를 전송드립니다.

            생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            첨부파일:
            - sunae_property_report.xlsx (상세 분석 데이터)
            - property_analysis_charts.png (분석 차트)
            - sunae_property_map.html (매물 위치 지도)

            감사합니다.
            """

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 파일 첨부
            attachments = [
                'sunae_property_report.xlsx',
                'property_analysis_charts.png',
                'sunae_property_map.html'
            ]

            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}',
                    )
                    msg.attach(part)

            # 이메일 발송
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()

            print(f"리포트 이메일 발송 완료: {datetime.now()}")

        except Exception as e:
            print(f"이메일 발송 실패: {e}")

    def run_full_analysis(self):
        """전체 분석 파이프라인 실행"""
        try:
            print(f"매물 분석 시작: {datetime.now()}")

            # 여기에 실제 크롤링 및 분석 코드 실행
            # 예: exec(open('main_analysis.py').read())

            print("매물 분석 완료")

            # 이메일 발송
            self.send_report_email()

        except Exception as e:
            print(f"분석 실행 실패: {e}")

def main():
    automation = PropertyReportAutomation()

    # 스케줄러 설정
    scheduler = BlockingScheduler()

    # 매일 오전 9시 실행
    scheduler.add_job(
        automation.run_full_analysis,
        'cron',
        hour=9,
        minute=0,
        id='daily_report'
    )

    # 주간 리포트 (매주 월요일 오전 10시)
    scheduler.add_job(
        automation.run_full_analysis,
        'cron',
        day_of_week='mon',
        hour=10,
        minute=0,
        id='weekly_report'
    )

    print("스케줄러 시작 - 작업 예약됨")
    print("일일 리포트: 매일 09:00")
    print("주간 리포트: 매주 월요일 10:00")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("스케줄러 종료")
        scheduler.shutdown()

if __name__ == "__main__":
    # 테스트 실행 (실제 스케줄러는 주석 처리)
    automation = PropertyReportAutomation()
    print("테스트: 리포트 생성 및 이메일 발송")
    # automation.run_full_analysis()  # 실제 실행시 주석 해제

    # 스케줄러 실행 (실제 운영시 주석 해제)
    # main()
