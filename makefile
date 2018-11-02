install: retest.py
	cp retest.py retest
	chmod +x retest
	mkdir ~/.config -p
	mkdir ~/.config/retest -p
	touch ~/.config/retest/file.txt
	sudo mv retest /usr/bin

reinstall: retest.py
	cp retest.py retest
	chmod +x retest
	sudo mv retest /usr/bin

clean:
	rm retest

clear: clean
	rm retest
