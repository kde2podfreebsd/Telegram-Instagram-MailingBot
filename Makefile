pre_commit:
	 pre-commit run --all-files

pre_commit_flake8:
	pre-commit run flake8 --all-files

clean:
	find . -name __pycache__ -type d -print0|xargs -0 rm -r --
	rm -rf .idea/

fix_git_cache:
	git rm -rf --cached .
	git add .