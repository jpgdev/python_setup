from app.helpers import PacmanHelper, PacmanErrorType, PacmanException
import pytest
from unittest.mock import patch, Mock

# import unittest


class TestPacmanHelperBase:
    def setup(self):
        self.pacman_helper = PacmanHelper()

    def teardown(self):
        self.pacman_helper = None


class TestPacmanHelperGetErrorType(TestPacmanHelperBase):
    def test_package_not_found(self):
        err = self.pacman_helper.get_error_type('The package was not found')
        assert PacmanErrorType.package_not_found == err

    def test_need_root(self):
        err = self.pacman_helper.get_error_type('You need root to call this')
        assert PacmanErrorType.need_root == err

    def test_unknown(self):
        err = self.pacman_helper.get_error_type('a random error string')
        assert PacmanErrorType.unknown == err


class TestPacmanInstall(TestPacmanHelperBase):
    # TODO : Implement integration tests
    def setup(self):
        super(TestPacmanInstall, self).setup()
        self.only_needed_param = '--needed'
        self.no_confirm_param = '--noconfirm'
        self.fake_packages_names = ['not_a_package']

    def init_subprocess_mock(self, subprocess_mock):
        ''' Create the correct objects and functions to return from the
        subprocess.Popen mock '''

        return_mock = Mock(spec=['communicate', 'returncode'])
        subprocess_mock.return_value = return_mock

        return_mock.returncode = 0
        return_mock.communicate = Mock(return_value=(1, None))

        self.subprocess_mock = subprocess_mock

    @patch('subprocess.Popen')
    def test_only_needed_param_default_true(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(self.fake_packages_names)
        cmd = self.subprocess_mock.call_args[0][0]

        assert self.only_needed_param in cmd

    @patch('subprocess.Popen')
    def test_only_needed_param_set_correctly(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(self.fake_packages_names, only_needed=False)
        cmd = self.subprocess_mock.call_args[0][0]

        assert self.only_needed_param not in cmd

    @patch('subprocess.Popen')
    def test_skip_confirmation_param_default_false(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(self.fake_packages_names)
        cmd = self.subprocess_mock.call_args[0][0]

        assert self.no_confirm_param not in cmd

    @patch('subprocess.Popen')
    def test_skip_confirmation_param_set_correctly(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(
            self.fake_packages_names, skip_confirmation=True)
        cmd = self.subprocess_mock.call_args[0][0]

        assert self.no_confirm_param in cmd

    @patch('subprocess.Popen')
    def test_force_sudo_param_default_false(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(
            self.fake_packages_names)
        cmd = self.subprocess_mock.call_args[0][0]

        assert "sudo" not in cmd

    @patch('subprocess.Popen')
    def test_force_sudo_param_set_correctly(self, subprocess_mock):
        self.init_subprocess_mock(subprocess_mock)

        self.pacman_helper.install(
            self.fake_packages_names, force_sudo=True)
        cmd = self.subprocess_mock.call_args[0][0]

        assert "sudo" in cmd

    def test_raise_sudo_exception(self):
        with pytest.raises(PacmanException) as pacman_ex:
            self.pacman_helper.install(self.fake_packages_names)

        assert pacman_ex.value.error_type == PacmanErrorType.need_root

    def test_raise_package_not_found_exception(self):
        with pytest.raises(PacmanException) as pacman_ex:
            self.pacman_helper.install(self.fake_packages_names,
                    force_sudo=True)

        assert pacman_ex.value.error_type == PacmanErrorType.package_not_found

