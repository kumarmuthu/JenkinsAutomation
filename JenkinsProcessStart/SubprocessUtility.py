import subprocess
from threading import Thread
import os
import logging


__version__ = '2022.07.17.01'
__author__ = 'Muthukumar Subramanian'


class SubprocessUtility:
    """
    Subprocess utility
    """
    def __init__(self, log_obj):
        self.log_obj = log_obj

    def execute_subprocess_cmd(self, exec_cmd, cwd=None):
        """
        ..codeauthor:: Muthukumar Subramanian
        :param exec_cmd: executable cmd
        :param cwd: provide the current working directory
        :return:
        """
        ret_var = False
        # Subprocess logger object
        # sys.stdout = LogPipe(logging.INFO, logger_obj=self.log_obj) # killing all the parent threads
        # sys.stderr = LogPipe(logging.INFO, logger_obj=self.log_obj)
        std_out_obj = LogPipe(logging.INFO, logger_obj=self.log_obj)
        std_err_obj = LogPipe(logging.INFO, logger_obj=self.log_obj)

        try:
            subprocess.check_call(exec_cmd, stdout=std_out_obj, stderr=std_err_obj,
                                  cwd=cwd)
            return_output = subprocess.check_output(exec_cmd, stderr=std_err_obj)
        except Exception as SubProcessErr:
            self.log_obj.error("Error: Observed error while executing the Subprocess command! ,"
                               "Exception as: {}".format(SubProcessErr))
        else:
            ret_var = True
            self.log_obj.debug("Subprocess output: {}".format(return_output.decode("utf-8")))
        finally:
            std_out_obj.close()
            std_err_obj.close()
        return ret_var

    def subprocess_to_run_cmd_prompt(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        ipconfig example
        :return:
        """
        execute_cmd = ['cmd.exe', "/c", "ipconfig"]
        ret_code = self.execute_subprocess_cmd(exec_cmd=execute_cmd)
        return ret_code

    def subprocess_to_run_python_script(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        :return:
        """
        execute_cmd = ['python', "F:\\Python\\loc.py"]
        ret_code = self.execute_subprocess_cmd(exec_cmd=execute_cmd, cwd="F:\\Python")
        return ret_code


class LogPipe(Thread):
    """
    Subprocess logging
    """

    def __init__(self, level, logger_obj):
        """
        Setup the object with a logger and a loglevel and start the thread
        """
        Thread.__init__(self)
        self.daemon = True
        self.level = level
        self.logger_obj = logger_obj
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """
        Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """
        ..codeauthor:: Muthukumar Subramanian
        Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            self.logger_obj.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """
        Close the write end of the pipe.
        """
        os.close(self.fdWrite)
