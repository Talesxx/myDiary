import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import GlobalPlayer from './components/GlobalPlayer.vue'
export default {
  ...DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      // 在默认布局之后添加全局播放器
      'layout-bottom': () => h(GlobalPlayer)
    })
  }
}