.PHONY: test dev prod shell create_module __phony_dummy__

# Extract the module name from the command-line goals
# `firstword` gets the first target (create_module)
# `wordlist` gets all targets from the second one onwards
# `words` counts the total number of words in the goals
MODULE_NAME := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

# A general catch-all phony rule for targets without a specific recipe.
# It depends on a phony dummy target to prevent the "up to date" message.
%:: __phony_dummy__
	@true

__phony_dummy__:
	@true

create_module:
ifeq ($(MODULE_NAME),)
	@echo "Error: You must provide a module name. Usage: make create_module <module_name>"
	@exit 1
else
	@echo "Creating module: $(MODULE_NAME)"
	@mkdir -p $(MODULE_NAME)
	@touch $(MODULE_NAME)/__init__.py
	@touch $(MODULE_NAME)/models.py
	@touch $(MODULE_NAME)/views.py
	@touch $(MODULE_NAME)/test_$(MODULE_NAME).py
	@mkdir -p $(MODULE_NAME)/tests
endif

test:
ifeq ($(MODULE_NAME),)
	@pipenv run pytest .
else
	@pipenv run pytest $(MODULE_NAME)
endif

dev:
	@pipenv run fastapi dev main.py --host 0.0.0.0 --port 8000

prod:
	@pipenv run fastapi run main.py

shell:
	@pipenv shell
