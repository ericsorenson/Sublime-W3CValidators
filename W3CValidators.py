# -*- coding: utf-8 -*-
import sys
import json
import sublime
import sublime_plugin

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

    def validate(self, format, validator_url):
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

        message_contents = ''
        if not results['messages']:
            message_contents = 'This document was successfully checked as %s!' % format
        else:
            formatted_messages = []
            formatted_messages.append(
                'Errors found while checking this document as %s!\n\n' % format)
            for message in results['messages']:
                formatted_messages.append(
                    'Line %s: %s\n\n' % (message['lastLine'], message['message']))
            message_contents = message_contents.join(formatted_messages)
        sublime.message_dialog(message_contents)


class Validatehtml5Command(AbstractValidator):
    def run(self, edit):
        self.validate('HTML5', self.markup_validator_url)


class Validatehtml4strictCommand(AbstractValidator):
    def run(self, edit):
        self.validate('HTML 4.01 Strict', self.markup_validator_url)


class Validatehtml4transitionalCommand(AbstractValidator):
    def run(self, edit):
        self.validate('HTML 4.01 Transitional', self.markup_validator_url)


class Validatesvg11Command(AbstractValidator):
    def run(self, edit):
        self.validate('SVG 1.1', self.markup_validator_url)


class Validatesvg11tinyCommand(AbstractValidator):
    def run(self, edit):
        self.validate('SVG 1.1 Tiny', self.markup_validator_url)


class Validatesvg11basicCommand(AbstractValidator):
    def run(self, edit):
        self.validate('SVG 1.1 Basic', self.markup_validator_url)


# TODO: CSS Validation
class Validatecss3Command(AbstractValidator):
    def run(self, edit):
        self.validate('css3', self.css_validator_url)
