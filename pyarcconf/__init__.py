"""Python3 library for the arcconf tool."""
import subprocess
import pyarcconf.parser


class Arcconf():
    """Arcconf wrapper class."""

    def __init__(self, util_path):
        """Initialize a new Arcconf object."""
        self.path = util_path

    def _execute(self, cmd, args=[]):
        """Execute a command using arcconf.

        Args:
            args (list):
        Returns:
            str: arcconf output
        Raises:
            RuntimeError: if command fails
        """
        proc = subprocess.Popen([self.path, cmd] + args, shell=True,
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

    def get_version(self):
        """Check the versions of all connected controllers.

        Returns:
            dict: controller with there version numbers for bios, firmware, etc.
        """
        versions = {}
        result = _execute('GETVERSION')
        result = parser.cut_lines(result, 2, 3)
        for part in result.split('\n\n'):
            lines = part.split('\n')
            id_ = lines[0].split('#')[1]
            versions[id_] = {}
            for line in lines[2:]:
                key = line.split(':').strip()
                value = line.split(':').strip()
                versions[id_][key] = value
        return versions

    def list_adapters(self):
        """List all adapter by their ids.

        Returns:
            list: list of adapter ids
        """
        adapters = []
        result = _execute('LIST')
        result = parser.cut_lines(result, 6, 2)
        for line in result.split('\n'):
            adapters.append(line.split(':')[0].strip().split()[1])
        return adapters

    def get_adapters(self):
        """Get all adapter objects for further interaction.

        Returns:
            list: list of adapter objects.
        """
        adapters = []
        for id_ in self.list_adapters():
            adapters.append(Adapter(self.path, id_))
        return adapters
