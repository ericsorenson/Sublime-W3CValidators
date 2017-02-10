# -*- coding: utf-8 -*-
import sys
import json
import sublime
import sublime_plugin
import requests

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib import urlopen
    from urllib import urlencode


class AbstractValidator(sublime_plugin.TextCommand):
    markup_validator_url = 'http://validator.w3.org/check'
    css_validator_url = 'http://jigsaw.w3.org/css-validator/validator'

    def validate(self, edit, format, validator_url):
        region = sublime.Region(0, self.view.size())
        file_contents = self.view.substr(region)
        params = {'fragment': file_contents, 'doctype': format, 'output': 'json'}
        encoded_params = urlencode(params)

        if PY3:
            encoded_params = encoded_params.encode('utf-8')
        output = urlopen(validator_url, encoded_params).read()

        if PY3:
            output = output.decode('utf-8')
        results = json.loads(output)

        if not results['messages']:
            sublime.message_dialog('This document was successfully checked as %s!' % format)
        else:
            message_contents = ''
            formatted_messages = []
            formatted_messages.append(
                'Errors found while checking this document as %s:\n\n' % format)
            for message in results['messages']:
                formatted_messages.append(
                    'Line %s: %s\n\n' % (message['lastLine'], message['message']))
            message_contents = message_contents.join(formatted_messages)
            output = sublime.active_window().new_file()
            output.set_scratch(True)
            output.set_name('W3C Validation Errors')
            output.insert(edit, 0, message_contents)


class Validatehtml5Command(AbstractValidator):
    def run(self, edit):

        # This is no longer responding with valid JSON
        # self.validate(edit, 'HTML5', self.markup_validator_url)

        # Temporary fix
        # TODO: refactor this and DRY it up
        region = sublime.Region(0, self.view.size())
        file_contents = self.view.substr(region).encode('utf-8').strip()

        results = requests.post('https://html5.validator.nu?out=json', data=file_contents, headers={'Content-Type': 'text/html; charset=UTF-8'}).json()

        if not results['messages']:
            sublime.message_dialog('This document was successfully checked as HTML5')
        else:
            message_contents = ''
            formatted_messages = []
            formatted_messages.append(
                'Errors found while checking this document as HTML5:\n\n')
            for message in results['messages']:
                formatted_messages.append(
                    'Line %s: %s\n\n' % (message['lastLine'], message['message']))
            message_contents = message_contents.join(formatted_messages)
            output = sublime.active_window().new_file()
            output.set_scratch(True)
            output.set_name('W3C Validation Errors')
            output.insert(edit, 0, message_contents)


class Validatehtml4strictCommand(AbstractValidator):
    def run(self, edit):
        self.validate(edit, 'HTML 4.01 Strict', self.markup_validator_url)


class Validatehtml4transitionalCommand(AbstractValidator):
    def run(self, edit):
        self.validate(edit, 'HTML 4.01 Transitional', self.markup_validator_url)


class Validatesvg11Command(AbstractValidator):
    def run(self, edit):
        self.validate(edit, 'SVG 1.1', self.markup_validator_url)


class Validatesvg11tinyCommand(AbstractValidator):
    def run(self, edit):
        self.validate(edit, 'SVG 1.1 Tiny', self.markup_validator_url)


class Validatesvg11basicCommand(AbstractValidator):
    def run(self, edit):
        self.validate(edit, 'SVG 1.1 Basic', self.markup_validator_url)


class Validatecss3Command(AbstractValidator):
    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        file_contents = self.view.substr(region).encode('utf-8').strip()

        params = dict()
        params['text']  = file_contents
        params['output'] = "application/json"
        params['profile']= "css3"
        params['lang']= "en"

        results = requests.get(self.css_validator_url, params=params).json()

        if results['cssvalidation']["result"]["errorcount"] == 0:
            sublime.message_dialog('This document was successfully checked as CSS3')
        else:
            message_contents = ''
            formatted_messages = []
            formatted_messages.append(
                'Errors found while checking this document as CSS3:\n\n')
            for error in results["cssvalidation"]["errors"]:
                formatted_messages.append(
                    'Line %s: %s\n\n' % (error['line'], error['message']))
            message_contents = message_contents.join(formatted_messages)
            output = sublime.active_window().new_file()
            output.set_scratch(True)
            output.set_name('W3C Validation Errors')
            output.insert(edit, 0, message_contents)
