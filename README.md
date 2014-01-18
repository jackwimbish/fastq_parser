fastq_parser
============

lightweight, easy to use fastq parser/writer for Python

How to use:

    fastq = FastqParser("/path/to/my_fastq.fastq.gz")

    for read in fastq:
        # set its first two bases to GG
        read.sequence = 'GG' + read.sequence[2:]
        # write it to stdout if it passed filter
        if read.header.filter != 'Y':
            sys.stdout.write(str(read))

If you don't care about parsing the read headers, you can improve performance by initializing the parser with the parse_headers keyword argument set to False.