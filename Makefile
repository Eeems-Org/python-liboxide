define SCRIPT
if ! type pip &> /dev/null; then
    if ! type opkg &> /dev/null; then
        echo "Opkg not found, please install toltec"
        exit 1
    fi
    opkg update
    opkg install python3-pip
fi
pip install /tmp/liboxide-0.0.1.tar.gz
endef
export SCRIPT

dist/liboxide-0.0.1.tar.gz:
	python -m build --sdist

clean:
	git clean --force -dX

/tmp/liboxide-0.0.1.tar.gz: dist/liboxide-0.0.1.tar.gz
	rsync dist/liboxide-0.0.1.tar.gz root@10.11.99.1:/tmp

install: /tmp/liboxide-0.0.1.tar.gz
	echo -e "$$SCRIPT" | ssh root@10.11.99.1 bash -le

test: install
	cat test.py | ssh root@10.11.99.1 /opt/bin/python

.PHONY: clean install test /tmp/liboxide-0.0.1.tar.gz
