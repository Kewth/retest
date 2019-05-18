/usr/bin/ntest: neo.py ninit pip_lock atest
	sudo cp neo.py /usr/bin/retest
	sudo chmod +x /usr/bin/retest

~/.local/bin/ntest: neo.py ninit pip_lock
	cp neo.py ~/.local/bin/retest
	chmod +x ~/.local/bin/retest

ninit: ~/.config ~/.config/retest plugin retest.yaml spj
	cp retest.yaml ~/.config/retest
	cp spj ~/.config/retest
	cp -r plugin ~/.config/retest
	touch ninit

~/.config:
	mkdir ~/.config -p

~/.config/retest:
	mkdir ~/.config/retest -p

pip_lock:
	sudo apt install python3-pip
	pip3 install colorama
	pip3 install argparse
	pip3 install pyyaml
	touch pip_lock

atest:
	sudo cp extra/atest /usr/bin/atest
	sudo chmod +x /usr/bin/atest
