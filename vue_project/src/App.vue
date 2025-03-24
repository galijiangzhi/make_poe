<script>

export default {
  data() {
    return {
      // 按钮状态数组
      buttons: [
        { disabled: false },
        { disabled: false },
        { disabled: false },
        { disabled: false },
        { disabled: false },
        { disabled: false },
      ],
      inputText: '', // 文本输入框内容
      resultText: '', // 结果显示内容
    };
  },
  methods: {
    // 点击事件处理函数
    handleClick(index) {
      // 将按钮状态设置为已点击
      this.buttons[index].disabled = true;

      // 如果是第一个按钮，改变按钮颜色为红色
      if (index === 0) {
        this.$set(this.buttons[index], 'style', { backgroundColor: 'red' });
      }

      // 如果是后五个按钮，弹框提示
      if (index > 0) {
        alert('该功能待开发');
      }
    },
    // 处理文本输入
    handleTextInput(event) {
      const text = event.target.value;
      if (text.length <= 35) {
        this.inputText = text;
      } else {
        alert('输入文本不能超过七个字');
        event.target.value = this.inputText; // 保留之前的有效输入
      }
    },
    // 处理文本提交
    async handleTextSubmit() {
      if (!this.inputText) {
        alert('请输入一段文本');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:12000/process-text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: this.inputText }),
        });

        if (!response.ok) {
          throw new Error('提交失败');
        }

        const data = await response.json();
        this.resultText = data.result; // 假设后端返回的结果在 data.result 中
      } catch (error) {
        console.error('提交出错:', error);
        this.resultText = '提交出错，请重试';
      }
    },
  },
};
</script>

<template>
  <!-- 新增导航栏 -->
  <nav class="navbar">
    <div class="navbar-right">
      <button @click="aboutUs">关于我们</button>
      <button @click="help">帮助</button>
      <button @click="goToGitHub">GitHub</button>
    </div>
  </nav>

  <header>
    <div class="anniudiv">
      <!-- 使用 v-for 渲染按钮 -->
      <button
        v-for="(button, index) in buttons"
        :key="index"
        :class="{ disabled: button.disabled }"
        :style="{ backgroundColor: index === 0 && button.disabled ? 'rgb(161,49,47)' : '' }"
        @click="handleClick(index)"
      >
        {{ ['对句', '绝句', '藏头诗', '集句诗', '律师', '词'][index] }}
      </button>
    </div>
    <img alt="Vue logo" class="logo" src="./assets/logo-2021.png" width="125" height="125" />
    <img alt="myhead" class="myhead" src="./assets/image.png" />
    <img class='bird' src="./assets/bird.png"/>
    <img class='hehua' src="./assets/hehua.png"/>
    <img class='zuo' src="./assets/zuo.png"/>
    <img class='you' src="./assets/you.png"/>
    
    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <TheWelcome />

    <!-- 文本输入框 -->
    <div class="input-section">
      <input
        type="text"
        v-model="inputText"
        @input="handleTextInput"
        maxlength="7"
        placeholder="请输入文本"
      />
      <button @click="handleTextSubmit">提交文本</button>
    </div>

    <!-- 结果显示框 -->
    <div class="result-box">
      <div class='jieguobiaoti'>生成结果</div>
      <div class='jieguokuang'>
        <p>{{ resultText }}</p>
      </div>
    </div>
  </main>
</template>

<style>
body {
  background-image: url('./assets/background.png'); /* 设置背景图片 */
  background-size: cover; 
  color: white; /* 将文字颜色设置为白色，以便在黑色背景上可见 */
  overflow: hidden; /* 裁剪超出页面的部分 */
}

/* 新增导航栏样式 */
.jieguobiaoti{
  
  position: relative; /* 添加相对定位 */
  width:600px;
  height:35px;
  background-color:#a1312f;
  top:50%;
  left: 50%; /* 将 div 的左边移动到页面中间 */
  transform: translateX(-50%); /* 向左移动自身宽度的一半，实现横向居中 */
  text-align: center; /* 水平居中 */
  line-height: 35px; /* 垂直居中 */
  font-size:20px;
  font-family: "KaiTi", "楷体", serif; 
}
.jieguokuang{  
  position: relative; /* 添加相对定位 */
  width:600px;
  height:200px;
  background-color:#fff;
  top:60%;
  font-size:30px;
  font-family: "KaiTi", "楷体", serif;
  text-align: center; /* 水平居中 */
  line-height: 120px; /* 垂直居中 */
  }

