<script>
  import { mapState, mapMutations } from 'vuex'
  export default {
    name: 'messageCard',
    props: ['model'],
    data() {
      return {

      }
    },
    beforeMount() {

    },
    mounted() {

    },
    destroyed() {

    },
    computed: {
      ...mapState({

      })
    },
    methods: {
      ...mapMutations({

      })
    },
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">
</style>

<template>
  <div :id="$options.name" :class="$options.name">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">{{model.name}}</p>
        <a href="#" class="card-header-icon" aria-label="more options">
      <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
        </a>
      </header>
      <div class="card-content">
        <div class="content">
          <article class="message is-dark">
            <div class="message-body"><strong>基本信息</strong></div>
          </article>
          <table class="table is-fullwidth">
            <thead>
            <tr><td><strong>信息</strong></td><td><strong>内容</strong></td></tr>
            </thead>
            <tr v-for="(item, key, index) in model.data" v-if="key !== 'score_detail'">
              <td><strong>{{ key }}</strong></td><td>{{ item }}</td>
            </tr>
          </table>

          <article class="message is-dark">
            <div class="message-body"><strong>解题信息</strong></div>
          </article>
          <table class="table is-fullwidth">
            <thead>
            <tr>
              <td><strong>解题</strong></td>
              <td><strong>该题排名</strong></td>
              <td><strong>该题得分</strong></td>
              <td><strong>解题时间</strong></td>
            </tr>
            </thead>
            <tr v-for="slv in model.data.score_detail">
              <td>{{ slv.solve_question }}</td>
              <td>{{ slv.ranking }}</td>
              <td>{{ slv.gain_score }}</td>
              <td>{{ slv.solve_time }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
