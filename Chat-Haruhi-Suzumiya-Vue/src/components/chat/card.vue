<template>
  <div id="card">
  	<header>
  	</header>
  	<footer>

  	</footer>
		<el-input class="search" type="text" size="mini" v-model="$store.state.filterKey" placeholder="搜索" prefix-icon="el-icon-search"></el-input>
		<el-button class="searchBtn" size="mini"><i class="fa fa-plus" aria-hidden="true"></i></el-button>
  </div>
</template>

<script>
export default {
  name: 'card',
  data () {
    return {
      user:JSON.parse(window.sessionStorage.getItem('user'))
    }
  }
}
</script>

<style lang="scss" scoped>
#card {
	padding: 12px;
	margin-bottom: 5px;
  .avatar{
  	width: 40px;
  	height: 40px;
  	vertical-align: middle;/*这个是图片和文字居中对齐*/
  }
  .name {
  	display: inline-block;
  	padding: 10px;
  	margin-bottom: 15px;
  	font-size: 16px;
  }
  .search {
  	background-color: #DBD9D8;
		width: 150px;
  	height: 30px;
  	line-height: 30px;
  	padding: 0 10px;
  	border: 0;
  	border-radius: 4px;
  	outline: none;/*鼠标点击后不会出现蓝色边框*/
    color: #FFF;
  }
	.searchBtn{
		background-color: #DBD9D8;
		border: 0;
		margin-left: 3px;
	}
}
</style>
<style>
	/*当前组件的el-input样式设置*/
	#card .el-input__inner {
		background-color: #DBD9D8;
		outline: none;/*鼠标点击后不会出现蓝色边框*/
	}
</style>
