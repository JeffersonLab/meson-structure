#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include "podio/ROOTWriter.h"

#include <edm4hep/MCParticleCollection.h>

#include <iostream>
#include <string>

void readCollection() {
  // Start reading the input
  auto reader = podio::ROOTReader();
  reader.openFile("associations.root");

  const auto nEvents = reader.getEntries(podio::Category::Event);

  for (unsigned i = 0; i < 5; ++i) {
    auto store = podio::Frame(reader.readNextEntry(podio::Category::Event));

    auto& mcParticles = store.get<edm4hep::MCParticleCollection>("MCParticles");
    for (const auto& particle : mcParticles) {
        std::cout << particle.getPDG() << std::endl;
    }
    // if (clusters.isValid()) {
    //   for (const auto& cluster : clusters) {
    //     if (cluster.isAvailable()) {
    //       for (const auto& hit : cluster.Hits()) {
    //         if (hit.isAvailable()) {
    //           throw std::runtime_error("Hit is available, although it has not been written");
    //         }
    //       }
    //     }
    //   }
    // } else {
    //   throw std::runtime_error("Collection 'clusters' should be present");
    // }
    //
    // // Test for subset collections
    // auto& hits_subset = store.get<ExampleHitCollection>("hits_subset");
    // if (hits_subset.isValid()) {
    //   if (!hits_subset.isSubsetCollection()) {
    //     throw std::runtime_error("hits_subset should be a subset collection");
    //   }
    //
    //   if (hits_subset.size() != 2) {
    //     throw std::runtime_error("subset collection should have original size");
    //   }
    //
    //   for (const auto& hit : hits_subset) {
    //     if (hit.isAvailable()) {
    //       throw std::runtime_error("Hit is available, although it has not been written");
    //     }
    //   }
    // } else {
    //   throw std::runtime_error("Collection 'hits_subset' should be present");
    // }
  }
}

int main() {

  readCollection();

  return 0;
}