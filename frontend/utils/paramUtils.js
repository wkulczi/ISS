export const parametersUtil = {
  checkInflowRate(inflowRate) {
    if (inflowRate) {
      if (inflowRate > 250) {
        return 250
      } else if (inflowRate < 0) {
        return 0
      } else {
        return inflowRate
      }
    }
  },
  checkHeightSet(heightSet) {
    if (heightSet) {
      if (heightSet > 150) {
        return 150
      } else if (heightSet < 0.0001) {
        return 0.0001
      } else {
        return heightSet
      }
    }
  },
  checkHeightAtZero(heightAtZero) {
    if (heightAtZero) {
      if (heightAtZero > 150) {
        return 150
      } else if (heightAtZero < 0) {
        return 0
      } else {
        return heightAtZero
      }
    }
  },
  checkTestDuration(testDuration) {
    if (testDuration) {
      if (testDuration > 500) {
        return 500
      } else if (testDuration < 1) {
        return 1
      } else {
        return testDuration
      }
    }
  },
  checkSamplingFrequency(samplingFrequency) {
    if (samplingFrequency) {
      if (samplingFrequency > 500) {
        return 500
      } else if (samplingFrequency < 1) {
        return 1
      } else {
        return samplingFrequency
      }
    }
  },
  checkCrossSectionTankArea(crossSectionTankArea) {
    if (crossSectionTankArea) {
      if (crossSectionTankArea > 250) {
        return 250
      } else if (crossSectionTankArea < 1) {
        return 1
      } else {
        return crossSectionTankArea
      }
    }
  },
  checkFreeOutflowRate(freeOutflowRate) {
    if (freeOutflowRate) {
      if (freeOutflowRate > 250) {
        return 250
      } else if (freeOutflowRate < 0) {
        return 0
      } else {
        return freeOutflowRate
      }
    }
  },
  checkContainerHeight(containerHeight) {
    if (containerHeight) {
      if (containerHeight > 150) {
        return 150
      } else if (containerHeight < 0) {
        return 1
      } else {
        return containerHeight
      }
    }
  },
  validateParameters(simParams) {
    if (simParams.inflow_rate) {
      simParams.inflow_rate = this.checkInflowRate(simParams.inflow_rate)
    }
    if (simParams.height_set) {
      simParams.inflow_rate = this.checkHeightSet(simParams.height_set)
    }
    if (simParams.height_at_zero) {
      simParams.height_at_zero = this.checkHeightAtZero(
        simParams.height_at_zero
      )
    }
    if (simParams.test_duration) {
      simParams.test_duration = this.checkTestDuration(simParams.test_duration)
    }
    if (simParams.sampling_frequency) {
      simParams.sampling_frequency = this.checkSamplingFrequency(
        simParams.sampling_frequency
      )
    }
    if (simParams.cross_section_tank_area) {
      simParams.cross_section_tank_area = this.checkCrossSectionTankArea(
        simParams.cross_section_tank_area
      )
    }
    if (simParams.free_outflow_rate) {
      simParams.free_outflow_rate = this.checkFreeOutflowRate(
        simParams.free_outflow_rate
      )
    }
    if (simParams.container_height) {
      simParams.container_height = this.checkContainerHeight(
        simParams.container_height
      )
    }
    return simParams
  },
}
