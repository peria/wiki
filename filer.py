#!/usr/bin/env python

import logging
import optparse
import os

"""
filer command copies all files.
A template conversion is applied to HTML files.
"""

def getOption():
  parser = optparse.OptionParser()
  parser.add_option('-i', '--input', dest='input', default=None,
                    help='Figures the root directory of source files.')
  parser.add_option('-o', '--output', dest='output', default=None,
                    help='Figures the root directory of output files.')
  parser.add_option('-t', '--template', dest='template', default=None,
                    help='Figures a tempalte file to convert in.')
  parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                    default=False)

  options, arg = parser.pase_args()

  if not options.input or not options.output or not options.template:
    parser.print_help()
    exit()

  if options.verbose:
    logging.getLogger().setLevel(logging.INFO)

  return (option, arg)


def readTemplate(filename):
  if not os.path.exists(filename):
    logging.error("Template file %s cannot be read." % filename)
    return None
  template = []
  for line in open(filename):
    template.append(line)
  # Simplify |template|


def applyTemplate(template, input, output):
  """
  Recursively apply a template to input files and writes to output files.
  Returns False if something goes wrong.
  """

  for (dirpath, dirnames, filenames) in os.walk(input):
    for dirname in dirnames:
      src_dir = os.path.join(dirpath, dirname)
      dst_dir = src_dir.replace(input, output)
      if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in filenames:
      src = os.path.join(dirpath, filename)
      dst = src.replace(input, output)
      if os.path.exists(dst) and os.path.getmtime(src) < os.path.getmtime(dst):
        continue
      # Check if |src| is a HTML file.  We don't need templates for other file types.
      ApplyTemplateFile(template, src, dst)



def main():
  options, arg = getOption()

  # Check if template file exists
  template_filename = options.template
  template = readTemplate(template_filename)
  if not template:
    exit()

  applyTemplate(template, input, output)


if __name__ == '__main__':
  main()
