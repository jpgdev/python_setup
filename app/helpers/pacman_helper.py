import subprocess
from . import PacmanErrorType, PacmanException


class PacmanHelper:
    def install(self,
                packages,
                only_needed=True,
                skip_confirmation=False,
                force_sudo=False):
        ''' Install packages using pacman.'''

        cmd = ["pacman", "-S"] + packages

        if force_sudo:
            cmd.insert(0, "sudo")

        if only_needed:
            cmd.append("--needed")

        if skip_confirmation:
            cmd.append("--noconfirm")

        # Run the command
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        output, error = p.communicate()

        # If error
        if p.returncode and p.returncode is not 0:
            # Decode the byte string to an actual string
            error_str = error.decode("utf-8")
            # lines = error_str.split('\n')
            # print(lines)
            error_type = self.get_error_type(error_str)

            raise PacmanException(
                message=error_str,
                args=cmd,
                error_type=error_type,
                status_code=p.returncode)

        # return p.return_code

    def get_error_type(self, error_str):
        """Get the type of error from a pacman error message"""
        # lines = error_str.split('\n')

        # If error is 'package not found'
        not_found_pos = error_str.find('not found')
        if not_found_pos > 0:
            return PacmanErrorType.package_not_found
            # semi_colon_pos = error_str.find(':')
            # missing_pkgs = []
            # for line in lines:
            #     # Split the string to get the packages names
            #     missing_pkgs.append(line[not_found_pos + semi_colon_pos:])

            # raise PacmanException(
            #     message='Pacman could not find this packages: '
            #     ', '.join(missing_pkgs),
            #     args=cmd)

        need_root = error_str.find('root')
        if need_root > 0:
            return PacmanErrorType.need_root
        else:
            return PacmanErrorType.unknown
