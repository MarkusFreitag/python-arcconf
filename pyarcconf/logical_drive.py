"""Pyarcconf submodule, which provides a logical drive representing class."""


class LogicalDrive():
    """Object which represents a logical drive."""

    def __init__(self, util_path, adapter_id, id_):
        """Initialize a new LogicalDrive object."""
        self.path = util_path
        self.adapter_id = adapter_id
        self.id_ = id_
        self.logical_drive_name = None
        self.raid_level = None
        self.status_of_logical_drive = None
        self.size = None
        self.read_cache_mode = None
        self.write_cache_mode = None
        self.write_cache_setting = None
        self.partitioned = None
        self.protected_by_hot_spare = None
        self.bootable = None
        self.failed_stripes = None
        self.power_settings = None
        self.segments = []

    def _execute(self, cmd, args=[]):
        """Execute a command using arcconf.

        Args:
            args (list):
        Returns:
            str: arcconf output
        Raises:
            RuntimeError: if command fails
        """
        if cmd 'GETCONFIG':
            base_cmd = [self.path, cmd, self.adapter_id]
        else:
            base_cmd = [self.path, cmd, self.adapter_id, 'LOGICALDRIVE', self.id_]
        proc = subprocess.Popen(base_cmd + args, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode().lstrip().rstrip()
        if isinstance(err, bytes):
            err = err.decode().lstrip().rstrip()
        if proc.returncode:
            ex = RuntimeError(err)
            ex.exitcode = proc.returncode
            raise ex
        return out

    def __str__(self):
        """Build a string formatted object representation."""
        return '{}|{} {} {} {}'.format(self.id_, self.logical_drive_name, self.raid_level,
                                       self.status_of_logical_drive, self.size)


class LogicalDriveSegment():
    """Object which represents a logical drive segment."""

    def __init__(self, channel, port, state, serial, proto, type_):
        """Initialize a new PhysicalDrive object."""
        self.channel = channel
        self.port = port
        self.state = state
        self.serial = serial
        self.proto = proto
        self.type_ = type_

    def __str__(self):
        """Build a string formatted object representation."""
        return '{},{} {} {}'.format(self.channel, self.port, self.state, self.serial)
