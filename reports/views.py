from django.views.generic.base import TemplateView
import firebirdsql
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from datetime import datetime


class GeneralReportView(TemplateView):
    template_name = "reports/report_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # GET CONNECT TO DATABASE
        server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 3050)
                )
        server.start()
        print(server)

        conn = firebirdsql.connect(
                host='127.0.0.1',
                database='C:/MasterD/MDGarant/PentadaDB/Db/MDGARANT.FDB',
                port=3050,
                user='SYSDBA',
                password='masterkey',
                charset='UTF8'
        )

        if self.request.user.company_code != '36701373':
            edrpou = self.request.user.company_code
        else:
            edrpou = ''

        print('EDRPOU: ', edrpou)

        currentYear = datetime.now().year
        pd.set_option('display.float_format', lambda x: '%.2f' % x)

        # GET DATA FROM DATABASE
        df = pd.read_sql('''
                    SELECT
                        GL_NUM,
                        GL_DATE_CR,
                        DATE_END,
                        GL_CL_CNT,
                        GL_CL_NAME,
                        GL_CL_OKPO,
                        GL_CAR_CNT,
                        GL_CAR_NAME,
                        GL_CAR_ADR,
                        GL_TRANS_NUM,
                        GL_DR_NAME,
                        GL_PEREG_NUM,
                        GL_LIST_PROC,
                        GL_CUS_CODE_IN,
                        GL_CUS_IN_DATE,
                        GL_CUS_CODE_OUT,
                        GL_CUS_OUT_DATE,
                        GL_PR,
                        GL_CCD_07_01,
                        GL_CCD_07_02,
                        GL_CCD_07_03,
                        GL_CCD_DATE,
                        GG_33_01,
                        GG_31_01,
                        GG_35_01,
                        GL_SUMMA,
                        GL_DATE_EXP,
                        DATE_CREATE,
                        EXTRACT(MONTH FROM GL_DATE_CR) AS GL_MONTH,
                        EXTRACT(YEAR FROM GL_DATE_CR) AS GL_YEAR
                    FROM GARANT_LIST
                    INNER JOIN GARANT_LIST_GOODS
                    ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                    WHERE GL_CL_OKPO LIKE '%{}' AND GL_DATE_CR>='01.01.{} 00:00' AND GL_PR!=2
                    ORDER BY GL_NUM DESC;
                    '''.format(edrpou, currentYear), conn)

        df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['DATE_END'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['GL_CUS_IN_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['GL_CUS_OUT_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)
        df['DATE_CREATE'].replace({'30.12.1899 00:00': ''}, inplace=True)

        df = df.groupby('GL_NUM').agg({
            'GL_NUM': 'first',
            'GL_DATE_CR': 'first',
            'DATE_END': 'first',
            'GL_CL_CNT': 'first',
            'GL_CL_NAME': 'first',
            'GL_CL_OKPO': 'first',
            'GL_CAR_CNT': 'first',
            'GL_CAR_NAME': 'first',
            'GL_CAR_ADR': 'first',
            'GL_TRANS_NUM': 'first',
            'GL_DR_NAME': 'first',
            'GL_PEREG_NUM': 'first',
            'GL_LIST_PROC': 'first',
            'GL_CUS_CODE_IN': 'first',
            'GL_CUS_IN_DATE': 'first',
            'GL_CUS_CODE_OUT': 'first',
            'GL_CUS_OUT_DATE': 'first',
            'GL_PR': 'first',
            'GL_CCD_07_01': 'first',
            'GL_CCD_07_02': 'first',
            'GL_CCD_07_03': 'first',
            'GL_CCD_DATE': 'first',
            'GG_33_01': ', '.join,
            'GG_31_01': '; '.join,
            'GG_35_01': sum,
            'GL_SUMMA': 'first',
            'GL_DATE_EXP': 'first',
            'DATE_CREATE': 'first',
            'GL_MONTH': 'first',
            'GL_YEAR': 'first',
        })

        df.fillna("-", inplace=True)

        context['df'] = df.rename(
            columns={
                'GL_NUM': 'Номер',
                'GL_DATE_CR': 'Дата', #1
                'DATE_END': 'Вивільнення',
                'GL_CL_CNT': 'Країна клієнта', #3
                'GL_CL_NAME': 'Клієнт', #4
                'GL_CL_OKPO': 'ЄДРПОУ', #5
                'GL_CAR_CNT': 'Країна перевізника', #6
                'GL_CAR_NAME': 'Перевізник', #7
                'GL_CAR_ADR': 'Адреса перевізника',
                'GL_TRANS_NUM': 'Номер Т/З',
                'GL_DR_NAME': 'Водій',
                'GL_PEREG_NUM': 'Процедура', #11
                'GL_LIST_PROC': 'Режим', #12
                'GL_CUS_CODE_IN': 'Митниця відправлення', #13
                'GL_CUS_IN_DATE': 'Початок переміщення',
                'GL_CUS_CODE_OUT': 'Митниця призначення', #15
                'GL_CUS_OUT_DATE': 'Завершення переміщення',
                'GL_PR': 'Статус',
                'GL_CCD_07_01': 'Підрозділ МД',
                'GL_CCD_07_02': 'Рік МД',
                'GL_CCD_07_03': 'Номер МД',
                'GL_CCD_DATE': 'Дата МД',
                'GG_33_01': 'УКТЗЕД', #22
                'GG_31_01': 'Товар',
                'GG_35_01': 'Вага, кг',
                'GL_SUMMA': 'Сума гарантії',
                'GL_DATE_EXP': 'Термін дії',
                'DATE_CREATE': 'Дата',
                'GL_MONTH': 'Місяць',
                'GL_YEAR': 'Рік'
            }, inplace=False)

        conn.close()
        server.stop()

        return context