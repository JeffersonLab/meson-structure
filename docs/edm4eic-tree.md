# EDM4eic tree

EDM4eic is a format that is used by EIC reconstruction software (EICRecon).
This page, for convenience, has full tree structure. You can explore it yourself
(without installing CERN ROOT):

- [online using jsroot](https://jsroot.gsi.de/latest/)
- [uproot-browser](https://github.com/scikit-hep/uproot-browser) command line: 

  ```
  python -m pip install --upgrade uproot-browser 
  
  uproot-browser tree k_lambda_18x275_5000evt_001.edm4eic.root
  ```

The next is printout of uproot-browser
```
┣━━ 🌴 events (1000)
┃   ┣━━ 🌿 B0ECalClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 B0ECalClusterAssociations.weight float[]
┃   ┣━━ 🌿 B0ECalClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0ECalClusterLinks.weight float[]
┃   ┣━━ 🌿 B0ECalClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 B0ECalClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.energy float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.energyError float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.position.x float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.position.y float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.position.z float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.time float[]
┃   ┃   ┣━━ 🍃 B0ECalClusters.timeError float[]
┃   ┃   ┗━━ 🍃 B0ECalClusters.type int32_t[]
┃   ┣━━ 🌿 B0ECalRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 B0ECalRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 B0ECalRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 B0ECalRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 B0ECalRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 B0ECalRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.energy float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 B0ECalRecHits.time float[]
┃   ┃   ┗━━ 🍃 B0ECalRecHits.timeError float[]
┃   ┣━━ 🌿 B0TrackerCKFTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackAssociations.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackLinks.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTrackParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.phi float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.theta float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParameters.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackParameters.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTrackParametersUnfiltered vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.phi float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.qOverP float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.theta float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackParametersUnfiltered.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTrackUnfilteredAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackUnfilteredAssociations.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTrackUnfilteredLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrackUnfilteredLinks.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.charge float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.position.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.position.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.position.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.time float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.timeError float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTracks.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTracksUnfiltered vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.charge float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.chi2 float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.momentum.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.momentum.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.momentum.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.position.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.position.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.position.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.time float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.timeError float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTracksUnfiltered.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTracksUnfiltered.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTrajectories vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectories.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrajectories.type uint32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTrajectoriesUnfiltered vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTrajectoriesUnfiltered.type uint32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackAssociations.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackLinks.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.phi float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.theta float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackParameters.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackParametersUnfiltered vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.phi float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.qOverP float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.theta float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackParametersUnfiltered.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackUnfilteredAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackUnfilteredAssociations.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrackUnfilteredLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrackUnfilteredLinks.weight float[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.charge float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.position.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.position.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.position.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.time float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.timeError float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTracks.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTracksUnfiltered vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.charge float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.chi2 float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.momentum.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.momentum.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.momentum.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.position.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.position.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.position.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.time float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.timeError float[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTracksUnfiltered.type int32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrajectories vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectories.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrajectories.type uint32_t[]
┃   ┣━━ 🌿 B0TrackerCKFTruthSeededTrajectoriesUnfiltered vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerCKFTruthSeededTrajectoriesUnfiltered.type uint32_t[]
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
┃   ┣━━ 🌿 B0TrackerMeasurements vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.xx float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.xy float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.xz float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.yy float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.yz float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.covariance.zz float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.time float[]
┃   ┃   ┣━━ 🍃 B0TrackerMeasurements.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerMeasurements.weights_end uint32_t[]
┃   ┣━━ 🌿 B0TrackerRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 B0TrackerRawHitAssociations.weight float[]
┃   ┣━━ 🌿 B0TrackerRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 B0TrackerRawHitLinks.weight float[]
┃   ┣━━ 🌿 B0TrackerRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 B0TrackerRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 B0TrackerRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.edep float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 B0TrackerRecHits.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerRecHits.timeError float[]
┃   ┣━━ 🌿 B0TrackerSeedParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.phi float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.theta float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeedParameters.time float[]
┃   ┃   ┗━━ 🍃 B0TrackerSeedParameters.type int32_t[]
┃   ┣━━ 🌿 B0TrackerSeeds vector<edm4eic::TrackSeedData>
┃   ┃   ┣━━ 🍃 B0TrackerSeeds.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerSeeds.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 B0TrackerSeeds.perigee.x float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeeds.perigee.y float[]
┃   ┃   ┣━━ 🍃 B0TrackerSeeds.perigee.z float[]
┃   ┃   ┗━━ 🍃 B0TrackerSeeds.quality float[]
┃   ┣━━ 🌿 B0TrackerTruthSeeds_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 B0TrackerTruthSeeds_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 B0TrackerTruthSeeds_objIdx.index int32_t[]
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
┃   ┣━━ 🌿 BackwardMPGDEndcapRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 BackwardMPGDEndcapRawHitAssociations.weight float[]
┃   ┣━━ 🌿 BackwardMPGDEndcapRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 BackwardMPGDEndcapRawHitLinks.weight float[]
┃   ┣━━ 🌿 BackwardMPGDEndcapRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 BackwardMPGDEndcapRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 BackwardMPGDEndcapRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.edep float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 BackwardMPGDEndcapRecHits.time float[]
┃   ┃   ┗━━ 🍃 BackwardMPGDEndcapRecHits.timeError float[]
┃   ┣━━ 🌿 CalorimeterTrackProjections vector<edm4eic::TrackSegmentData>
┃   ┃   ┣━━ 🍃 CalorimeterTrackProjections.length float[]
┃   ┃   ┣━━ 🍃 CalorimeterTrackProjections.lengthError float[]
┃   ┃   ┣━━ 🍃 CalorimeterTrackProjections.points_begin uint32_t[]
┃   ┃   ┗━━ 🍃 CalorimeterTrackProjections.points_end uint32_t[]
┃   ┣━━ 🌿 CentralAndB0TrackVertices vector<edm4eic::VertexData>
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.associatedParticles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.associatedParticles_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.ndf int32_t[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.position.t float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.position.x float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.position.y float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.position.z float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.tt float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.xt float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.xx float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.xy float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.xz float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.yt float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.yy float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.yz float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.zt float[]
┃   ┃   ┣━━ 🍃 CentralAndB0TrackVertices.positionError.zz float[]
┃   ┃   ┗━━ 🍃 CentralAndB0TrackVertices.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 CentralCKFTrackAssociations.weight float[]
┃   ┣━━ 🌿 CentralCKFTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 CentralCKFTrackLinks.weight float[]
┃   ┣━━ 🌿 CentralCKFTrackParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.phi float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.theta float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParameters.time float[]
┃   ┃   ┗━━ 🍃 CentralCKFTrackParameters.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTrackParametersUnfiltered vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.phi float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.qOverP float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.theta float[]
┃   ┃   ┣━━ 🍃 CentralCKFTrackParametersUnfiltered.time float[]
┃   ┃   ┗━━ 🍃 CentralCKFTrackParametersUnfiltered.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTrackUnfilteredAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 CentralCKFTrackUnfilteredAssociations.weight float[]
┃   ┣━━ 🌿 CentralCKFTrackUnfilteredLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 CentralCKFTrackUnfilteredLinks.weight float[]
┃   ┣━━ 🌿 CentralCKFTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 CentralCKFTracks.charge float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.position.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.position.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.position.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.time float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.timeError float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTracks.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTracksUnfiltered vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.charge float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.momentum.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.momentum.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.momentum.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.position.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.position.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.position.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.time float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.timeError float[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTracksUnfiltered.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTracksUnfiltered.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTrajectories vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectories.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTrajectories.type uint32_t[]
┃   ┣━━ 🌿 CentralCKFTrajectoriesUnfiltered vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTrajectoriesUnfiltered.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTrajectoriesUnfiltered.type uint32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackAssociations.weight float[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackLinks.weight float[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.phi float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.theta float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParameters.time float[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackParameters.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackParametersUnfiltered vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.phi float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.qOverP float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.theta float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.time float[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackParametersUnfiltered.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackUnfilteredAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackUnfilteredAssociations.weight float[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrackUnfilteredLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrackUnfilteredLinks.weight float[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.charge float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.position.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.position.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.position.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.time float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.timeError float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTracks.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTracksUnfiltered vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.charge float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.momentum.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.momentum.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.momentum.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.position.x float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.position.y float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.position.z float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.time float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.timeError float[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTracksUnfiltered.type int32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrajectories vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectories.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrajectories.type uint32_t[]
┃   ┣━━ 🌿 CentralCKFTruthSeededTrajectoriesUnfiltered vector<edm4eic::TrajectoryData>
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.measurementChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.measurementChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.measurements_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.measurements_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.nHoles uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.nMeasurements uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.nOutliers uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.nSharedHits uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.nStates uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.outlierChi2_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.outlierChi2_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.outliers_deprecated_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.outliers_deprecated_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.trackParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.trackParameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CentralCKFTruthSeededTrajectoriesUnfiltered.type uint32_t[]
┃   ┣━━ 🌿 CentralTrackSeedParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.phi float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.theta float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeedParameters.time float[]
┃   ┃   ┗━━ 🍃 CentralTrackSeedParameters.type int32_t[]
┃   ┣━━ 🌿 CentralTrackSeeds vector<edm4eic::TrackSeedData>
┃   ┃   ┣━━ 🍃 CentralTrackSeeds.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackSeeds.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackSeeds.perigee.x float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeeds.perigee.y float[]
┃   ┃   ┣━━ 🍃 CentralTrackSeeds.perigee.z float[]
┃   ┃   ┗━━ 🍃 CentralTrackSeeds.quality float[]
┃   ┣━━ 🌿 CentralTrackSegments vector<edm4eic::TrackSegmentData>
┃   ┃   ┣━━ 🍃 CentralTrackSegments.length float[]
┃   ┃   ┣━━ 🍃 CentralTrackSegments.lengthError float[]
┃   ┃   ┣━━ 🍃 CentralTrackSegments.points_begin uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackSegments.points_end uint32_t[]
┃   ┣━━ 🌿 CentralTrackVertices vector<edm4eic::VertexData>
┃   ┃   ┣━━ 🍃 CentralTrackVertices.associatedParticles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.associatedParticles_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.chi2 float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.ndf int32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.position.t float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.position.x float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.position.y float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.position.z float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.tt float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.xt float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.xx float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.xy float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.xz float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.yt float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.yy float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.yz float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.zt float[]
┃   ┃   ┣━━ 🍃 CentralTrackVertices.positionError.zz float[]
┃   ┃   ┗━━ 🍃 CentralTrackVertices.type int32_t[]
┃   ┣━━ 🌿 CentralTrackerMeasurements vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.xx float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.xy float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.xz float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.yy float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.yz float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.covariance.zz float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.loc.a float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.loc.b float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.surface uint64_t[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.time float[]
┃   ┃   ┣━━ 🍃 CentralTrackerMeasurements.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackerMeasurements.weights_end uint32_t[]
┃   ┣━━ 🌿 CentralTrackerTruthSeeds_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 CentralTrackerTruthSeeds_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackerTruthSeeds_objIdx.index int32_t[]
┃   ┣━━ 🌿 CentralTrackingRawHitAssociations_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 CentralTrackingRawHitAssociations_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackingRawHitAssociations_objIdx.index int32_t[]
┃   ┣━━ 🌿 CentralTrackingRawHitLinks_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 CentralTrackingRawHitLinks_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackingRawHitLinks_objIdx.index int32_t[]
┃   ┣━━ 🌿 CentralTrackingRecHits_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 CentralTrackingRecHits_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 CentralTrackingRecHits_objIdx.index int32_t[]
┃   ┣━━ 🌿 CombinedTOFParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 CombinedTOFParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 CombinedTOFParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CombinedTOFParticleIDs.type int32_t[]
┃   ┣━━ 🌿 CombinedTOFTruthSeededParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 CombinedTOFTruthSeededParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFTruthSeededParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFTruthSeededParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 CombinedTOFTruthSeededParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 CombinedTOFTruthSeededParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 CombinedTOFTruthSeededParticleIDs.type int32_t[]
┃   ┣━━ 🌿 DIRCParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 DIRCParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 DIRCParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 DIRCParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 DIRCParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DIRCParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 DIRCParticleIDs.type int32_t[]
┃   ┣━━ 🌿 DIRCRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 DIRCRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 DIRCRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 DIRCRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 DIRCTruthSeededParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 DIRCTruthSeededParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 DIRCTruthSeededParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 DIRCTruthSeededParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 DIRCTruthSeededParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DIRCTruthSeededParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 DIRCTruthSeededParticleIDs.type int32_t[]
┃   ┣━━ 🌿 DRICHAerogelIrtCherenkovParticleID vector<edm4eic::CherenkovParticleIDData>
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.hypotheses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.hypotheses_end uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.npe float[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.photonEnergy float[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.rawHitAssociations_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.rawHitAssociations_end uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.refractiveIndex float[]
┃   ┃   ┣━━ 🍃 DRICHAerogelIrtCherenkovParticleID.thetaPhiPhotons_begin uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHAerogelIrtCherenkovParticleID.thetaPhiPhotons_end uint32_t[]
┃   ┣━━ 🌿 DRICHAerogelTracks vector<edm4eic::TrackSegmentData>
┃   ┃   ┣━━ 🍃 DRICHAerogelTracks.length float[]
┃   ┃   ┣━━ 🍃 DRICHAerogelTracks.lengthError float[]
┃   ┃   ┣━━ 🍃 DRICHAerogelTracks.points_begin uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHAerogelTracks.points_end uint32_t[]
┃   ┣━━ 🌿 DRICHGasIrtCherenkovParticleID vector<edm4eic::CherenkovParticleIDData>
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.hypotheses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.hypotheses_end uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.npe float[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.photonEnergy float[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.rawHitAssociations_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.rawHitAssociations_end uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.refractiveIndex float[]
┃   ┃   ┣━━ 🍃 DRICHGasIrtCherenkovParticleID.thetaPhiPhotons_begin uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHGasIrtCherenkovParticleID.thetaPhiPhotons_end uint32_t[]
┃   ┣━━ 🌿 DRICHGasTracks vector<edm4eic::TrackSegmentData>
┃   ┃   ┣━━ 🍃 DRICHGasTracks.length float[]
┃   ┃   ┣━━ 🍃 DRICHGasTracks.lengthError float[]
┃   ┃   ┣━━ 🍃 DRICHGasTracks.points_begin uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHGasTracks.points_end uint32_t[]
┃   ┣━━ 🌿 DRICHParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 DRICHParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 DRICHParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 DRICHParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 DRICHParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHParticleIDs.type int32_t[]
┃   ┣━━ 🌿 DRICHRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 DRICHRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 DRICHRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 DRICHRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 DRICHRawHitsAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 DRICHRawHitsAssociations.weight float[]
┃   ┣━━ 🌿 DRICHRawHitsLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 DRICHRawHitsLinks.weight float[]
┃   ┣━━ 🌿 DRICHTruthSeededParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 DRICHTruthSeededParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 DRICHTruthSeededParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 DRICHTruthSeededParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 DRICHTruthSeededParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 DRICHTruthSeededParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 DRICHTruthSeededParticleIDs.type int32_t[]
┃   ┣━━ 🌿 EcalBarrelClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalBarrelClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalBarrelClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalBarrelClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalBarrelClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalBarrelClusters.type int32_t[]
┃   ┣━━ 🌿 EcalBarrelImagingClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalBarrelImagingClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalBarrelImagingClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalBarrelImagingClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalBarrelImagingClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingClusters.type int32_t[]
┃   ┣━━ 🌿 EcalBarrelImagingProcessedHitContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHitContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingProcessedHitContributions.time float[]
┃   ┣━━ 🌿 EcalBarrelImagingProcessedHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingProcessedHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingProcessedHits.position.z float[]
┃   ┣━━ 🌿 EcalBarrelImagingRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalBarrelImagingRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelImagingRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalBarrelImagingRecHits.timeError float[]
┃   ┣━━ 🌿 EcalBarrelScFiClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalBarrelScFiClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalBarrelScFiClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalBarrelScFiClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalBarrelScFiClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiClusters.type int32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiNAttenuatedHitContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNAttenuatedHitContributions.time float[]
┃   ┣━━ 🌿 EcalBarrelScFiNAttenuatedHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNAttenuatedHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNAttenuatedHits.position.z float[]
┃   ┣━━ 🌿 EcalBarrelScFiNCALOROCHits vector<edm4eic::RawCALOROCHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.aSamples_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.aSamples_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.bSamples_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.bSamples_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCALOROCHits.samplePhase int32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNCALOROCHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiNCombinedPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNCombinedPulses.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiNCombinedPulsesWithNoise vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNCombinedPulsesWithNoise.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiNPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiNPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiNPulses.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiPAttenuatedHitContributions vector<edm4hep::CaloHitContributionData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.PDG int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.stepLength float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.stepPosition.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.stepPosition.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.stepPosition.z float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPAttenuatedHitContributions.time float[]
┃   ┣━━ 🌿 EcalBarrelScFiPAttenuatedHits vector<edm4hep::SimCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.contributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.contributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPAttenuatedHits.position.y float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPAttenuatedHits.position.z float[]
┃   ┣━━ 🌿 EcalBarrelScFiPCALOROCHits vector<edm4eic::RawCALOROCHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.aSamples_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.aSamples_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.bSamples_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.bSamples_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCALOROCHits.samplePhase int32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPCALOROCHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiPCombinedPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPCombinedPulses.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiPCombinedPulsesWithNoise vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPCombinedPulsesWithNoise.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiPPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.integral float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.interval float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiPPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiPPulses.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalBarrelScFiRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelScFiRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalBarrelScFiRecHits.timeError float[]
┃   ┣━━ 🌿 EcalBarrelTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 EcalBarrelTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 EcalBarrelTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalBarrelTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalBarrelTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalBarrelTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalBarrelTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalBarrelTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalBarrelTruthClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapNClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapNClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapNClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapNClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapNClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapNRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapNRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalEndcapNRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalEndcapNRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNRecHits.timeError float[]
┃   ┣━━ 🌿 EcalEndcapNSplitMergeClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapNSplitMergeClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapNSplitMergeClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapNSplitMergeClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapNSplitMergeClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNSplitMergeClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNSplitMergeClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapNTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 EcalEndcapNTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 EcalEndcapNTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapNTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapNTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapNTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapNTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapNTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapNTruthClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapPClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapPClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapPClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapPClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapPClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapPRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapPRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalEndcapPRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalEndcapPRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPRecHits.timeError float[]
┃   ┣━━ 🌿 EcalEndcapPSplitMergeClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapPSplitMergeClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapPSplitMergeClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapPSplitMergeClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapPSplitMergeClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPSplitMergeClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPSplitMergeClusters.type int32_t[]
┃   ┣━━ 🌿 EcalEndcapPTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 EcalEndcapPTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 EcalEndcapPTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalEndcapPTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalEndcapPTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalEndcapPTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalEndcapPTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalEndcapPTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalEndcapPTruthClusters.type int32_t[]
┃   ┣━━ 🌿 EcalFarForwardZDCClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalFarForwardZDCClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalFarForwardZDCClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCClusters.type int32_t[]
┃   ┣━━ 🌿 EcalFarForwardZDCRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalFarForwardZDCRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCRecHits.timeError float[]
┃   ┣━━ 🌿 EcalFarForwardZDCTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalFarForwardZDCTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalFarForwardZDCTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalFarForwardZDCTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalFarForwardZDCTruthClusters.type int32_t[]
┃   ┣━━ 🌿 EcalLumiSpecClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalLumiSpecClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalLumiSpecClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalLumiSpecClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalLumiSpecClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecClusters.type int32_t[]
┃   ┣━━ 🌿 EcalLumiSpecRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 EcalLumiSpecRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.energy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecRecHits.time float[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecRecHits.timeError float[]
┃   ┣━━ 🌿 EcalLumiSpecTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 EcalLumiSpecTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 EcalLumiSpecTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 EcalLumiSpecTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 EcalLumiSpecTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 EcalLumiSpecTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 EcalLumiSpecTruthClusters.type int32_t[]
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
┃   ┣━━ 🌿 ForwardMPGDEndcapRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 ForwardMPGDEndcapRawHitAssociations.weight float[]
┃   ┣━━ 🌿 ForwardMPGDEndcapRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ForwardMPGDEndcapRawHitLinks.weight float[]
┃   ┣━━ 🌿 ForwardMPGDEndcapRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 ForwardMPGDEndcapRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 ForwardMPGDEndcapRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.edep float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 ForwardMPGDEndcapRecHits.time float[]
┃   ┃   ┗━━ 🍃 ForwardMPGDEndcapRecHits.timeError float[]
┃   ┣━━ 🌿 ForwardOffMRecParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.charge float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.energy float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.mass float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMRecParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ForwardOffMRecParticles.type int32_t[]
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
┃   ┣━━ 🌿 ForwardOffMTrackerRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 ForwardOffMTrackerRawHitAssociations.weight float[]
┃   ┣━━ 🌿 ForwardOffMTrackerRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ForwardOffMTrackerRawHitLinks.weight float[]
┃   ┣━━ 🌿 ForwardOffMTrackerRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 ForwardOffMTrackerRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 ForwardOffMTrackerRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.edep float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 ForwardOffMTrackerRecHits.time float[]
┃   ┃   ┗━━ 🍃 ForwardOffMTrackerRecHits.timeError float[]
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
┃   ┣━━ 🌿 ForwardRomanPotRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 ForwardRomanPotRawHitAssociations.weight float[]
┃   ┣━━ 🌿 ForwardRomanPotRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ForwardRomanPotRawHitLinks.weight float[]
┃   ┣━━ 🌿 ForwardRomanPotRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardRomanPotRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 ForwardRomanPotRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 ForwardRomanPotRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.edep float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecHits.time float[]
┃   ┃   ┗━━ 🍃 ForwardRomanPotRecHits.timeError float[]
┃   ┣━━ 🌿 ForwardRomanPotRecParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.charge float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.energy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.mass float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotRecParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ForwardRomanPotRecParticles.type int32_t[]
┃   ┣━━ 🌿 ForwardRomanPotStaticRecParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.charge float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.energy float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.mass float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ForwardRomanPotStaticRecParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ForwardRomanPotStaticRecParticles.type int32_t[]
┃   ┣━━ 🍁 GPDoubleKeys std::vector<std::string>
┃   ┣━━ 🍁 GPDoubleValues std::vector<std::vector<double>>
┃   ┣━━ 🍁 GPFloatKeys std::vector<std::string>
┃   ┣━━ 🍁 GPFloatValues std::vector<std::vector<float>>
┃   ┣━━ 🍁 GPIntKeys std::vector<std::string>
┃   ┣━━ 🍁 GPIntValues std::vector<std::vector<int32_t>>
┃   ┣━━ 🍁 GPStringKeys std::vector<std::string>
┃   ┣━━ 🍁 GPStringValues std::vector<std::vector<std::string>>
┃   ┣━━ 🌿 GeneratedBreitFrameParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.charge float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.energy float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.mass float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedBreitFrameParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 GeneratedBreitFrameParticles.type int32_t[]
┃   ┣━━ 🌿 GeneratedCentauroJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.charge float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.energy float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.mass float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedCentauroJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 GeneratedCentauroJets.type int32_t[]
┃   ┣━━ 🌿 GeneratedChargedJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.charge float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.energy float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.mass float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedChargedJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 GeneratedChargedJets.type int32_t[]
┃   ┣━━ 🌿 GeneratedJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 GeneratedJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.charge float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.energy float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.mass float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 GeneratedJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 GeneratedJets.type int32_t[]
┃   ┣━━ 🌿 GeneratedParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 GeneratedParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.charge float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.energy float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.mass float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 GeneratedParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 GeneratedParticles.type int32_t[]
┃   ┣━━ 🌿 HadronicFinalState vector<edm4eic::HadronicFinalStateData>
┃   ┃   ┣━━ 🍃 HadronicFinalState.gamma float[]
┃   ┃   ┣━━ 🍃 HadronicFinalState.hadrons_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HadronicFinalState.hadrons_end uint32_t[]
┃   ┃   ┣━━ 🍃 HadronicFinalState.pT float[]
┃   ┃   ┗━━ 🍃 HadronicFinalState.sigma float[]
┃   ┣━━ 🌿 HcalBarrelClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalBarrelClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalBarrelClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalBarrelClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalBarrelClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalBarrelClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalBarrelClusters.type int32_t[]
┃   ┣━━ 🌿 HcalBarrelMergedHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelMergedHits.time float[]
┃   ┃   ┗━━ 🍃 HcalBarrelMergedHits.timeError float[]
┃   ┣━━ 🌿 HcalBarrelRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalBarrelRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 HcalBarrelRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 HcalBarrelRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelRecHits.time float[]
┃   ┃   ┗━━ 🍃 HcalBarrelRecHits.timeError float[]
┃   ┣━━ 🌿 HcalBarrelSplitMergeClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalBarrelSplitMergeClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalBarrelSplitMergeClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalBarrelSplitMergeClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalBarrelSplitMergeClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalBarrelSplitMergeClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalBarrelSplitMergeClusters.type int32_t[]
┃   ┣━━ 🌿 HcalBarrelTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 HcalBarrelTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 HcalBarrelTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalBarrelTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalBarrelTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalBarrelTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalBarrelTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalBarrelTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalBarrelTruthClusters.type int32_t[]
┃   ┣━━ 🌿 HcalEndcapNClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalEndcapNClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalEndcapNClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalEndcapNClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalEndcapNClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNClusters.type int32_t[]
┃   ┣━━ 🌿 HcalEndcapNMergedHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNMergedHits.time float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNMergedHits.timeError float[]
┃   ┣━━ 🌿 HcalEndcapNRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapNRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 HcalEndcapNRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 HcalEndcapNRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNRecHits.time float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNRecHits.timeError float[]
┃   ┣━━ 🌿 HcalEndcapNSplitMergeClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalEndcapNSplitMergeClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalEndcapNSplitMergeClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalEndcapNSplitMergeClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalEndcapNSplitMergeClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNSplitMergeClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNSplitMergeClusters.type int32_t[]
┃   ┣━━ 🌿 HcalEndcapNTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 HcalEndcapNTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 HcalEndcapNTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalEndcapNTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalEndcapNTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalEndcapNTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalEndcapNTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalEndcapNTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalEndcapNTruthClusters.type int32_t[]
┃   ┣━━ 🌿 HcalEndcapPInsertClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalEndcapPInsertClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalEndcapPInsertClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertClusters.type int32_t[]
┃   ┣━━ 🌿 HcalEndcapPInsertMergedHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertMergedHits.time float[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertMergedHits.timeError float[]
┃   ┣━━ 🌿 HcalEndcapPInsertRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 HcalEndcapPInsertRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalEndcapPInsertRecHits.time float[]
┃   ┃   ┗━━ 🍃 HcalEndcapPInsertRecHits.timeError float[]
┃   ┣━━ 🌿 HcalFarForwardZDCClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCClusterAssociationsBaseline vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClusterAssociationsBaseline.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCClusterLinksBaseline vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClusterLinksBaseline.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClusters.type int32_t[]
┃   ┣━━ 🌿 HcalFarForwardZDCClustersBaseline vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.energyError float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.position.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.position.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.time float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCClustersBaseline.timeError float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCClustersBaseline.type int32_t[]
┃   ┣━━ 🌿 HcalFarForwardZDCRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 HcalFarForwardZDCRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCRecHits.time float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCRecHits.timeError float[]
┃   ┣━━ 🌿 HcalFarForwardZDCSubcellHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.energyError float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.local.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.local.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.local.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.position.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.position.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCSubcellHits.time float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCSubcellHits.timeError float[]
┃   ┣━━ 🌿 HcalFarForwardZDCTruthClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCTruthClusterAssociations.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCTruthClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCTruthClusterLinks.weight float[]
┃   ┣━━ 🌿 HcalFarForwardZDCTruthClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.energy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.energyError float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.position.x float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.position.y float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.position.z float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.time float[]
┃   ┃   ┣━━ 🍃 HcalFarForwardZDCTruthClusters.timeError float[]
┃   ┃   ┗━━ 🍃 HcalFarForwardZDCTruthClusters.type int32_t[]
┃   ┣━━ 🌿 InclusiveKinematicsDA vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsDA.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsDA.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsDA.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsDA.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsDA.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsESigma vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsESigma.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsESigma.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsESigma.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsESigma.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsESigma.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsElectron vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsElectron.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsElectron.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsElectron.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsElectron.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsElectron.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsJB vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsJB.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsJB.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsJB.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsJB.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsJB.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsML vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsML.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsML.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsML.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsML.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsML.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsSigma vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsSigma.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsSigma.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsSigma.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsSigma.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsSigma.y float[]
┃   ┣━━ 🌿 InclusiveKinematicsTruth vector<edm4eic::InclusiveKinematicsData>
┃   ┃   ┣━━ 🍃 InclusiveKinematicsTruth.Q2 float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsTruth.W float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsTruth.nu float[]
┃   ┃   ┣━━ 🍃 InclusiveKinematicsTruth.x float[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicsTruth.y float[]
┃   ┣━━ 🌿 InclusiveKinematicseSigma_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 InclusiveKinematicseSigma_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 InclusiveKinematicseSigma_objIdx.index int32_t[]
┃   ┣━━ 🌿 LFHCALClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 LFHCALClusterAssociations.weight float[]
┃   ┣━━ 🌿 LFHCALClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 LFHCALClusterLinks.weight float[]
┃   ┣━━ 🌿 LFHCALClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 LFHCALClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.energy float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.energyError float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.position.x float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.position.y float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.position.z float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.time float[]
┃   ┃   ┣━━ 🍃 LFHCALClusters.timeError float[]
┃   ┃   ┗━━ 🍃 LFHCALClusters.type int32_t[]
┃   ┣━━ 🌿 LFHCALRawHits vector<edm4hep::RawCalorimeterHitData>
┃   ┃   ┣━━ 🍃 LFHCALRawHits.amplitude int32_t[]
┃   ┃   ┣━━ 🍃 LFHCALRawHits.cellID uint64_t[]
┃   ┃   ┗━━ 🍃 LFHCALRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 LFHCALRecHits vector<edm4eic::CalorimeterHitData>
┃   ┃   ┣━━ 🍃 LFHCALRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.dimension.x float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.dimension.y float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.dimension.z float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.energy float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.energyError float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.layer int32_t[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.local.x float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.local.y float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.local.z float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.sector int32_t[]
┃   ┃   ┣━━ 🍃 LFHCALRecHits.time float[]
┃   ┃   ┗━━ 🍃 LFHCALRecHits.timeError float[]
┃   ┣━━ 🌿 LFHCALSplitMergeClusterAssociations vector<edm4eic::MCRecoClusterParticleAssociationData>
┃   ┃   ┗━━ 🍃 LFHCALSplitMergeClusterAssociations.weight float[]
┃   ┣━━ 🌿 LFHCALSplitMergeClusterLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 LFHCALSplitMergeClusterLinks.weight float[]
┃   ┣━━ 🌿 LFHCALSplitMergeClusters vector<edm4eic::ClusterData>
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.energy float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.energyError float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.hitContributions_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.hitContributions_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.intrinsicDirectionError.xx float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.intrinsicDirectionError.xy float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.intrinsicDirectionError.yy float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.intrinsicPhi float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.intrinsicTheta float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.nhits uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.position.x float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.position.y float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.position.z float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.xx float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.xy float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.xz float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.yy float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.yz float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.positionError.zz float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.shapeParameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.shapeParameters_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.subdetectorEnergies_begin uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.subdetectorEnergies_end uint32_t[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.time float[]
┃   ┃   ┣━━ 🍃 LFHCALSplitMergeClusters.timeError float[]
┃   ┃   ┗━━ 🍃 LFHCALSplitMergeClusters.type int32_t[]
┃   ┣━━ 🌿 LFHCALTrackClusterMatches vector<edm4eic::TrackClusterMatchData>
┃   ┃   ┗━━ 🍃 LFHCALTrackClusterMatches.weight float[]
┃   ┣━━ 🌿 MCBeamElectrons_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCBeamElectrons_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCBeamElectrons_objIdx.index int32_t[]
┃   ┣━━ 🌿 MCBeamProtons_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCBeamProtons_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCBeamProtons_objIdx.index int32_t[]
┃   ┣━━ 🌿 MCNonScatteredElectronAssociations_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCNonScatteredElectronAssociations_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCNonScatteredElectronAssociations_objIdx.index int32_t[]
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
┃   ┣━━ 🌿 MCParticlesHeadOnFrameNoBeamFX vector<edm4hep::MCParticleData>
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.PDG int32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.charge float[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.daughters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.daughters_end uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.endpoint.x double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.endpoint.y double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.endpoint.z double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.generatorStatus int32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.helicity int32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.mass double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentum.x double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentum.y double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentum.z double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentumAtEndpoint.x double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentumAtEndpoint.y double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.momentumAtEndpoint.z double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.parents_begin uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.parents_end uint32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.simulatorStatus int32_t[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.time float[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.vertex.x double[]
┃   ┃   ┣━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.vertex.y double[]
┃   ┃   ┗━━ 🍃 MCParticlesHeadOnFrameNoBeamFX.vertex.z double[]
┃   ┣━━ 🌿 MCScatteredElectronAssociations_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCScatteredElectronAssociations_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCScatteredElectronAssociations_objIdx.index int32_t[]
┃   ┣━━ 🌿 MCScatteredElectrons_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCScatteredElectrons_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCScatteredElectrons_objIdx.index int32_t[]
┃   ┣━━ 🌿 MCScatteredProtons_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 MCScatteredProtons_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 MCScatteredProtons_objIdx.index int32_t[]
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
┃   ┣━━ 🌿 MPGDBarrelRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 MPGDBarrelRawHitAssociations.weight float[]
┃   ┣━━ 🌿 MPGDBarrelRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 MPGDBarrelRawHitLinks.weight float[]
┃   ┣━━ 🌿 MPGDBarrelRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 MPGDBarrelRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 MPGDBarrelRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 MPGDBarrelRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.edep float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 MPGDBarrelRecHits.time float[]
┃   ┃   ┗━━ 🍃 MPGDBarrelRecHits.timeError float[]
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
┃   ┣━━ 🌿 OuterMPGDBarrelRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 OuterMPGDBarrelRawHitAssociations.weight float[]
┃   ┣━━ 🌿 OuterMPGDBarrelRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 OuterMPGDBarrelRawHitLinks.weight float[]
┃   ┣━━ 🌿 OuterMPGDBarrelRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 OuterMPGDBarrelRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 OuterMPGDBarrelRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.edep float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 OuterMPGDBarrelRecHits.time float[]
┃   ┃   ┗━━ 🍃 OuterMPGDBarrelRecHits.timeError float[]
┃   ┣━━ 🌿 PrimaryVertices_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 PrimaryVertices_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 PrimaryVertices_objIdx.index int32_t[]
┃   ┣━━ 🌿 RICHEndcapNParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 RICHEndcapNParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 RICHEndcapNParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 RICHEndcapNParticleIDs.type int32_t[]
┃   ┣━━ 🌿 RICHEndcapNRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 RICHEndcapNRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 RICHEndcapNRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 RICHEndcapNRawHitsAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 RICHEndcapNRawHitsAssociations.weight float[]
┃   ┣━━ 🌿 RICHEndcapNRawHitsLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 RICHEndcapNRawHitsLinks.weight float[]
┃   ┣━━ 🌿 RICHEndcapNTruthSeededParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 RICHEndcapNTruthSeededParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNTruthSeededParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNTruthSeededParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 RICHEndcapNTruthSeededParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 RICHEndcapNTruthSeededParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 RICHEndcapNTruthSeededParticleIDs.type int32_t[]
┃   ┣━━ 🌿 ReconstructedBreitFrameParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedBreitFrameParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedBreitFrameParticles.type int32_t[]
┃   ┣━━ 🌿 ReconstructedCentauroJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedCentauroJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedCentauroJets.type int32_t[]
┃   ┣━━ 🌿 ReconstructedChargedJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedChargedJets.type int32_t[]
┃   ┣━━ 🌿 ReconstructedChargedParticleAssociations vector<edm4eic::MCRecoParticleAssociationData>
┃   ┃   ┗━━ 🍃 ReconstructedChargedParticleAssociations.weight float[]
┃   ┣━━ 🌿 ReconstructedChargedParticleLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ReconstructedChargedParticleLinks.weight float[]
┃   ┣━━ 🌿 ReconstructedChargedParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedChargedParticles.type int32_t[]
┃   ┣━━ 🌿 ReconstructedChargedRealPIDParticleIDs vector<edm4hep::ParticleIDData>
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticleIDs.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticleIDs.algorithmType int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticleIDs.likelihood float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticleIDs.parameters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticleIDs.parameters_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedChargedRealPIDParticleIDs.type int32_t[]
┃   ┣━━ 🌿 ReconstructedChargedRealPIDParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedChargedRealPIDParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedChargedRealPIDParticles.type int32_t[]
┃   ┣━━ 🌿 ReconstructedElectrons_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 ReconstructedElectrons_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedElectrons_objIdx.index int32_t[]
┃   ┣━━ 🌿 ReconstructedFarForwardZDCLambdaDecayProductsCM vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedFarForwardZDCLambdaDecayProductsCM.type int32_t[]
┃   ┣━━ 🌿 ReconstructedFarForwardZDCLambdas vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCLambdas.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedFarForwardZDCLambdas.type int32_t[]
┃   ┣━━ 🌿 ReconstructedFarForwardZDCNeutrals vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedFarForwardZDCNeutrals.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedFarForwardZDCNeutrals.type int32_t[]
┃   ┣━━ 🌿 ReconstructedJets vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedJets.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedJets.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedJets.type int32_t[]
┃   ┣━━ 🌿 ReconstructedParticleAssociations vector<edm4eic::MCRecoParticleAssociationData>
┃   ┃   ┗━━ 🍃 ReconstructedParticleAssociations.weight float[]
┃   ┣━━ 🌿 ReconstructedParticleLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ReconstructedParticleLinks.weight float[]
┃   ┣━━ 🌿 ReconstructedParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedParticles.type int32_t[]
┃   ┣━━ 🌿 ReconstructedTruthSeededChargedParticleAssociations vector<edm4eic::MCRecoParticleAssociationData>
┃   ┃   ┗━━ 🍃 ReconstructedTruthSeededChargedParticleAssociations.weight float[]
┃   ┣━━ 🌿 ReconstructedTruthSeededChargedParticleLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 ReconstructedTruthSeededChargedParticleLinks.weight float[]
┃   ┣━━ 🌿 ReconstructedTruthSeededChargedParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.charge float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.energy float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.mass float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 ReconstructedTruthSeededChargedParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 ReconstructedTruthSeededChargedParticles.type int32_t[]
┃   ┣━━ 🌿 ScatteredElectronsEMinusPz_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 ScatteredElectronsEMinusPz_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 ScatteredElectronsEMinusPz_objIdx.index int32_t[]
┃   ┣━━ 🌿 ScatteredElectronsTruth_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 ScatteredElectronsTruth_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 ScatteredElectronsTruth_objIdx.index int32_t[]
┃   ┣━━ 🌿 SecondaryVerticesHelix vector<edm4eic::VertexData>
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.associatedParticles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.associatedParticles_end uint32_t[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.chi2 float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.ndf int32_t[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.position.t float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.position.x float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.position.y float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.position.z float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.tt float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.xt float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.xx float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.xy float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.xz float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.yt float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.yy float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.yz float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.zt float[]
┃   ┃   ┣━━ 🍃 SecondaryVerticesHelix.positionError.zz float[]
┃   ┃   ┗━━ 🍃 SecondaryVerticesHelix.type int32_t[]
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
┃   ┣━━ 🌿 SiBarrelRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 SiBarrelRawHitAssociations.weight float[]
┃   ┣━━ 🌿 SiBarrelRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 SiBarrelRawHitLinks.weight float[]
┃   ┣━━ 🌿 SiBarrelRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 SiBarrelRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiBarrelRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 SiBarrelRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 SiBarrelTrackerRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.edep float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 SiBarrelTrackerRecHits.time float[]
┃   ┃   ┗━━ 🍃 SiBarrelTrackerRecHits.timeError float[]
┃   ┣━━ 🌿 SiBarrelVertexRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 SiBarrelVertexRawHitAssociations.weight float[]
┃   ┣━━ 🌿 SiBarrelVertexRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 SiBarrelVertexRawHitLinks.weight float[]
┃   ┣━━ 🌿 SiBarrelVertexRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 SiBarrelVertexRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 SiBarrelVertexRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 SiBarrelVertexRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.edep float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 SiBarrelVertexRecHits.time float[]
┃   ┃   ┗━━ 🍃 SiBarrelVertexRecHits.timeError float[]
┃   ┣━━ 🌿 SiEndcapTrackerRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 SiEndcapTrackerRawHitAssociations.weight float[]
┃   ┣━━ 🌿 SiEndcapTrackerRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 SiEndcapTrackerRawHitLinks.weight float[]
┃   ┣━━ 🌿 SiEndcapTrackerRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 SiEndcapTrackerRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 SiEndcapTrackerRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.edep float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 SiEndcapTrackerRecHits.time float[]
┃   ┃   ┗━━ 🍃 SiEndcapTrackerRecHits.timeError float[]
┃   ┣━━ 🌿 TOFBarrelADCTDC vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFBarrelADCTDC.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelADCTDC.charge int32_t[]
┃   ┃   ┗━━ 🍃 TOFBarrelADCTDC.timeStamp int32_t[]
┃   ┣━━ 🌿 TOFBarrelClusterHits vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.loc.a float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.loc.b float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.time float[]
┃   ┃   ┣━━ 🍃 TOFBarrelClusterHits.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TOFBarrelClusterHits.weights_end uint32_t[]
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
┃   ┣━━ 🌿 TOFBarrelRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 TOFBarrelRawHitAssociations.weight float[]
┃   ┣━━ 🌿 TOFBarrelRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TOFBarrelRawHitLinks.weight float[]
┃   ┣━━ 🌿 TOFBarrelRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFBarrelRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 TOFBarrelRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 TOFBarrelRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.edep float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 TOFBarrelRecHits.time float[]
┃   ┃   ┗━━ 🍃 TOFBarrelRecHits.timeError float[]
┃   ┣━━ 🌿 TOFEndcapADCTDC vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFEndcapADCTDC.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFEndcapADCTDC.charge int32_t[]
┃   ┃   ┗━━ 🍃 TOFEndcapADCTDC.timeStamp int32_t[]
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
┃   ┣━━ 🌿 TOFEndcapRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 TOFEndcapRawHitAssociations.weight float[]
┃   ┣━━ 🌿 TOFEndcapRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TOFEndcapRawHitLinks.weight float[]
┃   ┣━━ 🌿 TOFEndcapRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFEndcapRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFEndcapRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 TOFEndcapRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 TOFEndcapRecHits vector<edm4eic::TrackerHitData>
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.edep float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.edepError float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.position.x float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.position.y float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.position.z float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.positionError.xx float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.positionError.yy float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.positionError.zz float[]
┃   ┃   ┣━━ 🍃 TOFEndcapRecHits.time float[]
┃   ┃   ┗━━ 🍃 TOFEndcapRecHits.timeError float[]
┃   ┣━━ 🌿 TOFEndcapSharedHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.eDep float[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.position.x double[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.position.y double[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.position.z double[]
┃   ┃   ┣━━ 🍃 TOFEndcapSharedHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TOFEndcapSharedHits.time float[]
┃   ┣━━ 🌿 TaggerTrackerCombinedPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.integral float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.interval float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.position.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.position.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.position.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerCombinedPulses.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerCombinedPulsesWithNoise vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.integral float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.interval float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.position.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.position.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.position.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerCombinedPulsesWithNoise.trackerHits_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerHitPulses vector<edm4eic::SimPulseData>
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.amplitude_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.amplitude_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.calorimeterHits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.calorimeterHits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.integral float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.interval float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.position.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.position.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.position.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.pulses_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.pulses_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerHitPulses.trackerHits_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerHitPulses.trackerHits_end uint32_t[]
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
┃   ┣━━ 🌿 TaggerTrackerLocalTrackAssociations_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 TaggerTrackerLocalTrackAssociations_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerLocalTrackAssociations_objIdx.index int32_t[]
┃   ┣━━ 🌿 TaggerTrackerLocalTrackLinks_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 TaggerTrackerLocalTrackLinks_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerLocalTrackLinks_objIdx.index int32_t[]
┃   ┣━━ 🌿 TaggerTrackerLocalTracks_objIdx vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 TaggerTrackerLocalTracks_objIdx.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerLocalTracks_objIdx.index int32_t[]
┃   ┣━━ 🌿 TaggerTrackerM1L0ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L0ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM1L0ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM1L1ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L1ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM1L1ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM1L2ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L2ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM1L2ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM1L3ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1L3ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM1L3ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM1LocalTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 TaggerTrackerM1LocalTrackAssociations.weight float[]
┃   ┣━━ 🌿 TaggerTrackerM1LocalTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TaggerTrackerM1LocalTrackLinks.weight float[]
┃   ┣━━ 🌿 TaggerTrackerM1LocalTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.charge float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.position.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.position.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.position.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.timeError float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM1LocalTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM1LocalTracks.type int32_t[]
┃   ┣━━ 🌿 TaggerTrackerM2L0ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L0ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM2L0ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM2L1ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L1ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM2L1ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM2L2ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L2ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM2L2ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM2L3ClusterPositions vector<edm4eic::Measurement2DData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.covariance.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.loc.a float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.loc.b float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2L3ClusterPositions.weights_begin uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM2L3ClusterPositions.weights_end uint32_t[]
┃   ┣━━ 🌿 TaggerTrackerM2LocalTrackAssociations vector<edm4eic::MCRecoTrackParticleAssociationData>
┃   ┃   ┗━━ 🍃 TaggerTrackerM2LocalTrackAssociations.weight float[]
┃   ┣━━ 🌿 TaggerTrackerM2LocalTrackLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TaggerTrackerM2LocalTrackLinks.weight float[]
┃   ┣━━ 🌿 TaggerTrackerM2LocalTracks vector<edm4eic::TrackData>
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.charge float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.chi2 float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.measurements_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.measurements_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.momentum.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.momentum.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.momentum.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.ndf uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.pdg int32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.position.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.position.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.position.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.positionMomentumCovariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.time float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.timeError float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerM2LocalTracks.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerM2LocalTracks.type int32_t[]
┃   ┣━━ 🌿 TaggerTrackerRawHitAssociations vector<edm4eic::MCRecoTrackerHitAssociationData>
┃   ┃   ┗━━ 🍃 TaggerTrackerRawHitAssociations.weight float[]
┃   ┣━━ 🌿 TaggerTrackerRawHitLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TaggerTrackerRawHitLinks.weight float[]
┃   ┣━━ 🌿 TaggerTrackerRawHits vector<edm4eic::RawTrackerHitData>
┃   ┃   ┣━━ 🍃 TaggerTrackerRawHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerRawHits.charge int32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerRawHits.timeStamp int32_t[]
┃   ┣━━ 🌿 TaggerTrackerReconstructedParticleAssociations vector<edm4eic::MCRecoParticleAssociationData>
┃   ┃   ┗━━ 🍃 TaggerTrackerReconstructedParticleAssociations.weight float[]
┃   ┣━━ 🌿 TaggerTrackerReconstructedParticleLinks vector<podio::LinkData>
┃   ┃   ┗━━ 🍃 TaggerTrackerReconstructedParticleLinks.weight float[]
┃   ┣━━ 🌿 TaggerTrackerReconstructedParticles vector<edm4eic::ReconstructedParticleData>
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.PDG int32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.charge float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.clusters_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.clusters_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.tt float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.xt float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.xx float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.xy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.xz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.yt float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.yy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.yz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.zt float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.covMatrix.zz float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.energy float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.goodnessOfPID float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.mass float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.momentum.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.momentum.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.momentum.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.particleIDs_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.particleIDs_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.particles_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.particles_end uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.referencePoint.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.referencePoint.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.referencePoint.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.tracks_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerReconstructedParticles.tracks_end uint32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerReconstructedParticles.type int32_t[]
┃   ┣━━ 🌿 TaggerTrackerSharedHits vector<edm4hep::SimTrackerHitData>
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.cellID uint64_t[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.eDep float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.momentum.x float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.momentum.y float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.momentum.z float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.pathLength float[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.position.x double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.position.y double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.position.z double[]
┃   ┃   ┣━━ 🍃 TaggerTrackerSharedHits.quality int32_t[]
┃   ┃   ┗━━ 🍃 TaggerTrackerSharedHits.time float[]
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
┃   ┣━━ 🌿 TrackerTruthSeedParameters vector<edm4eic::TrackParametersData>
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.covariance.covariance[21] float[][21]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.loc.a float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.loc.b float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.pdg int32_t[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.phi float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.qOverP float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.surface uint64_t[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.theta float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeedParameters.time float[]
┃   ┃   ┗━━ 🍃 TrackerTruthSeedParameters.type int32_t[]
┃   ┣━━ 🌿 TrackerTruthSeeds vector<edm4eic::TrackSeedData>
┃   ┃   ┣━━ 🍃 TrackerTruthSeeds.hits_begin uint32_t[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeeds.hits_end uint32_t[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeeds.perigee.x float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeeds.perigee.y float[]
┃   ┃   ┣━━ 🍃 TrackerTruthSeeds.perigee.z float[]
┃   ┃   ┗━━ 🍃 TrackerTruthSeeds.quality float[]
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
┃   ┣━━ 🌿 _B0ECalClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _B0ECalClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _B0ECalClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0ECalClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0ECalClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _B0ECalClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _B0ECalClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _B0ECalClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _B0ECalClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _B0ECalClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _B0ECalRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0ECalRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0ECalRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackUnfilteredAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackUnfilteredAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackUnfilteredAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackUnfilteredAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackUnfilteredAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackUnfilteredAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackUnfilteredLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackUnfilteredLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackUnfilteredLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrackUnfilteredLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrackUnfilteredLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrackUnfilteredLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracksUnfiltered_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracksUnfiltered_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracksUnfiltered_measurements.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracksUnfiltered_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracksUnfiltered_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracksUnfiltered_tracks.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracksUnfiltered_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracksUnfiltered_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracksUnfiltered_trajectory.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTracks_trajectory.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTrajectoriesUnfiltered_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTrajectoriesUnfiltered_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrajectoriesUnfiltered_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_seed.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrajectoriesUnfiltered_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectoriesUnfiltered_trackParameters.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTrajectories_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectories_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTrajectories_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectories_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrajectories_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectories_seed.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTrajectories_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTrajectories_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTrajectories_trackParameters.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrackUnfilteredLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracksUnfiltered_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_measurements.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracksUnfiltered_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_tracks.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracksUnfiltered_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracksUnfiltered_trajectory.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTracks_trajectory.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_seed.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectoriesUnfiltered_trackParameters.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectories_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectories_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectories_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_seed.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerCKFTruthSeededTrajectories_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerCKFTruthSeededTrajectories_trackParameters.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerMeasurements_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerMeasurements_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerMeasurements_hits.index int32_t[]
┃   ┣━━ 🍃 _B0TrackerMeasurements_weights std::vector<float>
┃   ┣━━ 🌿 _B0TrackerRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerSeeds_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerSeeds_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerSeeds_hits.index int32_t[]
┃   ┣━━ 🌿 _B0TrackerSeeds_params vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _B0TrackerSeeds_params.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _B0TrackerSeeds_params.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _BackwardMPGDEndcapRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _BackwardMPGDEndcapRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _BackwardMPGDEndcapRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _CalorimeterTrackProjections_points vector<edm4eic::TrackPoint>
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.directionError.xx float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.directionError.xy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.directionError.yy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentum.x float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentum.y float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentum.z float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.xx float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.xy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.xz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.yy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.yz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.momentumError.zz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.pathlength float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.pathlengthError float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.phi float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.position.x float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.position.y float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.position.z float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.xx float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.xy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.xz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.yy float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.yz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.positionError.zz float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.surface uint64_t[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.system uint32_t[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.theta float[]
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_points.time float[]
┃   ┃   ┗━━ 🍃 _CalorimeterTrackProjections_points.timeError float[]
┃   ┣━━ 🌿 _CalorimeterTrackProjections_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CalorimeterTrackProjections_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CalorimeterTrackProjections_track.index int32_t[]
┃   ┣━━ 🌿 _CentralAndB0TrackVertices_associatedParticles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralAndB0TrackVertices_associatedParticles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralAndB0TrackVertices_associatedParticles.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackUnfilteredAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackUnfilteredAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackUnfilteredAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackUnfilteredAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackUnfilteredAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackUnfilteredAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackUnfilteredLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackUnfilteredLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackUnfilteredLinks_from.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrackUnfilteredLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrackUnfilteredLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrackUnfilteredLinks_to.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracksUnfiltered_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracksUnfiltered_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracksUnfiltered_measurements.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracksUnfiltered_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracksUnfiltered_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracksUnfiltered_tracks.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracksUnfiltered_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracksUnfiltered_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracksUnfiltered_trajectory.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTracks_trajectory.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTrajectoriesUnfiltered_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectoriesUnfiltered_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTrajectoriesUnfiltered_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectoriesUnfiltered_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrajectoriesUnfiltered_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectoriesUnfiltered_seed.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrajectoriesUnfiltered_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectoriesUnfiltered_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectoriesUnfiltered_trackParameters.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTrajectories_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTrajectories_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectories_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectories_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTrajectories_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTrajectories_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectories_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectories_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrajectories_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectories_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectories_seed.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTrajectories_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTrajectories_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTrajectories_trackParameters.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackUnfilteredAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackUnfilteredAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackUnfilteredLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredLinks_from.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrackUnfilteredLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrackUnfilteredLinks_to.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracksUnfiltered_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_measurements.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracksUnfiltered_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_tracks.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracksUnfiltered_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracksUnfiltered_trajectory.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTracks_trajectory.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectoriesUnfiltered_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_seed.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectoriesUnfiltered_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectoriesUnfiltered_trackParameters.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_measurementChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectories_measurements_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_measurements_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectories_measurements_deprecated.index int32_t[]
┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_outlierChi2 std::vector<float>
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectories_outliers_deprecated vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_outliers_deprecated.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectories_outliers_deprecated.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectories_seed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_seed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectories_seed.index int32_t[]
┃   ┣━━ 🌿 _CentralCKFTruthSeededTrajectories_trackParameters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralCKFTruthSeededTrajectories_trackParameters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralCKFTruthSeededTrajectories_trackParameters.index int32_t[]
┃   ┣━━ 🌿 _CentralTrackSeeds_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralTrackSeeds_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralTrackSeeds_hits.index int32_t[]
┃   ┣━━ 🌿 _CentralTrackSeeds_params vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralTrackSeeds_params.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralTrackSeeds_params.index int32_t[]
┃   ┣━━ 🌿 _CentralTrackSegments_points vector<edm4eic::TrackPoint>
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.directionError.xx float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.directionError.xy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.directionError.yy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentum.x float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentum.y float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentum.z float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.xx float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.xy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.xz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.yy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.yz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.momentumError.zz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.pathlength float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.pathlengthError float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.phi float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.position.x float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.position.y float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.position.z float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.xx float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.xy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.xz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.yy float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.yz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.positionError.zz float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.surface uint64_t[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.system uint32_t[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.theta float[]
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_points.time float[]
┃   ┃   ┗━━ 🍃 _CentralTrackSegments_points.timeError float[]
┃   ┣━━ 🌿 _CentralTrackSegments_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralTrackSegments_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralTrackSegments_track.index int32_t[]
┃   ┣━━ 🌿 _CentralTrackVertices_associatedParticles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralTrackVertices_associatedParticles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralTrackVertices_associatedParticles.index int32_t[]
┃   ┣━━ 🌿 _CentralTrackerMeasurements_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CentralTrackerMeasurements_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CentralTrackerMeasurements_hits.index int32_t[]
┃   ┣━━ 🍃 _CentralTrackerMeasurements_weights std::vector<float>
┃   ┣━━ 🍃 _CombinedTOFParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _CombinedTOFParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CombinedTOFParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CombinedTOFParticleIDs_particle.index int32_t[]
┃   ┣━━ 🍃 _CombinedTOFTruthSeededParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _CombinedTOFTruthSeededParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _CombinedTOFTruthSeededParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _CombinedTOFTruthSeededParticleIDs_particle.index int32_t[]
┃   ┣━━ 🍃 _DIRCParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _DIRCParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DIRCParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DIRCParticleIDs_particle.index int32_t[]
┃   ┣━━ 🍃 _DIRCTruthSeededParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _DIRCTruthSeededParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DIRCTruthSeededParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DIRCTruthSeededParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _DRICHAerogelIrtCherenkovParticleID_chargedParticle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_chargedParticle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_chargedParticle.index int32_t[]
┃   ┣━━ 🌿 _DRICHAerogelIrtCherenkovParticleID_hypotheses vector<edm4eic::CherenkovParticleIDHypothesis>
┃   ┃   ┣━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_hypotheses.PDG int32_t[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_hypotheses.npe float[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_hypotheses.weight float[]
┃   ┣━━ 🌿 _DRICHAerogelIrtCherenkovParticleID_rawHitAssociations vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_rawHitAssociations.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_rawHitAssociations.index int32_t[]
┃   ┣━━ 🌿 _DRICHAerogelIrtCherenkovParticleID_thetaPhiPhotons vector<edm4hep::Vector2f>
┃   ┃   ┣━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_thetaPhiPhotons.a float[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelIrtCherenkovParticleID_thetaPhiPhotons.b float[]
┃   ┣━━ 🌿 _DRICHAerogelTracks_points vector<edm4eic::TrackPoint>
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.directionError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.directionError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.directionError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentum.x float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentum.y float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentum.z float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.xz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.yz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.momentumError.zz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.pathlength float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.pathlengthError float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.phi float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.position.x float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.position.y float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.position.z float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.xz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.yz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.positionError.zz float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.surface uint64_t[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.system uint32_t[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.theta float[]
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_points.time float[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelTracks_points.timeError float[]
┃   ┣━━ 🌿 _DRICHAerogelTracks_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHAerogelTracks_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHAerogelTracks_track.index int32_t[]
┃   ┣━━ 🌿 _DRICHGasIrtCherenkovParticleID_chargedParticle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHGasIrtCherenkovParticleID_chargedParticle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHGasIrtCherenkovParticleID_chargedParticle.index int32_t[]
┃   ┣━━ 🌿 _DRICHGasIrtCherenkovParticleID_hypotheses vector<edm4eic::CherenkovParticleIDHypothesis>
┃   ┃   ┣━━ 🍃 _DRICHGasIrtCherenkovParticleID_hypotheses.PDG int32_t[]
┃   ┃   ┣━━ 🍃 _DRICHGasIrtCherenkovParticleID_hypotheses.npe float[]
┃   ┃   ┗━━ 🍃 _DRICHGasIrtCherenkovParticleID_hypotheses.weight float[]
┃   ┣━━ 🌿 _DRICHGasIrtCherenkovParticleID_rawHitAssociations vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHGasIrtCherenkovParticleID_rawHitAssociations.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHGasIrtCherenkovParticleID_rawHitAssociations.index int32_t[]
┃   ┣━━ 🌿 _DRICHGasIrtCherenkovParticleID_thetaPhiPhotons vector<edm4hep::Vector2f>
┃   ┃   ┣━━ 🍃 _DRICHGasIrtCherenkovParticleID_thetaPhiPhotons.a float[]
┃   ┃   ┗━━ 🍃 _DRICHGasIrtCherenkovParticleID_thetaPhiPhotons.b float[]
┃   ┣━━ 🌿 _DRICHGasTracks_points vector<edm4eic::TrackPoint>
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.directionError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.directionError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.directionError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentum.x float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentum.y float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentum.z float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.xz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.yz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.momentumError.zz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.pathlength float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.pathlengthError float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.phi float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.position.x float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.position.y float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.position.z float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.xx float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.xy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.xz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.yy float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.yz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.positionError.zz float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.surface uint64_t[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.system uint32_t[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.theta float[]
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_points.time float[]
┃   ┃   ┗━━ 🍃 _DRICHGasTracks_points.timeError float[]
┃   ┣━━ 🌿 _DRICHGasTracks_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHGasTracks_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHGasTracks_track.index int32_t[]
┃   ┣━━ 🍃 _DRICHParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _DRICHParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _DRICHRawHitsAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHRawHitsAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHRawHitsAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _DRICHRawHitsAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHRawHitsAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHRawHitsAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _DRICHRawHitsLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHRawHitsLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHRawHitsLinks_from.index int32_t[]
┃   ┣━━ 🌿 _DRICHRawHitsLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHRawHitsLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHRawHitsLinks_to.index int32_t[]
┃   ┣━━ 🍃 _DRICHTruthSeededParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _DRICHTruthSeededParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _DRICHTruthSeededParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _DRICHTruthSeededParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalBarrelClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelImagingClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelImagingClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelImagingClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelImagingClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalBarrelImagingClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelImagingProcessedHitContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingProcessedHitContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingProcessedHitContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingProcessedHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingProcessedHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingProcessedHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelImagingRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelImagingRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelImagingRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalBarrelScFiClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiNAttenuatedHitContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNAttenuatedHitContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNAttenuatedHitContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNAttenuatedHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNAttenuatedHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNAttenuatedHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCALOROCHits_aSamples vector<edm4eic::CALOROC1ASample>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCALOROCHits_aSamples.ADC uint16_t[]
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCALOROCHits_aSamples.timeOfArrival uint16_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCALOROCHits_aSamples.timeOverThreshold uint16_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCALOROCHits_bSamples vector<edm4eic::CALOROC1BSample>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCALOROCHits_bSamples.highGainADC uint16_t[]
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCALOROCHits_bSamples.lowGainADC uint16_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCALOROCHits_bSamples.timeOfArrival uint16_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulsesWithNoise_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulsesWithNoise_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulsesWithNoise_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulsesWithNoise_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulsesWithNoise_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNCombinedPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNCombinedPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNCombinedPulses_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiNPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiNPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiNPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiNPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiNPulses_trackerHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPAttenuatedHitContributions_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPAttenuatedHitContributions_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPAttenuatedHitContributions_particle.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPAttenuatedHits_contributions vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPAttenuatedHits_contributions.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPAttenuatedHits_contributions.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCALOROCHits_aSamples vector<edm4eic::CALOROC1ASample>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCALOROCHits_aSamples.ADC uint16_t[]
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCALOROCHits_aSamples.timeOfArrival uint16_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCALOROCHits_aSamples.timeOverThreshold uint16_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCALOROCHits_bSamples vector<edm4eic::CALOROC1BSample>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCALOROCHits_bSamples.highGainADC uint16_t[]
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCALOROCHits_bSamples.lowGainADC uint16_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCALOROCHits_bSamples.timeOfArrival uint16_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulsesWithNoise_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulsesWithNoise_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulsesWithNoise_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulsesWithNoise_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulsesWithNoise_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPCombinedPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPCombinedPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPCombinedPulses_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelScFiPPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelScFiPPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiPPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiPPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiPPulses_trackerHits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelScFiRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelScFiRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelScFiRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalBarrelTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalBarrelTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalBarrelTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalBarrelTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalBarrelTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalBarrelTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapNClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNSplitMergeClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNSplitMergeClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapNSplitMergeClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapNTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapNTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapNTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapNTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapPClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPSplitMergeClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPSplitMergeClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapPSplitMergeClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalEndcapPTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalEndcapPTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalEndcapPTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalEndcapPTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalFarForwardZDCClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalFarForwardZDCClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalFarForwardZDCClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalFarForwardZDCRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalFarForwardZDCTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalFarForwardZDCTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalFarForwardZDCTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalLumiSpecClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalLumiSpecClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalLumiSpecClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalLumiSpecClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalLumiSpecClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _EcalLumiSpecRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _EcalLumiSpecTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _EcalLumiSpecTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _EcalLumiSpecTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🍃 _EventHeader_weights std::vector<double>
┃   ┣━━ 🌿 _ForwardMPGDEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _ForwardMPGDEndcapRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardMPGDEndcapRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardMPGDEndcapRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ForwardMPGDEndcapRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ForwardMPGDEndcapRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardMPGDEndcapRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardMPGDEndcapRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMRecParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMRecParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMRecParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ForwardOffMTrackerRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardOffMTrackerRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardOffMTrackerRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotHits_particle.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotRecParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotRecParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotRecParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ForwardRomanPotStaticRecParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ForwardRomanPotStaticRecParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ForwardRomanPotStaticRecParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _GeneratedBreitFrameParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedBreitFrameParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedBreitFrameParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_particles.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _GeneratedCentauroJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedCentauroJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedCentauroJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_particles.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _GeneratedChargedJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedChargedJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedChargedJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_particles.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _GeneratedJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _GeneratedParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _GeneratedParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _GeneratedParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _HadronicFinalState_hadrons vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HadronicFinalState_hadrons.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HadronicFinalState_hadrons.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalBarrelClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalBarrelClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalBarrelMergedHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelMergedHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelMergedHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelSplitMergeClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelSplitMergeClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalBarrelSplitMergeClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalBarrelTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalBarrelTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalBarrelTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalBarrelTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalBarrelTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalBarrelTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalBarrelTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalEndcapNClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNMergedHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNMergedHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNMergedHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNSplitMergeClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNSplitMergeClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalEndcapNSplitMergeClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapNTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapNTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapNTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalEndcapNTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapPInsertClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapPInsertClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalEndcapPInsertClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalEndcapPInsertMergedHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertMergedHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertMergedHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalEndcapPInsertRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalEndcapPInsertRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalEndcapPInsertRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterAssociationsBaseline_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterAssociationsBaseline_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterAssociationsBaseline_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterAssociationsBaseline_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterAssociationsBaseline_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterAssociationsBaseline_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterLinksBaseline_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterLinksBaseline_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterLinksBaseline_from.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterLinksBaseline_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterLinksBaseline_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterLinksBaseline_to.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClustersBaseline_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClustersBaseline_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalFarForwardZDCClustersBaseline_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClustersBaseline_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClustersBaseline_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClustersBaseline_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalFarForwardZDCClustersBaseline_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalFarForwardZDCClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalFarForwardZDCClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalFarForwardZDCClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _HcalFarForwardZDCRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCSubcellHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCSubcellHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCSubcellHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _HcalFarForwardZDCTruthClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _HcalFarForwardZDCTruthClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _HcalFarForwardZDCTruthClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _InclusiveKinematicsDA_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsDA_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsDA_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsESigma_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsESigma_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsESigma_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsElectron_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsElectron_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsElectron_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsJB_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsJB_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsJB_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsML_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsML_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsML_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsSigma_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsSigma_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsSigma_scat.index int32_t[]
┃   ┣━━ 🌿 _InclusiveKinematicsTruth_scat vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _InclusiveKinematicsTruth_scat.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _InclusiveKinematicsTruth_scat.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _LFHCALClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _LFHCALClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _LFHCALClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _LFHCALClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _LFHCALClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _LFHCALRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusterAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusterAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusterAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusterAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusterAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusterAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusterLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusterLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusterLinks_from.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusterLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusterLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusterLinks_to.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusters_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusters_clusters.index int32_t[]
┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_hitContributions std::vector<float>
┃   ┣━━ 🌿 _LFHCALSplitMergeClusters_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusters_hits.index int32_t[]
┃   ┣━━ 🌿 _LFHCALSplitMergeClusters_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALSplitMergeClusters_particleIDs.index int32_t[]
┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_shapeParameters std::vector<float>
┃   ┣━━ 🍃 _LFHCALSplitMergeClusters_subdetectorEnergies std::vector<float>
┃   ┣━━ 🌿 _LFHCALTrackClusterMatches_cluster vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALTrackClusterMatches_cluster.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALTrackClusterMatches_cluster.index int32_t[]
┃   ┣━━ 🌿 _LFHCALTrackClusterMatches_track vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _LFHCALTrackClusterMatches_track.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _LFHCALTrackClusterMatches_track.index int32_t[]
┃   ┣━━ 🌿 _MCParticlesHeadOnFrameNoBeamFX_daughters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticlesHeadOnFrameNoBeamFX_daughters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticlesHeadOnFrameNoBeamFX_daughters.index int32_t[]
┃   ┣━━ 🌿 _MCParticlesHeadOnFrameNoBeamFX_parents vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticlesHeadOnFrameNoBeamFX_parents.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticlesHeadOnFrameNoBeamFX_parents.index int32_t[]
┃   ┣━━ 🌿 _MCParticles_daughters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticles_daughters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticles_daughters.index int32_t[]
┃   ┣━━ 🌿 _MCParticles_parents vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MCParticles_parents.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MCParticles_parents.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _MPGDBarrelRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _MPGDBarrelRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _MPGDBarrelRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _OuterMPGDBarrelRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _OuterMPGDBarrelRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _OuterMPGDBarrelRecHits_rawHit.index int32_t[]
┃   ┣━━ 🍃 _RICHEndcapNParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _RICHEndcapNParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _RICHEndcapNRawHitsAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNRawHitsAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNRawHitsAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _RICHEndcapNRawHitsAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNRawHitsAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNRawHitsAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _RICHEndcapNRawHitsLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNRawHitsLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNRawHitsLinks_from.index int32_t[]
┃   ┣━━ 🌿 _RICHEndcapNRawHitsLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNRawHitsLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNRawHitsLinks_to.index int32_t[]
┃   ┣━━ 🍃 _RICHEndcapNTruthSeededParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _RICHEndcapNTruthSeededParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _RICHEndcapNTruthSeededParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _RICHEndcapNTruthSeededParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedBreitFrameParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedBreitFrameParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedBreitFrameParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedCentauroJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedCentauroJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedCentauroJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticleAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticleAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticleAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticleAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticleAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticleAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticleLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticleLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticleLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticleLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticleLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticleLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedParticles_tracks.index int32_t[]
┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticleIDs_parameters std::vector<float>
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticleIDs_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticleIDs_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticleIDs_particle.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedChargedRealPIDParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedChargedRealPIDParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedChargedRealPIDParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdaDecayProductsCM_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdaDecayProductsCM_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCLambdas_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCLambdas_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCLambdas_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedFarForwardZDCNeutrals_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedFarForwardZDCNeutrals_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedFarForwardZDCNeutrals_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedJets_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedJets_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedJets_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticleAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticleAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticleAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticleAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticleAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticleAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticleLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticleLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticleLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticleLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticleLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticleLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticleAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticleAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticleAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticleAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticleAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticleAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticleLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticleLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticleLinks_from.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticleLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticleLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticleLinks_to.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _ReconstructedTruthSeededChargedParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _ReconstructedTruthSeededChargedParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _ReconstructedTruthSeededChargedParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _SecondaryVerticesHelix_associatedParticles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SecondaryVerticesHelix_associatedParticles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SecondaryVerticesHelix_associatedParticles.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelTrackerRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelTrackerRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelTrackerRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelVertexRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelVertexRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelVertexRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelVertexRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelVertexRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelVertexRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelVertexRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelVertexRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelVertexRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelVertexRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelVertexRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelVertexRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _SiBarrelVertexRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiBarrelVertexRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiBarrelVertexRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _SiEndcapTrackerRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiEndcapTrackerRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiEndcapTrackerRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _SiEndcapTrackerRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiEndcapTrackerRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiEndcapTrackerRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _SiEndcapTrackerRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiEndcapTrackerRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiEndcapTrackerRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _SiEndcapTrackerRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiEndcapTrackerRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiEndcapTrackerRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _SiEndcapTrackerRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _SiEndcapTrackerRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _SiEndcapTrackerRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelClusterHits_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelClusterHits_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelClusterHits_hits.index int32_t[]
┃   ┣━━ 🍃 _TOFBarrelClusterHits_weights std::vector<float>
┃   ┣━━ 🌿 _TOFBarrelHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TOFBarrelRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFBarrelRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFBarrelRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapRecHits_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapRecHits_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapRecHits_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TOFEndcapSharedHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TOFEndcapSharedHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TOFEndcapSharedHits_particle.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_amplitude std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulsesWithNoise_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulsesWithNoise_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_particles.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulsesWithNoise_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_pulses.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulsesWithNoise_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulsesWithNoise_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerCombinedPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerCombinedPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerCombinedPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerCombinedPulses_trackerHits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerHitPulses_amplitude std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerHitPulses_calorimeterHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHitPulses_calorimeterHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHitPulses_calorimeterHits.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerHitPulses_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHitPulses_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHitPulses_particles.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerHitPulses_pulses vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHitPulses_pulses.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHitPulses_pulses.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerHitPulses_trackerHits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHitPulses_trackerHits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHitPulses_trackerHits.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1L0ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1L0ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1L0ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM1L0ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM1L1ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1L1ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1L1ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM1L1ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM1L2ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1L2ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1L2ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM1L2ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM1L3ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1L3ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1L3ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM1L3ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM1LocalTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM1LocalTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM1LocalTracks_trajectory.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2L0ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2L0ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2L0ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM2L0ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM2L1ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2L1ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2L1ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM2L1ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM2L2ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2L2ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2L2ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM2L2ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM2L3ClusterPositions_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2L3ClusterPositions_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2L3ClusterPositions_hits.index int32_t[]
┃   ┣━━ 🍃 _TaggerTrackerM2L3ClusterPositions_weights std::vector<float>
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTrackAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTrackAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTrackAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTrackAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTrackAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTrackAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTrackLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTrackLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTrackLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTrackLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTrackLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTrackLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTracks_measurements vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTracks_measurements.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTracks_measurements.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTracks_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTracks_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTracks_tracks.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerM2LocalTracks_trajectory vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerM2LocalTracks_trajectory.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerM2LocalTracks_trajectory.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerRawHitAssociations_rawHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerRawHitAssociations_rawHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerRawHitAssociations_rawHit.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerRawHitAssociations_simHit vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerRawHitAssociations_simHit.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerRawHitAssociations_simHit.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerRawHitLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerRawHitLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerRawHitLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerRawHitLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerRawHitLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerRawHitLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticleAssociations_rec vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticleAssociations_rec.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticleAssociations_rec.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticleAssociations_sim vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticleAssociations_sim.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticleAssociations_sim.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticleLinks_from vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticleLinks_from.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticleLinks_from.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticleLinks_to vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticleLinks_to.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticleLinks_to.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_clusters vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_clusters.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_clusters.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_particleIDUsed vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_particleIDUsed.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_particleIDUsed.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_particleIDs vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_particleIDs.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_particleIDs.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_particles vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_particles.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_particles.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_startVertex vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_startVertex.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_startVertex.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerReconstructedParticles_tracks vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerReconstructedParticles_tracks.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerReconstructedParticles_tracks.index int32_t[]
┃   ┣━━ 🌿 _TaggerTrackerSharedHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TaggerTrackerSharedHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TaggerTrackerSharedHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TrackerEndcapHits_particle vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TrackerEndcapHits_particle.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TrackerEndcapHits_particle.index int32_t[]
┃   ┣━━ 🌿 _TrackerTruthSeeds_hits vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TrackerTruthSeeds_hits.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TrackerTruthSeeds_hits.index int32_t[]
┃   ┣━━ 🌿 _TrackerTruthSeeds_params vector<podio::ObjectID>
┃   ┃   ┣━━ 🍃 _TrackerTruthSeeds_params.collectionID uint32_t[]
┃   ┃   ┗━━ 🍃 _TrackerTruthSeeds_params.index int32_t[]
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