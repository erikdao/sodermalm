import os
from subprocess import check_output


def _get_git_revision(path):
    if not os.path.exists(os.path.join(path, 'git')):
        return None
    try:
        revision = check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=path, env=os.environ)
    except Exception:
        return None
    return revision.decode('utf-8').strip()


def get_revision():
    """
    Returns the revision number of this checkout/branch if possible
    """
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(
        os.path.join(package_dir, os.pardir, os.pardir))
    path = os.path.join(checkout_dir)
    if os.path.exists(path):
        return _get_git_revision(path)
    return None


__build__ = get_revision()
