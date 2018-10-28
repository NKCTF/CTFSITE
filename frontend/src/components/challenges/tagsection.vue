<script>
  import { mapState, mapMutations } from 'vuex'
  export default {
    name: 'tagsection',
    props: ['title', 'subtitle', 'content'],
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">

</style>

<template>
  <div :id="$options.name" :class="$options.name">
    <router-link tag="div" :to="'challenges/tag/' + title" class="tile is-parent" style="cursor: pointer">
      <article class="tile box is-child has-text-centered">
        <p class="title">{{ title }}</p>
        <p class="subtitle">{{ subtitle }}</p>
        <div class="content"style="height: 100%">{{ content }}</div>
      </article>
    </router-link>
  </div>
</template>
