define SCRIPT
if ! type pip &> /dev/null; then
    if ! type opkg &> /dev/null; then
        echo "Opkg not found, please install toltec"
        exit 1
    fi
    opkg update
    opkg install python3-pip
fi
pip install --force-reinstall /tmp/liboxide-0.0.1-py3-none-any.whl
endef
export SCRIPT

dist/liboxide-0.0.1.tar.gz: $(shell find liboxide -type f)
	python -m build --sdist

dist/liboxide-0.0.1-py3-none-any.whl: $(shell find liboxide -type f)
	python -m build --wheel

clean:
	git clean --force -dX

deploy: dist/liboxide-0.0.1-py3-none-any.whl
	rsync dist/liboxide-0.0.1-py3-none-any.whl root@10.11.99.1:/tmp

install: deploy
	echo -e "$$SCRIPT" | ssh root@10.11.99.1 bash -le

test: install
	cat test.py | ssh root@10.11.99.1 /opt/bin/python

.PHONY: clean install test deploy
