<script>
  import { mapState, mapMutations } from 'vuex'
  export default {
    name: 'reg-info',
    inheritAttrs: false,
    props: ['model'],
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">

</style>

<template>
  <div class="field">
    <label class="label"><slot></slot></label>
    <div class="notification">
      {{model.value}}
    </div>
  </div>
</template>
