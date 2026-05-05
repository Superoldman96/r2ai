# r2ai XPS integration for radare2.
# Included from libr/xps/meson.build when r2ai sources live under
# libr/xps/p/r2ai/. Appends sources and include paths to the r_core
# aggregate so the static plugin is linked into libr_core.

core_plugins += ['r2ai']

r_core_additional_inc += include_directories(join_paths('..', 'src'))

r_core_additional_sources += files(
  '../src/anthropic.c',
  '../src/apikeys.c',
  '../src/async.c',
  '../src/auto.c',
  '../src/claw.c',
  '../src/gemini.c',
  '../src/http.c',
  '../src/json.c',
  '../src/llm.c',
  '../src/markdown.c',
  '../src/messages.c',
  '../src/openai.c',
  '../src/query.c',
  '../src/r2ai.c',
  '../src/rawtools.c',
  '../src/tools.c',
  '../src/vdb.c',
  '../src/vertex.c',
  '../src/wizard.c',
)
