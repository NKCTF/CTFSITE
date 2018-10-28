<script>
  import { mapState, mapMutations } from 'vuex'

  const {STATE_ERROR, STATE_PENDING, STATE_NONE, STATE_SUCCESS} = require('../../utils/fieldModel');

  export default {
    name: 'solvedetail',
    data() {
      return {
        tableState: STATE_NONE,
        solveList: [],
        errorMsg: '',
        STATE_ERROR,
        STATE_PENDING,
        STATE_NONE,
      }
    },
    mounted(){
      this.fetch();
    },
    computed: {
      ...mapState({

      })
    },
    methods: {
      ...mapMutations({

      }),
      fetch (){
        this.tableState = STATE_PENDING;
        let solveq = this.$route.params["solveq"];
        return APIFetch(`/question/slv?question_id=${solveq}`).then(
            data => {
              console.log(data);
              if(data.code === 0) {
                this.solveList = data.data;
                this.tableState = STATE_SUCCESS;
              }else {
                this.errorMsg = `${data.msg}: ${data.error}`;
                this.tableState = STATE_ERROR;
              }
            }
        );
      },
    },
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">
  .solvedetail {
    justify-content: unset !important;
  }
  .solvedetail {
    padding-bottom: 2rem;
  }
</style>

<template>
  <div :id="$options.name" :class="$options.name">
    <article class="message is-danger" v-if="tableState === STATE_ERROR">
      <div class="message-body">
        {{errorMsg}}
      </div>
    </article>
    <table class="table is-striped is-hoverable is-fullwidth"  :class="{'is-loading': tableState === STATE_PENDING}">
      <thead>
      <tr>
        <th>位次</th>
        <th>用户名</th>
        <th>解题得分</th>
        <th>所得总分</th>
        <th>解题时间</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(solve, index) in solveList">
        <td>{{ index+1 }}</td>
        <td>{{ solve.username }}</td>
        <td>{{ solve.gain_score }}</td>
        <td>{{ solve.total_score }}</td>
        <td>{{ solve.solve_time }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>
