"""Pyarcconf submodule, which provides a logical drive representing class."""

import subprocess
from pyarcconf import parser

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
        if cmd == 'GETCONFIG':
            base_cmd = [self.path, cmd, self.adapter_id]
        else:
            base_cmd = [self.path, cmd, self.adapter_id, 'LOGICALDRIVE', self.id_]
        proc = subprocess.Popen(base_cmd + args,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode().strip()
        return out

    def __str__(self):
        """Build a string formatted object representation."""
        return '{}|{} {} {} {}'.format(self.id_, self.logical_drive_name, self.raid_level,
                                       self.status_of_logical_drive, self.size)

    def set_name(self, name):
        """Set the name for the logical drive.

        Args:
            name (str): new name
        Returns:
            bool: command result
        """
        result = self._execute('SETNAME', [name])
        if bool(result.endswith('Command completed successfully.')):
            result = _execute('GETCONFIG', ['LD', self.id_])
            result = parser.cut_lines(result, 4, 4)
            for line in result.split('\n'):
                if line.strip().startswith('Logical Device Name'):
                    self.logical_device_name = line.split(':')[1].strip().lower()
            return True
        return False

    def set_state(self, state):
        """Set the state for the logical drive.

        Args:
            state (str): new state
        Returns:
            bool: command result
        """
        result = self._execute('SETSTATE', [state])
        if bool(result.endswith('Command completed successfully.')):
            result = _execute('GETCONFIG', ['LD', self.id_])
            result = parser.cut_lines(result, 4, 4)
            for line in result.split('\n'):
                if line.strip().startswith('Status'):
                    self.status_of_logical_device = line.split(':')[1].strip().lower()
            return True
        return False

    def set_cache(self, mode):
        """Set the cache for the logical drive.

        Args:
            mode (str): new mode
        Returns:
            bool: command result
        """
        result = self._execute('SETCACHE', [mode])
        if bool(result.endswith('Command completed successfully.')):
            result = _execute('GETCONFIG', ['LD', self.id_])
            result = parser.cut_lines(result, 4, 4)
            for line in result.split('\n'):
                if line.split(':')[0].strip() in ['Read-cache', 'Write-cache']:
                    key, value = convert_attribute(*line.split(':'))
                    self.__setattr__(key, value)
            return True
        return False


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
