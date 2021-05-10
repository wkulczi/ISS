<template>
  <v-container fluid>
    <v-col cols="12">
      <v-row justify="center" align="center">
        <v-container style="background: #1e1e1e">
          <v-card-title class="headline"> Wykres funkcji h(n) </v-card-title>
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
                    v-model="pid_parameters.test_duration"
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
                    v-model="pid_parameters.height_at_zero"
                    label="Poziom substancji w zbiorniku w chwili 0"
                    value="0"
                    prefix="h(0) = "
                    suffix="m"
                    max="150"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="pid_parameters.regulator_gain"
                    label="Wzmocnienie regulatora"
                    prefix="kp = "
                    value="0"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="4">
                  <!--                  todo validator, nie może być mniejsze niż 0-->
                  <v-text-field
                    v-model="pid_parameters.sampling_frequency"
                    label="Częstotliwość próbkowania"
                    prefix="Tp = "
                    suffix="Hz"
                    value="1"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="pid_parameters.height_set"
                    label="Wartość zadana (poziom substancji w zbiorniku)"
                    suffix="m"
                    value="0"
                    prefix="h* = "
                    max="150"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="pid_parameters.lead_time"
                    label="Czas wyprzedzenia"
                    prefix="Td = "
                    suffix="s"
                    value="0"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="4">
                  <!--                  todo validacja-->
                  <v-text-field
                    v-model="pid_parameters.cross_section_tank_area"
                    label="Pole pow. przekroju poprzecznego zbiornika"
                    value="1"
                    prefix="A = "
                    suffix="m²"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="pid_parameters.free_outflow_rate"
                    label="Współczynnik wypływu swobodnego ze zbiornika"
                    prefix="β = "
                    suffix="m^(5/2)/s"
                    value="0"
                    type="number"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="pid_parameters.doubling_time"
                    label="Czas zdwojenia"
                    prefix="Ti = "
                    suffix="s"
                    value="0"
                    type="number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-btn @click="sendAndDrawGraph()">
                  Rozpocznij pracę układu
                </v-btn>
              </v-row>
            </v-container>
          </v-form>
        </v-container>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      pid_parameters: {
        height_set: 0,
        height_at_zero: 0,
        test_duration: 0,
        regulator_gain: 0,
        sampling_frequency: 1,
        lead_time: 0,
        cross_section_tank_area: 1,
        free_outflow_rate: 0,
        doubling_time: 0,
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
                return seriesName + `(${dataPointIndex}) = `
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
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
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
        },
      },
    }
  },
  async fetch() {
    const response = await this.$axios.$post('/api/pid', this.pid_parameters)
    console.log(response)
  },
  methods: {
    sendAndDrawGraph() {
      // this.series.push({
      //   name: 'h',
      //   data: [10, 41, 35, 51, 49, 62, 69, 91, 148],
      // })
      this.$fetch()
    },
  },
}
</script>

<style></style>
