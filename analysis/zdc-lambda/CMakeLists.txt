# -------------  CMakeLists.txt  -----------------
cmake_minimum_required(VERSION 3.18)
project(cpp_meson_structure LANGUAGES CXX)

# ----- compiler settings ------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# -----------------------------------------------------------------------------#
#  Dependencies                                                                #
# -----------------------------------------------------------------------------#

find_package(ROOT REQUIRED COMPONENTS Core RIO Tree Hist Gpad Graf)
find_package(podio CONFIG REQUIRED)
find_package(EDM4HEP CONFIG REQUIRED)
find_package(EDM4EIC CONFIG REQUIRED)

# -----------------------------------------------------------------------------#
#  Build executable                                                            #
# -----------------------------------------------------------------------------#
add_executable(e01_edm4hep test_edm4eic.cxx)

target_link_libraries(e01_edm4hep
        PRIVATE
        ROOT::Core ROOT::RIO ROOT::Tree ROOT::Hist ROOT::Gpad
        podio::podio podio::podioRootIO
        EDM4HEP::edm4hep
        EDM4EIC::edm4eic)
