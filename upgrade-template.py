#!/usr/bin/env python3

"""
Dependencies:
cookiecutter

Usage:
This needs to be run in the root of the project you are upgrading.
The template branch needs to be in your local repo, but must not be active/checked out. (git doesn't like this)
"""

import argparse
import json
import subprocess
import shutil
import os
import tempfile
from os import listdir
from os.path import join, exists, isdir, abspath, basename


from cookiecutter.generate import generate_files
from cookiecutter.main import prompt_for_config, generate_context


def load_context(path):
    if not exists(path):
        return None

    with open(path, 'r') as infile:
        context = json.load(infile)

    return context


def dump_context(path, context):
    with open(path, 'w') as outfile:
        json.dump(context, outfile, sort_keys=True, indent=4)


def get_or_create_context(template_context_path, context_path):
    template_context = generate_context(context_file=template_context_path)
    ask_config = not exists(context_path)

    context = None  # not necessary but PyCharm likes to complain

    if not ask_config:
        context = load_context(context_path)

        if 'cookiecutter' not in context:
            print('Invalid context file, regenerating')
            ask_config = True

        template_keys = set(template_context['cookiecutter'].keys())
        context_keys = set(context['cookiecutter'].keys())

        if template_keys != context_keys:
            print('Context keys mismatch, regenerating')
            print('Template keys:', template_keys)
            print('Existing keys:', context_keys)
            ask_config = True

    if ask_config:
        context = {'cookiecutter': prompt_for_config(template_context)}

    return context, ask_config


def get_stdout_lines(cmd):
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode().split('\n')
    output = [line.strip() for line in output]
    return output


class Git:
    def get_version(self, repo_path):
        cmd = 'cd {path} && git rev-parse HEAD'.format(path=repo_path)
        return get_stdout_lines(cmd)[0]

    def has_branch(self, branch):
        return branch in get_stdout_lines('git branch')

    def clone(self, **kwargs):
        cmd = 'git clone -b {branch} "{source}" "{target}"'.format(**kwargs)
        return 'done.' in get_stdout_lines(cmd)

    def add_all(self, repo_path):
        cmd = 'cd {path} && git add -A'.format(path=repo_path)
        get_stdout_lines(cmd)

    def commit_all(self, repo_path, message="Template auto-update"):
        cmd = 'cd {path} && git commit -a -m "{message}"'.format(path=repo_path, message=message)
        get_stdout_lines(cmd)

    def push(self, repo_path, branch=None):
        cmd = 'cd {path} && git push origin{branch}'.format(
            path=repo_path, branch=' {}'.format(branch) if branch else ''
        )
        get_stdout_lines(cmd)

    def has_changes(self, repo_path):
        output = get_stdout_lines('cd {path} && git status -s'.format(path=repo_path))
        return output


class Mercurial:
    def get_version(self, repo_path):
        cmd = 'cd {path} && hg id -n && hg id -i'.format(path=repo_path)
        rev, rev_hash = get_stdout_lines(cmd)[:-1]
        return '{rev} ({hash})'.format(rev=rev, hash=rev_hash)

    def has_branch(self, branch):
        return branch in [x.split()[0] for x in get_stdout_lines('hg branches') if x]

    def clone(self, **kwargs):
        cmd = 'hg clone "{source}" "{target}" -r {branch}'.format(**kwargs)
        return get_stdout_lines(cmd)

    def add_all(self, repo_path):
        cmd = 'cd {path} && hg addremove'.format(path=repo_path)
        get_stdout_lines(cmd)

    def commit_all(self, repo_path, message="Template auto-update"):
        cmd = 'cd {path} && hg commit -m "{message}"'.format(path=repo_path, message=message)
        get_stdout_lines(cmd)

    def push(self, repo_path, branch=None):
        cmd = 'cd {path} && hg push'.format(path=repo_path)
        get_stdout_lines(cmd)

    def has_changes(self, repo_path):
        output = get_stdout_lines('cd {path} && hg summary'.format(path=repo_path))
        return 'commit: (clean)' not in output


def get_vcs(path):
    if isdir(join(path, '.git')):
        return Git()
    elif isdir(join(path, '.hg')):
        return Mercurial()
    return None


def update_template(path, template_path, tmp_dir):
    vcs = get_vcs(path)
    assert vcs, "Couldn't detect VCS in \"{}\", are you sure you have the right path?".format(path)

    template_vcs = get_vcs(template_path)
    template_version = template_vcs.get_version(template_path) if template_vcs else None

    project_name = basename(abspath(path))
    tmp_path = join(tmp_dir, project_name)

    assert vcs.has_branch('template'), "Template branch does not exist or is active (checkout a different branch)"
    assert not isdir(tmp_path), "Can't clone temporary repo, target directory \"{}\" isn't empty".format(tmp_path)

    vcs.clone(source=path, target=tmp_path, branch='template')

    # clean up everything except for VCS directories and cookiecutter config
    for f in listdir(tmp_path):
        if f in ['.git', '.hg', '.cookiecutterrc']:
            continue
        real_path = join(tmp_path, f)
        if isdir(real_path):
            shutil.rmtree(join(tmp_path, f))
        else:
            os.remove(real_path)

    # find or create cookiecutter context
    template_context_path = join(template_path, 'cookiecutter.json')
    context_path = join(path, '.cookiecutterrc')

    # prompt if necessary
    context, created = get_or_create_context(template_context_path, context_path)
    if created:
        dump_context(join(tmp_path, '.cookiecutterrc'), context)

    generate_files(
        repo_dir=template_path,
        context=context,
        overwrite_if_exists=True,
        output_dir=tmp_dir,
    )

    vcs.add_all(tmp_path)

    assert vcs.has_changes(tmp_path), "No changes found, your template branch is up to date"

    commit_msg = "Upgrade template"
    if template_vcs:
        commit_msg = "Upgrade template to {}".format(template_version)

    vcs.commit_all(tmp_path, message=commit_msg)
    vcs.push(tmp_path, branch='template')


if __name__ == '__main__':
    template_path = os.path.dirname(__file__)

    try:
        with tempfile.TemporaryDirectory() as tmp:
            update_template('.', template_path, tmp)

        print('Great! An upgrade commit was pushed to your template branch.')
        print('Now all you need to do is merge the template branch into your main branch (be it master, a feature '
              'branch, etc), fix any merge conflicts and commit.')
    except AssertionError as e:
        print('Did not upgrade: ' + ' '.join(e.args))
