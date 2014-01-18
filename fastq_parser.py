class FastqReadHeader(object):
    """Parsed header of a casava 1.8-style fastq read."""
    fieldslist = ['instrument', 'run', 'flowcell', 'lane', 'tile', 'x', 'y',
                  'pair', 'filter', 'ctrl', 'idxseq']
    _nfields = len(fieldslist)
    _lfields = fieldslist[:7]
    _rfields = fieldslist[7:]

    def __init__(self, line):
        self.line = line
        line = line.lstrip('@')
        line = ':'.join(line.split())
        fields = line.split(':')
        for i in range(self._nfields):
            setattr(self, self.fieldslist[i], fields[i])

    def __str__(self):
        lfields = ':'.join(str(getattr(self, f)) for f in self._lfields)
        rfields = ':'.join(str(getattr(self, f)) for f in self._rfields)
        return '@{0} {1}'.format(lfields, rfields)


class FastqRead(object):
    """Represents 1 read, or 4 lines of a casava 1.8-style fastq file."""
    def __init__(self, file_obj, parse_header=True):
        header = file_obj.next().rstrip()
        assert header.startswith('@')
        if parse_header:
            self.header = FastqReadHeader(header)
        else:
            self.header = header
        self.sequence = file_obj.next().rstrip()
        file_obj.next()
        self.quality = file_obj.next().rstrip()

    def __str__(self):
        return "{0}\n{1}\n+\n{2}\n".format(self.header, self.sequence,
                                           self.quality)


class FastqParser(object):
    """Parses a fastq file into FastqReads."""
    def __init__(self, filename, parse_headers=True):
        if filename.endswith('.gz'):
            self._file = gzip.open(filename)
        else:
            self._file = open(filename, 'rU')
        self._line_index = 0
        self.parse_headers = parse_headers

    def __iter__(self):
        return self

    def next(self):
        read = FastqRead(self._file, self.parse_headers)
        self._line_index += 4
        return read

