from multicorn import ForeignDataWrapper
import os, glob, re

class LogFileForeignDataWrapper(ForeignDataWrapper):

    APACHE_COMMON_LOG_FORMAT = '(?P<host>[^ ]*) (?P<ident>[^ ]*) (?P<remote_user>[^ ]*) \[(?P<time>[^]]*)\] "(?P<method>[^ ]*)(?: *(?P<url>[^ ]*) *(?P<proto>[^ ]*))?" (?P<status>[^ ]*) (?P<bytes>[^ ]*)'
    APACHE_VHOST_COMMON_LOG_FORMAT = '(?P<vhost>[^ ]*) ' + APACHE_COMMON_LOG_FORMAT
    APACHE_COMBINED_LOG_FORMAT = APACHE_COMMON_LOG_FORMAT + ' "(?P<referer>.*?)" "(?P<agent>.*?)"'
    APACHE_VHOST_COMBINED_LOG_FORMAT = APACHE_VHOST_COMMON_LOG_FORMAT + ' "(?P<referer>.*?)" "(?P<agent>.*?)"'
    APACHE_COMBINED_IO_LOG_FORMAT = APACHE_COMBINED_LOG_FORMAT + ' (?P<input_bytes>[^ ]*) (?P<output_bytes>[^ ]*)'
    APACHE_VHOST_COMBINED_IO_LOG_FORMAT = APACHE_VHOST_COMBINED_LOG_FORMAT + ' (?P<input_bytes>[^ ]*) (?P<output_bytes>[^ ]*)'

    defaultFormat = {
        'apache_common': re.compile(APACHE_COMMON_LOG_FORMAT),
        'apache_vhost_common': re.compile(APACHE_VHOST_COMMON_LOG_FORMAT),
        'apache_combined': re.compile(APACHE_COMBINED_LOG_FORMAT),
        'apache_vhost_combined': re.compile(APACHE_VHOST_COMBINED_LOG_FORMAT),
        'apache_combined_io': re.compile(APACHE_COMBINED_IO_LOG_FORMAT),
        'apache_vhost_combined_io': re.compile(APACHE_VHOST_COMBINED_IO_LOG_FORMAT)
    }

    def __init__(self, options, columns):
        super(LogFileForeignDataWrapper, self).__init__(options, columns)
        self.columns = columns
        log_pt = options['log_pattern']
        self.log_pattern = self.defaultFormat.get(log_pt, re.compile(log_pt))
        self.file_pattern = options['file_pattern']

    def execute(self, quals, columns):
          for file in glob.glob(self.file_pattern):
              if not os.path.isfile(file):
                  continue
              with open(file, 'r') as f:
                  for line in f:
                      matches = self.log_pattern.match(line)
                      if matches:
                          yield matches.groupdict()
                      else:
                          raise Exception('Invalid format. line: ' + line)
