#!/usr/bin/env python
# This file is part of hdlcc.
#
# hdlcc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hdlcc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hdlcc.  If not, see <http://www.gnu.org/licenses/>.
"Script should be called within Vim to launch tests"

import os
from sys import argv, path, stdout
import logging
import nose2
import coverage

_logger = logging.getLogger(__name__)

def test(nose2_argv):
    cov = coverage.Coverage(config_file='.coveragerc')
    cov.start()

    nose2.discover(exit=False, argv=nose2_argv)

    cov.stop()
    cov.save()
    cov.combine()
    cov.html_report()

def clear():
    for cmd in ('git clean -fdx',
                'git submodule foreach --recursive git clean -fdx'):
        print cmd
        print os.popen(cmd).read()

def debug():
    path.insert(0, './dependencies/rainbow_logging_handler/')
    from rainbow_logging_handler import RainbowLoggingHandler
    stream_handler = RainbowLoggingHandler(
        stdout,
        #  Customizing each column's color
        # pylint: disable=bad-whitespace
        color_asctime          = ('dim white',  'black'),
        color_name             = ('dim white',  'black'),
        color_funcName         = ('green',      'black'),
        color_lineno           = ('dim white',  'black'),
        color_pathname         = ('black',      'red'),
        color_module           = ('yellow',     None),
        color_message_debug    = ('color_59',   None),
        color_message_info     = (None,         None),
        color_message_warning  = ('color_226',  None),
        color_message_error    = ('red',        None),
        color_message_critical = ('bold white', 'red'))
        # pylint: enable=bad-whitespace

    logging.root.addHandler(stream_handler)


def main():
    if '--clear' in argv[1:]:
        clear()
        argv.pop(argv.index('--clear'))

    if '--debug' in argv[1:]:
        debug()
        argv.pop(argv.index('--debug'))

    file_handler = logging.FileHandler("tests.log")
    log_format = "[%(asctime)s] %(levelname)-8s || %(name)-30s || %(message)s"
    file_handler.formatter = logging.Formatter(log_format)
    logging.root.addHandler(file_handler)
    logging.root.setLevel(logging.DEBUG)

    test(nose2_argv=argv)

if __name__ == '__main__':
    main()
