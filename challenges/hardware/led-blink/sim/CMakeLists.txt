cmake_minimum_required(VERSION 3.25)

project(led-blink)

file(GLOB CSources ./src/*.c)
add_library(ctfavrsim SHARED ${CSources})
target_include_directories(ctfavrsim PUBLIC include)

# Get simavr
find_library(SIMAVR_DIR simavr libs/simavr/lib)
target_include_directories(ctfavrsim PUBLIC libs/simavr/include/simavr)
target_link_libraries(ctfavrsim ${SIMAVR_DIR})