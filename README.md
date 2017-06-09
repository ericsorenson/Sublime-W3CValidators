Sublime-W3CValidators
=====================

## About

This is a simplified markup validator package for the Sublime Text editor that uses the W3C validator web service located at [http://validator.w3.org](http://validator.w3.org).

Unlike similar packages, curl is not required!

## Installation

Via the [Sublime Package Manager](http://wbond.net/sublime_packages/package_control):

* `Ctrl+Shift+P` or `Cmd+Shift+P` in Linux / Windows / OS X
* Type `install`, select `Package Control: Install Package`
* Select `W3CValidators`

## Usage

Open an HTML or SVG file, and from the Tools menu go to W3C Validators, and then select the type of document you're validating. The results will be displayed in a new buffer.

## Design Decisions

Automatic detection of document types has proven unreliable, therefore only explicit document type validation is supported. Not all document types are supported, because most of them should be deprecated in practice.
