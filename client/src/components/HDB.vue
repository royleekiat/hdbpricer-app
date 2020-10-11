<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>HDB</h1>
        <hr />
        <br /><br />
		<alert :message=message v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-b-modal.HDB-modal
        >
          Price new HDB
        </button>

        <br /><br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Town</th>
              <th scope="col">Flat type</th>
              <th scope="col">Block</th>
              <th scope="col">Street name</th>
              <th scope="col">Storey range</th>
              <th scope="col">Floor area (sqm)</th>
              <th scope="col">Flat Model</th>
              <th scope="col">Lease commence date</th>
              <th scope="col">Remaining Lease</th>
              <th scope="col">Resale price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(hdb, index) in hdbs" :key="index">
              <td>{{ hdb.town }}</td>
              <td>{{ hdb.flat_type }}</td>
              <td>{{ hdb.block }}</td>
              <td>{{ hdb.street_name }}</td>
              <td>{{ hdb.storey_range }}</td>
              <td>{{ hdb.floor_area_sqm }}</td>
              <td>{{ hdb.flat_model }}</td>
              <td>{{ hdb.lease_commence_date }}</td>
              <td>{{ hdb.remaining_lease }}</td>
              <td>{{ hdb.resale_price }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal
      ref="priceHDBModal"
      id="HDB-modal"
      title="Price an HDB"
      hide-footer
    >
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-town-group"
          label="Town:"
          label-for="form-town-input"
        >
          <b-form-input
            id="form-town-input"
            type="text"
            v-model="priceHDBForm.town"
            required
            placeholder="Enter town"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-flat_type-group"
          label="Flat type:"
          label-for="form-flat_type-input"
        >
          <b-form-input
            id="form-flat_type-input"
            type="text"
            v-model="priceHDBForm.flat_type"
            required
            placeholder="Enter Flat type"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-block-group"
          label="Block:"
          label-for="form-block-input"
        >
          <b-form-input
            id="form-block-input"
            type="text"
            v-model="priceHDBForm.block"
            required
            placeholder="Enter block"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-street_name-group"
          label="Street name :"
          label-for="form-street_name-input"
        >
          <b-form-input
            id="form-street_name-input"
            type="text"
            v-model="priceHDBForm.street_name"
            required
            placeholder="Enter Street name"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-storey_range-group"
          label="Storey range:"
          label-for="form-storey_range-input"
        >
          <b-form-input
            id="form-storey_range-input"
            type="text"
            v-model="priceHDBForm.storey_range"
            required
            placeholder="Enter Storey range"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-floor_area_sqm-group"
          label="Floor area (sqm):"
          label-for="form-floor_area_sqm-input"
        >
          <b-form-input
            id="form-floor_area_sqm-input"
            type="text"
            v-model="priceHDBForm.floor_area_sqm"
            required
            placeholder="Enter Floor area (sqm)"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-flat_model-group"
          label="Flat model:"
          label-for="form-flat_model-input"
        >
          <b-form-input
            id="form-flat_model-input"
            type="text"
            v-model="priceHDBForm.flat_model"
            required
            placeholder="Enter Flat model"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-lease_commence_date-group"
          label="Lease commence date (Year):"
          label-for="form-lease_commence_date-input"
        >
          <b-form-input
            id="form-lease_commence_date-input"
            type="text"
            v-model="priceHDBForm.lease_commence_date"
            required
            placeholder="Enter Lease commence date (Year)"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-remaining_lease-group"
          label="Remaining lease:"
          label-for="form-remaining_lease-input"
        >
          <b-form-input
            id="form-remaining_lease-input"
            type="text"
            v-model="priceHDBForm.remaining_lease"
            required
            placeholder="Enter Remaining lease"
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
import axios from "axios";
import Alert from './Alert.vue';

export default {
  data() {
    return {
      hdbs: [],
      priceHDBForm: {
        town: "",
        flat_type: "",
        block: "",
        street_name: "",
        storey_range: "",
        floor_area_sqm: "",
        flat_model: "",
        lease_commence_date: "",
        remaining_lease: "",
	  },
	  message: '',
	  showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getHDBs() {
      const path = "http://localhost:5000/hdbs";
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
      this.priceHDBForm.town = "";
      this.priceHDBForm.flat_type = "";
      this.priceHDBForm.block = "";
      this.priceHDBForm.street_name = "";
      this.priceHDBForm.storey_range = "";
      this.priceHDBForm.floor_area_sqm = "";
      this.priceHDBForm.flat_model = "";
      this.priceHDBForm.lease_commence_date = "";
      this.priceHDBForm.remaining_lease = "";
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.priceHDBModal.hide();
      const payload = {
        town: this.priceHDBForm.town,
        flat_type: this.priceHDBForm.flat_type,
        block: this.priceHDBForm.block,
        street_name: this.priceHDBForm.street_name ,
        storey_range: this.priceHDBForm.storey_range ,
        floor_area_sqm: this.priceHDBForm.floor_area_sqm ,
        flat_model: this.priceHDBForm.flat_model ,
        lease_commence_date: this.priceHDBForm.lease_commence_date ,
        remaining_lease: this.priceHDBForm.remaining_lease ,
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