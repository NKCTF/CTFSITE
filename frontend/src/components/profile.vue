<script>
import {mapState, mapMutations} from 'vuex';
const {STATE_NONE, STATE_ERROR, STATE_PENDING, STATE_SUCCESS, getModel} = require('../utils/fieldModel');

const username = getModel();
const password = getModel();
const email = getModel();
const description = getModel();
const qq = getModel();
const github = getModel();
const user_career = getModel();
const apply_for = getModel();

const team_name = getModel();
const team_description = getModel();
const join_date = getModel();
const members = getModel();
const application = getModel();

const search_team = getModel();
const email_title =getModel();
const email_content = getModel();
const build_team_name = getModel();
const build_team_decription = getModel();

const mail_box = getModel();

export default {
  name: 'profile',
    data() {
    return {
      username, password, email, description, qq, github, user_career, apply_for,
      team_name, team_description, join_date, members, application,
      search_team, email_title, email_content,
      build_team_name, build_team_decription, mail_box,
      current: 0,
      refreshState: STATE_NONE,
      STATE_ERROR,
      STATE_SUCCESS,
      STATE_PENDING,
    }
  },
  watch: {
    current: function(newVar) {
        this.flush();
    },
  },
  mounted() {
    this.search_team.value = null;
    this.$root.updateUserInfo().then(() => {
      this.username.value = this.userInfo.username;
      this.email.value = this.userInfo.email;
      this.description.value = this.userInfo.description;
      this.qq.value = this.userInfo.qq;
      this.github.value = this.userInfo.github;
      this.user_career.value = this.userInfo.user_career || "请选择..";
      this.apply_for.value = this.userInfo.apply_for;
      console.log(this.userInfo);
      this.team_name.value = this.teamInfo.team_name;
      this.team_description.value = this.teamInfo.description;
      this.join_date.value = this.teamInfo.join_date;
      this.members.value = this.teamInfo.members;
      this.application.value = this.teamInfo.application;
      console.log(this.teamInfo);
    });
  },
  computed: {
    ...mapState({
      userInfo: state => state.user,
      teamInfo: state => state.team,
    }),
  },
  methods: {
    ...mapMutations({}),
    flush (){
      this.$root.updateUserInfo().then(() => {
        this.username.value = this.userInfo.username;
        this.email.value = this.userInfo.email;
        this.description.value = this.userInfo.description;
        this.qq.value = this.userInfo.qq;
        this.github.value = this.userInfo.github;
        this.user_career.value = this.userInfo.user_career || "请选择..";
        this.apply_for.value = this.userInfo.apply_for;
        console.log(this.userInfo);
        this.team_name.value = this.teamInfo.team_name;
        this.team_description.value = this.teamInfo.description;
        this.join_date.value = this.teamInfo.join_date;
        this.members.value = this.teamInfo.members;
        this.application.value = this.teamInfo.application;
        console.log(this.teamInfo);
      });
      APIFetch("/message/mail_box/").then( data => {
        if (data.code === 0) {
          this.mail_box.value = data.data["join_request"].concat(data.data["normal_mail"]);
        }else{
          alert("Hello World");
          console.log(data);
        }
      })
    },
    navTo(which) {
      this.$data.current = which;
    },
    update(type) {
        this[type].state = STATE_PENDING;
        APIPost(`/user/alter/${this.current === 0 ? "alter_personal/" : "alter_team/"}`,
            {attribute: (type === "team_description" ? "description":type), value: this[type].value}).then(
          data => {
            if (data.code === 0) {
              this[type].message = data.msg;
              this[type].state = STATE_SUCCESS;
            }else{
              this[type].message = `${data.msg}: ${data.error}`;
              this[type].state = STATE_ERROR;
            }
          }
      )
    },
    updateselect(type) {
      console.log(this.$data);
      APIPost('/user/alter/alter_personal/', {attribute: type, value: this[type].value}).then(
        data => {
          if (data.code === 0){
            this[type].message = data.msg;
            this[type].state = STATE_SUCCESS;
          }else{
            this[type].message = data.error;
            this[type].state = STATE_ERROR;
          }
        }
      )
    },
    logout() {
      APIFetch('/user/logout/').then(
        data => {
          console.log(data);
          if(data.code === 0){
            setTimeout(() => this.$router.push('/login'), 800)
          }
        }
      );
    },
    searchTeam(){
      this.search_team.state = STATE_PENDING;
      return APIFetch(`/user/search/team?team_name=${this.search_team.value}`).then(
          data =>{
            if (data.code === 0) {
              this.search_team.message = "战队存在";
              this.search_team.state = STATE_SUCCESS;
            } else {
              this.search_team.message = `${data.msg}:${data.error}`;
              this.search_team.state = STATE_ERROR;
            }
          }
      )
    },
    create_team() {
      this.build_team_name.state = STATE_PENDING;
      APIPost("/user/alter/create_team/", {"team_name": this.build_team_name.value,
        "description": this.build_team_decription.value}).then(data => {
        if (data.code === 0) {
          this.build_team_name.message = data.msg;
          this.build_team_name.state = STATE_SUCCESS;
        }else{
          this.build_team_name.message = data.msg;
          this.build_team_name.state = STATE_ERROR;
        }
        this.$root.updateUserInfo();
        this.teamInfo.isJoin = true;
      });
      this.flush();
    },
    check_team_name() {
      this.build_team_name.state = STATE_PENDING;
      APIFetch(`/user/check/team_name?team_name=${this.build_team_name.value}`).then(data => {
          if (data.code === 0) {
            this.build_team_name.message = data.msg;
            this.build_team_name.state = STATE_SUCCESS;
          }else{
            this.build_team_name.message = `${data.msg} : ${data.error}`;
            this.build_team_name.state = STATE_ERROR;
          }
        }
      )
    },
    join_request(){
      this.search_team.state = STATE_PENDING;
      APIPost("/user/alter/join_team/", {"team_name": this.search_team.value,
            "email_title": this.email_title.value, "email_content": this.email_content.value,}
        ).then(data => {
            if (data.code === 0) {
              this.search_team.message = data.msg;
              this.search_team.state = STATE_SUCCESS;
            }else{
              this.search_team.message = data.msg;
              this.search_team.state = STATE_ERROR;
            }
          });
      this.flush();
    },
    refresh (){
      this.refreshState = STATE_PENDING;
      return APIFetch(`/message/refresh/team/?team_name=${this.team_name.value}`).then(data =>{
        if (data.code === 0) {
          this.flush();
          this.refreshState = STATE_SUCCESS;
        } else {
          this.errorMsg = `${data.msg}: ${data.err}`;
          this.tableState = STATE_ERROR;
        }
      })
    }
  },
};

