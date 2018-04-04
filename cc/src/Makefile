CC = g++
WARNINGS = -Wall -Wextra -Wno-unused-result -Wcast-qual
OPT_FLAGS = -O2 -flto
CFLAGS = $(WARNINGS) -Werror -std=c++11 -pedantic
LFLAGS =
SRC_DIR = ./  # src/
OBJ_DIR = ./  # obj/
EMSCRIPTEN_SRC = $(SRC_DIR)program_js.cc
SRCS = $($(wildcard $(SRC_DIR)*.cc))
OBJS = $(addprefix $(OBJ_DIR),$(notdir $(SRCS:.cc=.o)))
EXECUTABLE = quiver
MKDIR_P = mkdir -p



main: main.cc truco-player.cc truco-player.h
	clang++ -o main main.cc
