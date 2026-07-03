# Edm4Hep EIC tree

This format is used for DD4HEP (Geant4) simulation outputs prior the reconstruction

```
📁 msf_5x41_1000evt_0740.edm4hep.root
┣━━ 🌴 events (1000)
┃   ┣━━ 🌿 B0ECalHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 B0ECalHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 B0ECalHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalHits.energy float[]
┃   ┃   ┣━━ 🍃 B0ECalHits.position.x float[]
┃   ┃   ┣━━ 🍃 B0ECalHits.position.y float[]
┃   ┃   ┗━━ 🍃 B0ECalHits.position.z float[]
┃   ┣━━ 🌿 B0ECalHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 B0ECalHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 B0ECalHitsContributions.time float[]
┃   ┣━━ 🌿 B0TrackerHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 B0TrackerHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.eDep float[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.pathLength float[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.position.x double[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.position.y double[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.position.z double[]
┃   ┃   ┣━━ 🍃 B0TrackerHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerHits.time float[]
┃   ┣━━ 🌿 BackwardMPGDEndcapHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.eDep float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.pathLength float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.position.x double[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.position.y double[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.position.z double[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 BackwardMPGDEndcapHits.time float[]
┃   ┣━━ 🌿 DIRCBarHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 DIRCBarHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.eDep float[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.pathLength float[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.position.x double[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.position.y double[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.position.z double[]
┃   ┃   ┣━━ 🍃 DIRCBarHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 DIRCBarHits.time float[]
┃   ┣━━ 🌿 DRICHHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 DRICHHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 DRICHHits.eDep float[]
┃   ┃   ┣━━ 🍃 DRICHHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 DRICHHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 DRICHHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 DRICHHits.pathLength float[]
┃   ┃   ┣━━ 🍃 DRICHHits.position.x double[]
┃   ┃   ┣━━ 🍃 DRICHHits.position.y double[]
┃   ┃   ┣━━ 🍃 DRICHHits.position.z double[]
┃   ┃   ┣━━ 🍃 DRICHHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 DRICHHits.time float[]
┃   ┣━━ 🌿 EcalBarrelImagingHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingHits.position.z float[]
┃   ┣━━ 🌿 EcalBarrelImagingHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingHitsContributions.time float[]
┃   ┣━━ 🌿 EcalBarrelScFiHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiHits.position.z float[]
┃   ┣━━ 🌿 EcalBarrelScFiHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiHitsContributions.time float[]
┃   ┣━━ 🌿 EcalEndcapNHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNHits.position.z float[]
┃   ┣━━ 🌿 EcalEndcapNHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNHitsContributions.time float[]
┃   ┣━━ 🌿 EcalEndcapPHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPHits.position.z float[]
┃   ┣━━ 🌿 EcalEndcapPHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPHitsContributions.time float[]
┃   ┣━━ 🌿 EcalFarForwardZDCHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCHits.position.z float[]
┃   ┣━━ 🌿 EcalFarForwardZDCHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCHitsContributions.time float[]
┃   ┣━━ 🌿 EcalLumiSpecHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecHits.position.z float[]
┃   ┣━━ 🌿 EcalLumiSpecHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecHitsContributions.time float[]
┃   ┣━━ 🌿 EventHeader vector<edm4hep::EventHeaderData>
┃   ┃   ┣━━ 🍃 EventHeader.eventNumber uint64_t[]
┃   ┃   ┣━━ 🍃 EventHeader.runNumber uint32_t[]
┃   ┃   ┣━━ 🍃 EventHeader.timeStamp uint64_t[]
┃   ┃   ┣━━ 🍃 EventHeader.weight double[]
┃   ┃   ┣━━ 🍃 EventHeader.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EventHeader.weights_end uint32_t[]
┃   ┣━━ 🌿 ForwardMPGDEndcapHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.eDep float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.pathLength float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.position.x double[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.position.y double[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.position.z double[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 ForwardMPGDEndcapHits.time float[]
┃   ┣━━ 🌿 ForwardOffMTrackerHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.eDep float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.pathLength float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.position.x double[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.position.y double[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.position.z double[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 ForwardOffMTrackerHits.time float[]
┃   ┣━━ 🌿 ForwardRomanPotHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.eDep float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.pathLength float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.position.x double[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.position.y double[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.position.z double[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 ForwardRomanPotHits.time float[]
┃   ┣━━ 🍁 GPDoubleKeys std::vector<std::string>
┃   ┣━━ 🍁 GPDoubleValues std::vector<std::vector<double>>
┃   ┣━━ 🍁 GPFloatKeys std::vector<std::string>
┃   ┣━━ 🍁 GPFloatValues std::vector<std::vector<float>>
┃   ┣━━ 🍁 GPIntKeys std::vector<std::string>
┃   ┣━━ 🍁 GPIntValues std::vector<std::vector<int32_t>>
┃   ┣━━ 🍁 GPStringKeys std::vector<std::string>
┃   ┣━━ 🍁 GPStringValues std::vector<std::vector<std::string>>
┃   ┣━━ 🌿 HcalBarrelHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHits.position.y float[]
┃   ┃   ┗━━ 🍃 HcalBarrelHits.position.z float[]
┃   ┣━━ 🌿 HcalBarrelHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 HcalBarrelHitsContributions.time float[]
┃   ┣━━ 🌿 HcalEndcapNHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHits.position.y float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNHits.position.z float[]
┃   ┣━━ 🌿 HcalEndcapNHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNHitsContributions.time float[]
┃   ┣━━ 🌿 HcalEndcapPInsertHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHits.position.y float[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertHits.position.z float[]
┃   ┣━━ 🌿 HcalEndcapPInsertHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertHitsContributions.time float[]
┃   ┣━━ 🌿 HcalFarForwardZDCHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHits.position.y float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCHits.position.z float[]
┃   ┣━━ 🌿 HcalFarForwardZDCHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCHitsContributions.time float[]
┃   ┣━━ 🌿 LFHCALHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 LFHCALHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 LFHCALHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALHits.energy float[]
┃   ┃   ┣━━ 🍃 LFHCALHits.position.x float[]
┃   ┃   ┣━━ 🍃 LFHCALHits.position.y float[]
┃   ┃   ┗━━ 🍃 LFHCALHits.position.z float[]
┃   ┣━━ 🌿 LFHCALHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 LFHCALHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 LFHCALHitsContributions.time float[]
┃   ┣━━ 🌿 LumiDirectPCALHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.energy float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.position.x float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHits.position.y float[]
┃   ┃   ┗━━ 🍃 LumiDirectPCALHits.position.z float[]
┃   ┣━━ 🌿 LumiDirectPCALHitsContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.energy float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 LumiDirectPCALHitsContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 LumiDirectPCALHitsContributions.time float[]
┃   ┣━━ 🌿 LumiSpecTrackerHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.eDep float[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.pathLength float[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.position.x double[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.position.y double[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.position.z double[]
┃   ┃   ┣━━ 🍃 LumiSpecTrackerHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 LumiSpecTrackerHits.time float[]
┃   ┣━━ 🌿 MCParticles vector<edm4hep::MCParticleData>
┃   ┃   ┣━━ 🍃 MCParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.charge float[]
┃   ┃   ┣━━ 🍃 MCParticles.daughters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.daughters_end uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.endpoint.x double[]
┃   ┃   ┣━━ 🍃 MCParticles.endpoint.y double[]
┃   ┃   ┣━━ 🍃 MCParticles.endpoint.z double[]
┃   ┃   ┣━━ 🍃 MCParticles.generatorStatus int32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.helicity int32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.mass double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentum.x double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentum.y double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentum.z double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentumAtEndpoint.x double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentumAtEndpoint.y double[]
┃   ┃   ┣━━ 🍃 MCParticles.momentumAtEndpoint.z double[]
┃   ┃   ┣━━ 🍃 MCParticles.parents_begin uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.parents_end uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.simulatorStatus int32_t[]
┃   ┃   ┣━━ 🍃 MCParticles.time float[]
┃   ┃   ┣━━ 🍃 MCParticles.vertex.x double[]
┃   ┃   ┣━━ 🍃 MCParticles.vertex.y double[]
┃   ┃   ┗━━ 🍃 MCParticles.vertex.z double[]
┃   ┣━━ 🌿 MPGDBarrelHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.eDep float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.pathLength float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.position.x double[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.position.y double[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.position.z double[]
┃   ┃   ┣━━ 🍃 MPGDBarrelHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 MPGDBarrelHits.time float[]
┃   ┣━━ 🌿 OuterMPGDBarrelHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.eDep float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.pathLength float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.position.x double[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.position.y double[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.position.z double[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 OuterMPGDBarrelHits.time float[]
┃   ┣━━ 🌿 PFRICHHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 PFRICHHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 PFRICHHits.eDep float[]
┃   ┃   ┣━━ 🍃 PFRICHHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 PFRICHHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 PFRICHHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 PFRICHHits.pathLength float[]
┃   ┃   ┣━━ 🍃 PFRICHHits.position.x double[]
┃   ┃   ┣━━ 🍃 PFRICHHits.position.y double[]
┃   ┃   ┣━━ 🍃 PFRICHHits.position.z double[]
┃   ┃   ┣━━ 🍃 PFRICHHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 PFRICHHits.time float[]
┃   ┣━━ 🌿 SiBarrelHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 SiBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.eDep float[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.pathLength float[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.position.x double[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.position.y double[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.position.z double[]
┃   ┃   ┣━━ 🍃 SiBarrelHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 SiBarrelHits.time float[]
┃   ┣━━ 🌿 TOFBarrelHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.eDep float[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.position.x double[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.position.y double[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.position.z double[]
┃   ┃   ┣━━ 🍃 TOFBarrelHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TOFBarrelHits.time float[]
┃   ┣━━ 🌿 TOFEndcapHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFEndcapHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.eDep float[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.position.x double[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.position.y double[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.position.z double[]
┃   ┃   ┣━━ 🍃 TOFEndcapHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TOFEndcapHits.time float[]
┃   ┣━━ 🌿 TaggerTrackerHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.eDep float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.position.x double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.position.y double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.position.z double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerHits.time float[]
┃   ┣━━ 🌿 TrackerEndcapHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.eDep float[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.position.x double[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.position.y double[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.position.z double[]
┃   ┃   ┣━━ 🍃 TrackerEndcapHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TrackerEndcapHits.time float[]
┃   ┣━━ 🌿 VertexBarrelHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 VertexBarrelHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.eDep float[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.pathLength float[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.position.x double[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.position.y double[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.position.z double[]
┃   ┃   ┣━━ 🍃 VertexBarrelHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 VertexBarrelHits.time float[]
┃   ┣━━ 🌿 _B0ECalHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _B0ECalHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _DIRCBarHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DIRCBarHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DIRCBarHits_particle.index int32_t[]
┃   ┣━━ 🌿 _DRICHHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHHits_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecHits_contributions.index int32_t[]
┃   ┣━━ 🍃 _EventHeader_weights std::vector<double>
┃   ┣━━ 🌿 _ForwardMPGDEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotHits_particle.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _LFHCALHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _LFHCALHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _LumiDirectPCALHitsContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LumiDirectPCALHitsContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LumiDirectPCALHitsContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _LumiDirectPCALHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LumiDirectPCALHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LumiDirectPCALHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _LumiSpecTrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LumiSpecTrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LumiSpecTrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _MCParticles_daughters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticles_daughters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticles_daughters.index int32_t[]
┃   ┣━━ 🌿 _MCParticles_parents vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticles_parents.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticles_parents.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _PFRICHHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _PFRICHHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _PFRICHHits_particle.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TrackerEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TrackerEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TrackerEndcapHits_particle.index int32_t[]
┃   ┗━━ 🌿 _VertexBarrelHits_particle vector<podio::ObjectID>
┃       ┣━━ 🍃 _VertexBarrelHits_particle.collectionID uint32_t[]
┃       ┗━━ 🍃 _VertexBarrelHits_particle.index int32_t[]
┣━━ 🌴 meta (1)
┃   ┣━━ 🍁 GPDoubleKeys std::vector<std::string>
┃   ┣━━ 🍁 GPDoubleValues std::vector<std::vector<double>>
┃   ┣━━ 🍁 GPFloatKeys std::vector<std::string>
┃   ┣━━ 🍁 GPFloatValues std::vector<std::vector<float>>
┃   ┣━━ 🍁 GPIntKeys std::vector<std::string>
┃   ┣━━ 🍁 GPIntValues std::vector<std::vector<int32_t>>
┃   ┣━━ 🍁 GPStringKeys std::vector<std::string>
┃   ┗━━ 🍁 GPStringValues std::vector<std::vector<std::string>>
┣━━ 🌴 metadata (1)
┃   ┣━━ 🍁 GPDoubleKeys std::vector<std::string>
┃   ┣━━ 🍁 GPDoubleValues std::vector<std::vector<double>>
┃   ┣━━ 🍁 GPFloatKeys std::vector<std::string>
┃   ┣━━ 🍁 GPFloatValues std::vector<std::vector<float>>
┃   ┣━━ 🍁 GPIntKeys std::vector<std::string>
┃   ┣━━ 🍁 GPIntValues std::vector<std::vector<int32_t>>
┃   ┣━━ 🍁 GPStringKeys std::vector<std::string>
┃   ┗━━ 🍁 GPStringValues std::vector<std::vector<std::string>>
┣━━ 🌴 podio_metadata (1)
┃   ┣━━ 🌿 EDMDefinitions vector<tuple<string,string> >
┃   ┃   ┣━━ 🍁 EDMDefinitions._0 std::string[]
┃   ┃   ┗━━ 🍁 EDMDefinitions._1 std::string[]
┃   ┣━━ 🌿 PodioBuildVersion podio::version::Version
┃   ┃   ┣━━ 🍁 major uint16_t
┃   ┃   ┣━━ 🍁 minor uint16_t
┃   ┃   ┗━━ 🍁 patch uint16_t
┃   ┣━━ 🌿 edm4hep___Version podio::version::Version
┃   ┃   ┣━━ 🍁 major uint16_t
┃   ┃   ┣━━ 🍁 minor uint16_t
┃   ┃   ┗━━ 🍁 patch uint16_t
┃   ┣━━ 🌿 events___CollectionTypeInfo vector<podio::root_utils::CollectionWriteInfo>
┃   ┃   ┣━━ 🍃 events___CollectionTypeInfo.collectionID uint32_t[]
┃   ┃   ┣━━ 🍁 events___CollectionTypeInfo.dataType std::string[]
┃   ┃   ┣━━ 🍃 events___CollectionTypeInfo.isSubset bool[]
┃   ┃   ┣━━ 🍁 events___CollectionTypeInfo.name std::string[]
┃   ┃   ┣━━ 🍃 events___CollectionTypeInfo.schemaVersion uint32_t[]
┃   ┃   ┗━━ 🍁 events___CollectionTypeInfo.storageType std::string[]
┃   ┣━━ 🌿 meta___CollectionTypeInfo vector<podio::root_utils::CollectionWriteInfo>
┃   ┃   ┣━━ 🍃 meta___CollectionTypeInfo.collectionID uint32_t[]
┃   ┃   ┣━━ 🍁 meta___CollectionTypeInfo.dataType std::string[]
┃   ┃   ┣━━ 🍃 meta___CollectionTypeInfo.isSubset bool[]
┃   ┃   ┣━━ 🍁 meta___CollectionTypeInfo.name std::string[]
┃   ┃   ┣━━ 🍃 meta___CollectionTypeInfo.schemaVersion uint32_t[]
┃   ┃   ┗━━ 🍁 meta___CollectionTypeInfo.storageType std::string[]
┃   ┣━━ 🌿 metadata___CollectionTypeInfo vector<podio::root_utils::CollectionWriteInfo>
┃   ┃   ┣━━ 🍃 metadata___CollectionTypeInfo.collectionID uint32_t[]
┃   ┃   ┣━━ 🍁 metadata___CollectionTypeInfo.dataType std::string[]
┃   ┃   ┣━━ 🍃 metadata___CollectionTypeInfo.isSubset bool[]
┃   ┃   ┣━━ 🍁 metadata___CollectionTypeInfo.name std::string[]
┃   ┃   ┣━━ 🍃 metadata___CollectionTypeInfo.schemaVersion uint32_t[]
┃   ┃   ┗━━ 🍁 metadata___CollectionTypeInfo.storageType std::string[]
┃   ┗━━ 🌿 runs___CollectionTypeInfo vector<podio::root_utils::CollectionWriteInfo>
┃       ┣━━ 🍃 runs___CollectionTypeInfo.collectionID uint32_t[]
┃       ┣━━ 🍁 runs___CollectionTypeInfo.dataType std::string[]
┃       ┣━━ 🍃 runs___CollectionTypeInfo.isSubset bool[]
┃       ┣━━ 🍁 runs___CollectionTypeInfo.name std::string[]
┃       ┣━━ 🍃 runs___CollectionTypeInfo.schemaVersion uint32_t[]
┃       ┗━━ 🍁 runs___CollectionTypeInfo.storageType std::string[]
┗━━ 🌴 runs (1)
    ┣━━ 🍁 GPDoubleKeys std::vector<std::string>
    ┣━━ 🍁 GPDoubleValues std::vector<std::vector<double>>
    ┣━━ 🍁 GPFloatKeys std::vector<std::string>
    ┣━━ 🍁 GPFloatValues std::vector<std::vector<float>>
    ┣━━ 🍁 GPIntKeys std::vector<std::string>
    ┣━━ 🍁 GPIntValues std::vector<std::vector<int32_t>>
    ┣━━ 🍁 GPStringKeys std::vector<std::string>
    ┗━━ 🍁 GPStringValues std::vector<std::vector<std::string>>
```
