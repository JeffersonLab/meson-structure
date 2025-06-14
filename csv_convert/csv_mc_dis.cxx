// only inside the ROOT prompt / root -x
#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include "podio/ROOTWriter.h"

#include <edm4hep/MCParticleCollection.h>

#include <fmt/core.h>
#include <fmt/format.h>

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>

// Global variables for analysis configuration
int events_limit = -1;  // -1 means process all events
int total_evt_counter = 0;
std::ofstream csv_file;
bool header_written = false;

// Function declarations
void print_usage(const char* program_name);
void process_file(const std::string& filename);
void process_event(const podio::Frame& event, int event_number);

int main(int argc, char* argv[]) {
    // Simple argument parsing - collect files and look for -n and -o option
    std::vector<std::string> input_files;
    std::string output_file = "dis_parameters.csv";

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-n" && i + 1 < argc) {
            events_limit = std::atoi(argv[++i]);
            fmt::print("Event limit set to: {}\n", events_limit);
        } else if (arg == "-o" && i + 1 < argc) {
            output_file = argv[++i];
        } else if (arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            return 0;
        } else if (arg[0] != '-') {
            input_files.push_back(arg);
        } else {
            fmt::print("Unknown option: {}\n", arg);
            print_usage(argv[0]);
            return 1;
        }
    }

    // Check if we have input files
    if (input_files.empty()) {
        fmt::print("Error: No input files provided\n");
        print_usage(argv[0]);
        return 1;
    }

    // Open CSV file
    csv_file.open(output_file);
    if (!csv_file) {
        fmt::print("Error: Cannot open output file {}\n", output_file);
        return 1;
    }

    // Process each file
    fmt::print("Processing {} file(s)\n", input_files.size());
    for (const auto& filename : input_files) {
        fmt::print("\n=== Processing file: {} ===\n", filename);
        process_file(filename);

        // Check if we've reached the event limit
        if (events_limit > 0 && total_evt_counter >= events_limit) {
            fmt::print("\nReached event limit of {}, stopping.\n", events_limit);
            break;
        }
    }

    csv_file.close();
    fmt::print("\nTotal events processed: {}\n", total_evt_counter);
    fmt::print("DIS parameters written to: {}\n", output_file);
    return 0;
}

void print_usage(const char* program_name) {
    fmt::print("Usage: {} [options] file1.root [file2.root ...]\n", program_name);
    fmt::print("Options:\n");
    fmt::print("  -n <number>  Process only <number> events (default: all)\n");
    fmt::print("  -o <file>    Output CSV file (default: dis_parameters.csv)\n");
    fmt::print("  -h           Show this help message\n");
    fmt::print("\nNote: Options and files can be mixed in any order\n");
    fmt::print("Example: {} file1.root -n 100 file2.root file3.root\n", program_name);
}

void process_file(const std::string& filename) {
    try {
        // Open the ROOT file
        auto reader = podio::ROOTReader();
        reader.openFile(filename);

        // Get nevents
        const auto nEvents = reader.getEntries(podio::Category::Event);
        fmt::print("File contains {} events\n", nEvents);

        // Process events
        for (unsigned i = 0; i < nEvents; ++i) {
            // Check event limit
            if (events_limit > 0 && total_evt_counter >= events_limit) {
                break;
            }

            // Read event
            auto event = podio::Frame(reader.readNextEntry(podio::Category::Event));

            // For the first event we show event level parameters
            if (i==0) {
                const auto& cols = event.getParameterKeys<std::string>();
                fmt::print("===== Parameters for the first event =====\n");
                for (const auto& col : cols) {
                    fmt::print("  {} {}\n", col, event.getParameter<std::string>(col).value_or("None"));
                }
                fmt::print("===========================================\n");
            }
            process_event(event, total_evt_counter);
            total_evt_counter++;
        }
    } catch (const std::exception& e) {
        fmt::print("Error processing file {}: {}\n", filename, e.what());
    }
}

void process_event(const podio::Frame& event, int event_number) {
    // Write CSV header once
    if (!header_written) {
        csv_file << "evt,alphas,mx2,nu,p_rt,pdrest,pperps,pperpz,q2,s_e,s_q,tempvar,tprime,tspectator,twopdotk,twopdotq,w,x_d,xbj,y_d,yplus\n";
        header_written = true;
    }

    // Write event data
    csv_file << event_number << ","
             << event.getParameter<std::string>("dis_alphas").value_or("") << ","
             << event.getParameter<std::string>("dis_mx2").value_or("") << ","
             << event.getParameter<std::string>("dis_nu").value_or("") << ","
             << event.getParameter<std::string>("dis_p_rt").value_or("") << ","
             << event.getParameter<std::string>("dis_pdrest").value_or("") << ","
             << event.getParameter<std::string>("dis_pperps").value_or("") << ","
             << event.getParameter<std::string>("dis_pperpz").value_or("") << ","
             << event.getParameter<std::string>("dis_q2").value_or("") << ","
             << event.getParameter<std::string>("dis_s_e").value_or("") << ","
             << event.getParameter<std::string>("dis_s_q").value_or("") << ","
             << event.getParameter<std::string>("dis_tempvar").value_or("") << ","
             << event.getParameter<std::string>("dis_tprime").value_or("") << ","
             << event.getParameter<std::string>("dis_tspectator").value_or("") << ","
             << event.getParameter<std::string>("dis_twopdotk").value_or("") << ","
             << event.getParameter<std::string>("dis_twopdotq").value_or("") << ","
             << event.getParameter<std::string>("dis_w").value_or("") << ","
             << event.getParameter<std::string>("dis_x_d").value_or("") << ","
             << event.getParameter<std::string>("dis_xbj").value_or("") << ","
             << event.getParameter<std::string>("dis_y_d").value_or("") << ","
             << event.getParameter<std::string>("dis_yplus").value_or("") << "\n";
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'csv_mc_dis.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_mc_dis(const char* infile, const char* outfile = "dis_parameters.csv", int events = -1) {

    fmt::print("'csv_mc_dis' entry point is used. Arguments:\n");
    fmt::print("  infile:  {}\n", infile);
    fmt::print("  outfile: {}\n", outfile);
    fmt::print("  events:  {} {}\n", events, (events == -1 ? "(process all)" : ""));

    csv_file.open(outfile);
    if (!csv_file) {
        fmt::print("Error: Cannot open output file {}\n", outfile);
        return;
    }

    events_limit = events;
    total_evt_counter = 0;
    header_written = false;

    process_file(infile);

    csv_file.close();
    fmt::print("\nTotal events processed: {}\n", total_evt_counter);
    fmt::print("DIS parameters written to: {}\n", outfile);
}