.anniudiv{
    width: 100%; /* 宽度可以根据需求调整 */
    height: 100px; /* 高度可以根据需求调整 */
    position: absolute; /* 使用绝对定位 */
    top: 90px; /* 距离顶部 90px */
    left: 50%; /* 将 div 的左边移动到页面中间 */
    transform: translateX(-50%); /* 向左移动自身宽度的一半，实现横向居中 */
    display: flex; /* 使用 Flexbox 布局 */
    justify-content: center; /* 横向居中 */
    align-items: center; /* 纵向居中 */
    gap: 10px; /* 按钮之间的间距 */
}
/* 圆形按钮的样式 */
.anniudiv button {
    width: 100px; /* 按钮宽度 */
    height: 100px; /* 按钮高度 */
    border-radius: 50%; /* 圆形按钮 */
    background-color: rgb(169,149,123); /* 默认背景颜色 */
    color: white; /* 文字颜色 */
    border: none; /* 去掉边框 */
    cursor: pointer; /* 鼠标指针为手型 */
    font-size: 14px; /* 文字大小 */
}

.navbar {
  height: 44px; /* 调整导航栏的高度 */
  position: absolute; /* 设置为绝对定位 */
  width: 100%;
  top: 0; /* 距离顶部的距离 */
  left: 0;
  padding: 1rem;
  background-color: rgb(161,49,47);
  color: white;
  display: flex;
  justify-content: flex-end; /* 使内容从右往左排列 */
  gap: 10px; /* 可选：设置按钮之间的间距 */
  align-items: center; /* 使内容垂直居中 */
}

.navbar-right button {
  padding: 5px 10px; /* 调整按钮的内边距 */
  margin-left: 1rem;
  background-color: rgb(151,39,37);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.navbar-right button:hover {
  background-color: rgb(131,19,17);
}

header {
  line-height: 1.5;
}

.logo {
  position: absolute; /* 设置为绝对定位 */
  top: 50%; /* 距离顶部的距离 */
  left: 15%; /* 距离左侧的距离，这里设置为页面水平居中 */
  transform: translateX(-50%); /* 通过 transform 实现水平居中 */
  margin: 0 auto 2rem;
  width: 320px; /* 限制预览框宽度 */
  height: 200px; /* 限制预览框高度 */
}

.bird{
  position: absolute; /* 设置为绝对定位 */
  top: 44px; /* 距离顶部的距离 */
  left: 0px;
}

.zuo{
  position:absolute;
  top:80%;
  left:10%;
}

.you{
  position:absolute;
  top:55%;
  left:75%;
}

.hehua{
  position:absolute;
  top:65%;
  left:75%;
}
.myhead {
  position: absolute; /* 设置为绝对定位 */
  top: 24%; /* 距离顶部的距离 */
  left: 50%; /* 距离左侧的距离，这里设置为页面水平居中 */
  transform: translateX(-50%); /* 通过 transform 实现水平居中 */
  margin: 0 auto 2rem;
  width: 540px; /* 限制预览框宽度 */
  height: 150px; /* 限制预览框高度 */
}

.input-section {
  margin: 0rem auto;
  text-align: center;
  background-color:red;
  position: absolute; /* 设置为绝对定位 */
  top:45%;
  left:50%;
  transform: translateX(-50%); 
}

.input-section input {
  height: 40px;
  padding: 0.5rem;
  width:400px;
  font-size: 1rem;
  margin-right: 0rem;
  border: 1px solid #ccc;
  border-radius: 0px;
  position: relative;
  box-sizing: border-box; /* 统一盒模型 */
  vertical-align: middle; /* 对齐方式 */
}

.input-section button {
  height: 40px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color:#a1312f;
  color: white;
  border: 1px solid #ccc;
  border-radius: 0px;
  cursor: pointer;
  position: relative;
  box-sizing: border-box; /* 统一盒模型 */
  vertical-align: middle; /* 对齐方式 */
}
.input-section button:hover {
  background-color: #3aa876;
}

.result-box {
  position: absolute; /* 使用绝对定位 */
  top:51%;
  left:50%;
  transform: translateX(-50%); /* 通过 transform 实现水平居中 */
  margin: 2rem auto;
  background-color: #f9f9f9;
  text-align: center;
  color: black; /* 结果文本颜色设置为黑色 */
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>