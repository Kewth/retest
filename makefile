init:
	cp retest.py retest
	chmod +x retest

install:
	sudo cp retest /usr/bin
	rm retest
