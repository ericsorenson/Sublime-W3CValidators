import sublime
import sublime_plugin
import urllib
import json

class AbstractValidator(sublime_plugin.TextCommand):

  markupValidatorUrl = 'http://validator.w3.org/check'
  cssValidatorUrl = 'http://jigsaw.w3.org/css-validator/validator'

  def validate(self, format, validatorUrl):
    region = sublime.Region(0, self.view.size())
    fileContents = self.view.substr(region)
    params = { 'fragment':fileContents, 'doctype': format, 'output':'json' }
    encodedParams = urllib.urlencode(params)
    output = urllib.urlopen(validatorUrl, encodedParams).read()
    results = json.loads(output)
    messageContents = ''
    if not results['messages']:
      messageContents = 'This document was successfully checked as %s!' % format
    else:
      formattedMessages = []
      formattedMessages.append('Errors found while checking this document as %s!\n\n' % format)
      for message in results['messages']:
        formattedMessages.append('Line %s: %s\n\n' % (message['lastLine'], message['message']))
      messageContents = messageContents.join(formattedMessages)
    sublime.message_dialog(messageContents)

class Validatehtml5Command(AbstractValidator):

  def run(self, edit):
    self.validate('HTML5', self.markupValidatorUrl)

class Validatehtml4strictCommand(AbstractValidator):

  def run(self, edit):
    self.validate('HTML 4.01 Strict', self.markupValidatorUrl)

class Validatehtml4transitionalCommand(AbstractValidator):

  def run(self, edit):
    self.validate('HTML 4.01 Transitional', self.markupValidatorUrl)

class Validatesvg11Command(AbstractValidator):

  def run(self, edit):
    self.validate('SVG 1.1', self.markupValidatorUrl)

class Validatesvg11tinyCommand(AbstractValidator):

  def run(self, edit):
    self.validate('SVG 1.1 Tiny', self.markupValidatorUrl)

class Validatesvg11basicCommand(AbstractValidator):

  def run(self, edit):
    self.validate('SVG 1.1 Basic', self.markupValidatorUrl)

# TODO: CSS Validation
class Validatecss3Command(AbstractValidator):

  def run(self, edit):
    self.validate('css3', self.cssValidatorUrl)
