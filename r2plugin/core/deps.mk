R2AI_CORE_WD=$(LIBR)/xps/p/r2ai
CFLAGS+=-I$(R2AI_CORE_WD)/src
R2AI_CORE_OBJ= \
	$(R2AI_CORE_WD)/src/anthropic.o \
	$(R2AI_CORE_WD)/src/apikeys.o \
	$(R2AI_CORE_WD)/src/async.o \
	$(R2AI_CORE_WD)/src/auto.o \
	$(R2AI_CORE_WD)/src/claw.o \
	$(R2AI_CORE_WD)/src/gemini.o \
	$(R2AI_CORE_WD)/src/http.o \
	$(R2AI_CORE_WD)/src/json.o \
	$(R2AI_CORE_WD)/src/llm.o \
	$(R2AI_CORE_WD)/src/markdown.o \
	$(R2AI_CORE_WD)/src/messages.o \
	$(R2AI_CORE_WD)/src/openai.o \
	$(R2AI_CORE_WD)/src/query.o \
	$(R2AI_CORE_WD)/src/r2ai.o \
	$(R2AI_CORE_WD)/src/rawtools.o \
	$(R2AI_CORE_WD)/src/tools.o \
	$(R2AI_CORE_WD)/src/vdb.o \
	$(R2AI_CORE_WD)/src/vertex.o \
	$(R2AI_CORE_WD)/src/wizard.o
EXTERNAL_STATIC_OBJS+=$(R2AI_CORE_OBJ)
