# coding: utf-8

from python_terraform import *
import re
import logging

_tf_plan_exclude_action_list_re = re.compile('^[ ]*([\+\-\~])[ ]+(create|delete|modify)')
_tf_plan_diff_re = re.compile('^[ ]*([\+\-\~])[ ]+(.*)')
_tf_apply_summary_re = re.compile('^(.*Apply complete.*)')
_tf_destroy_summary_re = re.compile('^(.*Destroy complete.*)')

_convert_diff_type = {
            '+': 'add',
            '~': 'update',
            '-': 'remove'}


class TerraformWrapper():

    def __init__(self,terraform_file_path ):
        self.tf_provider = Terraform(working_dir=terraform_file_path)
        self.tf_provider.init()

    def apply(self):
        option_dict = dict()
        option_dict['auto-approve'] = IsFlagged

        return_code, stdout, stderr = self.tf_provider.apply(**option_dict)
        if not stderr:
            logging.info(stdout)
            apply_output = self._parse_apply(stdout)
            return return_code, apply_output, None
        else:
            logging.info('*****ERROR*****')
            logging.info(stderr)
            logging.info('*****OUTPUT*****')
            logging.info(stdout)
            return return_code, stdout, stderr

    def plan(self):
        return_code, stdout, stderr = self.tf_provider.plan()
        if not stderr:
            logging.info(stdout)
            plan_output = self._parse_plan(stdout)
            return return_code, plan_output, None
        else:
            logging.info('*****ERROR*****')
            logging.info(stderr)
            logging.info('*****OUTPUT*****')
            logging.info(stdout)
            return return_code, stdout, stderr

    def destroy(self):
        # WARNING FORCE DESTROY without confirmation
        option_dict = dict()
        option_dict['force'] = IsFlagged
        return_code, stdout, stderr = self.tf_provider.destroy(**option_dict)
        if not stderr:
            logging.info(stdout)
            destroy_output = self._parse_destroy(stdout)
            return return_code, destroy_output, None
        else:
            logging.info('*****ERROR*****')
            logging.info(stderr)
            logging.info('*****OUTPUT*****')
            logging.info(stdout)
            return return_code, stdout, stderr


    def _parse_plan(self, tf_output):
        output = []
        for line in tf_output.split('\n'):
            matches = _tf_plan_exclude_action_list_re.match(line)
            if (matches):
                continue
            matches = _tf_plan_diff_re.match(line)
            if (matches):
                o = '%s %s' % (_convert_diff_type[matches.group(1)], matches.group(2))
                output.append(o)
        return output

    def _parse_apply(self, tf_output):
        output = ''
        for line in tf_output.split('\n'):
            matches = _tf_apply_summary_re.match(line)
            if not matches:
                continue
            output = matches.group(1)
            break
        return output

    def _parse_destroy(self, tf_output):
        output = ''
        for line in tf_output.split('\n'):
            matches = _tf_destroy_summary_re.match(line)
            if not matches:
                continue
            output = matches.group(1)
            break
        return output