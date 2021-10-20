clean:
	rm -f dist/*
	rm -rf esper_tool.egg-info

upload:
	rm -f dist/*
	python3 -m build
	python3 -m twine upload dist/*

upgrade:
	pip install -U esper-tool