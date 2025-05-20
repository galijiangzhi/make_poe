<script>
export default {
  data() {
    return {
      // 按钮状态数组，增加到12个, ", "水调歌头/Shuidiaogetou", "菩萨蛮/Pusaman", "卜算子/Busuanzi"
      buttons: [
        { id: 0, name: '五言绝句', disabled: false, active: false },
        { id: 1, name: '七言绝句', disabled: false, active: false },
        { id: 2, name: '五言律诗', disabled: false, active: false },
        { id: 3, name: '七言律诗', disabled: false, active: false },
        { id: 4, name: '如梦令', disabled: false, active: false },
        { id: 5, name: '减字木兰花', disabled: false, active: false },
        { id: 6, name: '清平乐', disabled: false, active: false },
        { id: 7, name: '蝶恋花', disabled: false, active: false },
        { id: 8, name: '满江红', disabled: false, active: false },
        { id: 9, name: '沁园春', disabled: false, active: false },
        { id: 10, name: '水调歌头', disabled: false, active: false },
        { id: 11, name: '菩萨蛮', disabled: false, active: false },
        { id: 12, name: '卜算子', disabled: false, active: false }
      ],
      inputText: '',
      resultText: '',
      selectedButtonId: 0 // 当前选中的按钮ID
    };
  },
  methods: {
    // 点击事件处理函数
    handleClick(index) {
      // 如果点击的是已激活的按钮，则取消激活
      if (this.buttons[index].active) {
        this.buttons[index].active = false;
        this.selectedButtonId = null;
        return;
      }
      
      // 互斥逻辑：将所有按钮设为非激活状态
      this.buttons.forEach(button => {
        button.active = false;
      });
      
      // 激活当前点击的按钮
      this.buttons[index].active = true;
      this.selectedButtonId = index;
    },
    
    // 处理文本输入
    handleTextInput(event) {
      const text = event.target.value;
      if (text.length <= 235) {
        this.inputText = text;
      } else {
        alert('输入文本不能超过七个字');
        event.target.value = this.inputText;
      }
    },
    
    // 处理文本提交
    async handleTextSubmit() {
      if (!this.inputText) {
        alert('请输入一段文本');
        return;
      }
      
      if (this.selectedButtonId === null) {
        alert('请选择一个诗歌类型');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:12000/process-text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: this.inputText,
            poem_type: this.selectedButtonId // 提交选中的按钮ID
          }),
        });

        if (!response.ok) {
          throw new Error('提交失败');
        }

        const data = await response.json();
        this.resultText = data.result;
      } catch (error) {
        console.error('提交出错:', error);
        this.resultText = '提交出错，请重试';
      }
    },
    
    aboutUs() {
      alert('关于我们');
    },
    help() {
      alert('帮助');
    },
    goToGitHub() {
      window.open('https://github.com', '_blank');
    }
  },
};
</script>

<template>
  <nav class="navbar">
    <div class="navbar-right">
      <button @click="aboutUs">关于我们</button>
      <button @click="help">帮助</button>
      <button @click="goToGitHub">GitHub</button>
    </div>
  </nav>

  <header>
    <div class="anniudiv">
      <!-- 使用 v-for 渲染12个按钮 -->
      <button
        v-for="(button, index) in buttons"
        :key="index"
        :class="{ 
          disabled: button.disabled,
          active: button.active 
        }"
        @click="handleClick(index)"
      >
        {{ button.name }}
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
        maxlength="70"
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
    text-align: center; /* 水平居中 */ /* 垂直居中 */
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
      z-index: 2;
  }
  /* 圆形按钮的样式 */
  .anniudiv button {
      width: 90px; /* 按钮宽度 */
      height: 90px; /* 按钮高度 */
      border-radius: 50%; /* 圆形按钮 */
      background-color: rgb(169,149,123); /* 默认背景颜色 */
      color: white; /* 文字颜色 */
      border: none; /* 去掉边框 */
      cursor: pointer; /* 鼠标指针为手型 */
      font-size: 14px; /* 文字大小 */
  }
  
  /* 新增按钮激活状态的样式 */
.anniudiv button.active {
  background-color: #a1312f !important;
  color: white;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
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
    z-index: 1;
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