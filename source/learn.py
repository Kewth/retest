#!/usr/bin/python3
'retest -l'

def main():
    '--learn 的信息'
    print('''
How to write retest.yaml?
    The file retest.yaml is used by retest to judge.
    You can get a full example on ~/.config/retest/example.yaml .

    source: (required)
        The source code you want to judge.

    data: (required)
        The directory where include all data files.

        If a sub dict was given, retest will make data itself:
            rand: (required)
                The file which make input file.

            std: (required)
                The file which make output file.

            times: (required)
                The number of the test-cases.

    time:
        The time limit of each judgement.
        Its unit is millisecond.
        It's set to 1000 by default.

    memory:
        The memory limit of each judgement.
        Its unit is megabyte.
        NOTE: MLE won't be displayed somtimes (it'll be shown as RE).

    difftime:
        The time limit of checking answer(running spj).
        Its unit is millisecond.
        It's set to 1000 by default.

    input:
        The file where exe get input.
        It's set to standard input by default.

    output:
        The file where exe get output.
        It's set to standard output by default.

    spj:
        The Special Judge File (Lemon Style[1]).
        If it's set to ~ (null), retest will judge traditionally.
        It's set to ~ by default

    option:
        The option to compile (only used for g++ and gcc).
        Many Oier may want to open O2 switch. Just add 'option: -O2'.

    cd:
        The directory where the real retest.yaml is.
        Of course is's set to './' by default.

    before:
        The command you want to run before retest.

    after:
        The command you want to run after retest.
        For example, if the data directory is too lagre that is in the .rar file, just add this:
            before: rar x *.rar data
            after: rm -r data

    plugin:
        The plugins you want to use which is set to default by default :)
        You can use only one plugin or up to 10 plugins.
        For example:
            plugin: default
        Another example:
            plugin:
                - kewth
                - acm
        When you want to judge more than one problem, the plugin in sub_config is invalid.

    If you want to judge more problems, you can set 'Tn' sub configura
  tion.
        For example:
            time: 1000
            T1:
                source: a.cpp
                data: data/A
            T2:
                source: b.cpp
                data: data/B
        It will judge 2 problems in one time.

Some usefull arguments:
    You can rough understanding by using 'retest -h' or 'retest --help'.

    --learn, -l:
        Print this message to learn how to use retest.
        To display this better, you can use 'less' command:
            retest -l | less

    --plugin, -p:
        Print all plugins you can use.

    --use, -u:
        Use subconfig of retest.yaml.

    [1]: Lemon Style
        The spj is given 6 arguments.
        Argv[1] is the input file.
        Argv[2] is the output file of user.
        Argv[3] is the answer file.
        Argv[4] is the a number which means max scores of the test-case.
        Argv[5] is the output file of spj which include the scores user get.
        Argv[6] is the log file of spj.
    ''')

if __name__ == '__main__':
    main()
