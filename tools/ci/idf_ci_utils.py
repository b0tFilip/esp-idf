# SPDX-FileCopyrightText: 2020-2023 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

# internal use only for CI
# some CI related util functions

import logging
import os
import subprocess
import sys
import typing as t
from functools import cached_property
from pathlib import Path

IDF_PATH = os.path.abspath(os.getenv('IDF_PATH', os.path.join(os.path.dirname(__file__), '..', '..')))


def get_submodule_dirs(full_path: bool = False) -> t.List[str]:
    """
    To avoid issue could be introduced by multi-os or additional dependency,
    we use python and git to get this output
    :return: List of submodule dirs
    """
    dirs = []
    try:
        lines = (
            subprocess.check_output(
                [
                    'git',
                    'config',
                    '--file',
                    os.path.realpath(os.path.join(IDF_PATH, '.gitmodules')),
                    '--get-regexp',
                    'path',
                ]
            )
            .decode('utf8')
            .strip()
            .split('\n')
        )
        for line in lines:
            _, path = line.split(' ')
            if full_path:
                dirs.append(os.path.join(IDF_PATH, path))
            else:
                dirs.append(path)
    except Exception as e:  # pylint: disable=W0703
        logging.warning(str(e))

    return dirs


def _check_git_filemode(full_path: str) -> bool:
    try:
        stdout = subprocess.check_output(['git', 'ls-files', '--stage', full_path]).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        return True

    mode = stdout.split(' ', 1)[0]  # e.g. 100644 for a rw-r--r--
    if any([int(i, 8) & 1 for i in mode[-3:]]):
        return True
    return False


def is_executable(full_path: str) -> bool:
    """
    os.X_OK will always return true on windows. Use git to check file mode.
    :param full_path: file full path
    :return: True is it's an executable file
    """
    if sys.platform == 'win32':
        return _check_git_filemode(full_path)
    return os.access(full_path, os.X_OK)


def get_git_files(path: str = IDF_PATH, full_path: bool = False) -> t.List[str]:
    """
    Get the result of git ls-files
    :param path: path to run git ls-files
    :param full_path: return full path if set to True
    :return: list of file paths
    """
    try:
        # this is a workaround when using under worktree
        # if you're using worktree, when running git commit a new environment variable GIT_DIR would be declared,
        # the value should be <origin_repo_path>/.git/worktrees/<worktree name>
        # This would affect the return value of `git ls-files`, unset this would use the `cwd`value or its parent
        # folder if no `.git` folder found in `cwd`.
        workaround_env = os.environ.copy()
        workaround_env.pop('GIT_DIR', None)
        files = (
            subprocess.check_output(['git', 'ls-files'], cwd=path, env=workaround_env)
            .decode('utf8')
            .strip()
            .split('\n')
        )
    except Exception as e:  # pylint: disable=W0703
        logging.warning(str(e))
        files = []
    return [os.path.join(path, f) for f in files] if full_path else files


def to_list(s: t.Any) -> t.List[t.Any]:
    if not s:
        return []

    if isinstance(s, (set, tuple)):
        return list(s)

    if isinstance(s, list):
        return s

    return [s]


class GitlabYmlConfig:
    def __init__(self, root_yml_filepath: str = os.path.join(IDF_PATH, '.gitlab-ci.yml')) -> None:
        self._config: t.Dict[str, t.Any] = {}
        self._defaults: t.Dict[str, t.Any] = {}

        self._load(root_yml_filepath)

    def _load(self, root_yml_filepath: str) -> None:
        # avoid unused import in other pre-commit hooks
        import yaml

        all_config = dict()
        root_yml = yaml.load(open(root_yml_filepath), Loader=yaml.FullLoader)
        for item in root_yml['include']:
            all_config.update(yaml.load(open(os.path.join(IDF_PATH, item)), Loader=yaml.FullLoader))

        if 'default' in all_config:
            self._defaults = all_config.pop('default')

        self._config = all_config

    @property
    def default(self) -> t.Dict[str, t.Any]:
        return self._defaults

    @property
    def config(self) -> t.Dict[str, t.Any]:
        return self._config

    @cached_property
    def global_keys(self) -> t.List[str]:
        return ['default', 'include', 'workflow', 'variables', 'stages']

    @cached_property
    def anchors(self) -> t.Dict[str, t.Any]:
        return {k: v for k, v in self.config.items() if k.startswith('.')}

    @cached_property
    def jobs(self) -> t.Dict[str, t.Any]:
        return {k: v for k, v in self.config.items() if not k.startswith('.') and k not in self.global_keys}

    @cached_property
    def rules(self) -> t.Set[str]:
        return {k for k, _ in self.anchors.items() if self._is_rule_key(k)}

    @cached_property
    def used_rules(self) -> t.Set[str]:
        res = set()

        for v in self.config.values():
            if not isinstance(v, dict):
                continue

            for item in to_list(v.get('extends')):
                if self._is_rule_key(item):
                    res.add(item)

        return res

    @staticmethod
    def _is_rule_key(key: str) -> bool:
        return key.startswith('.rules:') or key.endswith('template')


def get_all_manifest_files() -> t.List[str]:
    """

    :rtype: object
    """
    paths: t.List[str] = []

    for p in Path(IDF_PATH).glob('**/.build-test-rules.yml'):
        if 'managed_components' in p.parts:
            continue

        paths.append(str(p))

    return paths
