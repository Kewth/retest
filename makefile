/usr/bin/retest: retest init
	sudo cp retest /usr/bin

init: ~/.config ~/.config/retest
	mkdir ~/.config -p
	mkdir ~/.config/retest -p
	touch ~/.config/retest/file.txt
	touch init

retest: retest.py
	cp retest.py retest
	chmod +x retest

uninstall: clean
	sudo rm /usr/bin/retest

clean:
	rm retest
	rm init
