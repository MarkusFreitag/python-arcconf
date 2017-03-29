"""Pyarcconf submodule, which provides a logical drive representing class."""


class PhysicalDrive():
    """Object which represents a physical drive."""

    def __init__(self, util_path, adapter_id, channel, id_):
        """Initialize a new LogicalDriveSegment object."""
        self.path = util_path
        self.adapter_id = adapter_id
        self.channel = channel
        self.id_ = id_
        self.model = None
        self.serial_number = None

    def _execute(self, cmd, args=[]):
        """Execute a command using arcconf.

        Args:
            args (list):
        Returns:
            str: arcconf output
        Raises:
            RuntimeError: if command fails
        """
        if cmd == 'GETCONFIG':
            base_cmd = [self.path, cmd, self.adapter_id]
        else:
            base_cmd = [self.path, cmd, self.adapter_id, 'DEVICE', self.channel, self.id_]
        proc = subprocess.Popen(base_cmd + args, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode().strip()
        if isinstance(err, bytes):
            err = err.decode().strip()
        if proc.returncode:
            ex = RuntimeError(err)
            ex.exitcode = proc.returncode
            raise ex
        return out

    def __str__(self):
        """Build a string formatted object representation."""
        return '{}|{} {}'.format(self.id_, self.model, self.serial_number)
