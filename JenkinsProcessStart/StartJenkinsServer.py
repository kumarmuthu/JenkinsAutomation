from threading import Thread
import threading
import time
import re
import sys
import requests
from requests.auth import HTTPBasicAuth
import json
import logging.config
import ctypes
from SubprocessUtility import SubprocessUtility



__version__ = '2022.07.17.01'
__author__ = 'Muthukumar Subramanian'


class JenkinsUrlCheck:
    """
    Jenkins job class
    """

    def __init__(self):
        self.base_login_url = 'http://localhost:8081'
        self.username = 'admin'
        self.API_token = '11abf2d2a5c6a26a75a6a69cacf9ef4d91'
        # Session because we want to maintain the cookies
        self.session = requests.Session()
        self.session.headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                            " Chrome/67.0.3396.99 Safari/537.36"
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        # self.session.headers['Content-Length'] = '43'
        self.cookies_dict = self.session.cookies.get_dict()
        self.js_id = ''
        if re.search(r'JSESSIONID.*', str(self.cookies_dict.keys())):
            self.js_id = list(self.cookies_dict.values())[0]
        self.session.headers['Cookie'] = "JSESSIONID=" + self.js_id
        self.job_url = self.base_login_url + '/job/Python_test' + '/api/json'
        self.build_url = ''

        # Logger
        self.formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')
        s1 = re.search(r'(.*).py', __file__)
        self.file_name = s1.group(1)
        logging.basicConfig(filename='%s.log' % (self.file_name),
                            format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S', filemode='w', level=logging.INFO)
        # File handler will create a file
        self.log_obj = logging.getLogger(self.file_name)
        self.file_name_with_extension = '%s.log' % (self.file_name)
        file_handler = logging.FileHandler(self.file_name_with_extension, mode='w')
        file_handler.setFormatter(self.formatter)
        logging.getLogger(self.file_name).addHandler(file_handler)

        # File handler written data will display on the console window
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(self.formatter)
        logging.getLogger(self.file_name).addHandler(screen_handler)

        self.log_obj.info("Logger object is initiated...")

    def jenkins_url_login(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        POST request for login
        :return: 
        """
        login_response = None
        try:
            login_response = self.session.post(self.base_login_url, auth=HTTPBasicAuth(self.username, self.API_token))
        except Exception as Err:
            s1 = re.search("HTTPConnectionPool.*:\s+(\W+WinError.*\w+)", str(Err))
            if s1:
                self.log_obj.error(
                    "Error: POST - Observed exception while accessing the URL, Exception: {}".format(s1.group(1)))
        else:
            if login_response.status_code == 403:
                self.log_obj.error("Error: Login is failed!, Status code: {}".format(login_response))
            elif login_response.status_code == 200:
                self.log_obj.info("Login is successful, Status code: {}".format(login_response))
                return True
            else:
                self.log_obj.error("Error: Login is failed, Status code: {}".format(login_response))
        return False


    def jenkins_url_get(self, url_check_only=None):
        """
        ..codeauthor:: Muthukumar Subramanian
        # GET request
        :return: 
        """
        try:
            ret_code_for_get = self.session.get(self.job_url, auth=HTTPBasicAuth(self.username, self.API_token))
            if ret_code_for_get.status_code == 200:
                self.log_obj.info("GET verification is passed, Status code: {}".format(ret_code_for_get))
                if url_check_only:
                    return True
                build_json = None
                total_build_numbers = 0
                build_data_from_url = []
                try:
                    build_data_from_url = json.loads(ret_code_for_get.text)
                except Exception as Err2:
                    self.log_obj.error("Error: Failed to parse json, Exception as: {}".format(Err2))

                if "lastBuild" in build_data_from_url:
                    total_builds = build_data_from_url.get("lastBuild")
                    total_build_numbers = total_builds.get("number")
                else:
                    self.log_obj.error("Error: Failed to get build!.")

                total_success = total_failure = total_missing = last_build_success = last_build_fail = 0
                if total_build_numbers >= 1:
                    for build in range(1, total_build_numbers):
                        self.build_url = self.job_url + '/' + str(build) + '/api/json'
                        print(self.build_url)
                        build_status = []
                        try:
                            response = requests.post(self.build_url, auth=HTTPBasicAuth(self.username, self.API_token),
                                                     verify=True)
                            build_status = json.loads(response.text)
                        except Exception as e:
                            total_missing = total_missing + 1

                        if 'lastSuccessfulBuild' in build_status:
                            last_build_success = build_status['lastSuccessfulBuild']['number']
                        if 'lastFailedBuild' in build_status:
                            last_build_fail = build_status['lastFailedBuild']['number']

                        # if "result" in build_status:
                        #     if build_status["result"] == "SUCCESS":
                        #         total_success = total_success + 1
                        #     if build_status["result"] == "FAILURE":
                        #         total_failure = total_failure + 1
                else:
                    self.log_obj.warning("Total build is less than 1 record!...")
                # Generate Output numbers
                self.log_obj.info(f"total builds:{total_build_numbers}")
                self.log_obj.info(f"total succeeded builds:{total_success}")
                self.log_obj.info(f"total failed builds:{total_failure}")
                self.log_obj.info(f"total skipped builds:{total_missing}")
                self.log_obj.info(f"last build success:{last_build_success}")
                self.log_obj.info(f"last build fail:{last_build_fail}")
                return True
        except Exception as Err1:
            s1 = re.search("HTTPConnectionPool.*:\s+(\W+WinError.*\w+)", str(Err1))
            if s1:
                self.log_obj.error(
                    "Error: GET - Observed exception while accessing the URL, Exception: {}".format(s1.group(1)))
        else:
            self.log_obj.error("Error: GET - verification is failed, Status code: {}".format(ret_code_for_get))
        return False

    def jenkins_process_start(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        Jenkins process start from command prompt
        :return:
        """
        jenkins_start_cmd = "java -jar jenkins.war start --httpPort=8081"
        # jenkins_start_cmd = "net start jenkins"
        # jenkins_start_cmd = ['runas', '/noprofile', '/user:Administrator', 'cmd.exe']
        # jenkins_start_cmd = "java -jar jenkins.war --ajp13Port=-1 --httpPort=8081"
        execute_cmd = ["cmd.exe", "/c", "{}".format(jenkins_start_cmd)]
        ret_code = None
        try:
            sub_process_obj = SubprocessUtility(self.log_obj)
            ret_code = sub_process_obj.execute_subprocess_cmd(exec_cmd=jenkins_start_cmd,
                                                                cwd='C:\\Program Files\\Jenkins')
        except Exception as Err:
            self.log_obj.error("Error: Observed exception - func: jenkins_process_start(),"
                               "Exception: {}".format(Err))
        self.log_obj.info("Return code: {}".format(ret_code))
        return ret_code


class ThreadWithReturnValue(Thread):
    """
    Multi-processor for Jenkins
    """
    def __init__(self, group=None, target=None, name=None, interval=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self.interval = interval
        self._return = None
        self.killed = False
        self.lock = threading.Lock()

    def start(self):
        Thread.start(self)

    def run(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        :return:
        """
        # print("RUN method")
        if self._target is not None:
            # self.lock.acquire()
            if self.interval:
                # Sleep as per the request
                time.sleep(self.interval)
                self._return = self._target(*self._args, **self._kwargs)
            else:
                self._return = self._target(*self._args, **self._kwargs)
            # self.lock.release()

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

    def get_id(self):
        if hasattr(self, 'thread_id'):
            return self._thread_id
        for thread_id, thread in threading._active.items():
            if thread is self:
                self._thread_id = thread_id
                return thread_id

    def kill(self):
        thread_id = self.get_id()
        self.killed = True
        response = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if response > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Exception in kill method")


def call_main():
    """
    Main method, program start here
    :return:
    """
    jenkins_obj = JenkinsUrlCheck()
    sub_obj = SubprocessUtility(jenkins_obj.log_obj)
    # Jenkins server status check
    get_ret_code = jenkins_obj.jenkins_url_get(url_check_only=True)
    # Creating threads
    t1 = ThreadWithReturnValue(target=jenkins_obj.jenkins_process_start, name='jenkins_process_start', interval=1)
    t2 = ThreadWithReturnValue(target=jenkins_obj.jenkins_url_get, name='jenkins_url_get_only', args=[True],
                               interval=30)
    t3 = ThreadWithReturnValue(target=jenkins_obj.jenkins_url_get, name='jenkins_url_get', interval=1)

    if not get_ret_code:
        jenkins_obj.log_obj.info("Jenkins server is down state... Brink up the server...")
        # t1.setDaemon(False)
        # t2.setDaemon(False)
        t1.start()
        t2.start()
        # t1_thread_ret_code = t1.join()
        # jenkins_obj.log_obj.info("Jenkins.jenkins_process_start(), return code: {}".format(t1_thread_ret_code))
        t2_thread_ret_code = t2.join()
        jenkins_obj.log_obj.info("Jenkins.jenkins_url_login(), return code: {}".format(t2_thread_ret_code))
        if t2_thread_ret_code:
            jenkins_obj.log_obj.info("Jenkins server is up, checking the localhost current status...")
            jenkins_obj.log_obj.info("Jenkins server is running in-progress...")
            # Sign-in/POST
            login_ret_code = jenkins_obj.jenkins_url_login()
            t3.start()
            t3_thread_ret_code = t3.join()
            jenkins_obj.log_obj.info("Jenkins.jenkins_url_get(), return code: {}".format(t3_thread_ret_code))
            if t3_thread_ret_code:
                jenkins_obj.log_obj.info("PASS: Successfully started the Jenkins process "
                                         "and collected record's details...")
            else:
                jenkins_obj.log_obj.error("Error: Observed error after the Jenkins server login!.")
                jenkins_obj.log_obj.error("Error: Failed while collecting the Jenkins job details!.")
        else:
            jenkins_obj.log_obj.error("Error: Unable to start the Jenkins process!...")
    else:
        jenkins_obj.log_obj.info("Jenkins is already running in-progress!.")

    # File write from currently in-progress file handler
    try:
        with open(jenkins_obj.file_name_with_extension, "r") as file:
            get_all_lines = file.readlines()
        # write on new file
        s2 = re.search(r'(.*)(.log)', jenkins_obj.file_name_with_extension)
        new_file_name = s2.group(1) + '_final_log_file' + s2.group(2)
        with open(new_file_name, "w") as file:
            file.write(''.join(i for i in get_all_lines))
    except Exception as FileHandlerError:
        jenkins_obj.log_obj.error("Observed exception while write a log file!, Exception: {}".format(FileHandlerError))
    else:
        jenkins_obj.log_obj.info("Successfully created/copied the log file")

    # TODO
    # slave machine up
    # java -jar agent.jar -jnlpUrl http://localhost:8081/computer/Slave%5Fmachine/jenkins-agent.jnlp -workDir "F:\Python"
    # java -jar agent.jar -jnlpUrl http://localhost:8081/computer/SLAVE/jenkins-agent.jnlp
    # -secret ecdfea7b31cbce0a1c269cd9e07fcf748adda67ee39b27561c4cab2508082153 -workDir "F:\Python"
    # ret_slave_ma = sub_obj.execute_subprocess_cmd(
    #     "javaws http://localhost:8081/computer/Slave%5Fmachine/jenkins-agent.jnlp",
    #     cwd='C:\\Program Files\\Jenkins')


if __name__ == '__main__':
    call_main()
