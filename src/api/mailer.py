import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.qq.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')

ALIYUN_SMS_ACCESS_KEY_ID = os.getenv('ALIYUN_SMS_ACCESS_KEY_ID', '')
ALIYUN_SMS_ACCESS_KEY_SECRET = os.getenv('ALIYUN_SMS_ACCESS_KEY_SECRET', '')
ALIYUN_SMS_SIGN_NAME = os.getenv('ALIYUN_SMS_SIGN_NAME', 'WiseDrama')
ALIYUN_SMS_TEMPLATE_CODE = os.getenv('ALIYUN_SMS_TEMPLATE_CODE', '')
ALIYUN_SMS_ENDPOINT = os.getenv('ALIYUN_SMS_ENDPOINT', 'dysmsapi.aliyuncs.com')

_sms_client = None


def _get_sms_client():
    global _sms_client
    if _sms_client is not None:
        return _sms_client
    if not ALIYUN_SMS_ACCESS_KEY_ID or not ALIYUN_SMS_ACCESS_KEY_SECRET:
        return None
    try:
        from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
        from alibabacloud_tea_openapi import models as open_api_models
        config = open_api_models.Config(
            access_key_id=ALIYUN_SMS_ACCESS_KEY_ID,
            access_key_secret=ALIYUN_SMS_ACCESS_KEY_SECRET,
        )
        config.endpoint = ALIYUN_SMS_ENDPOINT
        _sms_client = DysmsapiClient(config)
        return _sms_client
    except ImportError:
        print('[SMS] alibabacloud SDK not installed, falling back to mock')
        return None
    except Exception as e:
        print(f'[SMS] Failed to init Aliyun client: {e}')
        return None


def send_sms_code(phone: str, code: str) -> bool:
    client = _get_sms_client()
    if client is None or not ALIYUN_SMS_TEMPLATE_CODE:
        print(f'[SMS Mock] -> {phone} code={code}')
        return True
    try:
        from alibabacloud_dysmsapi20170525 import models as sms_models
        from alibabacloud_tea_util import models as util_models
        request = sms_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=ALIYUN_SMS_SIGN_NAME,
            template_code=ALIYUN_SMS_TEMPLATE_CODE,
            template_param=json.dumps({'code': code}),
        )
        runtime = util_models.RuntimeOptions()
        response = client.send_sms_with_options(request, runtime)
        body = response.body
        if body.code == 'OK':
            print(f'[SMS] Sent to {phone}, BizId={body.biz_id}')
            return True
        else:
            print(f'[SMS] API error: Code={body.code}, Message={body.message}')
            return False
    except Exception as e:
        print(f'[SMS] Exception: {e}')
        traceback.print_exc()
        return False


def send_email_code(to_email: str, code: str) -> bool:
    if not SMTP_USER or not SMTP_PASS:
        print(f'[Email Mock] -> {to_email} code={code}')
        return True
    try:
        msg = MIMEMultipart()
        msg['From'] = f'WiseDrama <{SMTP_USER}>'
        msg['To'] = to_email
        msg['Subject'] = 'WiseDrama - Verification Code'
        body = f'Your WiseDrama verification code is: {code}\n\nValid for 5 minutes.'
        msg.attach(MIMEText(body, 'plain'))
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f'[Email] Sent to {to_email}')
        return True
    except Exception as e:
        print(f'[Email] Failed: {e}')
        return False
