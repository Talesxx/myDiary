import { defineConfig } from 'vitepress'

import { withMermaid } from "vitepress-plugin-mermaid";

// https://vitepress.dev/reference/site-config
export default withMermaid(defineConfig({

  // lastUpdated: true,
  // cleanUrls: true,
  // // 配置静态资源处理
  vite: {
    publicDir: 'docsPublic',
  },

  markdown: {
    math: true,
    config: (md) => {
      // 使用更多的 Markdown-it 插件！
    }
  },
  title: "我的小记",
  description: "这是一个 VitePress Site",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'web', link: '/web/1.environment/newComputerInitialization' }
    ],

    sidebar: [
      // {
      //   text: 'Examples',
      //   items: [
      //     { text: 'Markdown Examples', link: '/markdown-examples' },
      //     { text: 'Runtime API Examples', link: '/api-examples' },
      //   ]
      // },
      {
        text: '高等数学',
        collapsed: true,
        items: [
          // 基础计算法则
          { text: '对数计算法则', link: '/AdvancedMathematics/1.对数计算法则' },
          { text: '指数计算法则', link: '/AdvancedMathematics/2.指数计算法则' },
          { text: '三角函数计算法则', link: '/AdvancedMathematics/3.三角函数计算法则' },
          { text: '求导8大公式', link: '/AdvancedMathematics/4.求导8大公式' },

          // 微积分基础
          { text: '第一节 极限', link: '/AdvancedMathematics/D1.第一节极限' },
          { text: '第二节 函数定义、连续函数、间断点、渐近线', link: '/AdvancedMathematics/D2.第二节函数定义，连续函数 间断点 渐近线' },
          { text: '导数', link: '/AdvancedMathematics/D3.导数' },
          { text: '多元函数求导与极值', link: '/AdvancedMathematics/D4.多元（二元以上）函数求导 求极大极小值' },

          // 积分学
          { text: '积分与面积', link: '/AdvancedMathematics/D5.积分与面积' },
          { text: '体积与二重积分', link: '/AdvancedMathematics/D6.体积与二重积分' },

          // 微分方程
          { text: '微分方程', link: '/AdvancedMathematics/D8.微分方程' },

          // 空间几何
          { text: '空间解析几何', link: '/AdvancedMathematics/D9.空间解析几何' },
          { text: '无穷级数', link: '/AdvancedMathematics/D10.无穷级数' },
          { text: '平面方程', link: '/AdvancedMathematics/D11.平面方程' },
          { text: '矩阵', link: '/AdvancedMathematics/D11.矩阵' },
          { text: '线性代数和空间向量', link: '/AdvancedMathematics/D11.线性代数和空间向量' },

          // 错题本
          { text: '错题本', link: '/AdvancedMathematics/Z.错题本' }
        ]
      },
      {
        text: 'web前端',
        collapsed: true,
        items: [
          {
            text: '环境安装与配置',
            collapsed: true,
            items: [
              { text: '环境安装与配置', link: '/web/1.environment/newComputerInitialization' },
            ]
          },
          {
            text: '包开发',
            collapsed: true,
            items: [
              { text: 'npm包快速联调', link: '/web/2.npmPackage/fastJointDebug' },
            ]
          },
          {
            text: '音视频',
            collapsed: true,
            items: [
              { text: 'webRTC', link: '/web/3.videoOrAudio/webRTC简易教程' },
            ]
          },
          {
            text: '面试题',
            collapsed: true,
            items: [
              { text: '浏览器渲染过程', link: '/web/4.interviewQuest/browser_rendering_detailed' },
              { text: '渲染过程图', link: '/web/4.interviewQuest/renderingProcess' },
            ]
          },
          {
            text: '其他',
            collapsed: true,
            items: [
              { text: 'ts导出问题', link: '/web/5.stepOnTheTrap/ts导出问题' },
            ]
          },
          {
            text: 'React',
            collapsed: true,
            items: [
              { text: 'React useEffect', link: '/web/12.react/react_useEffect' },
            ]
          },
          {
            text: '3D',
            collapsed: true,
            items: [
              { text: '3D模型问题', link: '/web/6.3D/3D模型问题' },
            ]
          },


        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
}))
