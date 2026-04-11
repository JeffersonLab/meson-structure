# -------------  CMakeLists.txt  -----------------
cmake_minimum_required(VERSION 3.18)
project(edm4hep_mcpart_lambda LANGUAGES CXX)

# ----- compiler settings ------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# -----------------------------------------------------------------------------#
#  Dependencies                                                                #
# -----------------------------------------------------------------------------#

find_package(ROOT REQUIRED COMPONENTS Core RIO Tree Hist Gpad)
find_package(podio CONFIG REQUIRED)
find_package(EDM4HEP CONFIG REQUIRED)
find_package(EDM4EIC CONFIG REQUIRED)
find_package(fmt REQUIRED)

# -----------------------------------------------------------------------------#
#  Build executable                                                            #
# -----------------------------------------------------------------------------#

add_executable(mcpart_lambda mcpart_lambda.cxx)

target_link_libraries(mcpart_lambda
        PRIVATE
        ROOT::Core ROOT::RIO ROOT::Tree ROOT::Hist ROOT::Gpad
        podio::podio podio::podioRootIO podio::podioDict
        EDM4HEP::edm4hep EDM4HEP::edm4hepDict
        EDM4EIC::edm4eic EDM4EIC::edm4eicDict
        fmt::fmt)

add_executable(acceptance acceptance.cxx)

target_link_libraries(acceptance
        PRIVATE
        ROOT::Core ROOT::RIO ROOT::Tree ROOT::Hist ROOT::Gpad
        podio::podio podio::podioRootIO podio::podioDict
        EDM4HEP::edm4hep EDM4HEP::edm4hepDict
        EDM4EIC::edm4eic EDM4EIC::edm4eicDict
        fmt::fmt)
