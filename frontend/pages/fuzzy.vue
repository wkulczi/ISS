<template>
  <v-container fluid>
    <v-col cols="12">
      <v-row justify="center" align="center">
        <v-container style="background: #1e1e1e">
          <v-card-title class="headline"> Wykres funkcji h(n)</v-card-title>
          <v-card-text>
            <apexchart
              id="chart"
              type="line"
              height="350"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </v-card-text>
        </v-container>
      </v-row>
      <v-row class="pt-3" justify="center" align="center">
        <v-container style="background: #1e1e1e">
          <v-form id="form">
            <v-container fluid>
              <v-row>
                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="simulation_parameters.test_duration"
                    label="Czas badania"
                    prefix="t ="
                    suffix="s"
                    value="0"
                    min="0"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="simulation_parameters.height_at_zero"
                    label="Poziom substancji w zbiorniku w chwili 0"
                    value="0"
                    prefix="h(0) = "
                    suffix="m"
                    max="150"
                    type="number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                  <!--                  todo validacja-->
                  <v-text-field
                    v-model="simulation_parameters.cross_section_tank_area"
                    label="Pole pow. przekroju poprzecznego zbiornika"
                    value="1"
                    prefix="A = "
                    suffix="m²"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="4">
                  <!--                  todo validator, nie może być mniejsze niż 0-->
                  <v-text-field
                    v-model="simulation_parameters.sampling_frequency"
                    label="Częstotliwość próbkowania"
                    prefix="Tp = "
                    suffix="Hz"
                    value="1"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="simulation_parameters.container_height"
                    label="Wysokość zbiornika substancji"
                    suffix="m"
                    value="0"
                    prefix="hmax = "
                    max="150"
                    type="number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="simulation_parameters.height_set"
                    label="Wartość zadana (poziom substancji w zbiorniku)"
                    suffix="m"
                    value="0"
                    prefix="h* = "
                    max="150"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" offset="4" sm="4">
                  <v-text-field
                    v-model="simulation_parameters.free_outflow_rate"
                    label="Współczynnik wypływu swobodnego ze zbiornika"
                    prefix="β = "
                    suffix="m^(5/2)/s"
                    value="0"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row justify="space-around">
                <v-btn @click="sendAndDrawGraph()">
                  Rozpocznij pracę układu
                </v-btn>
                <v-btn @click="clearGraphs()">Wyczyść</v-btn>
              </v-row>
            </v-container>
          </v-form>
        </v-container>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
import { parametersUtil } from '@/utils/paramUtils'

export default {
  data() {
    return {
      simulation_parameters: {
        height_set: 0,
        height_at_zero: 0,
        test_duration: 0,
        regulator_gain: 0,
        sampling_frequency: 1,
        lead_time: 0,
        cross_section_tank_area: 1,
        free_outflow_rate: 0,
        doubling_time: 0,
        container_height: 10,
      },
      series: [],
      chartOptions: {
        tooltip: {
          theme: 'dark',
          y: {
            formatter(value) {
              return value
            },
            title: {
              formatter(seriesName, { dataPointIndex }) {
                return 'h' + `(${dataPointIndex}) = `
              },
            },
          },
          x: {
            show: false,
          },
        },
        chart: {
          background: '#1e1e1e',
          height: 350,
          type: 'line',
          zoom: {
            enabled: false,
          },
          toolbar: {
            show: false,
          },
        },
        legend: {
          labels: {
            colors: '#ffffff',
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'stepline',
          width: 1,
        },
        yaxis: {
          labels: {
            style: {
              colors: '#ffffff',
            },
          },
        },
        xaxis: {
          labels: {
            style: {
              colors: '#ffffff',
            },
          },
          tickAmount: 25,
        },
      },
    }
  },
  methods: {
    async fetchData() {
      const params = parametersUtil.validateParameters(
        this.simulation_parameters
      )
      const response = await this.$axios.$post('/api/fuzzy', params)
      if (response.is_error === 1) {
        this.$toast.error(`Błąd obliczeń na ostatnim widocznym kroku`)
      }
      this.series.push({
        name: `Badanie ${this.series.length + 1}`,
        data: response.simulation_values,
      })
    },
    clearGraphs() {
      this.series = []
    },
    sendAndDrawGraph() {
      this.fetchData()
    },
  },
}
</script>

<style></style>
