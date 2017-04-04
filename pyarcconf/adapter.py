"""Pyarcconf submodule, which provides a raidcontroller representing Adapter class."""

import subprocess
from pyarcconf import parser
from pyarcconf.logical_drive import LogicalDrive
from pyarcconf.physical_drive import PhysicalDrive
from pyarcconf.task import Task


class Adapter():
    """Object which represents an adapter."""

    def __init__(self, util_path, id_):
        """Initialize a new Adapter object."""
        self.path = util_path
        self.id_ = id_
        self.controller_model = None
        self.channel_description = None
        self.raid_properties = {}
        self.versions = {}
        self.battery = {}
        self.phy_drives = []
        self.log_drives = []
        self.tasks = []

    def initialize(self):
        self.fetch_data()
        self.fetch_log_drives()
        self.fetch_phy_drives()
        self.fetch_tasks()

    def _execute(self, cmd, args=[]):
        """Execute a command using arcconf.

        Args:
            args (list):
        Returns:
            str: arcconf output
        Raises:
            RuntimeError: if command fails
        """
        proc = subprocess.Popen([self.path, cmd, self.id_] + args,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode().strip()
        return out

    def fetch_data(self):
        """Parse the info about the adapter itself."""
        result = self._execute('GETCONFIG', ['AD'])
        result = parser.cut_lines(result, 4, 3)
        info = result.split(56*'-')[0]
        raid_props = result.split(56*'-')[2]
        versions = result.split(56*'-')[4]
        battery = result.split(56*'-')[6]
        for line in info.split('\n'):
            if ' : ' in line:
                key, value = parser.convert_attribute(*line.split(' : '))
                self.__setattr__(key, value)
        for line in raid_props.split('\n'):
            if ' : ' in line:
                key, value = parser.convert_attribute(*line.split(' : '))
                self.raid_properties[key] = value
        for line in versions.split('\n'):
            if ' : ' in line:
                key, value = parser.convert_attribute(*line.split(' : '))
                self.versions[key] = value
        for line in battery.split('\n'):
            if ' : ' in line:
                key, value = parser.convert_attribute(*line.split(' : '))
                self.battery[key] = value

    def fetch_log_drives(self):
        """Parse the info about logical drives."""
        result = self._execute('GETCONFIG', ['LD'])
        if 'No logical devices configured' not in result:
            result = parser.cut_lines(result, 4, 4)
            for part in result.split('\n\n'):
                options, _, segments = part.split(56*'-')
                lines = list(filter(None, options.split('\n')))
                logid = lines[0].split()[-1]
                log_drive = LogicalDrive(self.path, self.id_, logid)
                for line in lines[1:]:
                    if ':' in line:
                        key, value = parser.convert_attribute(*line.split(':'))
                        log_drive.__setattr__(key, value)
                for line in list(filter(None, segments.split('\n'))):
                    line = ':'.join(line.split(':')[1:])
                    state = line.split()[0].strip()
                    serial = line.split(')')[-1].strip()
                    size, proto, type_, channel, port = line.split('(')[1].split(')')[0].split(',')
                    channel = channel.split(':')[1]
                    port = port.split(':')[1]
                    log_drive.segments.append(LogicalDriveSegment(channel, port, state, serial, proto, type_))
                self.log_drives.append(log_drive)

    def fetch_phy_drives(self):
        """Parse the info about physical drives."""
        result = self._execute('GETCONFIG', ['PD'])
        result = parser.cut_lines(result, 4, 5)
        for part in result.split('\n\n'):
            lines = list(filter(None, part.split('\n')))
            channel, device = lines[6].split(':')[2].split('(')[0].split(',')
            phyid = lines[0].split()[-1][1]
            phy_drive = PhysicalDrive(self.path, self.id_, phyid, channel.strip(), device)
            for line in lines[1:]:
                if ' : ' in line:
                    key, value = parser.convert_attribute(*line.split(' : '))
                    phy_drive.__setattr__(key, value)
            self.phy_drives.append(phy_drive)

    def fetch_tasks(self):
        """Parse the tasks."""
        result = self._execute('GETSTATUS')
        if 'Current operation              : None' not in result:
            result = parser.cut_lines(result, 1, 3)
            for part in result.split('\n\n'):
                task = Task()
                for line in part.split('\n')[1:]:
                    key, value = parser.convert_attribute(*line.split(' : '))
                    task.__setattr__(key, value)
                self.tasks.append(task)

    def __str__():
        """Build a string formatted object representation."""
        return '{}|{} {}'.format(self.id_, self.controller_model, self.channel_description)
