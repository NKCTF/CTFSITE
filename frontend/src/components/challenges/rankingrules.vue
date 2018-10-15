<script>
  import { mapState, mapMutations } from 'vuex'

  export default {
    name: 'rules',
  };

</script>
<!-- vue-loader's scoped css won't work with style-loader -->
<style scoped lang="vcss">

</style>

<template>
  <div :id="$options.name" :class="$options.name">
    <h>关于 NKCTF 的计分规则</h>
    <p>本系统参考遗传算法中的淘汰算法进行计分，在遗传算法中提出的是一个权值函数。假设 n 为当前的题目的解题人数，那么对 k ∈ [1,n] 表示第 k 个解出题目的用户，其分数权值应该为：</p>
  </div>
</template>
