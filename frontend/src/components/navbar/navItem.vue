<script>
  import {mapState, mapMutations} from 'vuex';

  export default {
    name: 'nav-item',
    props: ['to'],
    beforeMount() {

    },
    mounted() {

    },
    destroyed() {

    },
    computed: {
      ...mapState({}),
    },
    methods: {
      ...mapMutations({}),
    },
  };

</script>

<style>
.nav-item {
  display: flex !important;
  justify-content: center;
  align-items: center;
}
</style>

<template>
  <div :class="$options.name" class="column">
    <router-link :to="to" class="is-info">
      <slot></slot>
    </router-link>
  </div>
</template>
