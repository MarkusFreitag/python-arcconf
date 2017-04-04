"""Pyarcconf submodule, which provides a logical drive representing class."""

import subprocess
from pyarcconf import parser

class PhysicalDrive():
    """Object which represents a physical drive."""

    def __init__(self, util_path, adapter_id, dev_id, channel, device):
        """Initialize a new LogicalDriveSegment object."""
        self.path = util_path
        self.adapter_id = adapter_id
        self.id_ = dev_id
        self.channel = channel
        self.device = device
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
            base_cmd = [self.path, cmd, self.adapter_id, 'DEVICE', self.channel, self.device]
        proc = subprocess.Popen(base_cmd + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode().strip()
        return out

    def __str__(self):
        """Build a string formatted object representation."""
        return '{}|{},{} {} {}'.format(self.id_, self.channel, self.device,
                                 self.model, self.serial_number)

    def _get_config(self):
        result = self._execute('GETCONFIG', ['PD'])
        result = parser.cut_lines(result, 4, 4)
        for part in result.split('\n\n'):
            if 'Device #{}'.format(self.id_) in part and '{},{}'.format(self.channel, self.device) in part:
                return part

    def set_state(self, state):
        """Set the state for the physical drive.

        Args:
            state (str): new state
        Returns:
            bool: command result
        """
        result = self._execute('SETSTATE', [state])
        if bool(result.endswith('Command completed successfully.')):
            conf = self._get_config()
            lines = list(filter(None, conf.split('\n')))
            for line in lines:
                if line.strip().startswith('State'):
                    self.state = line.split(':')[1].strip().lower()
                    return True
        return False

    def set_cache(self, mode):
        """Set the cache for the physical drive.

        Args:
            mode (str): new mode
        Returns:
            bool: command result
        """
        result = self._execute('SETCACHE', [mode, 'noprompt'])
        if bool(result.endswith('Command completed successfully.')):
            conf = self._get_config()
            lines = list(filter(None, conf.split('\n')))
            for line in lines:
                if line.strip().startswith('Write Cache'):
                    self.write_cache = line.split(':')[1].strip().lower()
                    return True
        return False
