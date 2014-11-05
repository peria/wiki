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
  return ''.join(template)


def readContent(filename):
  """
  Reads |filename| and returns a dict.
  @param string filename : Filename to read
  @return : Dictionary type which includes contents' information.
  """
  contents = []
  for line in open(filename):
    contents.append(line)

  ret = {}
  # Read |contents| and build up a dict.
  return ret
  

def applyTemplate(template, src_filename, dst_filename):
  """
  Applies |template| to |src_filename| and writes to |dst_filename|.
  @param string template : Template string to match
  @param string src_filename : Filename of a source file.
  @param string dst_filename : Filename of a destination file.
  """
  content_dict = readContent(src_filename)
  content = template % content_dict

  try:
    f = open(dst_filename, 'w')
    f.write(content)
  else:
    print 'Could not process %s.' % dst_filename


def copyFiles(template, input, output):
  """
  Copies input files to output files.  Applies template if they are HTML files.
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
      applyTemplate(template, src, dst)


def main():
  options, arg = getOption()

  # Check if template file exists
  template_filename = options.template
  template = readTemplate(template_filename)
  if not template:
    exit()

  copyFiles(template, input, output)


if __name__ == '__main__':
  main()
