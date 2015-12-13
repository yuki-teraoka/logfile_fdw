logfile_fdw
==================================

postgresql foreign data wrapper for any log files.

install
---------------------

    % sudo pip install pgxnclient
    % sudo pip install git+https://github.com/yuki-teraoka/logfile_fdw.git
    % sudo pgxn install multicorn


create extention and server
---------------------

    % psql
    CREATE EXTENSION multicorn;
    
    CREATE SERVER logfile_fdw FOREIGN DATA WRAPPER multicorn options (
            wrapper 'logfile_fdw.LogFileForeignDataWrapper'
    );


example
---------------------

    % psql
    CREATE FOREIGN TABLE examplelog(
            level text,
           message text
    ) SERVER logfile_fdw OPTIONS (
            -- log line pattern regex. use named groups.
            log_pattern '(?P\<level\>[^ ]*) (?P\<message\>.*)',
            -- log file glob pattern. 
            file_pattern '/tmp/example*'
    );
    
    SELECT * FROM examplelog;
    
     level | message
    -------+----------
    (0 rows)
    
    \q

    % echo "INFO message1" \>\> /tmp/example1
    % echo "INFO message2" \>\> /tmp/example1
    % echo "WARN message3" \>\> /tmp/example2
    % echo "ERROR message4" \>\> /tmp/example2

    % psql
    SELECT * FROM examplelog;
    
     level | message
    -------+----------
     INFO  | message1
     INFO  | message2
     WARN  | message3
     ERROR | message4
    (4 rows)


embedded log patterns
---------------------

You can use the following shortcut name to log pattern.

| pattern name              | logformat   | regex       |
|:--------------------------|:------------|:------------|
| apache_common             | LogFormat "%h %l %u %t \"%r\" %\>s %b" common                                                  | (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) |
| apache_combined           | LogFormat "%h %l %u %t \"%r\" %\>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined             | (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) "(?P\<referer\>.*?)" "(?P\<agent\>.*?)" |
| apache_combined_io        | LogFormat "%h %l %u %t \"%r\" %\>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio     | (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) "(?P\<referer\>.*?)" "(?P\<agent\>.*?)" (?P\<input_bytes\>[^ ]*) (?P\<output_bytes\>[^ ]*) |
| apache_vhost_common       | LogFormat "%v %h %l %u %t \"%r\" %\>s %b" vcommon                                              | (?P\<vhost\>[^ ]*) (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) |
| apache_vhost_combined     | LogFormat "%v %h %l %u %t \"%r\" %\>s %b \"%{Referer}i\" \"%{User-Agent}i\"" vcombined         | (?P\<vhost\>[^ ]*) (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) "(?P\<referer\>.*?)" "(?P\<agent\>.*?)" |
| apache_vhost_combined_io  | LogFormat "%v %h %l %u %t \"%r\" %\>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" vcombinedio | (?P\<vhost\>[^ ]*) (?P\<host\>[^ ]*) (?P\<ident\>[^ ]*) (?P\<remote_user\>[^ ]*) \\[(?P\<time\>[^]]*)\\] "(?P\<method\>[^ ]*)(?: *(?P\<url\>[^ ]*) *(?P\<proto\>[^ ]*))?" (?P\<status\>[^ ]*) (?P\<bytes\>[^ ]*) "(?P\<referer\>.*?)" "(?P\<agent\>.*?)" (?P\<input_bytes\>[^ ]*) (?P\<output_bytes\>[^ ]*)' |


    % psql
    CREATE FOREIGN TABLE apachelog(
            host text,
            ident text,
            remote_user text,
            time text,
            method text,
            url text,
            proto text,
            status text,
            bytes text,
            referer text,
            agent text
    ) server logfile_fdw options (
            log_pattern 'apache_combined',
            file_pattern '/var/log/httpd/access_log*'
    );