</script>

<style scoped lang="vcss">
  .profile{
    padding-bottom: 2rem;
  }
  .profile {
    justify-content: unset!important;
  }
</style>

<template>
<div :id="$options.name" :class="$options.name">
  <div class="buttons has-addons">
    <span class="button" :class="{'is-info': current === 0}" @click="navTo(0)">用户信息</span>
    <span class="button" :class="{'is-info': current === 1}" @click="navTo(1)">团队信息</span>
    <span class="button" :class="{'is-info': current === 2}" @click="navTo(2)">邮箱信息</span>
  </div>
  <div style="width:50%">
    <template v-if="current === 0">
      <reg-input name="username" :model.sync="username" icon="fa-user"
                 placeholder="User Name" @blur="update('username')" showSuccess>Username
      </reg-input>
      <reg-input type="email" name="email" :model.sync="email" icon="fa-at"
                 placeholder="Email" @blur="update('email')" showSuccess>Email
      </reg-input>
      <reg-input type="text" name="qq" :model.sync="qq" icon="fab fa-qq"
                 placeholder="QQ" @blur="update('qq')" showSuccess>QQ
      </reg-input>
      <reg-input type="text" name="github" :model.sync="github" icon="fab fa-github-alt"
                 placeholder="GitHub" @blur="update('github')" showSuccess>Github
      </reg-input>
      <reg-input type="text" name="description" :model.sync="description" icon="fas fa-align-left"
                 placeholder="Description" @blur="update('description')" showSuccess>Description
      </reg-input>
      <reg-select usertitle="Career" :model.sync="user_career" @change="updateselect('user_career')" showSuccess>
        <option selected>请选择..</option>
        <option>WEB, 网络</option>
        <option>PWN, 二进制</option>
        <option>Reverse, 逆向</option>
        <option>Crypto, 密码学</option>
        <option>MISC, 杂项</option>
        <option>Almighty, 万精油</option>
      </reg-select>
      <a class="button is-danger is-fullwidth" @click="logout()">注销</a>
    </template>
    <template v-if="current === 1">
      <template v-if="teamInfo.isJoin">
        <reg-input type="text" name="team_name" :model.sync="team_name" icon="fas fa-users"
                   @blur="update('team_name')" placeholder="TeamName" showSuccess>Team Name</reg-input>
        <reg-input type="text" name="team_description" :model.sync="team_description" icon="fas fa-users"
                   @blur="update('team_description')" placeholder="TeamDescription" showSuccess>Team Description</reg-input>
        <!--<textarea class="textarea" placeholder="Team Description" rows="3"></textarea>-->
        <reg-info :model.sync="join_date">Join Date</reg-info>
        <div class="field">
          <label class="label">Members</label>
          <div class="notification is-warning">
            <ol><li v-for="user in members.value" style="margin-left: 3rem">{{user}}</li></ol>
          </div>
        </div>
        <label class="label">Join Request</label>
        <join_request v-for="requst in application.value" :model.sync="requst"></join_request>
        <a class="button is-dark is-fullwidth" :class="{'is-loading': refreshState === STATE_PENDING}"
            :disabled="refreshState === STATE_PENDING" @click="refresh">刷新申请</a>
      </template>
      <template v-else>
        <div class="notification is-light">您尚未加入战队，尝试<strong>加入</strong>一个？</div>
        <reg-input type="text" name="search_team" :model.sync="search_team" icon="fas fa-users-crown"
                   @blur="searchTeam" placeholder="SearchTeam" showSuccess>Which Team?</reg-input>
        <reg-input type="text" name="email_title" :model.sync="email_title" icon="fas fa-align-left"
                   placeholder="Title" showSuccess>Email Title</reg-input>
        <div class="field">
          <label class="label">Email Content</label>
          <textarea class="textarea" placeholder="Description" rows="3" v-model="email_content.value"></textarea>
        </div>
          <div class="notification" v-if="apply_for.value.length !== 0">
              您目前申请加入了这些战队：
              <ol><li v-for="team in apply_for.value" style="margin-left: 3rem">{{team}}</li></ol>
          </div>
          <a class="button is-success is-fullwidth" @click="join_request" style="margin-bottom: 3rem">发送入队申请</a>

        <div class="notification is-light">或者<strong>创建</strong>一个？</div>
        <reg-input type="text" name="build_team_name" :model.sync="build_team_name" icon="fas fa-users-crown"
                   placeholder="BuildTeam" @blur="check_team_name" showSuccess>Team Name?</reg-input>
        <div class="field">
          <label class="label">Slogan?</label>
          <textarea class="textarea" placeholder="Description" rows="3">{{build_team_decription.value}}</textarea>
        </div>
        <a class="button is-success is-fullwidth" @click="create_team" style="margin-bottom: 3rem">我要创建这个战队</a>
      </template>
    </template>
    <template v-if="current === 2">
      <div class="field" v-if="mail_box.value.length === 0">
        <label class="label">Mail Box</label>
        <div class="notification">您还没有任何邮件噢</div>
      </div>
      <normal-email v-else v-for="item in mail_box.value" :model="item"></normal-email>
    </template>
  </div>
</div>
</template>
