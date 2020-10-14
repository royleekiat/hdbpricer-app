<template>
<!-- eslint-disable max-len -->
<!-- eslint-disable no-mixed-spaces-and-tabs -->
<!-- eslint-disable no-tabs -->
  <div>
    <b-alert variant="success" show dismissible >{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],

};
</script>
