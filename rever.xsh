$PROJECT = $GITHUB_REPO = 'pygments-cache'
$GITHUB_ORG = 'xonsh'

$ACTIVITIES = ['version_bump', 'changelog',
               'tag', 'push_tag', 'pypi',
               'ghrelease']

$VERSION_BUMP_PATTERNS = [
    ('pygments_cache.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'VERSION\s*=.*', "VERSION = '$VERSION'")
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
