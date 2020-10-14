<template>
<!-- eslint-disable max-len -->
<!-- eslint-disable no-mixed-spaces-and-tabs -->
<!-- eslint-disable no-tabs -->
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>HDB</h1>
        <hr />
		<alert :message=message v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-b-modal.HDB-modal
        >
          Price new HDB
        </button>

        <br /><br />
        <table class="table table-striped table-dark">
          <thead>
            <tr>
              <th scope="col">Town</th>
              <th scope="col">Flat type</th>
              <th scope="col">Storey range</th>
              <th scope="col">Floor area (sqm)</th>
              <th scope="col">Lease commence date</th>
              <th scope="col">Resale price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(hdb, index) in hdbs" :key="index">
              <td>{{ hdb.town }}</td>
              <td>{{ hdb.flat_type }}</td>
              <td>{{ hdb.storey_range }}</td>
              <td>{{ hdb.floor_area_sqm }}</td>
              <td>{{ hdb.lease_commence_date }}</td>
              <td>S$ {{ hdb.resale_price }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--
      <div class="col-sm-6">
        <mappy></mappy>
      </div>

      <div class="col-sm-6">
        <rawdata></rawdata>
      </div>
      -->

    </div>
    <b-modal
      ref="priceHDBModal"
      id="HDB-modal"
      title="Price an HDB"
      header-bg-variant="dark"
      body-bg-variant="secondary"
      hide-footer
    >
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-town-group"
          label="Town:"
          label-for="form-town-input"
        >
          <b-form-select v-model="priceHDBForm.town" :options="townoptions" required></b-form-select>
        </b-form-group>
        <b-form-group
          id="form-flat_type-group"
          label="Flat type:"
          label-for="form-flat_type-input"
        >
          <b-form-select v-model="priceHDBForm.flat_type" :options="flat_typeoptions" required></b-form-select>
        </b-form-group>
        <b-form-group
          id="form-storey_range-group"
          label="Storey range:"
          label-for="form-storey_range-input"
        >
          <b-form-select v-model="priceHDBForm.storey_range" :options="storey_rangeoptions" required></b-form-select>
        </b-form-group>
        <b-form-group
          id="form-floor_area_sqm-group"
          label="Floor area (sqm):"
          label-for="form-floor_area_sqm-input"
        >
          <b-form-input
            id="form-floor_area_sqm-input"
            type="range"
            v-model="priceHDBForm.floor_area_sqm"
            min="30"
            max="300"
            required
            placeholder="Enter Floor area (sqm)"
          >
          </b-form-input>
          <div class="mt-2">Value: {{ priceHDBForm.floor_area_sqm }}</div>
        </b-form-group>

        <b-form-group
          id="form-lease_commence_date-group"
          label="Lease commence date (Year):"
          label-for="form-lease_commence_date-input"
        >
          <b-form-input
            id="form-lease_commence_date-input"
            type="number"
            v-model="priceHDBForm.lease_commence_date"
            min="1965"
            :max="currentYear"
            required
            placeholder="Enter Lease commence date (Year)"
          >
          </b-form-input>
        </b-form-group>
        <!-- <b-form-group id="form-read-group">
		      <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
		        <b-form-checkbox value="true">Read?</b-form-checkbox>
		      </b-form-checkbox-group>
		    </b-form-group> -->

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

  </div>
</template>
<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      hdbs: [],
      priceHDBForm: {
        town: null,
        flat_type: null,
        storey_range: null,
        floor_area_sqm: 120,
        lease_commence_date: '',
      },
      message: '',
      showMessage: false,
      variants: ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'light', 'dark'],
      headerBgVariant: 'dark',
      headerTextVariant: 'light',
      bodyBgVariant: 'light',
      bodyTextVariant: 'dark',
      footerBgVariant: 'warning',
      footerTextVariant: 'dark',
      currentYear: new Date().getFullYear(),
      townoptions: [
        { value: null, text: 'Please select a town' },
        { value: 'ANG MO KIO', text: 'ANG MO KIO' }, { value: 'BEDOK', text: 'BEDOK' }, { value: 'BISHAN', text: 'BISHAN' }, { value: 'BUKIT BATOK', text: 'BUKIT BATOK' }, { value: 'BUKIT MERAH', text: 'BUKIT MERAH' }, { value: 'BUKIT PANJANG', text: 'BUKIT PANJANG' }, { value: 'BUKIT TIMAH', text: 'BUKIT TIMAH' }, { value: 'CENTRAL AREA', text: 'CENTRAL AREA' }, { value: 'CHOA CHU KANG', text: 'CHOA CHU KANG' }, { value: 'CLEMENTI', text: 'CLEMENTI' }, { value: 'GEYLANG', text: 'GEYLANG' }, { value: 'HOUGANG', text: 'HOUGANG' }, { value: 'JURONG EAST', text: 'JURONG EAST' }, { value: 'JURONG WEST', text: 'JURONG WEST' }, { value: 'KALLANG/WHAMPOA', text: 'KALLANG/WHAMPOA' }, { value: 'MARINE PARADE', text: 'MARINE PARADE' }, { value: 'PASIR RIS', text: 'PASIR RIS' }, { value: 'PUNGGOL', text: 'PUNGGOL' }, { value: 'QUEENSTOWN', text: 'QUEENSTOWN' }, { value: 'SEMBAWANG', text: 'SEMBAWANG' }, { value: 'SENGKANG', text: 'SENGKANG' }, { value: 'SERANGOON', text: 'SERANGOON' }, { value: 'TAMPINES', text: 'TAMPINES' }, { value: 'TOA PAYOH', text: 'TOA PAYOH' }, { value: 'WOODLANDS', text: 'WOODLANDS' }, { value: 'YISHUN', text: 'YISHUN' },
      ],

      flat_typeoptions: [
        { value: null, text: 'Please select a Flat type' },
        { value: '1 ROOM', text: '1 ROOM' }, { value: '2 ROOM', text: '2 ROOM' }, { value: '3 ROOM', text: '3 ROOM' }, { value: '4 ROOM', text: '4 ROOM' }, { value: '5 ROOM', text: '5 ROOM' }, { value: 'EXECUTIVE', text: 'EXECUTIVE' }, { value: 'MULTI-GENERATION', text: 'MULTI-GENERATION' },
      ],

      storey_rangeoptions: [
        { value: null, text: 'Please select a Storey range' },
        { value: '01 TO 03', text: '01 TO 03' }, { value: '04 TO 06', text: '04 TO 06' }, { value: '07 TO 09', text: '07 TO 09' }, { value: '10 TO 12', text: '10 TO 12' }, { value: '13 TO 15', text: '13 TO 15' }, { value: '16 TO 18', text: '16 TO 18' }, { value: '19 TO 21', text: '19 TO 21' }, { value: '22 TO 24', text: '22 TO 24' }, { value: '25 TO 27', text: '25 TO 27' }, { value: '28 TO 30', text: '28 TO 30' }, { value: '31 TO 33', text: '31 TO 33' }, { value: '34 TO 36', text: '34 TO 36' }, { value: '37 TO 39', text: '37 TO 39' }, { value: '40 TO 42', text: '40 TO 42' }, { value: '43 TO 45', text: '43 TO 45' }, { value: '46 TO 48', text: '46 TO 48' }, { value: '49 TO 51', text: '49 TO 51' },
      ],

    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getHDBs() {
       const path = "http://localhost:5000/hdbs";
      //const path = '/hdbs';
      axios
        .get(path)
        .then((res) => {
          this.hdbs = res.data.hdbs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    priceHDB(payload) {
       const path = "http://localhost:5000/hdbs";
      //const path = '/hdbs';
      axios
        .post(path, payload)
        .then(() => {
          this.getHDBs();
          this.message = 'HDB priced!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getHDBs();
          this.message = 'This HDB could not be priced';
        });
    },
    initForm() {
      this.priceHDBForm.town = null;
      this.priceHDBForm.flat_type = null;
      this.priceHDBForm.storey_range = null;
      this.priceHDBForm.floor_area_sqm = 100;
      this.priceHDBForm.lease_commence_date = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.priceHDBModal.hide();
      const payload = {
        town: this.priceHDBForm.town,
        flat_type: this.priceHDBForm.flat_type,
        storey_range: this.priceHDBForm.storey_range,
        floor_area_sqm: this.priceHDBForm.floor_area_sqm,
        lease_commence_date: this.priceHDBForm.lease_commence_date,
      };
      this.priceHDB(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.priceHDBModal.hide();
      this.initForm();
    },
  },

  created() {
    this.getHDBs();
    this.showMessage = false;
  },
};
</script>
