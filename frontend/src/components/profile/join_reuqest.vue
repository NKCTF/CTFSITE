<script>
  import { mapState, mapMutations } from 'vuex'
const {STATE_NONE, STATE_ERROR, STATE_PENDING, STATE_SUCCESS, getModel} = require('../../utils/fieldModel');

  export default {
    name: 'join_request',
    props: ["model"],
    data() {
      return {
        STATE_NONE,
        STATE_ERROR,
        STATE_PENDING,
        STATE_SUCCESS,
        executed: false,
      }
    },
    beforeMount() {

    },
    mounted() {
      this.model.state = STATE_NONE;
    },
    destroyed() {

    },
    computed: {
      ...mapState({

      })
    },
    methods: {
      ...mapMutations({

      }),
      execute(is_agree) {
        this.model.state = STATE_PENDING;
        APIPost('/user/alter/exe_application/', {is_agree: is_agree, username: this.model.send_by}).then(
          data => {
            if(data.code === 0){
              this.model.state = STATE_SUCCESS;
              this.executed = true;
            }else{
              this.model.state = STATE_ERROR;
            }
            this.model.message = `${data.msg}: ${data.error}`;
          }
        )
      }
    },
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">
  .join-request {
    margin-bottom: 2rem;
  }
</style>

<template>
  <div :id="$options.name" :class="$options.name">
    <div class="card" v-if="!executed">
      <header class="card-header">
        <p class="card-header-title">
          {{model.title}}
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          {{model.content}}<br><br>
          <strong>SEND BY</strong>: {{model.send_by}}<br>
          <time :datetime="model.send_time"><strong>SEND TIME</strong>: {{model.send_time}}</time>
        </div>
      </div>
      <footer class="card-footer">
        <a @click="execute(1)" class="card-footer-item">同意加入</a>
        <a @click="execute(0)" class="card-footer-item">拒绝加入</a>
      </footer>
    </div>
  </div>
</template>
