import json
import re

import certifi
from bs4 import BeautifulSoup

from app.config import settings
from app.services.safer.controller import check_company
from app.services.tafs.customHttpAdapter import get_legacy_session
from app.services.tafs.schemas import TafDebtor


def select_best_debtor(debtor_list):
    best_debtor = None
    for debtor in debtor_list:
        if not best_debtor:
            best_debtor = debtor
        elif debtor.debtor_buy_status and 'Denied' not in debtor.debtor_buy_status:
            best_debtor = debtor
    return best_debtor


class TafsController:
    view_state = ''
    event_validation = ''
    view_state_gen = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Origin': '',
        'Referer': '',
        'Connection': 'keep-alive',
        'Cookie': '_gcl_au=1.1.1460970554.1697047867; _ga_C3LJ1WTQGN=GS1.1.1697047867.1.1.1697047926.1.0.0; _ga=GA1.2.476851898.1697047868; calltrk_referrer=direct; calltrk_landing=https%3A//www.tafs.com/; calltrk_session_id=6d8da3de-cbfc-4e60-bacf-7e9a56fcdd79; _fbp=fb.1.1697047868854.1068798243; _tt_enable_cookie=1; _ttp=WxyBz6vqvaA6X1lwaCL1_9WLX8K; _ga=GA1.3.476851898.1697047868; _ga_BCS4962E1W=GS1.2.1699367377.3.0.1699367377.0.0.0; _ga_RZ3938RG8T=GS1.3.1699367377.3.0.1699367377.0.0.0; _hjSessionUser_529778=eyJpZCI6ImEwOWFkODdiLTI5ODQtNTRmZS1hNzNlLWMxODVjYzNiNjJlYiIsImNyZWF0ZWQiOjE2OTcwNDc5Mjc5NzIsImV4aXN0aW5nIjp0cnVlfQ==; _ga_JPLQE4Q4FF=GS1.2.1699367376.3.1.1699367378.58.0.0; ASP.NET_SessionId=0mtpcd1bx12ewhnnvhfsgs43; b100=422154182.1.1930171552.2162984448; visid_incap_3014249=KBB+Cy4DQPaGTaQhs1iJgJA9SWUAAAAAQUIPAAAAAADHTYC5eUAUfilcEpIGX3JU; incap_ses_993_3014249=zC+KAHmKW3xwdRzkVtnHDZA9SWUAAAAAYwCJAyJ1RgMUSbOq0WxZ3w==; _gid=GA1.2.1452122556.1699298708; _gid=GA1.3.1452122556.1699298708; _gat_UA-133574691-1=1; incap_ses_8221_3014249=FoIjPM1Ginm015pbzNwWctBJSmUAAAAAIAmZveVG7WN3Y00dlF1Imw==; _gat=1; _dc_gtm_UA-80391233-1=1; _uetsid=321734507cda11ee908c0749117bf477; _uetvid=b05d5340686111eebedd21960c3a4c23; _hjIncludedInSessionSample_529778=0; _hjSession_529778=eyJpZCI6ImYyOWVlMjdkLWUwOTctNDJhMS1hMTQ2LWQzYTdmZDY5ZTEyNCIsImNyZWF0ZWQiOjE2OTkzNjczNzgyMzIsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; _hjAbsoluteSessionInProgress=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }
    payload = {
        'ctl00$db_script_manager': 'ctl00$db_script_manager|ctl00$cnt_main$btn_filter_debtor_list',
        'db_script_manager_TSM': ';;System.Web.Extensions Version=4.0.0.0 Culture=neutral PublicKeyToken=31bf3856ad364e35:en-US:5be88906-8317-4b03-ad50-a53dfdcc9d91:ea597d4b:b25378d2;Telerik.Web.UI:en-US:aa5505de-2c5c-46bb-a9da-169bdb14ed36:16e4e7cd:f7645509:ed16cbdc:ddbfcb67:88144a7a:2003d0b8:24ee1bba:c128760b:1e771326:f46195d3:33715776:aa288e2d:b092aa46:58366029:258f1c72',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': '123D9EF8',
        '__EVENTVALIDATION': event_validation,
        'ctl00$client_notice$hdn_notice_id': '',
        'ctl00$client_notice$hdn_audit_type': '',
        'ctl00$header$invoice_search$txt_search': '',
        'ctl00_header_invoice_search_lv_invoices_ClientState': '',
        'ctl00_header_lv_notifications_ClientState': '',
        'ctl00$header$cb_owner': '',
        'ctl00_header_cb_owner_ClientState': '',
        'ctl00$header$cb_refactor_client': '',
        'ctl00_header_cb_refactor_client_ClientState': '',
        'ctl00$cnt_main$hdn_account_id': '',
        'ctl00$cnt_main$txt_filter_text': '',
        'ctl00$cnt_main$grd_debtors_list$ctl00$ctl03$ctl01$PageSizeComboBox': '50',
        'ctl00_cnt_main_grd_debtors_list_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState': '',
        'ctl00_cnt_main_grd_debtors_list_ClientState': '',
        'ctl00$cnt_main$debtor_status$hdn_account_id': '',
        'ctl00$cnt_main$credit_requests$hdn_account_id': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_name': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_address': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_city': '',
        'ctl00$cnt_main$credit_requests$ddl_debtor_state': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_postal_code': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_phone': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_fax': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_mc_number': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_contact_name': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_email_address': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_credit_limit': '',
        'ctl00$cnt_main$credit_requests$txt_debtor_comments': '',
        'ctl00$cnt_main$credit_requests$txt_requestor_name': '',
        'ctl00$cnt_main$credit_requests$txt_requestor_phone': '',
        'ctl00$cnt_main$credit_requests$txt_additional_credit_requested': '',
        'ctl00$cnt_main$credit_requests$txt_additional_credit_requested_comments': '',
        'ctl00$cnt_main$credit_requests$txt_ac_requestor_name': '',
        'ctl00$cnt_main$credit_requests$txt_ac_requestor_phone': '',
        '__ASYNCPOST': True,
        'ctl00$cnt_main$btn_filter_debtor_list.x': '0',
        'ctl00$cnt_main$btn_filter_debtor_list.y': '0',
        'RadAJAXControlID': 'ctl00_master_ajax_manager'
    }

    def __init__(self):
        self.session = get_legacy_session()  # Maintain cookies automatically
        self.url_base = settings.tafs_portal_url
        self.url_login = f'{self.url_base}/login.aspx'
        self.url_debtor = f'{self.url_base}/debtor_search.aspx'

        # Internal state for ASP.NET tokens
        self.view_state = ''
        self.event_validation = ''
        self.view_state_gen = ''
        # Standard Headers (Cookies removed; handled by self.session)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'X-MicrosoftAjax': 'Delta=true',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Connection': 'keep-alive'
        }

    def _update_asp_state(self, html_content):
        """Extracts hidden ASP.NET tokens from the page."""
        soup = BeautifulSoup(html_content, "html.parser")
        vs = soup.find(attrs={"id": "__VIEWSTATE"})
        vsg = soup.find(attrs={"id": "__VIEWSTATEGENERATOR"})
        ev = soup.find(attrs={"id": "__EVENTVALIDATION"})

        if vs: self.view_state = vs.get('value', '')
        if vsg: self.view_state_gen = vsg.get('value', '')
        if ev: self.event_validation = ev.get('value', '')

    def is_authenticated(self):
        """Checks if the session is alive without full re-login."""
        try:
            response = self.session.get(self.url_debtor, headers=self.headers, timeout=10)
            if 'timeout|' in response.text or 'login.aspx' in response.url:
                return False
            return response.status_code == 200
        except Exception:
            return False

    def login(self):
        """Handshake to establish the session."""
        # 1. Initial GET to grab tokens
        res = self.session.get(self.url_login, headers=self.headers)
        self._update_asp_state(res.content)

        payload = {
            'txt_username': settings.tafs_portal_username,
            'txt_password': settings.tafs_portal_password,
            '__EVENTTARGET': 'btn_login',
            '__VIEWSTATE': self.view_state,
            '__VIEWSTATEGENERATOR': self.view_state_gen,
            '__EVENTVALIDATION': self.event_validation,
            '__ASYNCPOST': True,
            'RadAJAXControlID': 'master_ajax_manager'
        }

        headers = self.headers.copy()
        headers.update({'Referer': self.url_login, 'Origin': self.url_base})

        response = self.session.post(self.url_login, headers=headers, data=payload)
        return 'dashboard.aspx' in response.text or self.is_authenticated()

    def get_view(self, url):
        self.session.headers.update({
            'Sec-Fetch-User': '?1'
        })
        response = self.session.post(url, verify=certifi.where(), allow_redirects=True)
        # Check if we got redirected to login
        if 'login.aspx' in response.url or response.status_code != 200:
            print("⚠ Session expired, re-authenticating...")
            if not self.login():
                raise Exception("Failed to re-authenticate with TAFS portal")
            # Try again after login
            response = self.session.get(url, verify=certifi.where(), allow_redirects=True)

        self._update_asp_state(response.content)

    def search_broker(self, query: str):
        if query.isnumeric():
            filter_text = query
        else:
            filter_text = f'%{query}%'

        company = check_company(query_param='MC_MX', query_string=filter_text)
        broker_info = company.model_dump(by_alias=True)
        broker_info.update({'tafs_debtor': None})

        if not company.founded:
            return broker_info

        self.get_view(self.url_debtor)
        req_payload = self.payload.copy()
        req_payload['__VIEWSTATEGENERATOR'] = self.view_state_gen
        req_payload['__VIEWSTATE'] = self.view_state
        req_payload['__EVENTVALIDATION'] = self.event_validation
        req_payload['ctl00$cnt_main$txt_filter_text'] = filter_text

        local_headers = self.headers.copy()
        local_headers['Origin'] = self.url_base
        local_headers['Referer'] = self.url_base + '/batches.aspx'
        local_headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        local_headers['Sec-Fetch-User'] = '?1'
        local_headers['Sec-Fetch-Dest'] = 'document'
        local_headers['Upgrade-Insecure-Requests'] = '1'

        response = self.session.post(self.url_debtor, headers=local_headers, verify=certifi.where(), data=req_payload)
        soup = BeautifulSoup(response.content, "html.parser")
        _clientKeyValues = soup(text=re.compile('_clientKeyValues'))
        no_records = soup.find(attrs={"class": "rgNoRecords"})
        if no_records is not None:
            broker_info['tafs_debtor'] = TafDebtor.model_validate({'debtor_msg': "No records found in TAFS for this MC number"})
            return broker_info
        else:
            if _clientKeyValues:
                word_list = re.split(r"_clientKeyValues\"\:|\,\"_controlToFocus", _clientKeyValues[0],
                                     flags=re.IGNORECASE)
                debtors = json.loads(word_list[1])
                debtor_list = []
                if debtors:
                    for key, value in debtors.items():
                        debtor_list.append(self.load_debtor(value['id']))
                broker_info['tafs_debtor'] = select_best_debtor(debtor_list)
                return broker_info
            return None

    def load_debtor(self, account_id):
        req_payload = self.payload.copy()
        req_payload['ctl00$db_script_manager'] = 'ctl00$db_script_manager|ctl00$cnt_main$btn_load_debtor'
        req_payload['__VIEWSTATEGENERATOR'] = self.view_state_gen
        req_payload['__VIEWSTATE'] = self.view_state,
        req_payload['__EVENTVALIDATION'] = self.event_validation,
        req_payload['ctl00$cnt_main$txt_filter_text'] = ''
        req_payload['ctl00$cnt_main$hdn_account_id'] = account_id
        req_payload['ctl00$cnt_main$btn_load_debtor.x'] = '0'
        req_payload['ctl00$cnt_main$btn_load_debtor.y'] = '0'

        self.headers['Origin'] = self.url_base
        self.headers['Referer'] = self.url_debtor
        local_headers = self.headers.copy()

        response = self.session.post(self.url_debtor, headers=local_headers, data=req_payload, allow_redirects=True)
        if response:
            soup2 = BeautifulSoup(response.content, "html.parser")
            if not soup2:
                return TafDebtor.model_validate({'debtor_msg': "No records found in TAFS for this MC number"})
            if soup2:
                debtor_buy_status = soup2.find(attrs={"id": "cnt_main_debtor_status_lbl_buy_status"})
                debtor_rating = soup2.find(attrs={"id": "cnt_main_debtor_status_lbl_rating"})
                debtor_credit_limit = soup2.find(attrs={"id": "cnt_main_debtor_status_lbl_credit_limit"})
                mc_number = soup2.find(attrs={"id": "cnt_main_lbl_mc_number"})
                debtor_name = soup2.find(attrs={"id": "cnt_main_lbl_debtor_name"})
                main_lbl_address = soup2.find(attrs={"id": "cnt_main_lbl_address"})
                debtor_msg = soup2.find(attrs={"id": "cnt_main_debtor_status_lbl_debtor_msg"})

                modal_body = soup2.find(attrs={"class": "modal-body"})
                tafs_html = ''
                if modal_body:
                    children = modal_body.find("div", recursive=False).findChildren("div", recursive=False)
                    if children and len(children) >= 2:
                        children.pop(2)
                        children[0]['class'] = 'col-lg-4'
                        children[1]['class'] = 'col-lg-4'
                        tafs_html = children[0].encode() + children[1].encode()
                if mc_number:
                    return TafDebtor.model_validate({
                        'account_id': account_id,
                        'mc_number': mc_number.text,
                        'debtor_name': debtor_name.text,
                        'debtor_buy_status': debtor_buy_status.text,
                        'is_denied': 'Denied' in debtor_buy_status.text,
                        'debtor_rating': debtor_rating.text,
                        'debtor_credit_limit': debtor_credit_limit.text,
                        'debtor_address': main_lbl_address.text,
                        'debtor_msg': debtor_msg.text,
                        'tafs_html': tafs_html,
                    })
        return None

