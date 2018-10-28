<script>
import {mapState, mapMutations} from 'vuex';

export default {
  name: 'challenges',
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

<style scoped lang="vcss">
.tile.is-ancestor {
  width: 100%;
}
.challenges {
  padding-bottom: 2rem;
}
</style>

<template>
<div :id="$options.name" :class="$options.name">
  <div style="padding-bottom: 1rem">
    <a class="button is-rounded is-info" href="http://ctf.shesl.top:8000/rules.zip">
    <span class="icon">
      <i class="fas fa-info "></i>
    </span>
      <span>分数规则</span>
    </a>
  </div>
  <div class="tile is-ancestor">
    <tagsection title="PWN" subtitle="二进制"
      content="是一个黑客语法的俚语词，在黑客行话里，包括电脑（服务器或个人电脑）、网站、闸道装置、或是应用程序，
      'pwn'在这一方面的意思是攻破或是控制。"
      style="width:33%;"></tagsection>
    <tagsection title="WEB" subtitle="网络"
       content="在 CTF 竞赛中，WEB 也是占比重很大的一个方向之一，WEB 类的题目种类繁多，
       知识点细碎，时效性强，能紧跟时下热点漏洞，贴近实战。"
      style="width: 33%;"></tagsection>
    <tagsection title="Crypto" subtitle="密码学"
        content="古典密码学，作为一种实用性艺术存在，并没有对密码学原件进行清晰的定义。
       而现代密码学则起源于 20 世纪中后期出现的大量相关理论。密码学需要强大的数学基础。"
                style="width: 33%;"></tagsection>
  </div>
  <div class="tile is-ancestor">
    <tagsection title="Reverse" subtitle="逆向"
        content="软件代码逆向主要指对软件的结构，流程，算法，代码等进行逆向拆解和分析。
        主要应用于软件维护，软件破解，漏洞挖掘，恶意代码分析。"
        style="width:50%; height: 100%"></tagsection>
    <tagsection title="MISC" subtitle="杂项"
        content="Misc 是英文 Miscellaneous 的前四个字母，杂项、混合体、大杂烩的意思。
        Misc 在国外的比赛中其实又被具体划分为各个小块，有Recon, Forensic, Stego, Misc..."
        style="width:50%; height: 100%"></tagsection>
  </div>
</div>
</template>
