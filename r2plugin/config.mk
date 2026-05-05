EXTERNAL_PLUGINS+=r2ai
# EXTERNAL_PLUGINS+=hi

.PHONY: r2ai

r2ai: p/r2ai

p/r2ai:
	cd p && git clone https://github.com/radareorg/r2ai
