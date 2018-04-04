# vim:fileencoding=utf-8:
# <http://www.sphinx-doc.org/en/stable/config.html#confval-extensions>
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.intersphinx',
	'sphinx.ext.viewcode',
	'sphinx.ext.coverage',
]
master_doc = 'index'
source_suffix = '.rst'

project = 'Univention Updater'
copyright = '2005-2018, Philipp Hahn'
author = 'Philipp Hahn'
version = '1'
release = '13.0.1'

highlight_language = 'python'
language = 'en'
master_doc = 'modules'

intersphinx_mapping = {
	'python': ('https://docs.python.org/2.7', ('file:///usr/share/doc/python2.7/html/objects.inv', None)),
	# 'apt': ('', ('file:///usr/share/doc/python-apt-doc/html/objects.inv', None)),
	# 'configparser': ('', ('file:///usr/share/doc/python-configparser/html/objects.inv', None)),
	# 'git': ('', ('file:///usr/share/doc/python-git-doc/html/objects.inv', None)),
	# 'mock': ('', ('file:///usr/share/doc/python-mock-doc/html/objects.inv', None)),
	# 'mockldap': ('', ('file:///usr/share/doc/python-mockldap-doc/html/objects.inv', None)),
	# 'pexcpect': ('', ('file:///usr/share/doc/python-pexpect-doc/html/objects.inv', None)),
	# 'sphinx': ('', ('file:///usr/share/doc/sphinx-doc/html/objects.inv', None)),
	# 'tox': ('', ('file:///usr/share/doc/tox/html/objects.inv', None)),
}

html_theme = 'default'

autodoc_default_flags = [
	'members',
	'undoc-members',
	'private-members',
	# 'special-members',
	# 'inherited-members',
	'show-inheritance',
]
# autodoc_mock_imports =
