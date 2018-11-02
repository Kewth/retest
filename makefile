compile:
	cp retest.py retest
	chmod +x retest

install:
	mkdir ~/.config/retest -p
	touch ~/.config/retest/file.txt
	sudo mv retest /usr/bin

reinstall:
	cp retest.py retest
	chmod +x retest
	cp retest.py retest
	chmod +x retest
	sudo mv retest /usr/bin

uninstall:
	sudo rm /usr/bin/retest
