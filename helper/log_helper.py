import logging
import os
import errno
import datetime
import config as c


def mkdir(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise


class LogHelper:
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = LogHelper()
        return cls.__instance

    def __init__(self):
        self.log = None

        self.os_path = os.path.dirname(os.path.realpath(__file__)).replace('/core', '').replace('\\core', '')
        # os_path = os.path.dirname(os.path.realpath(__file__)) # 20200103 Log 폴더 경로 변경
        self.log_folder_nm = 'Log'
        self.is_log = c.LOG_CONFIG['is_log']
        self.is_debug = c.LOG_CONFIG['is_debug']
        self.is_info = c.LOG_CONFIG['is_info']
        self.is_error = c.LOG_CONFIG['is_error']

        self.today = None

        self.dir_check()

    def dir_check(self):
        if self.is_log:

            now_date = datetime.datetime.now().strftime('%Y%m%d')

            mkdir('{0}/{1}'.format(self.os_path, self.log_folder_nm))
            mkdir(
                '{0}/{1}/{2}'.format(self.os_path, self.log_folder_nm, now_date))
            '''
            log.basicConfig(filename='{0}/{1}/{2}/log.txt'
                            .format(self.os_path, self.log_folder_nm, datetime.datetime.now().strftime('%Y%m%d')),
                            level=log.DEBUG)
            '''
            if self.log is None or self.today != now_date:
                file_handler = logging.FileHandler('{0}/{1}/{2}/log.txt'.format(self.os_path,
                                                                                self.log_folder_nm, now_date), 'a')

                self.log = logging.getLogger()
                for handler in self.log.handlers[:]:
                    if isinstance(handler, logging.FileHandler):
                        self.log.removeHandler(handler)

                self.log.setLevel(logging.DEBUG)
                #fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fm = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
                file_handler.setFormatter(fm)

                self.log.addHandler(file_handler)

                self.today = now_date

    def d(self, msg):
        print(msg)
        if self.is_log and self.is_debug:
            self.dir_check()
            self.log.debug('{0} [{1}]'.format(msg, datetime.datetime.now().strftime('%H:%M:%S')))

    def i(self, msg):
        print(msg)
        if self.is_log and self.is_info:
            self.dir_check()
            self.log.info('{0} [{1}]'.format(msg, datetime.datetime.now().strftime('%H:%M:%S')))

    def e(self, msg, file_name=None, func_name=None):
        print(msg)
        if self.is_log and self.is_error:
            self.dir_check()
            self.log.error('{0} [{1}]'.format(msg, datetime.datetime.now().strftime('%H:%M:%S')))
            if file_name is not None:
                self.log.error('  * file_name: {0}'.format(file_name))
            if func_name is not None:
                self.log.error('  * func_name: {0}'.format(func_name))
