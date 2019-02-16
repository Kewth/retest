/usr/bin/ntest: neo.py ninit
	sudo cp neo.py /usr/bin/ntest
	sudo chmod +x /usr/bin/ntest

ninit: ~/.config ~/.config/retest
	cp retest.yaml ~/.config/retest
	cp spj ~/.config/retest
	cp -r plugin ~/.config/retest
	touch ninit

~/.config:
	mkdir ~/.config -p

~/.config/retest:
	mkdir ~/.config/retest -p

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
