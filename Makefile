sdist:
	make stamp; python setup.py sdist --formats=zip; 

stamp:
	sed -i '$$ d' gui_template/__init__.py ; sed -i '$$ d' gui_template/__init__.py ; echo '__version_date__ = "'`git log --pretty=format:'%cd' -n 1`'"' >> gui_template/__init__.py; echo '__version_hash__ = "'`git log --pretty=format:'%h' -n 1`'"' >> gui_template/__init__.py
