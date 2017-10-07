# documentation for `text_interface.py`.

See also [the documentation for each function](https://github.com/elterminad0r/cipher_tools/blob/master/action_doc.md)

The first thing you are likely to encounter is the file input. If you're not a command line user, this will work by pasting it in, entering another newline and pressing `ctrl-c`. For example, it might look like this:

    Manual file entry: paste in the file, or type it in line by line. When you're done, hit an extra newline to be safe and then hit ctrl-c 
    HVMTVH,
    DO DN BMZVO OJ CZVM AMJH TJP. RZ YDY KDXF PK NJHZ XCVOOZM V XJPKGZ JA HJIOCN VBJ VIY E RVN HZIODJIZY OCZMZ OJJ, NJ RZ VGMZVYT CVQZ V ADGZ JI CZM. CZM IVHZ DN EJYDZ VIY NCZ RJMFN VN GDVDNJI WZORZZI OCZ WMDODNC GDWMVMT VIY OCZ WMDODNC HPNZPH, MZNZVMXCDIB GDIFN WZORZZI VMOZAVXON VIY DHKZMDVG MJHVI OZSON, NJ OCVO ODZN DI RDOC OCZ DIOZGGDBZIXZ TJP CVQZ WZZI MZXZDQDIB. IJOCDIB NPBBZNON OCVO NCZ CVN WZZI DIQJGQZY DI VITOCDIB NCVYT VIY NCZ CVN CZGKZY RDOC NZQZMVG DINPMVIXZ AMVPY XVNZN. NCZ CVN VI DIOZMZNODIB WVXFBMJPIY. NCZ YDY V KCY JI CPHVI HDBMVODJI NOPYDZN, HVDIGT HVOCZHVODXVG HJYZGGDIB, OCZI HJQZY JI OJ NOPYT FIJRGZYBZ HDBMVODJI RCDXC BJO CZM DIOJ OCZ WDWGDJKCDGZ XDMXPDO. VAOZM BMVYPVODIB NCZ NKZIO NJHZ ODHZ RDOC JIZ JA OCZ GJIYJI VPXODJI CJPNZN RJMFDIB JI KMJQZIVIXZ WZAJMZ OVFDIB CZM XPMMZIO KJNDODJI RDOC OCZ GDWMVMT. OCZMZ MZVGGT DN IJOCDIB NPNKDXDJPN DI CZM WVXFBMJPIY VIY D RVN DIXGDIZY OJ RMDOZ CZM JAA VN V GZVY, WPO RCZI D BJO TJPM HZNNVBZ D YZXDYZY D RVIOZY OJ HZZO CZM. D OMDZY OJ NZO OCVO PK JIGT OJ WZ OJGY OCVO NCZ DN JPO JA XJPIOMT AJM V RCDGZ. DI XVDMJ.
    D RDGG NZZ TJP OCZMZ.
    CVMMT

    ^CAnything prefixed with...

The reasoning for this is that a script can only read a line of input. `ctrl-c` sends an "interrupt signal" to the script, telling it to stop, but this will also "corrupt" the line the script is currently trying to read, so this is made blank for safety.

The next thing the script will do is display the following help message (or a slightly expanded version of it if I've continued development):

    Anything prefixed with a ! will be considered a command. Anything else will be
    interpreted as a series of substitutions to make. The available commands are as
    follows:
    !frequency|freq|f  - Display frequencies - (pos=[1], pkw=['width', 'interval', 'pat'])
    !doubles|pairs|d   - Show repeating adjacent identical pairs - (pos=[1], pkw=[])
    !word|w            - Find words matching a prototype - (pos=[2], pkw=[])
    !runs|r            - Display frequently repeating runs - (pos=[1], pkw=['length', 'width', 'maxdisplay'])
    !delete|remove|x   - Remove letters from the subtable
    !print|p           - Show the subbed source - (pos=[1], pkw=['alt'])
    !source|s          - Show the source - (pos=[1], pkw=[])
    !table|t           - Show the subtable - (pos=[1], pkw=[])
    !missing|m         - Check for unused letters - (pos=[1], pkw=[])
    !general|g         - Show some general info (source, table, subbed source) - (pos=[1], pkw=[])
    !info|stats|i      - Display common frequency statistics - (pos=[1], pkw=[])
    !reset|clear|c     - Reset (clear) the subtable - (pos=[1], pkw=[])
    !help|h            - Show help message - (pos=[1], pkw=[])
    !exit|quit|q       - Exit the program - (pos=[1], pkw=[])
    A command can be given arguments, as space-separated words after the command.

This gives a quick, pretty terse summary of command syntax. To expand on it a little bit:

The "default" way the script tries to interpret anything you do is as a series of substitutions. This follows the convention of pairs of letters representing a substitution from the first to the second (ie `Ab` means `A` becomes `b`). You can give many at once, generally separated by whitespace. It is case sensitive and accepts any character (not just alphabetical ones).

Technically how the parsing works is by a `sh`-like argument parser (`shlex.split`), so if you want to use quotes you should escape them (either by in turn quoting them or using a backslash `\\`) or substitute whitespace, you can use `sh` syntax, eg `" ,"`.

Here is how you might add some substitutions:

    Enter a command/substitutions > Hm Va Mr Ty Ch Mr   

    Here is the current substitution table:
    Ch Hm Mr Ty Va
    C -> h
    H -> m
    M -> r
    T -> y
    V -> a

    Enter a command/substitutions > " ,"
    Here is the current substitution table:
    ' ,' Ch Hm Mr Ty Va
      -> ,
    C -> h
    H -> m
    M -> r
    T -> y
    V -> a

You can see that it also prints a line which in theory you should be able to paste straight back in.

Now, back to commands - this program supports more actions than just substitutions (for one you have to be able to see what the substitutions do to the text). These actions take the form of "commands". A command will always start with an exclamation mark `!` character.

The notation I use here and in the program help message is

    !<command>|<alt_command>|...

This means you can call the same command as either `!command` or `!alt_command`, etc. An example of a command you might use is:

    !print

This will print the source to the screen, making substitutions. So far all of the commands have a shorter alias, which more often than not is the first letter of the fully qualified command. (Notable exception is `!delete|remove|x`, which collides with `!runs` and `!doubles`).

Some commands also accept arguments. Most often you probably don't need to bother with these, but they can be useful (the most useful one I've found is `!r -length`). An argument has the following syntax:

    !com -arg=val

This means call the command "`com`" and give the argument of name "`arg`" the value "`val`". An example is `!runs`. This is a tool to analyse the frequency of adjacent "runs" of characters. However, when you call it as just "`!runs`" (or `!r`), it default to runs of length 3. You can specify the length of the runs to be, for example, 2 by doing the following:

    !runs -length=2

It also only displays 20 by default. If you want to see the 30 most frequent 4-length runs, you can do

    !runs -length=4 -maxdisplay=30

In the help message, you can see the possible arguments under `pkw` - for `!runs`, this is `pkw=['length', 'width', 'maxdisplay']`. This indicates that `!runs` will accept the arguments "`length`", "`width`", and "`maxdisplay`". `pkw` stands for "possible keyword arguments" - that's because these are strictly speaking "keyword arguments", as they're given by a keyword (which is their name).

Some functions also accept anonymous arguments - so far this is only used by `!delete` and `!word`. Here the argument is just given (again, `sh`-style) after the function call, eg:

    !x A B C
    !word "B\h\aV\e"