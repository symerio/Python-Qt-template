sdist:
	make stamp; make release_notes; python setup.py sdist --formats=zip; 

stamp:
	sed -i '$$ d' tagui/__init__.py ; sed -i '$$ d' tagui/__init__.py ; echo '__version_date__ = "'`git log --pretty=format:'%cd' -n 1`'"' >> tagui/__init__.py; echo '__version_hash__ = "'`git log --pretty=format:'%h' -n 1`'"' >> tagui/__init__.py

release_notes:
	echo "## tagui: release notes" > release_notes.md
	git log --pretty=format:" - [\`%h\`] *%ai*%n%n   - %s%n  %b" >> RELEASE.md

test2: 
	python2 /usr/bin/nosetests -s tagui --with-coverage --cover-package=tagui
test3: 
	python3 /usr/bin/nosetests -s tagui --with-coverage --cover-package=tagui
